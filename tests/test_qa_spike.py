import copy
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("spike", Path(__file__).resolve().parents[1] / "tools/qa-spike/spike.py")
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)


class SpikeTests(unittest.TestCase):
    def setUp(self):
        self.obs = s.load(s.ROOT / "examples/observation.json")
        self.bundle = s.load(s.ROOT / "examples/evidence-bundle.json")

    def test_all_examples(self):
        for kind in ("observation", "evidence-bundle", "diagnosis-report", "jira-draft"):
            s.validate(kind, s.load(s.ROOT / "examples" / (kind + ".json")))

    def test_secret_fixture_does_not_reach_prompt_or_draft(self):
        self.obs["reporter_note"] = "Bearer abc_SECRET token=token_SECRET user@example.invalid"
        self.bundle["network"][0]["url_redacted"] = "https://user:pass@example.invalid/api?token=query_SECRET#frag_SECRET"
        self.bundle["console_errors"] = [{"id": "console-1", "time": "2026-10-09T10:00:03Z",
                                          "message_redacted": "password=pw_SECRET sk-key_SECRET"}]
        seen = []
        def adapter(obs, bundle, runtime, timeout):
            seen.append({"observation": obs, "evidence": bundle})
            return s.load(s.ROOT / "examples/diagnosis-report.json")
        with tempfile.TemporaryDirectory() as d, patch.object(s, "diagnose", side_effect=adapter):
            s.run(self.obs, self.bundle, "fixture", Path(d) / "out")
            text = str(seen) + "".join(p.read_text() for p in (Path(d) / "out").iterdir())
            for secret in ("abc_SECRET", "token_SECRET", "query_SECRET", "frag_SECRET", "pw_SECRET",
                           "sk-key_SECRET", "user@example.invalid", "user:pass"):
                self.assertNotIn(secret, text)

    def test_input_mismatch_duplicate_and_format(self):
        for mutate in (lambda b: b.update(observation_id="wrong"),
                       lambda b: b["network"][0].update(id="ev-action-01"),
                       lambda b: b.update(collected_at="not-a-date"),
                       lambda b: b.update(raw_headers={"Authorization": "secret"})):
            b = copy.deepcopy(self.bundle)
            mutate(b)
            with self.assertRaises(Exception):
                s.prepare(self.obs, b)

    def test_invalid_model_results_fallback(self):
        for mutate in (lambda r: r.update(observation_id="wrong"),
                       lambda r: r["claims"][0].update(evidence_refs=["invented"]),
                       lambda r: r["claims"][0].update(evidence_refs=[]),
                       lambda r: r.update(fault_domain="invented"),
                       lambda r: r["claims"][0].update(statement="Bearer secret")):
            r = s.load(s.ROOT / "examples/diagnosis-report.json")
            mutate(r)
            with tempfile.TemporaryDirectory() as d, patch.object(s, "diagnose", return_value=r):
                result = s.run(self.obs, self.bundle, "codex", Path(d) / "out")
                self.assertEqual(result["status"], "analysis_failed")
                draft = s.load(Path(d) / "out/jira-draft.json")
                self.assertEqual(draft["approval_status"], "pending_review")
                self.assertEqual(draft["expected"], self.obs["expected"]["text"])
                self.assertNotIn("diagnosis_report_id", draft)

    def test_missing_cli_and_timeout(self):
        for failure in (RuntimeError("codex_not_installed"), s.subprocess.TimeoutExpired("codex", 1)):
            with tempfile.TemporaryDirectory() as d, patch.object(s, "diagnose", side_effect=failure):
                result = s.run(self.obs, self.bundle, "codex", Path(d) / "out")
                self.assertEqual(result["status"], "analysis_failed")
                self.assertFalse(result["jira_published"])

    def test_replay_explicit_and_stale_output_refused(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "out"
            result = s.run(self.obs, self.bundle, "fixture", out)
            self.assertEqual(result["status"], "fixture_replay")
            self.assertFalse(result["model_called"])
            with self.assertRaises(FileExistsError):
                s.run(self.obs, self.bundle, "fixture", out)


if __name__ == "__main__":
    unittest.main()

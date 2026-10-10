# Synthetic QA Spike

仅处理合成或获准的非敏感文本。无 HTTP 服务、Chrome Capture、Jira 发布或图片上传。

## 运行

Python 3.10+；建议使用虚拟环境：

```bash
python -m venv .venv
.venv/bin/python -m pip install -r tools/qa-spike/requirements.txt
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python tools/qa-spike/spike.py --runtime fixture --out artifacts/qa-spike/replay-1
.venv/bin/python tools/qa-spike/spike.py --runtime codex --out artifacts/qa-spike/model-1
```

每次使用新的输出目录，防止旧诊断被误当作本轮结果。fixture 模式回放仓库已有诊断，
不调用模型。codex 模式需要用户机器已安装 Codex CLI，并在该机器完成合法登录；
不把个人凭据上传本仓库，也不在公共 CI 配置订阅凭据。模型由本地 CLI 配置决定。

默认 120 秒超时，支持 --timeout。退出码：0 成功/回放；1 输入或输出目录被拒；
2 模型不可用、失败、超时或结果校验失败（仍输出基础草稿）。
Ctrl-C 取消当前进程；无持久任务、自动重试或发布队列，失败后可换新目录手动重试。
未验证复杂取消、子进程树终止或并发行为。

## 边界

- 校验原始 Observation/EvidenceBundle（64 KiB/文件）、日期格式、关联 ID 和证据 ID 唯一性。
- 二次文本脱敏：URL 用户信息/查询/fragment、Bearer、标记的 token/password/cookie/API key、邮箱。
  此规则仅验证固定 fixture 模式，无法识别任意姓名、地址、电话号码或 URL 路径中的秘密。
  输入现有 *_redacted 字段不等于信任已脱敏声明。禁止真实公司数据。
- Schema 不允许 headers/body 等额外原始字段，输入拒绝时不输出其内容。
- 模型只收到脱敏 Observation/EvidenceBundle；截图只传元数据，不读取或解析引用。
- codex exec 在空临时目录、read-only、ephemeral 模式运行；提示禁止工具调用，
  但提示不是工具禁用的安全边界。本地用户配置可能启用 MCP；真实数据接入前需独立隔离。
- 严格模型输出 Schema 只保留现有诊断合同必填字段，避免猜测团队与外部来源。
  该 CLI 适配器在本次环境未实际执行，具体版本/授权兼容性仍需本地复验。
- 服务侧再次校验 Schema、Observation ID、证据引用及 fact/inference 必须有引用；
  拒绝无检索来源的 source_references 和可识别的泄露文本。
  引用有效不能证明断言真实，必须人工评审内容。
- JiraDraft 从 QA 原文构造，保留 expected 来源、缺失证据与诊断分类，
  始终 pending_review；无审批或发布入口，不产生 Jira issue key。
- 失败草稿保留预期/实际/步骤/环境/证据和 gaps，不引用失败诊断。
- 原始 stderr、无效模型结果不保存；仅保存脱敏输入、已校验诊断、草稿和状态。

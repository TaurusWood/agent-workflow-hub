# 首个可执行 Technical Spike：2026-10-10

状态：**本地合成合同链路已运行；真实模型与浏览器/Jira闭环尚未验证。**
基线 main：325379ca2b49e7dd80970aa4501a6ad054e1d95a。
实现与运行说明：[tools/qa-spike](../../tools/qa-spike/README.md)。

## 实际结果

本次容器 Python 3.12、jsonschema 4.26.0。执行记录及合成输出：
[evidence/synthetic-spike-20261010](evidence/synthetic-spike-20261010/)。

| 验证 | 实际结果 |
|---|---|
| 四个现有 Schema / 样例 | 全部通过 |
| 合成输入 → 二次脱敏 → 样例诊断回放 → 结果校验 → Jira 草稿 | 通过，fixture_replay；没有模型调用 |
| codex 模式 | analysis_failed / codex_not_installed；没有模型请求 |
| 模型不可用时基础 Jira 草稿 | 已生成 pending_review 草稿，没有诊断 ID、没有发布 |
| 自动测试 | 6 个测试方法通过；覆盖输入 ID/重复 ID/日期/额外字段、秘密 fixture、无效诊断、缺失 CLI/超时、回放标记和旧目录拒绝 |
| Chrome Capture / source map /图片理解 | 未执行；截图为不工作的占位引用 |
| 人工 UI / Jira API /审批/附件/幂等发布 | 未实现、未执行 |
| 准确率、延迟、token、人工节省时间 | 未测量；回放不能用于评价模型质量 |

第一次测试发现运行环境缺少 date-time 格式检查的可选依赖，非法日期未被拒绝；
已增加显式日期检查，复跑全部通过。没有修改现有 Schema 合同。

## 合同判断

现有四个合同足以验证文本流转，无须先重做平台。Schema 单独不足：
跨对象一致性、证据 ID 唯一性、引用存在性、事实引用要求已由 Spike 校验。
这仍不能自动识别“有引用但内容不成立”的诊断。

Observation 保留 QA 的预期来源；JiraDraft.expected 仅为字符串，
因此生成器在 description_markdown 明确保留 source_kind，避免把 QA 预期冒充批准的 AC。
截图描述不作为已看过图像的事实。动作与请求时间接近不等于已证明因果关系。

## 下一个验证 Gate

在用户已授权的本地机器运行 README 的 codex 命令，记录 CLI 版本、模型、
登录类别（不记录令牌）、耗时和校验结果；人工核对：
HTTP 500 被识别为边界事实而非根因；加载现象来自 QA；
不把截图占位符当图像，不编造团队、部署版本或 AC。
测试一次超时/失败并确认基础草稿仍可审阅。成功后才评估模型质量。
官方 [Codex 非交互文档](https://learn.chatgpt.com/docs/non-interactive-mode)
支持 exec、output-schema、最终消息输出和 ephemeral；文档能力不等于本地运行成功。
本 Spike 不实现 SIWC 或付费 API 接入。

Jira Gate 另需获准的测试项目、账号、字段/附件权限、显式人工审批、
重复发布测试和返回 issue key 的运行证据，本次没有这些证据。

## Chrome Extension 的下一步最小边界（建议，尚未裁决）

下一实验只实现一个虚构页面的开始/停止短捕获、QA observation 输入、
按钮动作（时间和 testid）、选定请求（方法/去查询 URL/状态/耗时）、
console error 和 capture_gaps，导出符合现有 EvidenceBundle 的 JSON，
进入本 Spike 校验器。每个条目使用唯一稳定 ID，保持 Observation 关联。

先比较 DevTools 扩展与 chrome.debugger 的权限和共存行为，再选入口；
本次文本验证不构成选择 CDP 的证据。截图先保持明确缺失记录，
后续单独验证真实图片脱敏/附件。首轮不收 headers、body、输入值、
完整 HAR、后台日志或源代码，不接 Confluence、Jira 自动发布和多模型调度。
先完成本地真实诊断 Gate，再推进上述 Capture 实验；不开发完整 Extension。

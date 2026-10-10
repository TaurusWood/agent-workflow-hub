# AI 模型接入选择：Coding Plan、OAuth 与团队 API

**状态：外部能力的阶段性调研 + 实施建议；不是已批准的运行时架构。** 原始记录日期：2026-10-09。

## 核心区别

ChatGPT 订阅和 OpenAI Platform API 的标准计费是分开的。与此同时，OpenAI 已提供面向**符合条件的开源/本地应用**的 Sign in with ChatGPT（SIWC）路径：用户明确通过 OAuth 授权后，工具可在受限条件下发起使用其 ChatGPT 套餐额度的 Responses API 请求。

这**不等于**通用 API Key、多人共享额度或读取用户 ChatGPT 历史记录的权限。**仓库本身是 Public 并不意味着远程托管的企业 QA 服务自动符合 SIWC 的使用条件。** 权限与政策在真正实施前仍需按官方现行文档核实。

## 候选路径

| 路径 | Phase 0 是否适合 | 团队共享服务的适配度 | 核心限制 |
| --- | --- | --- | --- |
| 使用 ChatGPT 登录的 Codex CLI（非交互执行 / App Server） | 最快验证本地合成数据 | 不能自动等价为多人服务端接口 | 身份、个人额度、Runner 权限、运行管理 |
| SIWC OAuth 套餐调用 | 可验证本地开源 Companion 应用 | 远程托管/商业使用需满足相关准入条件 | 每位用户授权、支持范围、订阅额度限制 |
| 独立付费的 Platform API | 适合 PoC 和团队后端 | **默认推荐** | 公司审批、预算、密钥安全与账单 |
| 不使用 AI | 标准 Jira 模板及安全采集 | 始终可降级 | 缺少推理诊断能力 |

## 本地 PoC

~~~mermaid
flowchart LR
  E["Chrome Evidence"] --> L["本地 Companion / Worker\n脱敏、暂存"]
  L --> M["Codex CLI 或获准 SIWC Runtime"]
  M --> D["结构化 Diagnosis + Jira Draft"]
  D --> R["QA 审核"]
  R --> J["Jira API"]
~~~

PoC 应使用虚构数据。未经批准，不能向外部模型传输真实 HAR、Token、PII、客户信息或专有代码。

## 团队部署的候选形态

~~~mermaid
flowchart LR
  E["Chrome Capture"] --> API["QA Assistant 服务"]
  API --> STORE["受控 Evidence Storage"]
  API --> JOB["异步诊断 Worker"]
  JOB --> CTX["按需检索源码 / AC"]
  CTX --> MODEL["公司批准的模型 API"]
  MODEL --> JOB
  JOB --> REVIEW["QA Review UI"]
  REVIEW --> JIRA["Jira API"]
~~~

只保留一个内部 **ModelRuntime** 边界：输入为已脱敏证据引用及限定上下文，输出为通过校验的结构化诊断。模型本身不拥有 Jira 凭证、附件上传或发布权。初期只实现一个真正需要的适配器，不建设超前的多 Provider 平台。

## 原讨论记录的能力与限制（需实施时复核）

- Codex CLI 支持非交互的自动化执行（Codex Exec），但不是无需管理的企业级多人共享接口。
- SIWC 需用户明确授权特定范围。原调研指出 SIWC 的部分 Responses 请求受参数、后台模式与工具能力限制，且套餐调用共享用户已有额度。实际参数应以开发实施当天的官方文档为准。
- 面向本地/符合条件的开源工具的支持不等于自动开放远程托管或付费企业应用；企业场景需核对参与资格与审批。
- 不应该将个人 ChatGPT/Coding 订阅凭证汇聚成公司公共身份。
- 无论选择何种模型运行时，**本阶段 Jira 发布必须经过 QA 授权**。

## 目前推荐

**技术验证：** 先用本地 Codex Exec 跑通虚构 EvidenceBundle → DiagnosisReport → JiraDraft。若团队确实希望分发本地开源客户端，再验证 SIWC 模式。

**团队正式候选：** 默认由公司提供获批准、按使用量计费的模型服务；只有其他官方路径经核准后才替换。模型接入隔离在简单 Adapter 内，不能因为计费模式变化而重写 Chrome Capture、Review 或 Jira。

## 官方参考资料

- [SIWC 总览与准入](https://developers.openai.com/siwc/token-sharing-open-source)
- [SIWC 开源示例](https://developers.openai.com/cookbook/articles/sign-in-with-chatgpt)
- [SIWC 预览限制](https://developers.openai.com/siwc/token-sharing-open-source/preview-limitations)
- [Codex CLI 文档](https://learn.chatgpt.com/docs/cli/reference)
- [ChatGPT 与 API 分开计费](https://help.openai.com/en/articles/9039756-managing-billing-settings-on-chatgpt-web-and-platform)
- [在其他应用中使用套餐](https://help.openai.com/en/articles/20001542-using-your-chatgpt-plan-in-other-apps-and-sites)

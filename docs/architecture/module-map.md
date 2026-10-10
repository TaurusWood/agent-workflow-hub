# 系统模块图与团队协作职责

**状态：候选逻辑模块划分，不意味着微服务划分。**

| 能力 | 核心职责 | 主要参与角色 | v0.1 定位 |
| --- | --- | --- | --- |
| Observation & Capture | QA 入口、可复现操作、浏览器证据 | QA + 前端 | 必需，优先 PoC |
| Evidence Intake & Governance | 校验、脱敏、存储、保留期限、关联 | 平台/后端 + 安全 | 必需 |
| Context Resolution | 定向读取 PRD/AC、环境 → 候选仓库映射 | PM、Tech Lead、平台 | 初期最小化 |
| AI Diagnosis & Structuring | 有证据的分类、未知项、诊断报告和 Jira 文案 | AI/平台 + 前端 | 有界诊断，不要求 Root Cause |
| QA Review & Publication | 证据联动展示、编辑、审批和 Jira API | QA + 平台 | 必需 |
| Ownership & Notification | 责任团队建议、路由规则与通知 | 开发负责人 + Jira 管理员 | 初期只建议 |
| Backend Telemetry | Request/Trace/服务异常查询 | 后端 + SRE | 依赖可观测性，后续 |
| Test Data Provisioning | 场景数据查询、创建、回收与重置 | QA + 后端 | 后续，不阻塞 |
| PRD Preflight | 已有规则和代码影响提示 | PM + 工程 | 可并行试验 |

## 实现分组建议

第一版可以先验证 **一个浏览器采集入口 + 一个 QA Assistant 应用服务**。该服务内部可包含接入、异步分析、审核与 Jira Adapter，而不是分别部署九套微服务。

也不要将每一行都落实成独立 Repo、Skill 或 Agent。

## Tool、确定性代码、AI 与人的职责

- **Tool / Connector：** 在严格权限下执行明确读写，例如检索代码、读取获准 AC、上传附件、创建 Jira；错误必须可观察。
- **确定性应用代码：** Schema 校验、脱敏、Auth、保留期限、限流、任务状态、幂等、审批门禁。
- **AI / Agent：** 选择相关证据、解释对比、整理 Actual/Expected、有边界地判断 Fault Domain、标记未知、引用依据。
- **人：** 确认业务预期、修正错误推断、批准外部发布，定义工程任务分配策略。

## 要验证的基础前提

- Jira 项目所需字段及创建、编辑、附件权限。
- GitHub/GitLab 对获准 Repo 的读取权限；QA 不必 Clone。
- Confluence 文档权限；不未经授权复制全量内部文档。
- 企业 Chrome 策略允许何种采集能力。
- Ownership 应来自维护中的系统映射；Public 仓库只存虚构示例。
- 模型服务的授权、合规和数据处理范围。

# Agent Workflow Hub · AI 工程协作枢纽

> 让业务预期、真实运行证据与工程实现形成可追溯的协作链路，产出开发人员与 Coding Agent 都能直接理解和处理的任务。

**状态：设计基线 · 2026-10-09 · 尚无生产实现。**

本仓库公开记录团队 AI 工程协作体系的**已认可原则、目标流程、候选架构与验证计划**。第一个落地切口是 **Track B：QA 观察异常 → 证据采集 → 有界诊断 → 人工审核 → Jira**。PRD、业务规则与测试准备属于上游背景及未来集成点；当前不建设完整 SDLC 平台。

## 阅读入口

| 角色 | 建议先阅读 |
| --- | --- |
| 全体成员 | [目标、痛点与边界](docs/vision.md) |
| PM / QA / 开发 | [从需求到验收的协作流程](docs/workflows/requirement-to-verification.md) |
| QA / 前端 / 后端 | [Bug 生命周期](docs/workflows/bug-lifecycle.md) |
| 架构与实施人员 | [系统架构图](docs/architecture/system-overview.md) |
| 实施人员 | [Evidence → AI → Review → Jira 技术链路](docs/architecture/evidence-diagnosis-pipeline.md) |
| 团队负责人 | [路线图、可行性与 Gate](docs/roadmap.md) |
| 评审人员 | [已认可方向、提案及未解决问题](docs/decisions/README.md) |
| AI 平台负责人 | [模型接入及订阅权限边界](docs/architecture/model-runtime-options.md) |

Mermaid 图直接嵌入 Markdown，可在 GitHub 原生查看。

## 基本原则

- **预期行为、代码实现、运行时事实是三个不同的信息源**，不能互相替代。
- **人发现并确认问题；工具采集客观事实；AI 根据证据解释、推断并整理。**
- **Evidence First**：事实、证据支持的推断、假设、未知必须明确区分。
- 交付目标是**开发可执行的高质量 Jira**，不是必须自动证明 Root Cause。
- 不要求 QA 在本地 clone 多个代码仓库，也不要求 QA 人工整理所有技术细节。
- Jira 在本阶段先生成可审核草稿；自动指派与自动修复需要更高验证门槛。
- 先以真实工作流验证价值，不提前建设全量业务规则镜像、通用造数平台或复杂 Agent 基础设施。

## 首个目标场景

QA 在 QA/Staging 环境发现异常后，启动短时浏览器采集并复现。工具记录操作、相关 Network/Console 信号和截图；受控应用服务对证据脱敏、存储，并调用**已获准的模型运行时**，按需关联业务规则与源码。QA 查看并修改 Observation、Expected/Actual、证据与 Jira 草稿，确认后才通过 Jira API 创建工单。增强诊断可以异步执行，QA 不必原地等待。

**注意：** Coding Plan 或 ChatGPT 个人订阅不能自动当作团队服务端 API 凭证；可用的授权路径及限制见[模型接入选项](docs/architecture/model-runtime-options.md)。

## Public 仓库约束

**严禁提交：** 真实 Confluence 导出、保密 PRD、内部业务规则、令牌、内网地址、账号、真实 HAR、截图、堆栈、Trace ID、私有仓库名称、内部 Ownership 映射与客户/员工信息。本仓库的示例全部虚构。真实映射和证据必须放在适当权限控制的内部系统中。

## 本仓库不是什么

不是已部署的 QA 工具，不是内部 Confluence/Jira/代码仓库的替代品，也不是已经冻结的 API 与工程合同。文档中的决策状态会明确标记。

## 下一步

按照 [Chrome Evidence → AI Draft → QA Review → Jira 技术验证计划](docs/validation/qa-capture-spike.md) 使用虚构或获批的非敏感数据完成端到端 PoC，再基于验证结果冻结 v0.1 的技术边界。

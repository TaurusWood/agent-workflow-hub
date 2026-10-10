# 系统总体架构（逻辑视图）

**状态：候选架构，尚未冻结部署方案。**

## 整体关系

~~~mermaid
flowchart LR
  PM["PM / 产品"] --> DOCS["已批准业务知识\nConfluence / Requirements"]
  QA["QA"] --> CAPTURE["浏览器采集入口\nExtension 或可替代方案"]
  CAPTURE --> SVC["QA Assistant 服务"]
  DOCS -. "按权限、按需读取" .-> SVC
  REPO["GitHub / GitLab\n源码及 Owner"] -. "按需查询" .-> SVC
  LOGS["日志 / 分布式 Trace\n后续集成"] -. "受控查询" .-> SVC
  SVC --> MODEL["模型运行时适配器\nProvider 待定"]
  MODEL --> SVC
  SVC --> REVIEW["QA 审核界面\n事实、证据和 Draft"]
  REVIEW -->|"人工批准"| SVC
  SVC -->|"API 创建 / 更新"| JIRA["Jira"]
  JIRA --> DEV["开发 / Coding Agent"]
  DEV --> QA
~~~

以上是**逻辑组件，不等于多个微服务**。v0.1 可以用小型 API、后台 Worker 和共用数据库实现。Model Runtime 代表获授权的可编程推理入口，**不能默认等价于某个人的 Coding Plan 订阅**。

## 模块职责

| 组件 | 确定性职责 | AI 职责 |
| --- | --- | --- |
| Capture | 记录操作、异常、Network、截图、QA 说明 | 初期无必需 |
| Intake & Evidence Storage | 校验、脱敏、存储、访问控制、关联和保留期限 | 初期无必需 |
| Context Resolver | Environment → Repo 候选映射、按需读取权威文档 | 相关性判断、冲突解释 |
| Diagnosis Worker | 异步状态、重试、输出校验、证据来源检查 | 症状、故障域、假设、证据缺口 |
| Review & Jira | 鉴权、审核、附件关联、Jira API、失败反馈 | 生成可读工单和建议团队 |
| Observability Adapter | 根据 Request/Trace ID 受控检索日志 | 解读召回的故障信号 |

## 有意保留的简化

- QA/Staging 可以映射为**候选源码分支**。**分支内容不等于真实已部署构建**；只有验证表明偏差是重要问题时，才考虑引入部署 SHA。
- QA 无须本地维护所有 Repo。
- 每个逻辑模块不必成为单独的后端服务。
- 不在 Public 仓库镜像内部 Business Knowledge；先按需查询权威来源。
- 在日志/Trace 的 Owner、权限和质量明确之前，不提前承诺跨服务完整诊断。

## 运行时处理概念

~~~mermaid
flowchart TB
  IN["接收 Observation + Evidence"] --> VALIDATE["校验、脱敏、鉴权"]
  VALIDATE --> STORE["保存证据及引用"]
  STORE --> JOB["异步任务 / Worker"]
  JOB --> RULES["按需检索 AC / 业务规则"]
  JOB --> CODE["按需检索前端候选源码"]
  JOB --> OPTIONAL["可选日志 / Trace（后续）"]
  RULES --> AI["AI 使用有类型的证据推理"]
  CODE --> AI
  OPTIONAL --> AI
  AI --> REPORT["验证 Diagnosis + Jira Draft"]
  REPORT --> QA["QA 审核"]
  QA -->|修改 / 批准| JIRA["Jira API"]
  QA -->|信息不足| RECAPTURE["补充证据 / 修正预期"]
  RECAPTURE --> JOB
~~~

## 仍需团队确认的问题

- 哪种 Chrome 接入能够稳定采集，而不违反浏览器政策或干扰调试会话？
- 服务究竟能合法调用哪种模型运行时？数据协议、成本和额度如何？
- 内部 Confluence、源码及日志平台实际提供哪些授权接口？
- Jira 的必要字段、工作流权限和 Team Ownership 来自哪里？
- 证据的脱敏范围、存储权限和保留策略是什么？

参见 [采集与诊断链路](evidence-diagnosis-pipeline.md)、[模块职责](module-map.md)和[技术验证计划](../validation/qa-capture-spike.md)。

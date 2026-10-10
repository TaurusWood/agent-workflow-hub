# 浏览器证据 → AI 诊断 → QA 审核 → Jira

**状态：待技术验证的方案草案，尚未实施。**

## 核心边界

Browser Extension **不直接调用 AI 模型**。它将有类型、受大小限制且已脱敏的 Observation + Runtime Evidence 发送到受控接入 API。服务端完成身份校验、存储、按需上下文查询、使用合法模型权限进行推理、校验结构化输出，并在 QA 批准后发布 Jira。

Browser Extension 是一个候选入口，尚不能假定它就是最合适的 Chrome 调试集成方式。

~~~mermaid
sequenceDiagram
  actor QA
  participant Browser as Chrome 采集端
  participant API as QA Assistant API
  participant Store as Evidence 存储
  participant Worker as 诊断 Worker
  participant Context as 业务规则 / 源码工具
  participant AI as 获授权模型运行时
  participant Review as QA 审核界面
  participant Jira as Jira API
  QA->>Browser: 开始录制、复现、简述异常
  Browser->>API: POST Observation + 有界证据
  API->>API: 鉴权、校验、脱敏
  API->>Store: 保存证据和关联引用
  API-->>Browser: 返回 Observation ID、接收状态
  QA->>QA: 继续其他测试用例
  API->>Worker: 投递异步诊断任务
  Worker->>Context: 按范围查询 AC 和候选源码
  Context-->>Worker: 返回引用及必要片段
  Worker->>AI: 最小化证据、上下文和证据 ID
  AI-->>Worker: 结构化 Diagnosis / Jira Draft
  Worker->>Store: 校验并保存结果
  Worker-->>Review: 通知可供人工审核
  QA->>Review: 检查证据、修正、确认
  Review->>API: 授权发布 Jira
  API->>Jira: 创建 Issue、附加允许的证据
  Jira-->>API: 返回 Issue Key
  API-->>Review: 返回 Jira 链接或失败信息
~~~

## 四个核心对象（Schema 草案）

- **Observation：** QA 提供的场景、操作、实际/预期、环境、Capture ID。
- **EvidenceBundle：** 操作、截图、Console、Network 的分项证据；包含时间、来源、敏感度和采集缺口。并不意味着所有原始 Payload 都可以送给模型。
- **DiagnosisReport：** 附证据引用的事实、推断、假设、未知；Fault Domain 及缺失证据。
- **JiraDraft：** 可读的 Actual/Expected/复现步骤、附件引用、诊断摘要、建议路由及审批状态。

参见 [JSON Schema 草案](../../schemas/README.md)和[虚构示例](../../examples/fictional-bug.md)。

## 服务端操作示例：不是已冻结的 API

| 操作 | 意图 |
| --- | --- |
| POST /observations | 接收已校验的观察元数据并启动任务 |
| POST /observations/:id/artifacts | 以权限控制方式上传有界证据 |
| GET /observations/:id | 查询采集/诊断状态 |
| GET /observations/:id/draft | 查询可读草稿及证据引用 |
| PATCH /observations/:id/draft | QA 修正草稿 |
| POST /observations/:id/approve | 审批并以幂等方式发布 Jira |

元数据与大附件是否分离是实现选项，**不是 v0.1 必须的复杂度**。以上路径仅作示意。

## Evidence 不能等于不加筛选的 HAR 全量上传

1. 优先采集较短的复现操作和故障附近的 Network / Console 信号，限制规模。
2. 利用 Capture ID、时间戳和 Request ID 关联动作、请求及截图。
3. 尽可能**上传前**脱敏 Cookie、Authorization Header、凭证、PII、Token 和敏感请求体；入站服务再次检查。
4. 经批准的原始证据与模型可见摘要分开管理，并定义访问权限、保存与删除策略。
5. 仅把相关证据和目标源码 / AC 的必要片段及稳定引用交给 AI。
6. 校验 AI 的输出格式；强结论必须对应具体 Evidence。
7. 不确定的根因只能作为建议，不能直接悄然指派个人。

## Chrome 集成待比较方案

- Recorder 可复用操作路径，但自身不覆盖完整的 Console/Network 诊断。
- chrome.debugger / CDP 可捕获运行时和网络事件，但需要权限，并可能与 DevTools 调试会话相互影响。
- DevTools Extension API 可考虑用于按需导出/采集，但可能要求打开 DevTools。
- 可把现有浏览器自动化工具作为降级路径；**不要重新造一个通用浏览器调试器**。

Source Maps 用于将报错栈映射回可读源码，默认无须取消压缩。QA/Staging 分支只能提供**候选源码**，未经部署验证不可称作“实际线上代码”。

## AI Runtime 是真正的待决项

当前 Coding Plan **不能默认当作可嵌入的服务端推理接口**。必须确认可授权的模型 API、企业方案或获准 Runner，并在实现 Worker 前验证数据处理条款、存储限制、并发、成本和可观测性。

## 不同证据等级允许不同结论

| 证据 | 安全的输出边界 |
| --- | --- |
| 仅有 QA 描述 | 标准化 Jira、Symptom 类型 |
| 操作步骤 + Console | 针对性的前端排查建议 |
| 已关联的 API 请求和响应 | 与接口相关的推断或 Fault Domain 假设 |
| 跨服务 Trace 与获准日志 | 更深入的服务链故障假设 |
| 源码 + **已验证**部署构建 | 实现级诊断，仍不自动构成 Root Cause 证明 |

只有源码不能证明哪个版本已经部署。后端诊断的深度取决于服务 Owner 对日志和跨服务关联能力的确认。

## 失败与降级

浏览器采集失败不应丢失 QA 文字。分析超时不应无限阻塞，应允许以最低合格模板提交；Jira 发布需防重，错误必须可见。

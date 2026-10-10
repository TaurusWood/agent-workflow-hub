# Bug Lifecycle：从 QA 发现异常到工程可执行 Jira

**状态：目标工作流；审核关卡已明确，自动化实施细节尚待验证。**

~~~mermaid
flowchart TB
  CASE["QA 执行测试用例"] --> ISSUE{"发现异常？"}
  ISSUE -->|否| NEXT["继续测试"]
  ISSUE -->|是| START["启动短时采集并复现"]
  START --> NOTE["QA 提交场景、实际与预期"]
  NOTE --> ACCEPT["系统接收并持久化证据"]
  ACCEPT --> NEXT
  ACCEPT --> ENRICH["后台异步：脱敏、关联与诊断"]
  ENRICH --> REPORT["Diagnosis Report + Jira Draft"]
  REPORT --> READY{"QA 审核"}
  READY -->|确认或修改| CREATE["服务端创建 Jira 并关联证据"]
  READY -->|需要补充| MORE["修正预期或重新采集"]
  MORE --> ENRICH
  CREATE --> ROUTE["按照已批准规则通知相关团队"]
  ROUTE --> FIX["开发 / Agent 排查并修复"]
  FIX --> VERIFY["QA 按原场景验证"]
  VERIFY -->|通过| CLOSE["按团队流程关闭"]
  VERIFY -->|仍失败| ISSUE
~~~

## 各环节责任

| 环节 | 人 | 确定性系统 | AI | 阶段结果 |
| --- | --- | --- | --- | --- |
| 发现 | QA 识别异常和业务场景 | 可关联测试用例 | 无必需参与 | Observation |
| 采集 | QA 启动、复现 | 记录操作、截图、Network、Console | 无必需参与 | Evidence Bundle / 采集缺口 |
| 提交 | QA 简述 Actual / Expected | 持久化、回执和任务状态 | 无必需参与 | **QA 可继续下一用例** |
| 丰富信息 | 无必需参与 | 脱敏、按需检索、异步任务管理 | 分析证据与提出假设 | Diagnosis + Draft |
| 审核 | QA 核对事实、预期和重点，必要时补充 | 展示关联证据、编辑与校验 | 可提出澄清点 | 批准或退回 |
| 发布 | QA 授权 | Jira API、附件、去重键、通知 | 不自行进行特权写操作 | Jira Key 或明确失败 |
| 修复 | 开发 / Owner | 源码、日志、Issue 状态与回归记录 | Coding Agent 可读取结构化 Jira | Fix + Verification |

**不能混淆“已接收 Evidence”和“已创建 Jira”。** 后台处理失败时必须可见，并能降级为合规最小工单；不得静默丢失观察内容。

## 最小 Jira 合同

1. 环境、业务场景和必要测试上下文。
2. 可复现步骤（手填或录制，并标明不确定项）。
3. Expected Behaviour；若有权威来源则关联。
4. Actual Behaviour。
5. Symptom 类型；有证据时关联附件/引用。
6. 缺失证据及诊断可信度。
7. 建议责任团队；未批准自动路由策略前**不默认指定个人**。

即使没有源码或 Trace，也应该产出可用工单。Root Cause 不应成为创建 Jira 的强制前置条件。

## 虚构示例

**场景：** Guest 从 Booking Summary 进入 Payment。

**实际：** 点击 Continue 后一直 Loading。

**预期：** 当还有待付余额时应进入付款页。如果未找到已批准 AC，只能标记为“QA 提供的预期，待确认”。

**证据：** 按钮点击、已脱敏请求元信息和一张截图。只有网络与 Trace 实际支持时，才能提升 Backend Fault Domain 的判断等级。

**输出：** 明确复现步骤、Expected/Actual、环境、证据和路由建议；QA 确认后发布。

## 安全与运行边界

优先短时采集，不默认全天录屏。将 Token、PII、Cookie 和敏感请求内容在传给模型或作为附件之前完成脱敏。有效 Jira 创建之后再通知团队。操作支持重试与去重，避免一份 Observation 生成多个重复 Issue。

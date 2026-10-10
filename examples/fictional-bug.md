# 虚构案例：Guest Checkout 持续 Loading

**全部数据均为虚构示例，不对应真实客户、应用、服务或截图。**

QA 发现：Guest 在 Booking Summary 点击 Continue 后页面持续 Loading。短时采集获得一次点击和一个返回 HTTP 500 的 Payment Prepare 请求。截图仅为占位引用，**并不存在真实文件**。

分析结果明确分层：

- **事实（Fact）：** 所记录请求的 HTTP 状态是 500。
- **证据支持的推断（Inference）：** API 边界出现失败信号，但根因未得到证明。
- **假设（Hypothesis）：** 前端可能没有在请求失败后正确退出 Loading 状态。
- **未知（Unknown）：** 跨服务错误链及实际部署的源码版本。

当前尚未关联获批准的 Acceptance Criteria，因此“应该进入 Payment”只表示 **QA 提供的 Expected Behaviour**，并非系统已验证的业务规则。

Jira Draft 处于 **pending_review**，需要 QA 检查预期、修正或补充证据后再发布。

## 四份对象示例

- [Observation](observation.json)
- [EvidenceBundle](evidence-bundle.json)
- [DiagnosisReport](diagnosis-report.json)
- [JiraDraft](jira-draft.json)

JSON Schema 校验通过，不代表证据真实、安全或已获批准。

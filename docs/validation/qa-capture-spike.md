# 技术验证：Chrome Evidence → AI Draft → QA 审核 → Jira

**状态：下一阶段建议实验。** 只能使用虚构 Demo 应用或获得批准的非敏感测试环境与账号。

## 目标

验证 QA 能否轻量复现一条简单故障，提交短文本 Observation，拿到包含操作、运行证据与**有界诊断**的可审核 Jira 草稿，再由 QA 批准后，通过 Jira API 创建含正确证据引用的工单。

这**不是**提前确认 Extension 形态或模型供应商。

## 六个实验 Slice

1. **Capture：** 利用 Chrome 原生能力采集点击、截图、Console 和选择性 Network 请求；比较 Recorder、CDP Debugger、DevTools 入口，记录缺失证据。
2. **Frontend Transparency：** 使用虚构前端错误验证 Stack Trace → Source Map → 可读源码位置；同时记录 Source Map 不可用或版本不匹配时的表现。
3. **EvidenceBundle：** 构造有界、已脱敏的证据，关联操作与请求、记录 Capture Gap、稳定 Evidence ID。
4. **Inference：** 只发送必要的脱敏证据及授权上下文到**获准的可编程模型接口**；返回 Fact/Inference/Hypothesis/Unknown 及结构化 Jira Draft，并做服务端校验。
5. **Review：** QA 可以阅读 Observation、证据、Fault Domain 与草稿，修正 Expected/Actual 后选择批准或退回；后台处理期间 QA 无须等待。
6. **Jira：** 在获授权的测试项目创建工单并上传/关联允许的附件；验证权限、重试、幂等和错误反馈。

## 验收 Checklist

- [ ] QA 无须专业 DevTools 操作，即可开始/结束采集并记录一次点击复现。
- [ ] 关键 Network 与 Console 能和采集时间线关联，未获得的信号要明确展示。
- [ ] 带有虚构 Token/PII 特征的测试字符串不得泄露到模型请求或 Jira 附件。
- [ ] 不把候选源码分支错误表达为已部署构建。
- [ ] Review UI 能区分 QA 原始观察、检索事实和 AI 假设。
- [ ] 覆盖分析失败、重试、任务取消与重复发布等异常。
- [ ] 即使诊断失败，仍能得到包含环境、步骤、预期、实际、证据引用和不确定性的最低合格 Jira。
- [ ] 对照记录当前手动准备 Jira 的真实时间成本。

## 应实测的成本和风险

- Chrome Debugger 权限、与已打开 DevTools 的兼容性、企业插件部署限制。
- 证据文件大小、浏览器内存、端到端延迟和 Chrome 版本差异。
- 脱敏有效性、存储与保留期限、模型数据合规范围。
- 模型调用量、Token 使用，以及现有套餐是否真的提供可编程服务调用权限（不能默认有）。
- QA 审核耗时与被误判/错误引用证据的比例。
- 实际 Jira 项目的富文本、附件、权限和工作流行为。

## 范围控制

某一 Slice 失败时应记录阻塞点，优先降级到更窄的采集方案（例如筛选截图 + Console + 已脱敏 HAR 导入），不要因此建设完整调试平台。最终结果由 QA、前端、后端、PM、平台/安全和 Jira 管理员共同评审。

**在这一验证完成前，不启动通用造数平台或复杂跨服务日志平台建设。**

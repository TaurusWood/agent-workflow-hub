# JSON Schema 草案（尚未冻结）

这四份 JSON Schema Draft 2020-12 将 QA 原始描述、运行时证据、模型推断及经人工审核的 Jira 草稿分开。

| Schema | 作用 |
| --- | --- |
| [observation.schema.json](observation.schema.json) | QA 原始观察，以及 Expected Behaviour 的来源 |
| [evidence-bundle.schema.json](evidence-bundle.schema.json) | 已脱敏事实、证据引用和采集缺口 |
| [diagnosis-report.schema.json](diagnosis-report.schema.json) | 明确标注 Fact / Inference / Hypothesis / Unknown 的诊断陈述 |
| [jira-draft.schema.json](jira-draft.schema.json) | QA 可编辑、带审批状态的工单草稿 |

**只用于产品与技术讨论，不是生产 API 合同。** 当前刻意没有完整定义：Auth / 授权、文件上传协议、保留期限、Schema 版本协商、特定 Jira 实例字段、幂等键、审计日志与 Agent 编排。这些问题应基于实际 PoC 再收敛。

## 需要保留的不变量

- 新的 AI 诊断不能覆盖原始运行时证据。
- 强诊断陈述应引用稳定的 Evidence ID；缺乏证据时只能标记 Hypothesis / Unknown。
- Expected Behaviour 必须区分 QA 提供的预期和已批准的 AC。
- Capture Gap 要明确列出。
- 上传的证据、链接和 Payload 必须受权限控制、脱敏和保留期限约束；通过 JSON Schema 校验不代表安全合规。
- 在第一阶段，只能由经过身份验证的人类审批动作触发 Jira 发布。

设计评审可以使用[完全虚构的示例](../examples/fictional-bug.md)。待技术 Spike 验证真实但已脱敏的输入，再冻结真正需要的字段，避免设计一套万能 QA 数据标准。

**兼容性原则：** 中文版本只翻译 Schema 的 title / description 与示例自由文本；属性名、枚举值、required、类型、引用 ID 保持不变。这样中文文档和后续程序仍可共享同一数据合同。

# investment-framework v4.1.0 手动测试输入

**版本**: 4.1.0
**时间**: 2026-05-29 08:27:51

请将以下内容逐个发送给 LLM，记录输出并验证。

---

## TC001: 个股分析

**输入**:
```
分析贵州茅台是否值得投资
```

**预期技能**: ['value-analyzer', 'moat-evaluator', 'intrinsic-value-calculator', 'decision-checklist']

**必填字段**: ['status', 'request_type', 'recommendation', 'confidence', 'key_risks', 'action_items']

**输出**:
```json

```

**验证**:
- [ ] JSON 格式有效
- [ ] 字段完整
- [ ] 枚举值正确
- [ ] 推理连贯

---

## TC002: 个股分析

**输入**:
```
腾讯控股 0700.HK 现在可以买入吗
```

**预期技能**: ['value-analyzer', 'moat-evaluator', 'intrinsic-value-calculator']

**必填字段**: ['status', 'request_type', 'recommendation', 'confidence']

**输出**:
```json

```

**验证**:
- [ ] JSON 格式有效
- [ ] 字段完整
- [ ] 枚举值正确
- [ ] 推理连贯

---

## TC003: 个股分析

**输入**:
```
分析一下宁德时代的护城河
```

**预期技能**: ['moat-evaluator', 'industry-specialist']

**必填字段**: ['status', 'request_type', 'analysis_result']

**输出**:
```json

```

**验证**:
- [ ] JSON 格式有效
- [ ] 字段完整
- [ ] 枚举值正确
- [ ] 推理连贯

---

## TC004: 个股分析

**输入**:
```
招商银行 vs 工商银行，哪个更值得投资
```

**预期技能**: ['value-analyzer', 'moat-evaluator', 'intrinsic-value-calculator']

**必填字段**: ['status', 'request_type', 'recommendation']

**输出**:
```json

```

**验证**:
- [ ] JSON 格式有效
- [ ] 字段完整
- [ ] 枚举值正确
- [ ] 推理连贯

---

## TC005: 个股分析

**输入**:
```
比亚迪的内在价值是多少
```

**预期技能**: ['intrinsic-value-calculator', 'value-analyzer']

**必填字段**: ['status', 'request_type', 'analysis_result']

**输出**:
```json

```

**验证**:
- [ ] JSON 格式有效
- [ ] 字段完整
- [ ] 枚举值正确
- [ ] 推理连贯

---

## TC006: 个股分析

**输入**:
```
分析一只白酒股，要求安全边际>30%
```

**预期技能**: ['value-analyzer', 'intrinsic-value-calculator', 'thousand-mile-horse-screener']

**必填字段**: ['status', 'request_type', 'recommendation', 'confidence']

**输出**:
```json

```

**验证**:
- [ ] JSON 格式有效
- [ ] 字段完整
- [ ] 枚举值正确
- [ ] 推理连贯

---

## TC007: 个股分析

**输入**:
```
药明康德现在能抄底吗
```

**预期技能**: ['value-analyzer', 'moat-evaluator', 'risk-assessor']

**必填字段**: ['status', 'request_type', 'key_risks']

**输出**:
```json

```

**验证**:
- [ ] JSON 格式有效
- [ ] 字段完整
- [ ] 枚举值正确
- [ ] 推理连贯

---

## TC008: 个股分析

**输入**:
```
分析一下长江电力的分红能力
```

**预期技能**: ['value-analyzer', 'industry-specialist']

**必填字段**: ['status', 'request_type', 'analysis_result']

**输出**:
```json

```

**验证**:
- [ ] JSON 格式有效
- [ ] 字段完整
- [ ] 枚举值正确
- [ ] 推理连贯

---

## TC009: 个股分析

**输入**:
```
海天味业符合格雷厄姆防御型标准吗
```

**预期技能**: ['value-analyzer', 'decision-checklist']

**必填字段**: ['status', 'request_type', 'analysis_result']

**输出**:
```json

```

**验证**:
- [ ] JSON 格式有效
- [ ] 字段完整
- [ ] 枚举值正确
- [ ] 推理连贯

---

## TC010: 个股分析

**输入**:
```
帮我检查一下我投资隆基绿能的逻辑是否正确
```

**预期技能**: ['decision-checklist', 'value-analyzer', 'moat-evaluator']

**必填字段**: ['status', 'request_type', 'recommendation']

**输出**:
```json

```

**验证**:
- [ ] JSON 格式有效
- [ ] 字段完整
- [ ] 枚举值正确
- [ ] 推理连贯

---

## TC011: 趋势分析

**输入**:
```
AI 现在是趋势还是泡沫
```

**预期技能**: ['future-forecaster', 'moat-evaluator']

**必填字段**: ['status', 'request_type', 'recommendation', 'confidence']

**输出**:
```json

```

**验证**:
- [ ] JSON 格式有效
- [ ] 字段完整
- [ ] 枚举值正确
- [ ] 推理连贯

---

## TC012: 趋势分析

**输入**:
```
新能源车行业还值得投资吗
```

**预期技能**: ['future-forecaster', 'industry-specialist', 'moat-evaluator']

**必填字段**: ['status', 'request_type', 'recommendation']

**输出**:
```json

```

**验证**:
- [ ] JSON 格式有效
- [ ] 字段完整
- [ ] 枚举值正确
- [ ] 推理连贯

---

## TC013: 趋势分析

**输入**:
```
半导体是趋势还是周期
```

**预期技能**: ['future-forecaster', 'industry-specialist']

**必填字段**: ['status', 'request_type', 'analysis_result']

**输出**:
```json

```

**验证**:
- [ ] JSON 格式有效
- [ ] 字段完整
- [ ] 枚举值正确
- [ ] 推理连贯

---

## TC014: 趋势分析

**输入**:
```
人形机器人现在能投资吗
```

**预期技能**: ['future-forecaster', 'moat-evaluator', 'decision-checklist']

**必填字段**: ['status', 'request_type', 'key_risks']

**输出**:
```json

```

**验证**:
- [ ] JSON 格式有效
- [ ] 字段完整
- [ ] 枚举值正确
- [ ] 推理连贯

---

## TC015: 趋势分析

**输入**:
```
分析一下低空经济是不是炒作
```

**预期技能**: ['future-forecaster', 'sentiment-analyzer']

**必填字段**: ['status', 'request_type', 'recommendation']

**输出**:
```json

```

**验证**:
- [ ] JSON 格式有效
- [ ] 字段完整
- [ ] 枚举值正确
- [ ] 推理连贯

---

## TC016: 资产配置

**输入**:
```
我 35 岁，平衡型风险偏好，如何配置资产
```

**预期技能**: ['asset-allocator', 'decision-checklist']

**必填字段**: ['status', 'request_type', 'analysis_result', 'action_items']

**输出**:
```json

```

**验证**:
- [ ] JSON 格式有效
- [ ] 字段完整
- [ ] 枚举值正确
- [ ] 推理连贯

---

## TC017: 资产配置

**输入**:
```
我有 100 万，应该怎么投资
```

**预期技能**: ['asset-allocator', 'value-analyzer']

**必填字段**: ['status', 'request_type', 'analysis_result']

**输出**:
```json

```

**验证**:
- [ ] JSON 格式有效
- [ ] 字段完整
- [ ] 枚举值正确
- [ ] 推理连贯

---

## TC018: 资产配置

**输入**:
```
25 岁，激进型，想 5 年内攒够首付
```

**预期技能**: ['asset-allocator', 'future-forecaster']

**必填字段**: ['status', 'request_type', 'recommendation']

**输出**:
```json

```

**验证**:
- [ ] JSON 格式有效
- [ ] 字段完整
- [ ] 枚举值正确
- [ ] 推理连贯

---

## TC019: 资产配置

**输入**:
```
50 岁，保守型，如何规划退休
```

**预期技能**: ['asset-allocator', 'risk-assessor']

**必填字段**: ['status', 'request_type', 'analysis_result']

**输出**:
```json

```

**验证**:
- [ ] JSON 格式有效
- [ ] 字段完整
- [ ] 枚举值正确
- [ ] 推理连贯

---

## TC020: 资产配置

**输入**:
```
现在应该增加股票仓位还是债券仓位
```

**预期技能**: ['asset-allocator', 'sentiment-analyzer', 'risk-assessor']

**必填字段**: ['status', 'request_type', 'recommendation']

**输出**:
```json

```

**验证**:
- [ ] JSON 格式有效
- [ ] 字段完整
- [ ] 枚举值正确
- [ ] 推理连贯

---

## TC021: 决策检查

**输入**:
```
我想重仓 AI 板块，帮我检查逻辑
```

**预期技能**: ['decision-checklist', 'future-forecaster', 'risk-assessor']

**必填字段**: ['status', 'request_type', 'key_risks']

**输出**:
```json

```

**验证**:
- [ ] JSON 格式有效
- [ ] 字段完整
- [ ] 枚举值正确
- [ ] 推理连贯

---

## TC022: 决策检查

**输入**:
```
我是否应该卖出所有股票持有现金
```

**预期技能**: ['decision-checklist', 'asset-allocator', 'sentiment-analyzer']

**必填字段**: ['status', 'request_type', 'recommendation']

**输出**:
```json

```

**验证**:
- [ ] JSON 格式有效
- [ ] 字段完整
- [ ] 枚举值正确
- [ ] 推理连贯

---

## TC023: 决策检查

**输入**:
```
帮我检查这个投资想法：全仓买入纳斯达克 100ETF
```

**预期技能**: ['decision-checklist', 'asset-allocator', 'risk-assessor']

**必填字段**: ['status', 'request_type', 'key_risks']

**输出**:
```json

```

**验证**:
- [ ] JSON 格式有效
- [ ] 字段完整
- [ ] 枚举值正确
- [ ] 推理连贯

---

## TC024: 边界情况

**输入**:
```
分析这家公司值得投资吗
```

**预期技能**: []

**必填字段**: ['status', 'missing_info', 'action_items']

**预期状态**: error

**输出**:
```json

```

**验证**:
- [ ] JSON 格式有效
- [ ] 字段完整
- [ ] 枚举值正确
- [ ] 推理连贯

---

## TC025: 边界情况

**输入**:
```
哪只股票明天会涨
```

**预期技能**: []

**必填字段**: ['status', 'key_risks', 'disclaimer']

**预期状态**: error

**输出**:
```json

```

**验证**:
- [ ] JSON 格式有效
- [ ] 字段完整
- [ ] 枚举值正确
- [ ] 推理连贯

---


---
name: investment-framework
version: 3.0.0
description: ［何时使用］当用户需要进行投资决策时；当用户询问"这家公司值得投资吗"时；当用户需要资产配置建议时；当用户想检查投资逻辑时；当用户想识别市场趋势时；当用户需要避免认知偏差时
author: 燃冰 + 小蚂蚁
created: 2026-03-12
updated: 2026-03-19
skill_type: 核心🔴
related_skills:
  # 价值分析端（5 个）
  - value-analyzer: 格雷厄姆标准价值分析
  - moat-evaluator: 巴菲特护城河评估
  - intrinsic-value-calculator: 内在价值计算
  - stock-picker: 彼得·林奇选股法
  - simple-investor: 简单投资原则
  # 决策支持端（4 个）
  - decision-checklist: 芒格多元思维决策检查
  - bias-detector: 认知偏差识别
  - second-level-thinker: 第二层思维
  - portfolio-designer: 组合构建
  # 趋势周期端（4 个）
  - future-forecaster: KK 未来趋势预测
  - cycle-locator: 达利欧经济周期
  - industry-analyst: 行业研究
  - global-allocator: 全球宏观配置
  # 资产配置端（2 个）
  - asset-allocator: 马尔基尔生命周期配置
  # 中国大师系列（12 个）
  - china-masters/duan-yongping: 段永平（本分 + 能力圈）
  - china-masters/li-lu: 李录（文明 + 中国机会）
  - china-masters/qiu-guolu: 邱国鹭（价值 + 品质）
  - china-masters/wu-jun: 吴军（AI 趋势 + 数据驱动）
tags: [投资框架，价值投资，资产配置，决策清单，趋势预测，周期分析]
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": [] },
        "install": [],
      },
  }
---

# 投资框架 Skill 包 📈

> 基于 13 本投资经典 + 4 位中国大师智慧的 AI 辅助投资决策系统。

**理论来源**：
- 📘 《聪明的投资者》格雷厄姆 - 安全边际、市场先生
- 📗 《证券分析》格雷厄姆 & 多德 - 内在价值、财务分析
- 📙 《巴菲特致股东的信》巴菲特 - 护城河、能力圈
- 📕 《穷查理宝典》芒格 - 多元思维、逆向思考
- 📔 《漫步华尔街》马尔基尔 - 指数基金、资产配置
- 📖 《投资最重要的事》霍华德·马克斯 - 第二层思维
- 📚 《思考，快与慢》卡尼曼 - 认知偏差
- 📓 《彼得·林奇的成功投资》彼得·林奇 - 选股法
- 📕 《投资中最简单的事》邱国鹭 - 简单投资
- 📘 《机构投资者的创新之路》- 组合构建
- 📗 《资产配置的艺术》- 全球配置
- 📙 《经济机器是怎样运行的》达利欧 - 经济周期
- 📔 《如何快速了解一个行业》- 行业研究

---

## 📋 功能描述

**核心功能**：提供完整的投资决策支持系统，从价值分析到资产配置到趋势判断到决策检查。

**适用场景**：
- 个股深度分析（"这家公司值得投资吗"）
- 资产配置方案（"我应该如何配置资产"）
- 投资决策检查（"帮我检查这个投资逻辑"）
- 趋势周期判断（"现在是市场什么位置"）
- 行业研究分析（"这个行业前景如何"）
- 认知偏差识别（"我是否有 FOMO"）

**边界条件**：
- ❌ 不提供具体买卖建议（需用户自主决策）
- ❌ 不预测短期股价波动
- ❌ 不替代深入研究和尽职调查
- ✅ 提供分析框架和决策支持
- ✅ 帮助避免常见投资错误
- ✅ 基于经典投资理论

---

## 🎯 技能矩阵（33 个）

### 技能关系图

```
                    investment-framework（主技能）
                              ↓
         ┌────────────────────┼────────────────────┐
         ↓                    ↓                    ↓
   价值分析端            决策支持端            趋势周期端
         ↓                    ↓                    ↓
  ┌──────┴──────┐      ┌──────┴──────┐      ┌──────┴──────┐
  │value-       │      │decision-    │      │future-      │
  │analyzer     │      │checklist    │      │forecaster   │
  └──────┬──────┘      └──────┬──────┘      └──────┬──────┘
         │                    │                    │
    moat-evaluator      bias-detector        cycle-locator
         │                    │                    │
  intrinsic-value      second-level        industry-analyst
  -calculator          -thinker
         │                    │
    stock-picker       portfolio-
         │               designer
    simple-
   investor
         │
         └────────────────────┬────────────────────┘
                              ↓
                    资产配置端
                              ↓
                    asset-allocator
                              ↓
                    global-allocator
                              ↓
                    中国大师系列（12 个）
```

### 技能清单

#### 价值分析端（5 个）🔴

| 技能 | 理论来源 | 核心功能 | 触发词 |
|------|----------|----------|--------|
| **value-analyzer** | 《聪明的投资者》 | 格雷厄姆标准分析 | "分析这只股票" |
| **moat-evaluator** | 《巴菲特致股东的信》 | 护城河评估 | "评估护城河" |
| **intrinsic-value-calculator** | 《证券分析》 | 内在价值计算 | "计算内在价值" |
| **stock-picker** | 《彼得·林奇的成功投资》 | 选股法 | "如何选股" |
| **simple-investor** | 《投资中最简单的事》 | 简单投资原则 | "简单投资" |

#### 决策支持端（4 个）🔴

| 技能 | 理论来源 | 核心功能 | 触发词 |
|------|----------|----------|--------|
| **decision-checklist** | 《穷查理宝典》 | 多元思维决策检查 | "检查投资逻辑" |
| **bias-detector** | 《思考，快与慢》 | 认知偏差识别 | "是否有认知偏差" |
| **second-level-thinker** | 《投资最重要的事》 | 第二层思维 | "逆向思考" |
| **portfolio-designer** | 《机构投资者的创新之路》 | 组合构建 | "构建组合" |

#### 趋势周期端（4 个）🟡

| 技能 | 理论来源 | 核心功能 | 触发词 |
|------|----------|----------|--------|
| **future-forecaster** | 《必然》《失控》 | KK 未来趋势预测 | "这是趋势吗" |
| **cycle-locator** | 《经济机器是怎样运行的》 | 经济周期定位 | "市场周期位置" |
| **industry-analyst** | 《如何快速了解一个行业》 | 行业研究 | "分析这个行业" |
| **global-allocator** | 《资产配置的艺术》 | 全球宏观配置 | "全球配置" |

#### 资产配置端（2 个）🔴

| 技能 | 理论来源 | 核心功能 | 触发词 |
|------|----------|----------|--------|
| **asset-allocator** | 《漫步华尔街》 | 生命周期配置 | "如何配置资产" |
| **global-allocator** | 《资产配置的艺术》 | 全球配置 | "全球分散" |

#### 中国大师系列（12 个）🟡

| 大师 | 技能 | 核心功能 |
|------|------|----------|
| **段永平** | SKILL.md | 本分 + 能力圈 |
| | culture-analyzer | 企业文化分析 |
| | longterm-checker | 长期思维检查 |
| **李录** | SKILL.md | 文明 + 中国机会 |
| | civilization-analyzer | 文明视角分析 |
| | china-opportunity | 中国机会识别 |
| **邱国鹭** | SKILL.md | 价值 + 品质 |
| | valuation-analyzer | 价值分析 |
| | quality-analyzer | 品质投资分析 |
| **吴军** | SKILL.md | AI 趋势 + 数据驱动 |
| | ai-trend-analyzer | AI 趋势分析 |
| | data-driven-investor | 数据驱动投资 |

---

## 🔄 组合使用流程

### 流程 1：个股深度分析（推荐）

```
【适用场景】分析具体公司是否值得投资

Step 1: simple-investor → 快速初筛（是否简单易懂）
        输入：公司描述
        输出：是否符合简单投资原则

Step 2: value-analyzer → 格雷厄姆标准分析
        输入：财务数据
        输出：防御型/积极型评估

Step 3: moat-evaluator → 护城河评估
        输入：商业模式、竞争格局
        输出：护城河类型、强度评分

Step 4: intrinsic-value-calculator → 内在价值计算
        输入：财务数据
        输出：多种方法估值、安全边际

Step 5: decision-checklist → 决策检查
        输入：投资想法
        输出：能力圈、认知偏差检查

Step 6: asset-allocator → 仓位控制
        输入：配置方案、当前组合
        输出：建议仓位

【输出】完整投资分析报告
```

### 流程 2：趋势驱动型投资

```
【适用场景】识别和把握长期趋势

Step 1: future-forecaster → 识别趋势
Step 2: cycle-locator → 周期位置
Step 3: industry-analyst → 行业分析
Step 4: moat-evaluator → 护城河评估
Step 5: intrinsic-value-calculator → 估值
Step 6: decision-checklist → 检查 FOMO
Step 7: asset-allocator → 配置

【输出】趋势驱动型投资方案
```

### 流程 3：市场周期判断

```
【适用场景】判断市场位置，决定仓位

Step 1: cycle-locator → 经济周期定位
Step 2: second-level-thinker → 市场情绪分析
Step 3: bias-detector → 自我偏差检查
Step 4: asset-allocator → 仓位建议

【输出】市场周期报告 + 仓位建议
```

### 流程 4：资产配置方案

```
【适用场景】制定或调整资产配置

Step 1: asset-allocator → 设计配置方案
Step 2: global-allocator → 全球分散
Step 3: portfolio-designer → 组合构建
Step 4: decision-checklist → 最终检查

【输出】完整资产配置方案
```

### 流程 5：中国大师智慧应用

```
【适用场景】用中国大师智慧分析

段永平：
1. culture-analyzer → 企业文化分析
2. longterm-checker → 长期思维检查
3. 核心：本分 + 能力圈

李录：
1. civilization-analyzer → 文明视角
2. china-opportunity → 中国机会识别
3. 核心：文明 + 中国

邱国鹭：
1. valuation-analyzer → 价值分析
2. quality-analyzer → 品质投资
3. 核心：价值 + 品质

吴军：
1. ai-trend-analyzer → AI 趋势
2. data-driven-investor → 数据驱动
3. 核心：趋势 + 数据

【输出】中国大师视角分析报告
```

---

## ⚠️ 常见错误

### 错误 1：跳过深度分析直接决策
```
失败案例：
• 只听消息买入，未做价值分析
• 忽视护城河评估
• 结果：亏损 50%+

正确做法：
✓ 至少完成 simple→value→moat→intrinsic→decision
✓ 用 check-list 确保流程完整
✓ 安全边际<30% 不买入

预防清单：
- [ ] 是否分析了护城河？
- [ ] 是否计算了内在价值？
- [ ] 安全边际是否>30%？
- [ ] 是否在能力圈内？
```

### 错误 2：混淆趋势层级
```
失败案例：
• 把流行趋势当技术变革（如某些元宇宙概念）
• 用长期逻辑投资短期热点
• 结果：趋势退潮后深套

正确做法：
✓ 用 future-forecaster (layer-analyzer) 判断层级
✓ 流行趋势层：保持距离，不重仓
✓ 技术层：核心关注，识别爆发点
✓ 基础设施层：长期持有

预防清单：
- [ ] 这是流行/技术/基础设施？
- [ ] 变化速度是年/3-5 年/10 年 +？
- [ ] 投资周期是否匹配？
```

### 错误 3：忽视认知偏差
```
失败案例：
• 过度自信重仓单一股票
• 确认偏误只看利好信息
• 损失厌恶死扛亏损股
• 结果：重大损失

正确做法：
✓ 每次决策前用 decision-checklist + bias-detector
✓ 特别检查：过度自信/确认偏误/从众心理/损失厌恶
✓ 用 second-level-thinker 逆向思考

预防清单：
- [ ] 是否只看了利好信息？
- [ ] 是否找了反面证据？
- [ ] 仓位是否过度集中？
- [ ] 是否因亏损而不愿卖出？
```

### 错误 4：机械套用格雷厄姆标准
```
失败案例：
• 用同一标准评估所有行业
• 科技股用 P/B<1.5 标准
• 结果：错过优质成长股

正确做法：
✓ 传统行业：严格套用标准
✓ 科技行业：调整标准（更关注护城河）
✓ 结合 moat-evaluator 综合判断
✓ 用 stock-picker 彼得·林奇方法补充

预防清单：
- [ ] 行业类型是什么？
- [ ] 格雷厄姆标准是否适用？
- [ ] 护城河是否足够强？
- [ ] 是否需调整估值方法？
```

### 错误 5：资产配置僵化
```
失败案例：
• 机械套用"100-年龄"公式
• 忽视个人风险承受能力差异
• 结果：配置与实际不匹配

正确做法：
✓ 用 asset-allocator 综合评估
✓ 考虑年龄/收入/目标/经验
✓ 用 global-allocator 全球分散
✓ 定期再平衡但不机械

预防清单：
- [ ] 是否评估了风险承受能力？
- [ ] 配置是否符合投资目标？
- [ ] 是否有应急资金？
- [ ] 再平衡频率是否合理？
```

### 错误 6：能力圈外投资
```
失败案例：
• 投资完全不理解的行业（如生物医药）
• 只听"专家"推荐不做研究
• 结果：无法判断真假，亏损离场

正确做法：
✓ 用 decision-checklist 检查能力圈
✓ 能力圈外坚决不投（或先学习）
✓ 用 simple-investor 简化理解
✓ 用中国大师智慧（段永平：本分）

预防清单：
- [ ] 我是否理解这个商业模式？
- [ ] 能否预测 10 年后行业格局？
- [ ] 是否有相关专业知识？
- [ ] 是否投资过类似公司？
```

### 错误 7：忽视安全边际
```
失败案例：
• 好公司但价格过高时买入
• 忽视安全边际的重要性
• 结果：好公司也亏钱

正确做法：
✓ 用 intrinsic-value-calculator 计算价值
✓ 安全边际<30% 不买入
✓ 等待好价格
✓ 用 second-level-thinker 思考市场情绪

预防清单：
- [ ] 内在价值是多少？
- [ ] 安全边际是否>30%？
- [ ] 当前价格是否合理？
- [ ] 是否可等待更好价格？
```

### 错误 8：忽视周期位置
```
失败案例：
• 周期顶部重仓
• 周期底部轻仓或空仓
• 结果：高位套牢，低位踏空

正确做法：
✓ 用 cycle-locator 判断周期位置
✓ 顶部：降低仓位，防守为主
✓ 底部：增加仓位，进攻为主
✓ 用 second-level-thinker 逆向投资

预防清单：
- [ ] 当前经济周期位置？
- [ ] 市场情绪如何？
- [ ] 仓位是否匹配周期？
- [ ] 是否逆向思考？
```

---

## 📊 输入参数

### 主技能输入（路由到子技能）

```json
{
  "request_type": {
    "type": "string",
    "enum": ["个股分析", "趋势分析", "资产配置", "决策检查", "周期判断", "行业分析", "中国大师智慧"],
    "required": true,
    "description": "请求类型，路由到对应子技能"
  },
  "company_name": {
    "type": "string",
    "required": false,
    "description": "公司名称（个股分析时必填）"
  },
  "financial_data": {
    "type": "object",
    "required": false,
    "description": "财务数据（个股分析时提供）"
  },
  "trend_observation": {
    "type": "string",
    "required": false,
    "description": "趋势观察描述（趋势分析时必填）"
  },
  "investor_profile": {
    "type": "object",
    "properties": {
      "age": {"type": "number"},
      "risk_tolerance": {"type": "string"},
      "investment_goal": {"type": "string"},
      "total_assets": {"type": "number"}
    },
    "required": false,
    "description": "投资者画像（资产配置时必填）"
  },
  "investment_idea": {
    "type": "string",
    "required": false,
    "description": "投资想法描述（决策检查时必填）"
  },
  "master_preference": {
    "type": "string",
    "enum": ["duan-yongping", "li-lu", "qiu-guolu", "wu-jun"],
    "required": false,
    "description": "偏好的大师视角（中国大师分析时选用）"
  }
}
```

---

## 📤 输出格式

### 统一输出结构

```json
{
  "status": "success",
  "data": {
    "request_type": "个股分析 | 趋势分析 | 资产配置 | 决策检查 | 周期判断 | 行业分析",
    "skills_used": ["value-analyzer", "moat-evaluator", "..."],
    "analysis_result": {},
    "recommendation": "强烈推荐 | 推荐 | 观察 | 谨慎 | 避免",
    "key_risks": [],
    "action_items": [],
    "next_steps": []
  }
}
```

### 各技能输出详见子技能文档

- `value-analyzer/SKILL.md` - 价值分析输出
- `moat-evaluator/SKILL.md` - 护城河评估输出
- `intrinsic-value-calculator/SKILL.md` - 估值输出
- `decision-checklist/SKILL.md` - 决策检查输出
- `asset-allocator/SKILL.md` - 资产配置输出
- `future-forecaster/SKILL.md` - 趋势预测输出
- `cycle-locator/SKILL.md` - 周期定位输出
- `industry-analyst/SKILL.md` - 行业分析输出
- `china-masters/*/SKILL.md` - 中国大师视角输出

---

## 🧪 使用示例

### 示例 1：个股深度分析（贵州茅台）

**用户输入**：
```
分析贵州茅台是否值得投资
```

**处理流程**：
```
1. simple-investor → 快速初筛
2. value-analyzer → 格雷厄姆标准评估
3. moat-evaluator → 护城河评估
4. intrinsic-value-calculator → 内在价值计算
5. decision-checklist → 决策检查
6. asset-allocator → 仓位建议
```

**输出**：
```
【贵州茅台投资价值分析】

【简单投资评估】（simple-investor）
- 商业模式：简单易懂（高端白酒）✅
- 盈利模式：清晰（生产 + 销售）✅
- 是否符合简单投资：是

【价值分析】（value-analyzer）
- 投资者类型：积极型
- 符合标准：5/7（规模/财务/盈利/分红/增长✓，P/B/P/E✗）
- 初评：不符合防御型标准，适合积极型投资者

【护城河评估】（moat-evaluator）
- 护城河类型：品牌优势（5/5）、特许经营权（4/5）
- 综合评分：16/25 分（强）
- 趋势：稳定

【内在价值】（intrinsic-value-calculator）
- 多种方法估值：¥900-1100
- 当前价格：¥1700
- 安全边际：-35%（高估）

【决策检查】（decision-checklist）
- 能力圈评分：18/20（能力圈内）
- 认知偏差：1/8（低）
- 逻辑完整性：4/5

【仓位建议】（asset-allocator）
- 当前安全边际不足，建议仓位：0%

【综合建议】
建议：观察（等待更好价格）
理由：
1. 护城河强（16/25 分）
2. 但安全边际不足（-35%）
3. 建议等待更好价格（<¥1000）

【行动项】
1. 加入观察列表
2. 设定理想买入价：¥800-900
3. 持续跟踪护城河变化
```

### 示例 2：资产配置方案

**用户输入**：
```
我 35 岁，平衡型风险偏好，有 100 万，如何配置资产？
```

**处理流程**：
```
1. asset-allocator → 设计配置方案
2. global-allocator → 全球分散建议
3. portfolio-designer → 组合构建
4. decision-checklist → 最终检查
```

**输出**：
```
【35 岁平衡型资产配置方案】

【风险承受评估】（asset-allocator）
- 年龄：35 岁（中年）
- 风险偏好：平衡
- 投资期限：25 年 +（退休）
- 综合风险等级：平衡

【资产配置】（asset-allocator）
| 资产类别 | 比例 | 金额（100 万） |
| 股票 | 65% | 65 万 |
| 债券 | 25% | 25 万 |
| 现金 | 5% | 5 万 |
| 另类 | 5% | 5 万 |

股票细分：
- 国内指数：40%（26 万，沪深 300ETF）
- 国际指数：25%（16.25 万，标普 500ETF）

【全球分散】（global-allocator）
- 国内：60%
- 国际：40%（美国/欧洲/新兴市场）

【再平衡策略】
- 频率：每年 1 次（建议年初）
- 阈值：偏离>5% 时调整

【定投计划】
假设每月可投资 1 万：
- 沪深 300ETF：¥4000
- 标普 500ETF：¥2500
- 国债 ETF：¥2500
- 货币基金：¥1000

【决策检查】（decision-checklist）
- 配置逻辑：✓ 符合生命周期理论
- 风险认知：✓ 理解波动风险
- 长期承诺：✓ 准备持有 25 年 +

【综合建议】
建议：执行配置方案
理由：
1. 配置匹配风险承受能力
2. 全球分散降低风险
3. 定期定额降低择时风险

【行动项】
1. 开立证券账户
2. 设置基金定投（自动扣款）
3. 日历提醒：每年年初再平衡
```

---

## 📚 核心理念

### 投资第一性原理

```
好投资 = 好公司 × 好价格 × 长期持有 × 理性决策

好公司：moat-evaluator（护城河强）
好价格：intrinsic-value-calculator（安全边际>30%）
长期持有：asset-allocator（生命周期匹配）
理性决策：decision-checklist + bias-detector（避免认知偏差）
```

### 格雷厄姆安全边际

```
用 4 毛钱买 1 块钱的东西

核心公式：
安全边际 = (内在价值 - 当前价格) / 内在价值 × 100%

建议：
- 防御型：安全边际>30%
- 积极型：安全边际>50%
```

### 巴菲特护城河

```
护城河是结构性优势，不是短期优势

5 大护城河：
1. 品牌优势（用户愿付溢价）
2. 网络效应（用户越多价值越大）
3. 转换成本（用户更换困难）
4. 规模优势（规模带来成本优势）
5. 特许经营权（政府授权/专利）

真正的护城河必须能持续 10 年+
```

### 芒格多元思维

```
好决策 = 能力圈内 × (1 - 认知偏差) × 逻辑完整性 × 逆向思考

关键原则：
1. 能力圈外坚决不投
2. 认知偏差是最大敌人
3. 逆向思考（反过来想）
4. 清单是思考工具不是形式
```

### 马尔基尔资产配置

```
长期稳健收益 = 资产配置 × 定期定额 × 再平衡 × 全球分散

核心原则：
1. 定期定额投资（不择时）
2. 分散化（不要把所有鸡蛋放一个篮子）
3. 低成本（选择低费率指数基金）
4. 再平衡（每年调整一次）
5. 全球分散（地域分散）
```

### 霍华德·马克斯第二层思维

```
第一层思维：
"这是一家好公司，应该买入"

第二层思维：
"这是一家好公司，但价格已经反映了好，甚至高估了，应该等待"

关键：
1. 思考市场共识是什么
2. 思考共识是否正确
3. 思考什么情况下共识会错
```

### 达利欧经济周期

```
经济机器运行三要素：
1. 生产率增长（长期）
2. 债务周期（中期 5-8 年）
3. 去杠杆（长期债务周期 50-75 年）

应用：
- 周期顶部：降低仓位，防守
- 周期底部：增加仓位，进攻
- 和谐去杠杆：收入增长>债务利率
```

### 段永平本分 + 能力圈

```
本分：
- 做对的事情
- 把事情做对
- 不占人便宜

能力圈：
- 只投资能理解的公司
- 能力圈外坚决不投
- 持续学习扩大能力圈
```

### 健康公式

```
投资成功 = 能力圈 × 安全边际 × 护城河 × 长期思维 × (1 - 认知偏差) × 周期位置

关键变量：
- 能力圈：只投理解的
- 安全边际：价格<价值 30%+
- 护城河：结构性优势 10 年 +
- 长期思维：持有期 5 年 +
- 认知偏差：越少越好
- 周期位置：底部进攻，顶部防守
```

---

## 🔗 相关资源

### 渐进式披露结构

**核心文档**（本文件）：
- 投资框架总览和组合使用流程

**子技能文档**：
- `value-analyzer/SKILL.md` - 价值分析详情
- `moat-evaluator/SKILL.md` - 护城河评估详情
- `intrinsic-value-calculator/SKILL.md` - 估值计算详情
- `decision-checklist/SKILL.md` - 决策检查详情
- `asset-allocator/SKILL.md` - 资产配置详情
- `future-forecaster/SKILL.md` - 趋势预测详情
- `cycle-locator/SKILL.md` - 周期定位详情
- `industry-analyst/SKILL.md` - 行业分析详情
- `china-masters/*/SKILL.md` - 中国大师智慧详情

**参考资料**（references/）：
- `references/graham-principles.md` - 格雷厄姆核心原则
- `references/buffett-moat.md` - 巴菲特护城河理论
- `references/munger-models.md` - 芒格多元思维模型
- `references/malkiel-allocation.md` - 马尔基尔资产配置
- `references/marks-thinking.md` - 霍华德·马克斯第二层思维
- `references/dalio-cycle.md` - 达利欧经济周期
- `references/kk-prediction.md` - KK 未来预测方法论
- `references/chinese-masters.md` - 中国大师智慧合集

**示例集合**（examples/）：
- `examples/tech-company-analysis.md` - 科技公司分析示例
- `examples/consumer-company-analysis.md` - 消费公司分析示例
- `examples/trend-analysis.md` - 趋势分析示例
- `examples/allocation-cases.md` - 资产配置案例
- `examples/decision-cases.md` - 决策检查案例
- `examples/cycle-cases.md` - 周期判断案例

**模板文件**（templates/）：
- `templates/investment-report-template.md` - 投资分析报告模板
- `templates/decision-checklist-template.md` - 决策清单模板
- `templates/allocation-plan-template.md` - 配置方案模板
- `templates/review-template.md` - 复盘报告模板

**计算工具**（calculators/）：
- `calculators/valuation.py` - 估值计算脚本
- `calculators/safety-margin.py` - 安全边际计算
- `calculators/allocation.py` - 配置比例计算

---

## 🔗 相关文件

### 子技能文件路径

```
investment-framework-skill/
├── SKILL.md（本文件）
├── value-analyzer/
│   └── SKILL.md
├── moat-evaluator/
│   └── SKILL.md
├── intrinsic-value-calculator/
│   └── SKILL.md
├── decision-checklist/
│   └── SKILL.md
├── asset-allocator/
│   └── SKILL.md
├── future-forecaster/
│   └── SKILL.md
├── cycle-locator/
│   └── SKILL.md
├── industry-analyst/
│   └── SKILL.md
├── stock-picker/
│   └── SKILL.md
├── simple-investor/
│   └── SKILL.md
├── bias-detector/
│   └── SKILL.md
├── second-level-thinker/
│   └── SKILL.md
├── portfolio-designer/
│   └── SKILL.md
├── global-allocator/
│   └── SKILL.md
└── china-masters/
    ├── duan-yongping/
    │   ├── SKILL.md
    │   ├── culture-analyzer/
    │   └── longterm-checker/
    ├── li-lu/
    │   ├── SKILL.md
    │   ├── civilization-analyzer/
    │   └── china-opportunity/
    ├── qiu-guolu/
    │   ├── SKILL.md
    │   ├── valuation-analyzer/
    │   └── quality-analyzer/
    └── wu-jun/
        ├── SKILL.md
        ├── ai-trend-analyzer/
        └── data-driven-investor/
```

### 理论文档

- `THEORY.md` - 5 本核心理论详解
- `ADVANCED_THEORY.md` - 6 本进阶理论详解
- `ADVANCED_THEORY_II.md` - 达利欧 + 行业研究理论
- `APPLICATION_GUIDE.md` - 完整应用指南
- `USAGE.md` - 使用手册
- `workflows/WORKFLOW_GUIDE.md` - 自动化工作流指南

---

## 更新日志

- v3.0.0 (2026-03-19): 按照 SKILL-STANDARD-v2.md 深度重构
  - 添加完整 Front Matter（version/author/skill_type/related_skills）
  - description 改为触发说明式
  - skill_type 标注为"核心🔴"
  - related_skills 说明 33 个子技能关系
  - 添加技能关系图和组合流程
  - 添加 8 个常见错误（从失败案例提炼）
  - 添加渐进式披露结构（references/examples/templates/calculators）
  - 标准化输入输出格式（JSON Schema）
  - 添加 2 个完整使用示例
  - 优化核心理念和健康公式
  - 整合中国大师系列（12 个技能）

- v1.1.0 (2026-03-16): 新增 future-forecaster 技能

- v1.0.0 (2026-03-12): 初始版本，包含 5 个核心技能

---

*投资是认知的变现。用框架提升认知，用纪律保护资本，用时间换取复利。* 📈

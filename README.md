# 投资框架技能体系 · 完整版

**一人 CEO 的投资决策系统**

<p align="center">
  <a href="#快速开始"><img src="https://img.shields.io/badge/6_Skill-投资决策-d6a52e?style=for-the-badge" alt="6 Skill"/></a>
  <a href="https://github.com/lj22503/investment-framework-skill/blob/main/README_EN.md"><img src="https://img.shields.io/badge/English-README-blue?style=for-the-badge" alt="English README"/></a>
  <a href="https://github.com/lj22503/investment-framework-skill/blob/main/llms.txt"><img src="https://img.shields.io/badge/llms.txt-AI_Ready-green?style=for-the-badge" alt="llms.txt"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="MIT License"/></a>
  <a href="#4-个定期工作流"><img src="https://img.shields.io/badge/4_工作流-定期跟踪-purple?style=for-the-badge" alt="4 工作流"/></a>
</p>

<p align="center">
  <strong>13 本投资经典 · 6 个核心模块 · 4 个定期工作流</strong>
</p>

<!-- TODO: 添加 ≤10 秒的演示 GIF，提升 50% 转化率（见 GitHub 增长策略报告） -->

> **版本**: v3.0.0 | **作者**: 燃冰 + ant  
> **核心理念**: 从事件出发，挖掘信号，用范蠡视角解读，辅助投资决策

## 解决什么问题？

| 现状 | 用这个 Skill |
|------|-------------|
| 面对事件不知道怎么看 | 范蠡商情研判系统，4步拆解 |
| 不知道配什么基金 | 基金深度分析 + 实时数据 |
| 不知道现在该几成仓 | 周期定位 + 资产配置 |
| 不知道自己有没有认知偏差 | 偏见识别 + 决策检查 |

---

## 🎯 投资框架全景图

```
事件研判 → 信号挖掘 → 范蠡解读 → 操盘建议
   ↓          ↓          ↓          ↓
范蠡商情    信号库     三谋三怠   具体标的
研判系统              天时地利  仓位止损
                        人和      周期节奏
```

---

## 6 个核心模块

| 模块 | Skill | 核心功能 | 典型触发词 |
|------|-------|---------|-----------|
| ⭐ 事件研判 | `fanli-analyzer` | 采集/选择/判定/分析，四层拆解 | "分析这个事件"、"央行降准怎么看" |
| 基金分析 | `fund-analyzer-pro` | 持仓/业绩/风险深度分析 | "分析易方达蓝筹"、"对比这3个基金" |
| 资产配置 | `asset-allocator` | 美林时钟/风险平价/仓位建议 | "帮我配置100万"、"现在几成仓" |
| 周期定位 | `cycle-locator` | 康波/房地产/库存周期 | "现在什么周期"、"拐点到了吗" |
| 偏见识别 | `bias-detector` | 损失厌恶/从众/过度自信识别 | "我这样决策对吗"、"我有什么偏见" |
| 中国大师 | `china-masters` | 巴菲特/芒格/达利欧中国化视角 | "巴菲特会怎么看"、"用芒格思维分析" |

---

## 快速开始

### 1. 安装核心技能

```bash
clawhub install fanli-analyzer        # 事件研判（核心）
clawhub install fund-analyzer-pro     # 基金分析
clawhub install asset-allocator       # 资产配置
clawhub install cycle-locator         # 周期定位
clawhub install bias-detector         # 偏见识别
clawhub install china-masters         # 中国大师
```

### 2. 配置数据源（如需）

```bash
export QVERIS_API_KEY=sk-xxx          # 北向资金/宏观经济
export TTFUND_API_KEY=ttf_xxx       # 基金数据
```

### 3. 典型调用

```
帮我分析这个事件：央行宣布降准0.5个百分点

分析这个基金：易方达蓝筹精选

帮我配置100万，风险偏好中等

现在处于什么周期？

我这样决策对吗？最近想全仓押注新能源
```

---

## 4 个定期工作流

| 工作流 | 触发命令 | 时间 | 输出 |
|--------|---------|------|------|
| 每日市场扫描 | `@ant 每日市场扫描` | 交易日 09:00 | 仓位建议 + 风险提示 |
| 周度行业跟踪 | `@ant 周度行业跟踪` | 周一 10:00 | 行业配置建议 |
| 月度组合复盘 | `@ant 月度组合复盘` | 月末 | 调仓建议 + 诊断报告 |
| 季度深度研究 | `@ant 季度深度研究` | 季初 | 宏观分析 + 重点行业 |

---

## 数据源（8个）

| 数据源 | 类型 | 用途 |
|--------|------|------|
| QVeris API | 付费 | 北向资金/宏观经济 |
| 东方财富 API | 免费 | 大盘指数/个股行情 |
| 新浪财经 API | 免费 | 实时行情 |
| 港交所披露易 | 免费 | 北向/南向资金 |
| 国家统计局 | 免费 | 宏观经济数据 |
| 央行官网 | 免费 | 货币政策数据 |
| 且慢 MCP | 付费 | 全市场投顾策略 |
| 天天基金 API | 付费 | 基金净值/持仓 |

---

## 数据缓存策略

| 数据类型 | 缓存周期 |
|---------|---------|
| 宏观经济（GDP/CPI/PMI） | 7 天 |
| 北向资金 | 1 天 |
| 大盘指数 | 实时 |
| 基金净值 | 1 天 |
| 投顾策略 | 7 天 |

---

## 触发词映射（Agent 调用索引）

| 用户说 | 调用 Skill |
|--------|----------|
| "分析XX事件"、"怎么看" | `fanli-analyzer` |
| "降准了"、"油价涨了"、"这个数据" | `fanli-analyzer` |
| "分析这只基金"、"基金怎么样" | `fund-analyzer-pro` |
| "对比这X个基金/策略" | `fund-analyzer-pro` |
| "帮我配置XX万"、"怎么分配" | `asset-allocator` |
| "现在该几成仓"、"加仓还是减仓" | `asset-allocator` |
| "什么周期"、"康波"、"拐点" | `cycle-locator` |
| "萧条期配置什么"、"复苏期买什么" | `cycle-locator` |
| "我这样对吗"、"有没有偏见" | `bias-detector` |
| "全仓押注"、"想加杠杆" | `bias-detector` |
| "巴菲特视角"、"芒格会怎么看" | `china-masters` |
| "价值投资怎么做" | `china-masters` |
| "每日市场扫描"、"今天市场怎么样" | 工作流：fanli-analyzer + 市场情绪 |
| "周度跟踪"、"行业动态" | 工作流：cycle-locator + industry-rank |
| "月度复盘"、"持仓诊断" | 工作流：fund-analyzer-pro + holding-diagnoser |
| "季度研究"、"宏观分析" | 工作流：cycle-locator + 宏观分析 |

---

## FAQ

**Q：这个和直接问 AI 有什么区别？**

A：有结构。普通 AI 回答随心情，这个 Skill 有固定的研判流程（采集→选择→判定→分析），输出格式标准化，不会跳步。

**Q：需要付费数据源吗？**

A：不需要。东方财富/新浪财经/港交所/国家统计局等免费数据源已覆盖基础需求。付费 API（QVeris/且慢）仅增强北向资金和投顾策略的精度。

**Q：能直接给买卖建议吗？**

A：不能给具体标的的买入卖出建议，但能给出行业配置方向、仓位建议、偏见纠偏，帮助你做出更好的决策。

**Q：数据存在哪里？**

A：本 Skill 不存储数据，只处理你提供的持仓数据。所有分析在对话中完成。

**Q：和 SoloAdvisor-Toolkit 是什么关系？**

A：这是投资框架层，SoloAdvisor-Toolkit 是投顾流程层。前者专注"市场怎么看、基金好不好、周期在哪里"，后者专注"KYC→配置→产品→组合→报告"的全流程。

---

## 版本历史

<details>
<summary>点击展开 v1.0→v3.0 演进记录</summary>

### v3.0.0（2026-04-16）
- 新增范蠡商情研判系统（fanli-analyzer v2.0.4）
- 四层心法（采集/选择/判定/分析）
- 信息过滤（传闻/猜测/单次事件）
- 输出格式升级（数据锚点 + 可执行颗粒度）

### v2.0.0（2026-03-20）
- 新增基金分析技能（fund-analyzer-pro）
- 且慢 MCP + 天天基金 API 集成

### v1.0.0（2026-03-01）
- 初始版本：资产配置 + 周期定位 + 偏见识别 + 中国大师

</details>

---

## ⚠️ 免责声明

本文内容仅供参考，不构成任何投资建议。市场有风险，投资需谨慎。请独立判断并自行承担风险。

---

**GitHub**: https://github.com/lj22503/investment-framework-skill  
**ClawHub**: `clawhub install investment-framework`

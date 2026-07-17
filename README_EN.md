# Investment Framework Skill System · Complete Edition

**One-Person CEO's Investment Decision System**

## What problem does this solve?

| Pain Point | How this Skill helps |
|---|---|
| You face an event but don't know how to read it | Fan-Li event analysis system — 4-layer decomposition |
| You don't know which fund to allocate | Deep fund analysis + real-time data |
| You don't know your current position size | Cycle positioning + asset allocation |
| You don't know your cognitive biases | Bias detection + decision check |

## Investment Framework Overview

```
Event Analysis → Signal Mining → Fan-Li Interpretation → Trading Advice
     ↓               ↓                  ↓                    ↓
  Fan-Li         Signal          3 Strategies        Specific Targets
  System         Library        3 Avoidances       Position / Stop-Loss
                                 Timing-Location    Cycle Rhythm
                                 -People
```

## 6 Core Modules

| Module | Skill | Core Function | Sample Triggers |
|---|---|---|---|
| ⭐ Event Analysis | `fanli-analyzer` | Collect/Select/Judge/Analyze — 4-layer decomposition | "Analyze this event", "PBOC RRR cut — what's your view" |
| Fund Analysis | `fund-analyzer-pro` | Holdings/performance/risk deep analysis | "Analyze E Fund Blue Chip", "Compare these 3 funds" |
| Asset Allocation | `asset-allocator` | Merrill clock / risk parity / position advice | "Help me allocate 1M RMB", "Current position size" |
| Cycle Positioning | `cycle-locator` | Kondratieff / real estate / inventory cycles | "What cycle are we in", "Inflection point?" |
| Bias Detection | `bias-detector` | Loss aversion / herding / overconfidence | "Is my decision right", "What biases do I have" |
| China Masters | `china-masters` | Buffett/Munger/Dalio applied to China context | "How would Buffett see this", "Apply Munger's thinking" |

## Quick Start

### 1. Install Core Skills

```bash
clawhub install fanli-analyzer        # Event analysis (core)
clawhub install fund-analyzer-pro     # Fund analysis
clawhub install asset-allocator       # Asset allocation
clawhub install cycle-locator         # Cycle positioning
clawhub install bias-detector         # Bias detection
clawhub install china-masters         # China masters
```

### 2. Configure Data Sources (optional)

```bash
export QVERIS_API_KEY=sk-xxx          # Northbound flows / macro data
export TTFUND_API_KEY=ttf_xxx       # Fund data
```

### 3. Sample Invocations

```
Analyze this event: PBOC announces 0.5% RRR cut

Analyze this fund: E Fund Blue Chip Selected

Help me allocate 1M RMB with medium risk preference

What cycle are we in right now?

Is my decision right? I'm thinking of going all-in on new energy
```

## 4 Periodic Workflows

| Workflow | Trigger Command | Time | Output |
|---|---|---|---|
| Daily Market Scan | `@ant 每日市场扫描` | Trading day 09:00 | Position advice + risk alerts |
| Weekly Industry Track | `@ant 周度行业跟踪` | Mon 10:00 | Industry allocation advice |
| Monthly Portfolio Review | `@ant 月度组合复盘` | End of month | Rebalance advice + diagnostic report |
| Quarterly Deep Research | `@ant 季度深度研究` | Beginning of quarter | Macro analysis + key industries |

## 8 Data Sources

| Source | Type | Use |
|---|---|---|
| QVeris API | Paid | Northbound / macro |
| Eastmoney API | Free | Index / stock quotes |
| Sina Finance API | Free | Real-time quotes |
| HKEX Disclosure | Free | Northbound / Southbound |
| National Bureau of Statistics | Free | Macro economic data |
| PBOC Official | Free | Monetary policy data |
| Qiemai MCP | Paid | Market-wide advisory strategies |
| Tiantian Fund API | Paid | Fund NAV / holdings |

## Trigger Word Mapping (Agent Index)

| User Says | Invokes Skill |
|---|---|
| "Analyze XX event", "What's your view" | `fanli-analyzer` |
| "RRR cut", "Oil price up", "This data" | `fanli-analyzer` |
| "Analyze this fund", "How's this fund" | `fund-analyzer-pro` |
| "Compare these X funds / strategies" | `fund-analyzer-pro` |
| "Help me allocate XX M", "How to distribute" | `asset-allocator` |
| "Current position size", "Add or reduce" | `asset-allocator` |
| "What cycle", "Kondratieff", "Inflection" | `cycle-locator` |
| "Recession allocation", "Recovery buys" | `cycle-locator` |
| "Is my decision right", "Any biases" | `bias-detector` |
| "All-in", "Leverage" | `bias-detector` |
| "Buffett's view", "How would Munger see" | `china-masters` |
| "How to do value investing" | `china-masters` |
| "Daily market scan", "Today's market" | Workflow: `fanli-analyzer` + market sentiment |
| "Weekly track", "Industry dynamics" | Workflow: `cycle-locator` + industry-rank |
| "Monthly review", "Holding diagnosis" | Workflow: `fund-analyzer-pro` + holding-diagnoser |
| "Quarterly research", "Macro analysis" | Workflow: `cycle-locator` + macro analysis |

## FAQ

**Q: How is this different from just asking AI directly?**

A: Structure. A generic AI answers however it feels; this Skill has a fixed analysis pipeline (collect → select → judge → analyze), with standardized output that won't skip steps.

**Q: Do I need paid data sources?**

A: No. Free sources (Eastmoney / Sina / HKEX / NBS) cover basics. Paid APIs (QVeris / Qiemai) only enhance precision for northbound flows and advisory strategies.

**Q: Can you give direct buy/sell recommendations?**

A: Not specific buy/sell recommendations for individual names. But we provide industry allocation direction, position sizing advice, and bias correction — to help you make better decisions.

**Q: Where is my data stored?**

A: This Skill doesn't store data; it processes the holdings you provide. All analysis happens in conversation.

**Q: How does this relate to SoloAdvisor-Toolkit?**

A: This is the investment framework layer; SoloAdvisor-Toolkit is the advisory workflow layer. The former focuses on "how to read the market, whether a fund is good, where the cycle is"; the latter focuses on the full KYC → allocation → product → portfolio → report flow.

## Disclaimer

This content is for reference only and does not constitute investment advice. Markets carry risk; invest cautiously. Please make independent judgments and bear your own risk.

---

**GitHub**: https://github.com/lj22503/investment-framework-skill
**ClawHub**: `clawhub install investment-framework`

**Other languages**: [简体中文](README.md)
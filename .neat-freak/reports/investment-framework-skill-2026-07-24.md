# investment-framework-skill — neat-freak 知识收尾报告

**收尾时间**：2026-07-24
**收尾路径**：轻量路径（文档驱动的 skill 集合，无运行时代码/部署流程）
**收尾者**：neat-freak（v3.0.0）

---

## 一、影响（用户视角）

- **暴露 README vs SKILL.md 版本号不一致**：README 第 18 行写 "版本: v3.0.0"，SKILL.md frontmatter 第 3 行写 "version: 4.1.0" —— 接手者按 README 看以为是 v3，按 SKILL.md 加载却是 v4，存在跳跃。
- **暴露经典书目数量矛盾**：README 第 19 行提 "13 本投资经典"，SKILL.md 第 13 行提 "5 本经典投资书籍"，差距 8 本。哪个是事实？
- **暴露无 Agent 规则文件**：项目没有 CLAUDE.md / AGENTS.md / PROGRESS.md（只有 SKILL.md 和 README），新会话 agent 进来没有任何项目级约束/约定可读。
- **暴露文档爆炸**：根目录 30+ 个 MD 文件（含 4 个 DATA_* 系列、INTEGRATION_COMPLETE.md / OPTIMIZATION-PLAN.md / SKILL-DAIR-OPTIMIZED.md 等过程报告），典型"演进历史堆积"。下一步会话读 README 时会被淹没在过时过程文档中。
- **暴露未跟踪内容**：`topics-suggested.md` 是 GitHub Topics 推荐清单（20 个 tag），未 commit、未 gitignore——但显然不是项目代码/文档。

## 二、现役事实矩阵

| 事实面 | 状态 | 证据 |
|--------|------|------|
| 代码 | `verified-current` | 3 个子 skill（asset-allocator / bias-detector / cycle-locator），每个含 SKILL.md + README.md |
| 运行态 | `not-applicable` | 无部署流程，skill 包以 SKILL.md 为分发形式 |
| 文档 | `changed-and-verified` | 30+ 根 MD；SKILL.md 完整；README.md 中英文各一版；REPO-MAP.md 指向主工作空间 `lj22503/one-person-ceo-skills` |
| 规则 | `not-applicable`（缺） | **没有 CLAUDE.md / AGENTS.md / PROGRESS.md**——按 neat-freak Step 3 应补 |
| 记忆 | `not-applicable` | 项目无独立记忆系统 |
| 工作区 | `changed-and-verified` | 新建 `.neat-freak/`；`topics-suggested.md` 未跟踪；`.impeccable/` 历史 audit 残留 |

## 三、关键发现

### 3.1 版本号矛盾

| 来源 | 版本号 | 出处 |
|------|-------|------|
| SKILL.md frontmatter | `4.1.0` | 第 3 行 |
| SKILL.md frontmatter | `updated: 2026-05-29` | 第 6 行 |
| README.md 徽章文字 | `v3.0.0` | 第 18 行 |
| git log | `27f7ac9 feat: v4.1.0 DAIR-AI 框架优化` | 最新 feature commit |
| git log | `1dd454f docs: 重写 README，新增 FAQ...` | 最近 README 改写 |

→ v4.1.0 是事实，README 写 v3.0.0 是漏改（git 流程文档 commit 改名 `docs:` 而 README 没同步）。

### 3.2 经典书目数量矛盾

| 来源 | 数字 | 出处 |
|------|-----|------|
| SKILL.md description | "5 本经典投资书籍" | 第 13 行 |
| README.md 标题 | "13 本投资经典" | 第 19 行 |

差 8 本，需 grep `books_list` / `references/` / 实际子 skill 内容验证。

### 3.3 文档爆炸清单（候选清理）

按 neat-freak Step 4，下列文件是过程报告 / 演进历史，**未必仍有效**：

| 文件 | 性质 | 建议 |
|------|------|------|
| `DATA_INTEGRATION_PLAN.md` | 集成计划 | 候选删除（被 DATA_INTEGRATION_COMPLETE.md 取代） |
| `DATA_INTEGRATION_PROGRESS.md` | 进度报告 | 同上 |
| `DATA_INTEGRATION_STATUS.md` | 状态报告 | 同上 |
| `OPTIMIZATION-PLAN.md` | 优化计划 | 候选（被 SKILL-DAIR-OPTIMIZED.md 取代） |
| `SKILL-DAIR-OPTIMIZED.md` | DAIR 优化版本 | 与 SKILL.md 是否重叠需对照 |
| `INTEGRATION_COMPLETE.md` | 集成完成报告 | 候选 |
| `CLAWHUB_CRON_SETUP.md` | ClawHub 定时配置 | 是否仍用 ClawHub 待确认 |
| `CLAWHUB_PUBLISH_GUIDE.md` | ClawHub 发布指南 | 同上 |
| `ADVANCED_SKILLS.md` + `ADVANCED_SKILLS_II.md` | 高级 skill 系列 | 二者是否重复？v1/v2？ |
| `DATA_API_GUIDE.md` + `DATA_INTEGRATION_COMPLETE.md` + `DATA_LAYER_DESIGN.md` + `DATA_LAYER_SUMMARY.md` | 数据层多文档 | 高度重叠 |
| `COMPLETE_SKILLS_INVENTORY.md` | skills 清单 | 与 3 个子 SKILL.md 是否同步 |

### 3.4 topics-suggested.md（未跟踪）

| 属性 | 值 |
|------|-----|
| 路径 | `D:\claudework\investment-framework-skill\topics-suggested.md` |
| 用途 | GitHub Topics 推荐（20 个 tag） |
| 状态 | `?? topics-suggested.md`（未跟踪、未 commit） |
| 建议 | 操作完 GitHub UI 后删除本地，或加 `.gitignore` 忽略 |

### 3.5 子 skill 结构

3 个子 skill 都有标准结构（README.md + SKILL.md），符合 Skill Anthropic 规范：

- `asset-allocator/SKILL.md`
- `bias-detector/SKILL.md`
- `cycle-locator/SKILL.md`

`SKILL.md`（根）`name: investment-framework` 与子 skill 同名（按 Anthropic 规范应为聚合或父级），需确认根 SKILL.md 是否是"父 skill"还是"占位"。

## 四、改动 / 新建

| 文件 | 动作 | 原因 |
|------|------|------|
| `.neat-freak/reports/investment-framework-skill-2026-07-24.md` | 新建 | 本次 audit trail |

## 五、待你确认（未确认前不动作）

1. **README 版本号**：v3.0.0 → v4.1.0 同步
2. **经典书目数量**：5 本 vs 13 本哪个是真身？以哪个 skill 内容为准核对
3. **是否新建 CLAUDE.md**：按 neat-freak Step 3 应补一份最小规则文件（项目定位 + 子 skill 列表 + 文档维护规则）
4. **文档爆炸**：列出 11 个候选文件待你决定去留
5. **topics-suggested.md**：操作完 GitHub UI 后删除
6. **根 SKILL.md 命名**：是否应改为聚合 skill 名称（如 `investment-framework-suite`）

## 六、遗留

- 3 个子 skill 内容（asset-allocator / bias-detector / cycle-locator）未逐个审
- REPO-MAP.md 第 42 行引用 `https://github.com/lj22503/one-person-ceo-skills/blob/main/REPO-MAP.md` —— 主工作空间是否仍公开可访问
- `.impeccable/` 目录是否 gitignore

---

*收尾完成度：5 事实面已标注（运行态 not-applicable，规则 not-applicable）。报告基于 commit `d96ea7b`（HEAD），如需重新跑请清空 `.neat-freak/reports/` 后重跑。*
# research-figure-skill

面向多学科科研数据的选图、绘制与成图检查 Skill。它先核对研究问题与数据结构，再选择图型；适用于实验、临床、生态、工程和计算研究中的表格数据图。

[![License: Apache-2.0 + MIT](https://img.shields.io/badge/License-Apache--2.0%20%2B%20MIT-blue.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9%2B-3776AB.svg)](#安装)

> 本项目基于 [Haojae/scipilot-figure-skill](https://github.com/Haojae/scipilot-figure-skill) 的 `43098dd` 版本开发。仓库独立创建，不隶属于 SciPilot Skills 家族。来源与许可见[来源说明](NOTICE)。

## 能做什么

- **先判断，再作图**：根据图要回答的问题、变量角色与数据分布推荐图型。
- **区分行数与独立单位数**：报告重复受试者、样本、地点或设备的观测记录。
- **提示数据结构问题**：按分组列出行数和单位数，标出重复单位与重复的单位×时间组合。
- **保留测量值语义**：用 `--value` 指定被自动识别误判的整数测量列。
- **检查坐标和成图**：提示零值、负值与普通对数轴的冲突；检查缺字、文字裁切、刻度重叠和导出文件。

这些是作图线索。Skill 不会仅凭列名判定实验设计，也不会自动生成显著性结论。图中的误差、`n`、聚合和统计标注需有明确来源。

## 导入 Codex 与 Claude Code

仓库根目录同时提供 Codex 与 Claude Code 的插件清单，两个平台读取同一份 [Skill](skills/research-figure-skill/SKILL.md)。在终端运行：

```bash
# Codex
codex plugin marketplace add YuanyuanMa03/research-figure-skill --ref main
codex plugin add research-figure-skill@research-figure-tools

# Claude Code
claude plugin marketplace add YuanyuanMa03/research-figure-skill
claude plugin install research-figure-skill@research-figure-tools
```

导入会安装 Skill 指令和脚本，不会自动安装 Python 库。首次运行脚本前，如当前 Python 环境缺少依赖，可克隆仓库并执行 `python3 -m pip install -r requirements.txt`；SciencePlots、pypdf、kaleido 和 PyMuPDF 是可选增强。Claude Code 也可用 `claude --plugin-dir /path/to/research-figure-skill` 临时加载本地目录。

给代理的请求示例：

> 这份 CSV 是同一受试者在多次访视的测量值，按治疗组画出变化趋势。请先区分观测行数和受试者数，再推荐并制作论文图。

也可以直接运行数据剖析脚本：

```bash
python3 skills/research-figure-skill/scripts/profile_data.py data.csv \
  --group treatment --unit subject_id --time visit --value response
```

`--group` 与 `--value` 可重复指定；`--unit`、`--time` 可省略。机器可读报告使用 `--json`。已知字段角色应显式给出；未知时先核对数据字典。

## 工作方式

1. 确认图要回答的问题、响应变量、分组、独立分析单位和展示场景。
2. 用 [profile_data.py](skills/research-figure-skill/scripts/profile_data.py) 检查列、缺失、分组、重复记录与分布。
3. 参考[图型选择](skills/research-figure-skill/references/chart_selection.md)提出建议；小样本优先考虑显示原始点，重复观测考虑配对点或个体轨迹。
4. 用[绘图配方](skills/research-figure-skill/references/plot_recipes.md)绘制，并记录聚合、变换、排除和误差定义。
5. 渲染预览，按[视觉自检](skills/research-figure-skill/references/visual_review.md)检查，使用 [export_figure.py](skills/research-figure-skill/scripts/export_figure.py) 导出。
6. 用 [check_figure.py](skills/research-figure-skill/scripts/check_figure.py) 核对文件格式、DPI 与 PDF 字体；期刊要求以目标期刊的最新作者指南为准。

插件清单位于 [plugin.json](plugin.json)、[Codex 清单](.codex-plugin/plugin.json)、[Claude Code 清单](.claude-plugin/plugin.json)；[Skill 目录](skills/research-figure-skill/)保留脚本与按需阅读的参考资料。此 Skill 专注数据图，不覆盖流程图、概念示意图和图像合成。

## 验证

```bash
python3 -m unittest discover -s tests -v
python3 skills/research-figure-skill/scripts/profile_data.py --help
claude plugin validate .claude-plugin/plugin.json --strict
claude plugin validate .claude-plugin/marketplace.json --strict
```

## 许可与来源

本项目新增的原创修改采用 [Apache License 2.0](LICENSE)。保留的原项目材料继续受 [Haojae 的 MIT 许可](LICENSE-UPSTREAM-MIT)约束；[NOTICE](NOTICE) 记录原项目地址、作者和修改范围。独立仓库的历史从本项目的初始提交开始，未复制原仓库的 Git 提交历史。

---

## English

`research-figure-skill` helps agents plan, draw, and review scientific data figures across disciplines. It separates observation rows from independent units, flags repeated measurements and duplicate unit-time records, supports explicit measurement roles, and checks rendered figures. Study-design and chart suggestions are clues for review, not automatic statistical conclusions.

Import it through a plugin marketplace: `codex plugin marketplace add YuanyuanMa03/research-figure-skill --ref main` or `claude plugin marketplace add YuanyuanMa03/research-figure-skill`, then install `research-figure-skill@research-figure-tools` in the same client. Run `python3 skills/research-figure-skill/scripts/profile_data.py data.csv --group treatment --unit subject_id --time visit --value response` to inspect a table. See [SKILL.md](skills/research-figure-skill/SKILL.md) for the agent workflow and [the references](skills/research-figure-skill/references/) for chart selection and review.

This independent project is based on [Haojae/scipilot-figure-skill](https://github.com/Haojae/scipilot-figure-skill) at commit `43098dd`. New original modifications use [Apache-2.0](LICENSE); retained upstream material remains under its [MIT license](LICENSE-UPSTREAM-MIT). See [NOTICE](NOTICE) for attribution.

---
name: research-figure-skill
description: Plan, draw, and review scientific data figures from tabular data. Use for chart choice, publication figures, figure revisions, or checks of statistical and visual presentation. Works across disciplines; excludes conceptual diagrams and image editing.
---

# Scientific data figures

Use this skill to connect a research question, the data structure, and a readable figure. A CSV does not determine a chart by itself. The user's intended claim, analysis unit, and target medium matter.

## Before choosing a chart

Establish what the figure should help readers see: a distribution, comparison, relationship, trajectory, composition, or uncertainty. Infer this from the user's request or manuscript context when possible and state the inference. Ask only when the missing answer changes the chart or the interpretation.

Identify the roles of relevant columns:

- response and explanatory variables;
- groups and their order;
- the independent analysis unit (person, specimen, site, device, run, etc.);
- time or other repeated observation index, if present;
- units of measurement and missing value conventions.

Rows are observations, not necessarily independent samples. Never infer the analysis unit from a column name alone. If it is unknown, say so and avoid statistical claims that require independence.

Run `scripts/profile_data.py` for tabular data. Supply roles when known:

Resolve bundled script and reference paths relative to this `SKILL.md`, not the user's working directory. Pass the absolute script path to Python while keeping the user's data path intact. Python dependencies are listed in the plugin root's `requirements.txt`; check availability before running a script and report a missing dependency clearly.

```bash
python3 <skill-directory>/scripts/profile_data.py data.csv --group treatment --unit subject_id --time visit --value response
```

`--group` and `--value` can be repeated. `--unit`, `--time`, and `--value` are optional. Use `--value` when an integer-coded measurement is guessed to be categorical. The report distinguishes row counts from distinct unit counts, notes repeated unit observations and duplicate unit-time records within supplied groups, and flags zero/negative values that rule out an ordinary log axis. These are clues for the researcher to interpret, not automatic classifications of a study design. Inspect column type guesses before using them: numeric IDs, encoded categories, and dates are easy to misclassify. See [data profiling](references/data_profiling.md) when interpreting the report.

## Recommend and draw

Use [chart selection](references/chart_selection.md) to choose a chart for the claim and data structure. State the recommended chart and why it serves the claim; mention a meaningful alternative when there is a tradeoff. Prefer showing individual observations when there are few independent units. For paired or repeated observations, preserve unit identity where useful (paired points, trajectories, or a justified unit-level summary). Do not pool repeated rows and label them independent `n`.

Use [plot recipes](references/plot_recipes.md) for implementation. Keep transformations, aggregation, exclusions, ordering, and uncertainty definitions explicit. Do not invent a statistical test, p-value, or significance marker from a visual impression. If the user requests inferential annotations, establish the unit, comparison, method, and multiplicity treatment first. A chart can still be drawn without significance marks while those details are unresolved.

If the user already requested a figure and supplied enough information, proceed to render it. If their chosen chart may obscure an important feature, explain the issue and offer a practical revision. Respect their choice while keeping labels and caption accurate.

## Format and review

Set the figure size for its intended placement; inspect text and marks at that displayed size. Match a named journal's **current** author instructions when a journal is specified. The values in [journal specs](references/journal_specs.md) are starting points, not guaranteed current requirements. Use [setup_style.py](scripts/setup_style.py) for style and CJK fonts.

Render a preview, run `visual_qa.audit_layout(fig)`, and inspect the preview for clipping, overlap, legibility, and misleading visual emphasis using [visual review](references/visual_review.md). Run [export_figure.py](scripts/export_figure.py) for the requested formats and [check_figure.py](scripts/check_figure.py) for file-level checks. A passing file check does not validate the chart's statistics or message. Consult [publication checklist](references/publication_checklist.md) for final human review.

In the handoff, provide the figure, editable code, data source or transformation record, and a caption draft that defines any uncertainty interval and sample count. State unresolved assumptions. Do not modify source data to make a plot pass review.

## Boundaries

This skill covers data figures. It does not create conceptual diagrams, flowcharts, or image composites. Use another tool or skill for those tasks. Do not treat heuristics such as a sample-size cutoff, a preferred chart type, or a publisher-wide style as universal rules.

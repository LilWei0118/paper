# Fig. 11: ShareGPT, BS128, three models

`../Fig11_sharegpt_three_models_bs128_output2_20261018.png` and `.pdf` show:

- (a) Llama3-8B / Sarathi / RTX 3090;
- (b) Qwen3-8B / SGLang / RTX 3090;
- (c) Llama3-70B / SGLang / A100.

The blue line is measured total energy **saved relative to Auto** in kJ:
`Auto energy − capped-frequency energy`. The red line is actual inference
time in seconds. Auto therefore has zero energy saved. The earlier pale green
frequency-selection band is omitted, consistent with the prior two-panel
Fig. 11 selection. The two 8B model points average two runs per setting;
Llama3-70B uses one run per setting from `stage7_auto` (formerly `output2`).

`values.csv` contains the 31 BS128 ShareGPT rows from
`/home/hcw/LLM_pipeline_infer/analysis/fig11_all_configs_20261017/fig11_all_values.csv`.
Run `python plot.py` to regenerate the figure from this snapshot. The paper's
LaTeX source does not yet reference this preview.

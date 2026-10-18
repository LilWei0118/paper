# Fig. 11: ShareGPT, BS256, three models

`../Fig11_sharegpt_three_models_bs256_output2_20261018.png` and `.pdf` show
Llama3-8B/Sarathi/RTX 3090, Qwen3-8B/SGLang/RTX 3090, and
Llama3-70B/SGLang/A100 in three stacked panels.
The panel order, plotting area, page dimensions, and enlarged labels match the
selected ShareGPT Fig. 12 figure for side-by-side placement.

Only capped-frequency points are plotted; Auto is retained in the CSV solely
for provenance. The blue line is measured **total energy (kJ)** and the red
line is measured inference time (s). No selection band is shown. The two 8B
model points average two runs per setting; Llama3-70B uses one run per setting
from `stage7_auto` (formerly `output2`).

`values.csv` contains the 31 BS256 ShareGPT rows from
`/home/hcw/LLM_pipeline_infer/analysis/fig11_all_configs_20261017/fig11_all_values.csv`.
Run `python plot.py` to regenerate the figure from this snapshot. The paper's
LaTeX source does not yet reference this preview.

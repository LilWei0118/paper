# Fig. 4: Qwen3-8B and Llama3-70B, ShareGPT

The main `../Fig4_auto_context_main_range_20261017.png` and `.pdf` now show
two vertically stacked panels: Qwen3-8B/SGLang/RTX 3090 above
Llama3-70B/SGLang/A100. The visible titles show only model names, and the
two panels share one y-axis title and one BS color legend. The two
model-specific PNG/PDF pairs in this folder show the same data separately.

Only ShareGPT Auto repetition 1 is shown. The x axis, labeled "Sequence Length,"
is the **sum of request context lengths in a pure-decode batch**, limited to
0–15,000 tokens. The y
axis is the mean CUDA compute duration of the middle pipeline stages. Each
color consistently denotes one global batch size across both panels. The
values already average batches with exactly equal x; no smoothing or y-value
filtering is applied. The Qwen3-8B y axis starts at 0 ms and the Llama3-70B
y axis starts at 5 ms; both upper limits retain a 5% data-range margin.

`values.csv` contains the 11,512 in-range rows from
`/home/hcw/LLM_pipeline_infer/analysis/fig4_auto_context_20261017/exact_x_means.csv`.
Run `python plot.py` in this folder to regenerate all figures. A100 uses
the `stage7_auto` dataset, formerly `output2`. The paper's LaTeX source does
not yet reference this preview.

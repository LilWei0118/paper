# Fig. 4: Qwen3-8B and Llama3-70B, ShareGPT

The archived `../Fig4_auto_context_qwen_a100_20261017.png` and `.pdf` show
two vertically stacked panels: Qwen3-8B/SGLang/RTX 3090 above
Llama3-70B/SGLang/A100. The visible titles show only model names, and the
two panels share one y-axis title and one BS color legend. The two
model-specific PNG/PDF pairs in this folder show the same data separately.
The combined Fig. 4 PDF uses the same 8 × 7.27 inch page size as Fig. 3,
with larger model titles, axes, and BS legend for side-by-side placement.

Only ShareGPT Auto repetition 1 is shown. The x axis, labeled "Sequence Length,"
is the **sum of request context lengths in a pure-decode batch**, limited to
0–15,000 tokens. The y
axis is the mean CUDA compute duration of the middle pipeline stages. Each
color consistently denotes one global batch size across both panels. The
values already average batches with exactly equal x; no smoothing or y-value
filtering is applied. In the combined figure, the Qwen3-8B y axis starts at
2.4 ms and the Llama3-70B y axis at 7.5 ms to trim lower blank space. The panel
heights shrink with those ranges, keeping the data's vertical scale approximately
unchanged. The separately saved single-model views retain their 0 ms and 5 ms
lower limits. All upper limits retain a 5% data-range margin.

`values.csv` contains the 11,512 in-range rows from
`/home/hcw/LLM_pipeline_infer/analysis/fig4_auto_context_20261017/exact_x_means.csv`.
Run `python plot.py` in this folder to regenerate all figures. A100 uses
the `stage7_auto` dataset, formerly `output2`. The paper's LaTeX source does
not yet reference this preview.

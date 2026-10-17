# Fig. 4 style preview: Sarathi fixed-frequency run

Llama3-8B, Sarathi, RTX 3090, ShareGPT, global batch size 256, 1200 MHz on
stages 0–2 (last stage Auto), repetition 1. The plot uses the same definitions
and colors as the Sarathi row of the Auto Fig. 4 preview.

- X: sum of request context lengths in a pure-decode batch.
- Y: mean CUDA Event duration of the two middle stages (1 and 2).
- Only batches with the most frequent pure-decode request count are plotted;
  the actual count appears in the legend.
- Batches with exactly equal X are averaged. No smoothing or duration-based
  filtering is applied. The CSV files preserve selected batches and exact-X
  means.
- The main-range view clips the Y-axis at 1.15 times its 99th percentile;
  any points above the view appear as red triangles at the top. The full-range
  view shows all values on the Y-axis.

Run `python plot.py --data-root /home/hcw/LLM_pipeline_infer` from this folder
to regenerate the outputs. The experimental trace is outside this paper repo;
`method.json` identifies it relative to that data root. This preview is not
referenced by the manuscript.

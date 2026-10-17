# Locally redrawn paper figures

This folder holds the PDF and PNG figures generated for the local paper revision on 2026-10-17. The original Overleaf figures remain in the parent `figures/` folder. Each PDF has a PNG preview with the same stem.

| Figure group | Files |
| --- | --- |
| Fig. 3 and Fig. 4 | `Fig3_*`, `Fig4_*` |
| Fig. 4 fixed-frequency example | `fig4_sarathi_sharegpt_bs256_freq1200/` contains the Sarathi ShareGPT BS256 1200 MHz rep1 plot, script, and derived tables. |
| Fig. 6 and Fig. 7 | `Fig6_*`, `Fig7_*` (model and dataset variants) |
| Fig. 9 and Fig. 10 | `Fig9_*`, `Fig10_*` |
| Fig. 11 | `Fig11_sharegpt_a100_qwen_bs256_*` is the requested two-panel selection; `Fig11_all_configs_*` contains the 27-configuration overview and model sheets; `Fig11_frequency_*` is an earlier preview. |
| Fig. 12 | `Fig12_random_five_point_fit_*` is the latest seeded random five-point fit; `Fig12_five_point_fit_*` and `Fig12_frequency_fit_*` preserve earlier fixed five-point and all-point versions. |
| Energy and bubble reduction | `Energy_E2E_under_BatchSize_*`, `IDLE_Computing_under_BatchSize_*` |

The current LaTeX source does not reference these dated files. If a figure is selected for the paper, update its `\includegraphics` path to `figures/hcw_figures/<filename>.pdf`.

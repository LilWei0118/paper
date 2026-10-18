# Locally redrawn paper figures

This folder holds the PDF and PNG figures generated for the local paper revision on 2026-10-17. The original Overleaf figures remain in the parent `figures/` folder. Each PDF has a PNG preview with the same stem.

| Figure group | Files |
| --- | --- |
| Fig. 3 and Fig. 4 | `Fig3_*`, `Fig4_*` |
| Fig. 3 current selection | `Fig3_auto_stage_idle_sharegpt_bs256_20261017.*` now shows Qwen3-8B and Llama3-70B only; `fig3_qwen_a100_20261018/` contains its script and values. |
| Fig. 4 fixed-frequency example | `fig4_sarathi_sharegpt_bs256_freq1200/` contains the Sarathi ShareGPT BS256 1200 MHz rep1 plot, script, and derived tables. |
| Fig. 4 current selection | `Fig4_auto_context_main_range_20261017.*` now shows Qwen3-8B and Llama3-70B on ShareGPT with x = 0–15,000; `fig4_sharegpt_qwen_a100_x15000_20261018/` contains the script, values, and single-model views. |
| Fig. 6 and Fig. 7 | `Fig6_*`, `Fig7_*` (model and dataset variants) |
| Fig. 9 and Fig. 10 | `Fig9_*`, `Fig10_*` |
| Fig. 10 total bubble duration | `fig10_total_interbatch_bubble_reduction/` contains the latest full-run middle-stage gap-duration plot, script, and derived tables. |
| Fig. 11 | `Fig11_sharegpt_a100_qwen_bs256_*` is the requested two-panel selection; `Fig11_all_configs_*` contains the 27-configuration overview and model sheets; `Fig11_frequency_*` is an earlier preview. |
| Fig. 11 atlas energy axis | `Fig11_all_configs_atlas_output2_20261017.*` now shows measured total energy on the blue axis; `fig11_all_configs_atlas_actual_energy/` contains its script and values. |
| Fig. 12 | `Fig12_random_five_point_fit_*` is the latest seeded random five-point fit; `Fig12_five_point_fit_*` and `Fig12_frequency_fit_*` preserve earlier fixed five-point and all-point versions. |
| Energy and bubble reduction | `Energy_E2E_under_BatchSize_*`, `IDLE_Computing_under_BatchSize_*` |

The current LaTeX source does not reference these dated files. If a figure is selected for the paper, update its `\includegraphics` path to `figures/hcw_figures/<filename>.pdf`.

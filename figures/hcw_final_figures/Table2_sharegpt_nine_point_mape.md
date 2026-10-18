# ShareGPT Fig. 12 nine-point MAPE

Each percentage averages the absolute percentage errors at all nine measured frequencies on one fitted curve (four fit + five held-out points).

| Model | BS64 | BS128 | BS256 | BS512 |
|---|---:|---:|---:|---:|
| Llama3-8B | 2.88% | 8.49% | 3.07% | — |
| Qwen3-8B | 4.62% | 2.98% | 3.62% | — |
| Llama3-70B | — | 4.42% | 4.38% | 2.46% |

MAPE = (1/9) × Σ |predicted stage time − measured stage time| / measured stage time × 100%. This all-point MAPE includes fitting points; see the CSV for fit-only and held-out-only MAPE.

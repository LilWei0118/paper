# ShareGPT fitted stage-time alignment

Intersection frequency in MHz; the values are continuous fitted estimates.

| Model | BS64 | BS128 | BS256 | BS512 |
|---|---:|---:|---:|---:|
| Llama3-8B | 833.6 | 834.6 | 776.3 | — |
| Qwen3-8B | 1225.6 | 1189.6 | 1209.7 | — |
| Llama3-70B | — | 824.6 | 850.2 | 867.1 |

The target is the mean Auto decode time of the final stage (stage 3 for the 8B models; stage 7 for Llama3-70B). The fitted curve represents the mean intermediate-stage decode time. See the CSV for unrounded frequencies, targets, and selected fit points.

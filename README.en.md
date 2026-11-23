# RTX 5090 black screen and GPU loss (0x117)

[한국어](README.md) | **English**

On 10 November 2026, a replacement GeForce RTX 5090 lost its display signal after a period of normal use. Windows captured a `0x117` GPU timeout on NVIDIA driver 621.14. The workload running at the time is unknown. Later that day, after a rollback to 621.01, a cuDNN attention test reproduced the black screen. Windows captured another `0x117` live kernel dump and `nvidia-smi` reported “GPU is lost.”

For the repeat, the owner backed up and reset three disk caches (CUDA ComputeCache, NVIDIA DXCache and Windows D3DSCache) and restarted Windows. Both runs used driver 621.01, PyTorch 2.13.0+cu130 and cuDNN 9.20.

| Workload | After driver rollback, before restarting Windows | After cache reset and restart |
|---|---|---|
| H.264 NVENC encoding | Completed 30 s | Completed 30 s |
| NVIDIA D3D11 decoding | Completed 30 s | Completed 30 s |
| 256 MiB CPU–GPU round trip with a byte comparison | 221 iterations in 15.031 s | 232 iterations in 15.041 s |
| BF16 matrix multiplication, 8192 × 8192 | 5,898 iterations in 45.004 s | 5,802 iterations in 45.000 s |
| BF16 cuDNN attention | Last progress at 954 iterations and 35.308 s, followed by GPU loss | **Completed 1,227 iterations in 45.024 s** |

The exact time the GPU stopped responding in the first run is unknown. After the second run, the GPU still responded at the final check at 23:10 KST. Only one run followed the combined cache reset and restart. Their individual effects and the card’s long-term stability remain unknown.

The case report gives the test settings, the dump findings, and the differences between this run and the tests on the previous card. Times in the report and timeline are Korea Standard Time (UTC+9). The CUDA workload logs use UTC. [Full English report](REPORT.en.md) · [Timeline](data/timeline.csv)

- [Test environment](data/environment.json) · [Workload comparison](data/comparison.csv) · [Cache backup and reset records](data/cache-reset.json)
- [Guide to the logs and their sources](evidence/README.md) · [Selected diagnostic excerpts](evidence/diagnostic-excerpts.txt)
- [CUDA workload guide](repro/README.en.md) · [Original test script](repro/cuda_probe.py)
- [What the public repository contains](PRIVACY.en.md) · [SHA-256 file manifest](SHA256SUMS.txt)

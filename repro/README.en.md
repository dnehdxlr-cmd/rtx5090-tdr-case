# CUDA workload guide

[한국어](README.md) | **English**

The comparison on 10 November 2026 used the same `cuda_probe.py` for both runs. Its SHA-256 digest is

`C119A98DF9339448568409564B2F4732A03D3574F7ED24B745EA29012B57B3A3`

The test system used an RTX 5090 with PyTorch 2.13.0+cu130, CUDA 13.0 and cuDNN 9.20. The commands assume an existing Python environment with those versions. The repository does not provide an installer or a dependency lockfile.

The original test supervisor also ran the NVENC encode and D3D11 decode stages, monitored Windows events and applied an external process timeout. The three commands below cover the CUDA stages. Run them from the repository root with `python` pointing to the test environment.

```powershell
python -I -u .\repro\cuda_probe.py transfer --seconds 15
python -I -u .\repro\cuda_probe.py matmul --seconds 45
python -I -u .\repro\cuda_probe.py cudnn_attention --seconds 45
```

The attention test reproduced a black screen and left the GPU unavailable on this system. To review the case, read the [recorded outputs](../evidence/README.md). If repeating the tests, save open work and run one stage at a time on a test machine. Stop after an error or loss of the GPU.

`--seconds` controls how long the loop runs while CUDA calls return. A call can hang past that limit. The original supervisor applied a separate 100-second process timeout. Even after terminating the process, restoring the GPU may require a reboot.

The script sets PyTorch’s per-process GPU memory fraction to 35% and uses the random seed `20261110`. Power, clock, TDR, driver and cache settings are managed outside the script. Even the `--help` command imports PyTorch. For static review, open the [Python source](cuda_probe.py).

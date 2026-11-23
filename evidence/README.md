# Evidence provenance and transformations

[English overview](../README.en.md) · [한국어 개요](../README.md)

The files below concern tests performed on 2026-11-10. They were selected for sharing on 2026-11-23. They are not the full original evidence collection.

## Unmodified workload stdout

| Shared file | Original local evidence collection | Meaning |
|---|---|---|
| [before/transfer.jsonl](before/transfer.jsonl) | `gpu-rollback-repro-20261110` / `transfer-stdout.log` | Completed transfer test |
| [before/matmul.jsonl](before/matmul.jsonl) | `gpu-rollback-repro-20261110` / `matmul-stdout.log` | Completed matrix test |
| [before/cudnn_attention.jsonl](before/cudnn_attention.jsonl) | `gpu-rollback-repro-20261110` / `cudnn_attention-stdout.log` | Progress followed by CUDA unknown error |
| [after/transfer.jsonl](after/transfer.jsonl) | `gpu-cache-ab-20261110-2234` / `transfer-stdout.log` | Completed transfer test |
| [after/matmul.jsonl](after/matmul.jsonl) | `gpu-cache-ab-20261110-2234` / `matmul-stdout.log` | Completed matrix test |
| [after/cudnn_attention.jsonl](after/cudnn_attention.jsonl) | `gpu-cache-ab-20261110-2234` / `cudnn_attention-stdout.log` | Completed attention test |

The six JSONL files retain their original bytes; their timestamps are UTC. They contain generic device/software names, input shapes, iteration progress and completion/error output. Private local paths and device-instance identifiers were not present in these selected stdout files. A hash inventory is provided in [data/file-hashes.csv](../data/file-hashes.csv).

## Curated evidence

[diagnostic-excerpts.txt](diagnostic-excerpts.txt) retains selected CDB labels and function names from the 21:57 full 0x117 analysis, plus selected WER and `nvidia-smi` observations. Raw stack addresses, local paths, PCI bus address and report identifiers are omitted. The function chain is a readable projection of selected stack frames, not a complete raw stack trace. Explanatory lines distinguish source observations from interpretation.

[data/comparison.csv](../data/comparison.csv) combines process metadata from the two test runs with workload stdout values. Before-run attention has a last-progress time, not a completed loop duration. Its initial application-failed status is supplemented with later GPU-loss/dump observations; the historical immediate event result is not rewritten.

[data/environment.json](../data/environment.json), [data/cache-reset.json](../data/cache-reset.json) and [data/timeline.csv](../data/timeline.csv) are selected-field summaries, not byte-identical original logs. Paths, per-file cache names, unique device identifiers and process IDs are omitted.

Full dumps, cache contents, full WER, raw stderr stack traces with private paths, EVTX and system-maintenance scripts remain outside this share package. See the [public evidence scope](../PRIVACY.en.md).

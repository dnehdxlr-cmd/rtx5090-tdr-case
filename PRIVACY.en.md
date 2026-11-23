# Sharing scope

[한국어](PRIVACY.md) | **English**

This repository documents the test conditions, observations and limitations of the RTX 5090 investigation. It includes the code that ran the CUDA workloads.

## Included

- GPU product family, software versions, test settings, dates and times, results and unresolved points.
- Six JSON Lines (JSONL) files containing the original CUDA workload output. They contain no user names or private paths. The [evidence guide](evidence/README.md) identifies the source of each file.
- The original CUDA workload script, selected diagnostic classifications and function names, and GPU-lost messages.
- Cache file counts and sums of logical file lengths, without individual cache file names or contents.
- Tables and JSON summaries compiled from selected fields in the original records.

## Excluded

This package excludes original kernel or memory dumps, cache contents, complete WER/EVTX/ETL/PML records, registry exports, installation packages and full installation logs, account names, private folder paths, SIDs, device serial numbers and unique PnP instance IDs, report GUIDs, network addresses, remote-access details and links that connect personal accounts. Administrative scripts that automatically reboot the system, move caches or change drivers are also excluded.

The owner keeps the complete collection in a separate local archive. Sharing additional records requires selecting the relevant files and checking them for private information.

The SHA-256 digests let readers verify that the code and JSONL files match the originals. The owner has not specified an open-source license for this package.

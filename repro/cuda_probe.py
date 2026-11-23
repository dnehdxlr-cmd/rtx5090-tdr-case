"""Bounded CUDA comparison probes; no global GPU settings or telemetry polling."""
import argparse
import json
import math
import time
from datetime import datetime, timezone

import torch
import torch.nn.functional as F


def emit(event, **values):
    print(json.dumps({"time": datetime.now(timezone.utc).isoformat(), "event": event, **values}), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["transfer", "matmul", "cudnn_attention"])
    parser.add_argument("--seconds", type=float, default=45)
    args = parser.parse_args()
    if not 1 <= args.seconds <= 60:
        raise ValueError("Probe duration must be 1..60 seconds")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is unavailable")
    name = torch.cuda.get_device_name(0)
    if "RTX 5090" not in name:
        raise RuntimeError(f"Unexpected device: {name}")
    torch.manual_seed(20261110)
    torch.cuda.set_per_process_memory_fraction(0.35, 0)
    emit("environment", mode=args.mode, torch=torch.__version__, cuda=torch.version.cuda,
         cudnn=torch.backends.cudnn.version(), device=name,
         capability=torch.cuda.get_device_capability(0))
    started = time.monotonic()
    iterations = 0
    last_report = 0.0
    with torch.inference_mode():
        if args.mode == "transfer":
            # Two 256 MiB host/GPU buffers; exact byte equality on each round trip.
            host = torch.randint(0, 256, (256 * 1024 * 1024,), dtype=torch.uint8)
            while time.monotonic() - started < args.seconds:
                device_data = host.to("cuda")
                back = device_data.cpu()
                if not torch.equal(host, back):
                    raise RuntimeError("Host/GPU round-trip data mismatch")
                iterations += 1
                emit("progress", iterations=iterations, elapsed=time.monotonic() - started)
                del device_data, back
        elif args.mode == "matmul":
            n = 8192
            a = torch.randn((n, n), device="cuda", dtype=torch.bfloat16) / math.sqrt(n)
            b = torch.randn((n, n), device="cuda", dtype=torch.bfloat16)
            emit("shape", n=n, dtype="bfloat16")
            while time.monotonic() - started < args.seconds:
                out = a @ b
                torch.cuda.synchronize()
                iterations += 1
                elapsed = time.monotonic() - started
                if elapsed - last_report >= 1.0:
                    if not torch.isfinite(out).all().item():
                        raise RuntimeError("Non-finite matmul output")
                    emit("progress", iterations=iterations, elapsed=elapsed,
                         allocated_bytes=torch.cuda.memory_allocated())
                    last_report = elapsed
        else:
            from torch.nn.attention import SDPBackend, sdpa_kernel
            shape = (1, 56, 16384, 128)
            q, k, v = [torch.randn(shape, device="cuda", dtype=torch.bfloat16) for _ in range(3)]
            emit("shape", shape=shape, dtype="bfloat16", backend="CUDNN_ATTENTION",
                 causal=False, dropout=0.0,
                 limitation="PyTorch cuDNN path; not the old direct-cuDNN engine-plan reproduction")
            with sdpa_kernel(SDPBackend.CUDNN_ATTENTION):
                while time.monotonic() - started < args.seconds:
                    out = F.scaled_dot_product_attention(q, k, v, dropout_p=0.0, is_causal=False)
                    torch.cuda.synchronize()
                    iterations += 1
                    elapsed = time.monotonic() - started
                    if elapsed - last_report >= 1.0:
                        if not torch.isfinite(out).all().item():
                            raise RuntimeError("Non-finite cuDNN attention output")
                        emit("progress", iterations=iterations, elapsed=elapsed,
                             allocated_bytes=torch.cuda.memory_allocated())
                        last_report = elapsed
    if iterations == 0:
        raise RuntimeError("No GPU work completed within probe duration")
    torch.cuda.synchronize()
    emit("completed", iterations=iterations, elapsed=time.monotonic() - started,
         peak_allocated_bytes=torch.cuda.max_memory_allocated())


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        emit("failed", error=repr(exc))
        raise

"""Hashcat Benchmark Utilities

Executa benchmarks (hashcat -b) para comparar CPU vs GPU de forma segura,
sem depender de hashes reais.

A ideia é produzir números reprodutíveis para demo/apresentação:
- CPU: forçar device-types CPU
- GPU: forçar device-types GPU

Retorna resultados estruturados e prontos para exportação.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


_UNIT_TO_MULTIPLIER = {
    "H/s": 1.0,
    "kH/s": 1e3,
    "MH/s": 1e6,
    "GH/s": 1e9,
    "TH/s": 1e12,
    "PH/s": 1e15,
}


@dataclass(frozen=True)
class BenchmarkRun:
    device_kind: str  # "cpu" | "gpu"
    hash_mode: int
    hash_name: Optional[str]
    speed_hs: Optional[float]
    speed_raw: Optional[str]
    returncode: int
    stdout: str
    stderr: str
    command: str
    error: Optional[str] = None


class HashcatBenchmarker:
    """Wrapper para rodar `hashcat -b` e extrair speeds."""

    def __init__(self, hashcat_cmd: str = "hashcat", hashcat_cwd: Optional[str] = None):
        self.hashcat_cmd = hashcat_cmd
        self.hashcat_cwd = hashcat_cwd

    def run_cpu_vs_gpu(
        self,
        hash_modes: List[int],
        benchmark_time: int = 3,
        extra_args: Optional[List[str]] = None,
        timeout: int = 60,
    ) -> Dict:
        """Executa benchmark CPU e GPU para cada hash_mode.

        Returns:
            dict com lista de resultados e um resumo por hash_mode.
        """
        extra_args = extra_args or []

        runs: List[BenchmarkRun] = []
        for hash_mode in hash_modes:
            runs.append(
                self._run_single(
                    device_kind="cpu",
                    hash_mode=hash_mode,
                    benchmark_time=benchmark_time,
                    extra_args=extra_args,
                    timeout=timeout,
                )
            )
            runs.append(
                self._run_single(
                    device_kind="gpu",
                    hash_mode=hash_mode,
                    benchmark_time=benchmark_time,
                    extra_args=extra_args,
                    timeout=timeout,
                )
            )

        by_mode: Dict[int, Dict] = {}
        for run in runs:
            if run.hash_mode not in by_mode:
                by_mode[run.hash_mode] = {
                    "hash_mode": run.hash_mode,
                    "hash_name": run.hash_name,
                    "cpu": None,
                    "gpu": None,
                    "ratio_gpu_over_cpu": None,
                }
            by_mode[run.hash_mode][run.device_kind] = {
                "speed_hs": run.speed_hs,
                "speed_raw": run.speed_raw,
                "returncode": run.returncode,
                "error": run.error,
                "command": run.command,
            }
            if by_mode[run.hash_mode]["hash_name"] is None and run.hash_name:
                by_mode[run.hash_mode]["hash_name"] = run.hash_name

        for mode, data in by_mode.items():
            cpu = (data.get("cpu") or {}).get("speed_hs")
            gpu = (data.get("gpu") or {}).get("speed_hs")
            if cpu and gpu and cpu > 0:
                data["ratio_gpu_over_cpu"] = gpu / cpu

        return {
            "hashcat_cmd": self.hashcat_cmd,
            "benchmark_time": benchmark_time,
            "hash_modes": hash_modes,
            "runs": [run.__dict__ for run in runs],
            "by_mode": by_mode,
        }

    def _run_single(
        self,
        device_kind: str,
        hash_mode: int,
        benchmark_time: int,
        extra_args: List[str],
        timeout: int,
    ) -> BenchmarkRun:
        # Hashcat device types:
        # - OpenCL device types via -D: 1=CPU, 2=GPU
        # Em sistemas CUDA, o hashcat ainda aceita -D e normalmente filtra devidamente.
        device_flag = "1" if device_kind == "cpu" else "2"

        cmd = [
            self.hashcat_cmd,
            "-b",
            "-m",
            str(hash_mode),
            "-D",
            device_flag,
            "--runtime",
            str(int(benchmark_time)),
            "--force",
        ] + list(extra_args)

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.hashcat_cwd,
            )
            stdout = result.stdout or ""
            stderr = result.stderr or ""
            combined = stdout + "\n" + stderr

            error = None
            if "No devices found/left" in combined:
                error = "no devices found/left"
            elif "unrecognized option" in combined and "benchmark" in combined:
                error = "unsupported benchmark option"

            hash_name = _parse_hash_name(combined)
            speed_hs, speed_raw = _parse_total_speed(combined)

            return BenchmarkRun(
                device_kind=device_kind,
                hash_mode=hash_mode,
                hash_name=hash_name,
                speed_hs=speed_hs,
                speed_raw=speed_raw,
                returncode=result.returncode,
                stdout=stdout[-4000:],
                stderr=stderr[-2000:],
                command=" ".join(cmd),
                error=error,
            )
        except subprocess.TimeoutExpired as e:
            return BenchmarkRun(
                device_kind=device_kind,
                hash_mode=hash_mode,
                hash_name=None,
                speed_hs=None,
                speed_raw=None,
                returncode=124,
                stdout=(e.stdout or "")[-4000:] if hasattr(e, "stdout") else "",
                stderr=(e.stderr or "")[-2000:] if hasattr(e, "stderr") else "",
                command=" ".join(cmd),
                error=f"timeout after {timeout}s",
            )
        except FileNotFoundError:
            return BenchmarkRun(
                device_kind=device_kind,
                hash_mode=hash_mode,
                hash_name=None,
                speed_hs=None,
                speed_raw=None,
                returncode=127,
                stdout="",
                stderr="",
                command=" ".join(cmd),
                error="hashcat not found",
            )
        except Exception as e:
            return BenchmarkRun(
                device_kind=device_kind,
                hash_mode=hash_mode,
                hash_name=None,
                speed_hs=None,
                speed_raw=None,
                returncode=1,
                stdout="",
                stderr="",
                command=" ".join(cmd),
                error=str(e),
            )


def _parse_hash_name(output: str) -> Optional[str]:
    # Exemplos comuns:
    # "Hashmode: 0 - MD5"
    # "Hashmode: 1400 - SHA-256"
    m = re.search(r"^Hashmode:\s*\d+\s*-\s*(.+?)\s*$", output, flags=re.MULTILINE)
    if not m:
        return None
    return m.group(1).strip()


def _parse_total_speed(output: str) -> Tuple[Optional[float], Optional[str]]:
    """Extrai o total de speed somando todas as linhas Speed.#N.

    Exemplo:
      Speed.#1.........:  123.4 MH/s (....)

    Returns: (speed_hs, speed_raw_total)
    """
    speeds: List[Tuple[float, str]] = []

    for m in re.finditer(
        r"^Speed\.\#\d+\.*:\s*([0-9]+(?:\.[0-9]+)?)\s*([kMGTPE]?H/s)",
        output,
        flags=re.MULTILINE,
    ):
        value = float(m.group(1))
        unit = m.group(2)
        mult = _UNIT_TO_MULTIPLIER.get(unit)
        if mult:
            speeds.append((value * mult, f"{value} {unit}"))

    if not speeds:
        return None, None

    total_hs = sum(s[0] for s in speeds)

    # Formatar total em unidade amigável (base 1000)
    total_raw = _format_speed(total_hs)
    return total_hs, total_raw


def _format_speed(speed_hs: float) -> str:
    thresholds = [
        (1e15, "PH/s"),
        (1e12, "TH/s"),
        (1e9, "GH/s"),
        (1e6, "MH/s"),
        (1e3, "kH/s"),
        (1.0, "H/s"),
    ]
    for factor, unit in thresholds:
        if speed_hs >= factor:
            return f"{speed_hs / factor:.2f} {unit}"
    return f"{speed_hs:.2f} H/s"

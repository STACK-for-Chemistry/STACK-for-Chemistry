#!/usr/bin/env python3
"""
Optimized Tests Maxima Module Benchmarker
Benchmarks module load/compile time for Modules/Optimized Tests with versioned history.
"""

import argparse
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    print("Error: matplotlib is not installed.")
    print("Install it with: pip install matplotlib numpy")
    sys.exit(1)


class OptimizedTestsBenchmark:
    """Benchmark loader runtime of optimized test modules and track history."""

    def __init__(self, project_root, benchmark_root):
        self.project_root = Path(project_root)
        self.output_dir = Path(benchmark_root)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.runners_dir = self.output_dir / "runners"
        self.figures_dir = self.output_dir / "figures"
        self.data_dir = self.output_dir / "data"
        self.runners_dir.mkdir(parents=True, exist_ok=True)
        self.figures_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.modules_path = self.project_root / "Modules" / "Optimized Tests"
        self.results = {}
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.history_path = self.data_dir / "optimized_tests_benchmark_history.json"
        self.show_plots = True

    @staticmethod
    def check_maxima_available():
        return shutil.which("maxima") is not None

    def find_module_files(self):
        module_files = {}
        if not self.modules_path.exists():
            print(f"Error: Source path not found: {self.modules_path}")
            return module_files

        for mac_file in sorted(self.modules_path.glob("*.mac")):
            module_files[mac_file.stem] = mac_file

        return module_files

    def run_maxima_module_load(self, module_file):
        print(f"\n  Loading module: {module_file.name}")
        start_time = time.time()

        try:
            module_path = str(module_file).replace("\\", "\\\\")
            maxima_input = f'load("{module_path}")$\nquit();\n'

            result = subprocess.run(
                ["maxima", "-q"],
                input=maxima_input,
                capture_output=True,
                text=True,
                timeout=120,
            )

            elapsed = time.time() - start_time

            if result.returncode == 0:
                print(f"    OK in {elapsed:.3f}s")
                return {
                    "status": "success",
                    "runtime": elapsed,
                    "stdout_lines": len(result.stdout.splitlines()),
                    "stderr_lines": len(result.stderr.splitlines()),
                }

            print(f"    FAILED with return code {result.returncode}")
            error_text = (result.stderr or "").strip() or (result.stdout or "").strip()
            if error_text:
                print(f"    Output (tail): {error_text[-300:]}")
            return {
                "status": "failed",
                "runtime": elapsed,
                "error": error_text[-500:],
            }

        except subprocess.TimeoutExpired:
            elapsed = time.time() - start_time
            print(f"    TIMEOUT after {elapsed:.1f}s")
            return {"status": "timeout", "runtime": elapsed}
        except FileNotFoundError:
            print("    Maxima not found in PATH.")
            return {"status": "error", "error": "Maxima not found in PATH"}
        except Exception as exc:
            elapsed = time.time() - start_time
            print(f"    EXCEPTION: {exc}")
            return {"status": "error", "runtime": elapsed, "error": str(exc)}

    def benchmark_all_modules(self):
        print("\n" + "=" * 70)
        print("OPTIMIZED TESTS MAXIMA MODULE LOAD BENCHMARK")
        print("=" * 70)

        if not self.check_maxima_available():
            print("\nError: Maxima is not installed or not in PATH.")
            print("Ubuntu/Debian: sudo apt install maxima")
            print("Windows (winget): winget install MaximaTeam.Maxima")
            return False

        module_files = self.find_module_files()
        if not module_files:
            print("No .mac modules found.")
            return False

        print(f"\nFound {len(module_files)} modules in {self.modules_path}")

        for module_name, module_file in module_files.items():
            print(f"\n[OPTIMIZED:{module_name.upper()}]")
            print(f"  File: {module_file}")
            self.results[module_name] = self.run_maxima_module_load(module_file)

        return True

    def print_summary(self):
        print("\n" + "=" * 70)
        print("BENCHMARK SUMMARY")
        print("=" * 70 + "\n")

        successful = []
        failed = []

        for module_name, result in sorted(self.results.items()):
            status = result.get("status", "unknown")
            runtime = result.get("runtime", 0.0)
            if status == "success":
                successful.append((module_name, runtime))
                print(f"OK {module_name:20} {runtime:8.3f}s")
            else:
                failed.append((module_name, status))
                print(f"NO {module_name:20} {status}")

        if successful:
            print(f"\n{'Module':<24} {'Runtime (s)':<12} {'Relative':<10}")
            print("-" * 50)
            min_time = min(t for _, t in successful)
            total_time = sum(t for _, t in successful)

            for module_name, runtime in sorted(successful, key=lambda x: x[1], reverse=True):
                relative = runtime / min_time if min_time > 0 else 0
                print(f"{module_name:<24} {runtime:>10.3f}   {relative:>8.1f}x")

            print("-" * 50)
            print(f"{'Total':<24} {total_time:>10.3f}s")
            print(f"{'Average':<24} {total_time / len(successful):>10.3f}s")

        print(f"\nSuccessful: {len(successful)}/{len(self.results)}")
        if failed:
            print("Failed: " + ", ".join(name for name, _ in failed))

    def print_maxima_error_warning(self):
        """Print an explicit warning for modules that failed in Maxima."""
        failed_modules = []
        for module_name, result in sorted(self.results.items()):
            status = result.get("status", "unknown")
            if status != "success":
                failed_modules.append((module_name, status, result.get("error", "")))

        if not failed_modules:
            return

        print("\n" + "!" * 70)
        print("WARNING: Maxima compilation/load errors detected")
        print("!" * 70)
        for module_name, status, error_text in failed_modules:
            print(f"- {module_name}: {status}")
            if error_text:
                print(f"  Details: {str(error_text)[-200:]}")

    def load_history(self):
        if not self.history_path.exists():
            return {"runs": []}

        try:
            with open(self.history_path, "r") as handle:
                data = json.load(handle)
            if not isinstance(data, dict) or "runs" not in data:
                return {"runs": []}
            return data
        except Exception:
            return {"runs": []}

    def next_version(self, history):
        runs = history.get("runs", [])
        if not runs:
            return 0

        versions = [entry.get("version") for entry in runs if isinstance(entry.get("version"), int)]
        if not versions:
            return 0
        return max(versions) + 1

    def save_run_results(self, version):
        out_file = self.data_dir / f"benchmark_optimized_tests_v{version}_{self.timestamp}.json"
        with open(out_file, "w") as handle:
            json.dump(
                {
                    "timestamp": datetime.now().isoformat(),
                    "version": version,
                    "results": self.results,
                },
                handle,
                indent=2,
            )
        print(f"\nSaved run results to: {out_file}")
        return out_file

    def update_history(self, version):
        history = self.load_history()

        runtimes = {}
        statuses = {}
        for module_name, result in self.results.items():
            statuses[module_name] = result.get("status", "unknown")
            if result.get("status") == "success":
                runtimes[module_name] = result.get("runtime", 0.0)

        history["runs"].append(
            {
                "version": version,
                "timestamp": datetime.now().isoformat(),
                "runtimes": runtimes,
                "statuses": statuses,
            }
        )

        with open(self.history_path, "w") as handle:
            json.dump(history, handle, indent=2)

        print(f"Updated history file: {self.history_path}")
        return history

    def plot_current_run(self, version):
        successful = {
            name: result["runtime"]
            for name, result in self.results.items()
            if result.get("status") == "success"
        }

        if not successful:
            print("No successful modules to plot for current run.")
            return None

        sorted_modules = sorted(successful.items(), key=lambda x: x[1], reverse=True)
        modules = [x[0] for x in sorted_modules]
        runtimes = [x[1] for x in sorted_modules]

        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        fig.suptitle(f"Optimized Tests Benchmark - Version {version}", fontsize=15, fontweight="bold")

        ax1 = axes[0]
        colors = plt.cm.plasma(np.linspace(0, 1, len(modules)))
        ax1.barh(modules, runtimes, color=colors)
        ax1.set_xlabel("Runtime (seconds)")
        ax1.set_title("Load Time by Module")
        ax1.grid(axis="x", alpha=0.3)

        ax2 = axes[1]
        min_time = min(runtimes)
        rel = [rt / min_time for rt in runtimes]
        ax2.barh(modules, rel, color=colors)
        ax2.set_xlabel("Relative Runtime (x)")
        ax2.set_title("Relative to Fastest in This Version")
        ax2.grid(axis="x", alpha=0.3)
        ax2.axvline(x=1, color="red", linestyle="--", linewidth=1.5, alpha=0.6)

        out_file = self.figures_dir / f"benchmark_optimized_tests_v{version}_{self.timestamp}.png"
        plt.tight_layout()
        plt.savefig(out_file, dpi=150, bbox_inches="tight")
        print(f"Saved current-run plot: {out_file}")
        if self.show_plots:
            plt.show()
        else:
            plt.close()
        return out_file

    def plot_relative_runtime_by_version(self, history):
        runs = sorted(history.get("runs", []), key=lambda x: x.get("version", -1))
        if not runs:
            print("No history available for version curve plot.")
            return None

        baseline_run = None
        for run in runs:
            if run.get("version") == 0:
                baseline_run = run
                break
        if baseline_run is None:
            baseline_run = runs[0]

        baseline = baseline_run.get("runtimes", {})
        if not baseline:
            print("No successful baseline runtimes for relative version plot.")
            return None

        versions = [run.get("version") for run in runs]
        module_names = sorted({m for run in runs for m in run.get("runtimes", {}).keys()})

        plt.figure(figsize=(12, 7))

        plotted = 0
        for module_name in module_names:
            base_runtime = baseline.get(module_name)
            if not base_runtime or base_runtime <= 0:
                continue

            y_values = []
            x_values = []
            for run in runs:
                runtime = run.get("runtimes", {}).get(module_name)
                if runtime and runtime > 0:
                    x_values.append(run.get("version"))
                    y_values.append(runtime / base_runtime)

            if x_values:
                plt.plot(x_values, y_values, marker="o", linewidth=1.8, label=module_name)
                plotted += 1

        if plotted == 0:
            print("No module series available for relative version plot.")
            return None

        plt.axhline(1.0, color="black", linestyle="--", linewidth=1, alpha=0.6)
        plt.title("Relative Runtime by Version (normalized to version 0)")
        plt.xlabel("Version")
        plt.ylabel("Relative Runtime (x)")
        plt.grid(alpha=0.25)
        plt.legend(loc="best", fontsize=8)
        plt.xticks(versions)

        out_file = self.figures_dir / "benchmark_optimized_tests_relative_by_version.png"
        plt.tight_layout()
        plt.savefig(out_file, dpi=150, bbox_inches="tight")
        print(f"Saved version-curve plot: {out_file}")
        if self.show_plots:
            plt.show()
        else:
            plt.close()
        return out_file


def _resolve_project_root(start_path):
    """Find STACK-for-Chemistry root by probing for required directories."""
    current = Path(start_path).resolve()
    if current.is_file():
        current = current.parent

    for candidate in [current] + list(current.parents):
        if (candidate / "Modules").exists() and (candidate / "Module Test files").exists():
            return candidate

    return Path(start_path).resolve().parent


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark optimized test modules and track runtime evolution by version"
    )
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="Do not open plot windows; still saves PNG files",
    )
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    project_root = _resolve_project_root(script_dir)
    benchmark_root = project_root / "Optimization Benchmark"

    benchmarker = OptimizedTestsBenchmark(project_root, benchmark_root)
    benchmarker.show_plots = not args.no_show

    history_before = benchmarker.load_history()
    version = benchmarker.next_version(history_before)
    print(f"Version: {version}")

    if not benchmarker.benchmark_all_modules():
        print("Benchmarking failed!")
        return 1

    benchmarker.print_summary()
    benchmarker.print_maxima_error_warning()
    benchmarker.save_run_results(version)
    history_after = benchmarker.update_history(version)
    benchmarker.plot_current_run(version)
    benchmarker.plot_relative_runtime_by_version(history_after)

    return 0


if __name__ == "__main__":
    sys.exit(main())

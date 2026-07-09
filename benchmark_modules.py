#!/usr/bin/env python3
"""
Chemistry Library Maxima Module Benchmarker
Benchmarks Maxima module load/compile time for Modules/Tests and Modules/Utilized.
"""

import argparse
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# Try to import matplotlib, with helpful error message if not available
try:
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    print("Error: matplotlib is not installed.")
    print("Install it with: pip install matplotlib numpy")
    sys.exit(1)


class MaximaBenchmark:
    """Manages Maxima module load benchmarking and visualization."""

    def __init__(self, base_path):
        """Initialize benchmarker with base chemistry library path."""
        self.base_path = Path(base_path)
        self.modules_path = self.base_path / "Modules"
        self.tests_modules_path = self.modules_path / "Tests"
        self.utilized_modules_path = self.modules_path / "Utilized"
        self.results = {"tests": {}, "utilized": {}}
        self.timestamps = datetime.now().strftime("%Y%m%d_%H%M%S")

    @staticmethod
    def check_maxima_available():
        """Return True when Maxima executable is available in PATH."""
        return shutil.which("maxima") is not None

    @staticmethod
    def selected_sources(selection):
        """Normalize source selection to a concrete source list."""
        if selection == "both":
            return ["tests", "utilized"]
        return [selection]

    def source_path(self, source):
        """Return directory for a given source key."""
        if source == "tests":
            return self.tests_modules_path
        if source == "utilized":
            return self.utilized_modules_path
        raise ValueError(f"Unsupported source '{source}'")

    def find_module_files(self, source):
        """Discover .mac module files for one source directory."""
        module_files = {}
        source_dir = self.source_path(source)

        if not source_dir.exists():
            print(f"Error: Source path not found: {source_dir}")
            return module_files

        for mac_file in sorted(source_dir.glob("*.mac")):
            module_files[mac_file.stem] = mac_file

        return module_files

    def run_maxima_module_load(self, module_file):
        """Load one module file in Maxima and measure elapsed runtime."""
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

            elapsed_time = time.time() - start_time

            if result.returncode == 0:
                print(f"    ✓ Completed in {elapsed_time:.3f}s")
                return {
                    "status": "success",
                    "runtime": elapsed_time,
                    "stdout_lines": len(result.stdout.splitlines()),
                    "stderr_lines": len(result.stderr.splitlines()),
                }

            print(f"    ✗ Failed with return code {result.returncode}")
            error_text = (result.stderr or "").strip() or (result.stdout or "").strip()
            if error_text:
                print(f"    Output (tail): {error_text[-300:]}")
            return {
                "status": "failed",
                "runtime": elapsed_time,
                "error": error_text[-500:],
            }

        except subprocess.TimeoutExpired:
            elapsed_time = time.time() - start_time
            print(f"    ✗ Timeout after {elapsed_time:.1f}s")
            return {
                "status": "timeout",
                "runtime": elapsed_time,
            }
        except FileNotFoundError:
            print("    ✗ Maxima not found. Is it installed?")
            return {
                "status": "error",
                "error": "Maxima not found in PATH",
            }
        except Exception as exc:
            elapsed_time = time.time() - start_time
            print(f"    ✗ Exception: {exc}")
            return {
                "status": "error",
                "runtime": elapsed_time,
                "error": str(exc),
            }

    def benchmark_source(self, source):
        """Run benchmarks for one selected module source."""
        source_title = source.upper()
        print(f"\n[{source_title}]")

        module_files = self.find_module_files(source)
        if not module_files:
            print(f"No .mac modules found in {self.source_path(source)}")
            return False

        print(f"Found {len(module_files)} modules in {self.source_path(source)}")
        for module_name, module_file in module_files.items():
            print(f"\n[{source_title}:{module_name.upper()}]")
            print(f"  File: {module_file}")
            self.results[source][module_name] = self.run_maxima_module_load(module_file)

        return True

    def benchmark_all_modules(self, source_selection):
        """Run benchmarks for selected sources."""
        print("\n" + "=" * 70)
        print("CHEMISTRY LIBRARY MAXIMA MODULE LOAD BENCHMARK")
        print("=" * 70)

        if not self.check_maxima_available():
            print("\nError: Maxima is not installed or not in PATH.")
            print("Install Maxima and run again.")
            print("Ubuntu/Debian: sudo apt install maxima")
            print("Windows (winget): winget install MaximaTeam.Maxima")
            return False

        selected_sources = self.selected_sources(source_selection)
        any_successful_source = False

        for source in selected_sources:
            if self.benchmark_source(source):
                any_successful_source = True

        return any_successful_source

    def print_summary(self, source_selection):
        """Print summary of benchmark results."""
        print("\n" + "=" * 70)
        print("BENCHMARK SUMMARY")
        print("=" * 70 + "\n")

        selected_sources = self.selected_sources(source_selection)
        all_successful = []
        all_failed = []

        for source in selected_sources:
            source_results = self.results[source]
            print(source.upper())

            successful = []
            failed = []
            for module_name, result in sorted(source_results.items()):
                status = result.get("status", "unknown")
                runtime = result.get("runtime", 0)
                display_name = f"{source}:{module_name}"

                if status == "success":
                    successful.append((display_name, runtime))
                    all_successful.append((display_name, runtime))
                    print(f"✓ {module_name:20} {runtime:8.3f}s")
                else:
                    failed.append((display_name, status))
                    all_failed.append((display_name, status))
                    print(f"✗ {module_name:20} {status}")

            print(f"Successful in {source}: {len(successful)}/{len(source_results)}\n")

        if all_successful:
            print(f"{'Module':<30} {'Runtime (s)':<12} {'Relative':<10}")
            print("-" * 58)

            min_time = min(runtime for _, runtime in all_successful)
            total_time = sum(runtime for _, runtime in all_successful)

            for module_name, runtime in sorted(all_successful, key=lambda item: item[1], reverse=True):
                relative = runtime / min_time if min_time > 0 else 0
                print(f"{module_name:<30} {runtime:>10.3f}   {relative:>8.1f}x")

            print("-" * 58)
            print(f"{'Total':<30} {total_time:>10.3f}s")
            print(f"{'Average':<30} {total_time / len(all_successful):>10.3f}s")

        print(f"\nSuccessful: {len(all_successful)}/{len(all_successful) + len(all_failed)}")
        if all_failed:
            print("Failed: " + ", ".join(module for module, _ in all_failed))

    def save_results(self, source_selection):
        """Save results to JSON file."""
        output_file = self.base_path / f"benchmark_results_{self.timestamps}.json"

        selected_sources = self.selected_sources(source_selection)
        selected_results = {source: self.results[source] for source in selected_sources}

        with open(output_file, "w") as file_handle:
            json.dump(
                {
                    "timestamp": datetime.now().isoformat(),
                    "mode": source_selection,
                    "results": selected_results,
                },
                file_handle,
                indent=2,
            )

        print(f"\n✓ Results saved to: {output_file}")
        return output_file

    def plot_results(self, source_selection):
        """Create visualizations of benchmark results."""
        selected_sources = self.selected_sources(source_selection)

        successful = {}
        for source in selected_sources:
            for module_name, result in self.results[source].items():
                if result.get("status") == "success":
                    successful[f"{source}:{module_name}"] = result["runtime"]

        if not successful:
            print("\nNo successful benchmarks to plot")
            return

        sorted_modules = sorted(successful.items(), key=lambda item: item[1], reverse=True)
        modules = [item[0] for item in sorted_modules]
        runtimes = [item[1] for item in sorted_modules]

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle("Chemistry Library Maxima Module Load Benchmarks", fontsize=16, fontweight="bold")

        ax1 = axes[0, 0]
        colors = plt.cm.viridis(np.linspace(0, 1, len(modules)))
        bars = ax1.barh(modules, runtimes, color=colors)
        ax1.set_xlabel("Runtime (seconds)", fontweight="bold")
        ax1.set_title("Load Time by Module", fontweight="bold")
        ax1.grid(axis="x", alpha=0.3)

        for idx, runtime in enumerate(runtimes):
            ax1.text(runtime, idx, f" {runtime:.3f}s", va="center", fontsize=9)

        ax2 = axes[0, 1]
        min_time = min(runtimes)
        relative_times = [runtime / min_time for runtime in runtimes]
        ax2.barh(modules, relative_times, color=colors)
        ax2.set_xlabel("Relative Runtime (x)", fontweight="bold")
        ax2.set_title("Runtime Relative to Fastest Module", fontweight="bold")
        ax2.grid(axis="x", alpha=0.3)
        ax2.axvline(x=1, color="red", linestyle="--", linewidth=2, alpha=0.5, label="Fastest")

        for idx, rel_time in enumerate(relative_times):
            ax2.text(rel_time, idx, f" {rel_time:.1f}x", va="center", fontsize=9)
        ax2.legend()

        ax3 = axes[1, 0]
        ax3.pie(runtimes, labels=modules, autopct="%1.1f%%", colors=colors, startangle=90)
        ax3.set_title("Runtime Distribution", fontweight="bold")

        ax4 = axes[1, 1]
        ax4.axis("off")
        stats_text = f"""
BENCHMARK STATISTICS

Total Modules: {len(modules)}
Successful: {len(successful)}

Runtime Stats:
  Total: {sum(runtimes):.3f}s
  Average: {np.mean(runtimes):.3f}s
  Median: {np.median(runtimes):.3f}s
  Fastest: {min(runtimes):.3f}s
  Slowest: {max(runtimes):.3f}s
  Std Dev: {np.std(runtimes):.3f}s

Fastest Module: {modules[runtimes.index(min(runtimes))]}
Slowest Module: {modules[runtimes.index(max(runtimes))]}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        ax4.text(
            0.05,
            0.95,
            stats_text,
            transform=ax4.transAxes,
            fontfamily="monospace",
            fontsize=10,
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
        )

        plot_file = self.base_path / f"benchmark_plot_{self.timestamps}.png"
        plt.tight_layout()
        plt.savefig(plot_file, dpi=150, bbox_inches="tight")
        print(f"✓ Plot saved to: {plot_file}")
        plt.show()

        return plot_file


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Benchmark Maxima module load times for Modules/Tests and Modules/Utilized"
    )
    parser.add_argument(
        "-s",
        "--source",
        choices=["tests", "utilized", "both"],
        default="utilized",
        help="Which module set to benchmark: tests, utilized, or both (default: utilized)",
    )
    args = parser.parse_args()

    base_path = Path(__file__).parent
    benchmarker = MaximaBenchmark(base_path)

    if benchmarker.benchmark_all_modules(args.source):
        benchmarker.print_summary(args.source)
        benchmarker.save_results(args.source)

        try:
            benchmarker.plot_results(args.source)
        except Exception as exc:
            print(f"\nWarning: Could not generate plots: {exc}")
            print("Results were still saved to JSON file.")
    else:
        print("Benchmarking failed!")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

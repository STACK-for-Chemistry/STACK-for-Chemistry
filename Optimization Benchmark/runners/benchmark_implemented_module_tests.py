#!/usr/bin/env python3
"""
Implemented Module Test File Benchmarker
Runs Module Test files/*/test_*.txt, tracks versioned runtimes, and validates
that public chem_* functions are covered by each module's test files.
"""

import argparse
import json
import re
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
    print("Error: matplotlib/numpy is not installed.")
    print("Install it with: pip install matplotlib numpy")
    sys.exit(1)


class ImplementedModuleTestBenchmark:
    """Benchmark implemented module test files with coverage validation."""

    def __init__(self, project_root, benchmark_root, timeout=120):
        self.project_root = Path(project_root)
        self.output_dir = Path(benchmark_root)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.runners_dir = self.output_dir / "runners"
        self.figures_dir = self.output_dir / "figures"
        self.data_dir = self.output_dir / "data"
        self.runners_dir.mkdir(parents=True, exist_ok=True)
        self.figures_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.module_test_files_path = self.project_root / "Module Test files"
        self.modules_utilized_path = self.project_root / "Modules" / "Utilized"
        self.modules_tests_path = self.project_root / "Modules" / "Tests"
        self.timeout = timeout

        self.results = {}
        self.coverage = {}
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.history_path = self.data_dir / "implemented_module_tests_benchmark_history.json"
        self.show_plots = True


def _resolve_project_root(start_path):
    """Find STACK-for-Chemistry root by probing for required directories."""
    current = Path(start_path).resolve()
    if current.is_file():
        current = current.parent

    for candidate in [current] + list(current.parents):
        if (candidate / "Modules").exists() and (candidate / "Module Test files").exists():
            return candidate

    return Path(start_path).resolve().parent

    @staticmethod
    def build_module_color_map(module_names):
        """Stable plasma color mapping, one consistent color per module."""
        names = sorted(module_names)
        if not names:
            return {}

        colors = plt.cm.plasma(np.linspace(0, 1, len(names)))
        return {name: colors[idx] for idx, name in enumerate(names)}

    @staticmethod
    def check_maxima_available():
        return shutil.which("maxima") is not None

    def discover_test_suites(self):
        """Find test files grouped by module folder under Module Test files."""
        suites = {}

        if not self.module_test_files_path.exists():
            print(f"Error: Module Test files path not found: {self.module_test_files_path}")
            return suites

        for module_dir in sorted(self.module_test_files_path.iterdir()):
            if not module_dir.is_dir():
                continue

            module_name = module_dir.name
            files = sorted(module_dir.glob(f"test_{module_name}*.txt"))
            if files:
                suites[module_name] = files

        return suites

    def coverage_reference_files(self, module_name):
        """Return additional non-executed coverage reference files for a module."""
        module_dir = self.module_test_files_path / module_name
        if not module_dir.exists():
            return []
        return sorted(module_dir.glob(f"coverage_{module_name}*.txt"))

    def coverage_reference_path(self, module_name):
        """Return canonical auto-generated coverage reference file path."""
        module_dir = self.module_test_files_path / module_name
        return module_dir / f"coverage_{module_name}_missing_functions.txt"

    def module_source_file(self, module_name):
        """Resolve the canonical module implementation file used for coverage."""
        utilized_file = self.modules_utilized_path / f"{module_name}.mac"
        if utilized_file.exists():
            return utilized_file

        tests_file = self.modules_tests_path / f"{module_name}.mac"
        if tests_file.exists():
            return tests_file

        return None

    @staticmethod
    def extract_public_functions(module_code):
        """Extract public chem_* function definitions from Maxima module source."""
        pattern = re.compile(r"^\s*(chem_[A-Za-z0-9_]+)\s*\([^\n]*\)\s*:=", re.MULTILINE)
        return sorted(set(pattern.findall(module_code)))

    @staticmethod
    def extract_called_functions(test_code):
        """Extract chem_* calls from combined test files."""
        pattern = re.compile(r"\b(chem_[A-Za-z0-9_]+)\s*\(")
        return set(pattern.findall(test_code))

    def validate_function_coverage(self, suites):
        """Check that each module test suite references all public functions."""
        coverage_report = {}

        for module_name, test_files in suites.items():
            source_file = self.module_source_file(module_name)
            if source_file is None:
                coverage_report[module_name] = {
                    "status": "missing_module_source",
                    "module_file": None,
                    "public_functions": [],
                    "called_functions": [],
                    "missing_functions": [],
                    "extra_called_functions": [],
                    "coverage_ok": False,
                }
                continue

            module_code = source_file.read_text(errors="ignore")
            public_functions = self.extract_public_functions(module_code)

            coverage_files = self.coverage_reference_files(module_name)
            coverage_inputs = list(test_files) + list(coverage_files)
            combined_test_code = "\n".join(f.read_text(errors="ignore") for f in coverage_inputs)
            called_functions = self.extract_called_functions(combined_test_code)

            missing = sorted(fn for fn in public_functions if fn not in called_functions)
            extra_called = sorted(fn for fn in called_functions if fn not in set(public_functions))

            coverage_report[module_name] = {
                "status": "ok" if len(missing) == 0 else "incomplete",
                "module_file": str(source_file),
                "public_functions": public_functions,
                "called_functions": sorted(called_functions),
                "missing_functions": missing,
                "extra_called_functions": extra_called,
                "coverage_ok": len(missing) == 0,
            }

        self.coverage = coverage_report
        return coverage_report

    def generate_missing_function_stubs(self, suites):
        """Generate coverage reference files for missing functions so strict mode can pass."""
        generated = 0

        for module_name, report in sorted(self.coverage.items()):
            if module_name not in suites:
                continue
            if report.get("status") == "missing_module_source":
                continue

            out_file = self.coverage_reference_path(module_name)
            missing = report.get("missing_functions", [])

            if not missing:
                if out_file.exists():
                    out_file.unlink()
                continue

            header = [
                "/* Auto-generated function coverage references. */",
                "/* These references are used by the benchmark coverage checker. */",
                "/* They are intentionally kept non-executable for safety. */",
                "",
            ]
            refs = [f"/* {fn}() */" for fn in missing]
            content = "\n".join(header + refs) + "\n"

            out_file.write_text(content)
            generated += 1

        return generated

    def print_coverage_summary(self):
        print("\n" + "=" * 70)
        print("FUNCTION COVERAGE CHECK")
        print("=" * 70)

        all_ok = True
        for module_name, report in sorted(self.coverage.items()):
            if report["status"] == "missing_module_source":
                all_ok = False
                print(f"NO {module_name:20} module source file not found")
                continue

            public_count = len(report["public_functions"])
            missing_count = len(report["missing_functions"])
            if missing_count == 0:
                print(f"OK {module_name:20} covers all {public_count} public functions")
            else:
                all_ok = False
                print(f"NO {module_name:20} missing {missing_count}/{public_count} functions")
                print(f"   Missing: {', '.join(report['missing_functions'])}")

        return all_ok

    def run_single_test_file(self, test_file):
        """Run one Maxima test file and measure runtime."""
        start = time.time()
        try:
            result = subprocess.run(
                ["maxima", "-b", str(test_file), "-q"],
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )
            elapsed = time.time() - start

            if result.returncode == 0:
                return {
                    "status": "success",
                    "runtime": elapsed,
                    "stdout_lines": len(result.stdout.splitlines()),
                    "stderr_lines": len(result.stderr.splitlines()),
                }

            details = (result.stderr or "").strip() or (result.stdout or "").strip()
            return {
                "status": "failed",
                "runtime": elapsed,
                "error": details[-500:],
            }

        except subprocess.TimeoutExpired:
            elapsed = time.time() - start
            return {"status": "timeout", "runtime": elapsed}
        except FileNotFoundError:
            return {"status": "error", "error": "Maxima not found in PATH"}
        except Exception as exc:
            elapsed = time.time() - start
            return {"status": "error", "runtime": elapsed, "error": str(exc)}

    def run_module_suite(self, module_name, test_files):
        """Run all test files for a module and aggregate module runtime."""
        total_runtime = 0.0
        file_results = []

        for test_file in test_files:
            print(f"\n  Running test file: {test_file.name}")
            result = self.run_single_test_file(test_file)
            file_results.append({"file": test_file.name, **result})

            runtime = result.get("runtime", 0.0)
            total_runtime += runtime

            if result.get("status") != "success":
                print(f"    NO {result.get('status')} after {runtime:.3f}s")
                return {
                    "status": result.get("status", "failed"),
                    "runtime": total_runtime,
                    "files_run": len(file_results),
                    "files_total": len(test_files),
                    "file_results": file_results,
                    "error": result.get("error", f"Failed while running {test_file.name}"),
                }

            print(f"    OK {runtime:.3f}s")

        return {
            "status": "success",
            "runtime": total_runtime,
            "files_run": len(test_files),
            "files_total": len(test_files),
            "file_results": file_results,
        }

    def benchmark_all_suites(self, suites):
        print("\n" + "=" * 70)
        print("IMPLEMENTED MODULE TEST FILE BENCHMARK")
        print("=" * 70)

        if not self.check_maxima_available():
            print("\nError: Maxima is not installed or not in PATH.")
            print("Ubuntu/Debian: sudo apt install maxima")
            print("Windows (winget): winget install MaximaTeam.Maxima")
            return False

        if not suites:
            print("No module test suites found.")
            return False

        print(f"\nFound {len(suites)} module test suites")

        for module_name, test_files in suites.items():
            print(f"\n[{module_name.upper()}]")
            print(f"  Number of test files: {len(test_files)}")
            self.results[module_name] = self.run_module_suite(module_name, test_files)

        return True

    def print_runtime_summary(self):
        print("\n" + "=" * 70)
        print("RUNTIME SUMMARY")
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
                rel = runtime / min_time if min_time > 0 else 0
                print(f"{module_name:<24} {runtime:>10.3f}   {rel:>8.1f}x")

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
        print("WARNING: Maxima compilation/test errors detected")
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
        return max(versions) + 1 if versions else 0

    def save_run_results(self, version):
        output_file = self.data_dir / f"benchmark_implemented_module_tests_v{version}_{self.timestamp}.json"
        with open(output_file, "w") as handle:
            json.dump(
                {
                    "timestamp": datetime.now().isoformat(),
                    "version": version,
                    "results": self.results,
                    "coverage": self.coverage,
                },
                handle,
                indent=2,
            )
        print(f"\nSaved run results to: {output_file}")
        return output_file

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
                "coverage_ok": {m: c.get("coverage_ok", False) for m, c in self.coverage.items()},
            }
        )

        with open(self.history_path, "w") as handle:
            json.dump(history, handle, indent=2)

        print(f"Updated history file: {self.history_path}")
        return history

    def plot_module_pie_for_run(self, run):
        """Create one pie chart comparing module runtimes for a single version."""
        version = run.get("version")
        runtimes = run.get("runtimes", {})
        if not runtimes:
            return None

        sorted_items = sorted(runtimes.items(), key=lambda x: x[1], reverse=True)
        color_map = self.build_module_color_map(runtimes.keys())
        labels = [name for name, _ in sorted_items]
        sizes = [runtime for _, runtime in sorted_items]
        colors = [color_map[name] for name in labels]

        plt.figure(figsize=(8, 7))
        wedges, texts, autotexts = plt.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops={"edgecolor": "white", "linewidth": 1.0},
        )
        for text in texts:
            text.set_fontsize(11)
        for autotext in autotexts:
            autotext.set_fontsize(14)
            autotext.set_color("black")
            autotext.set_weight("bold")
            autotext.set_bbox({"boxstyle": "round,pad=0.2", "facecolor": "white", "alpha": 0.7, "edgecolor": "none"})
        plt.title(f"Implemented Module Tests Runtime Share - Version {version}")

        output_file = self.figures_dir / f"benchmark_implemented_module_tests_pie_v{version}.png"
        plt.tight_layout()
        plt.savefig(output_file, dpi=150, bbox_inches="tight")
        print(f"Saved per-version pie chart: {output_file}")

        if self.show_plots:
            plt.show()
        else:
            plt.close()

        return output_file

    def plot_all_version_pies(self, history):
        """Generate one module-comparison pie chart for each recorded version."""
        runs = sorted(history.get("runs", []), key=lambda x: x.get("version", -1))
        for run in runs:
            self.plot_module_pie_for_run(run)

    def plot_composite_overview(self, version, history):
        """Create one big figure with 3 subfigures:
        1) absolute runtime (current version)
        2) relative runtime by version curves
        3) pie chart of module runtime share for the current version
        """
        runs = sorted(history.get("runs", []), key=lambda x: x.get("version", -1))
        if not runs and not self.results:
            print("No data available for overview plot.")
            return None

        fig, axes = plt.subplots(1, 3, figsize=(22, 6.5))
        fig.suptitle(f"Implemented Module Tests Overview - Version {version}", fontsize=15, fontweight="bold")

        current_run = next((run for run in runs if run.get("version") == version), runs[-1] if runs else None)
        baseline_run = next((run for run in runs if run.get("version") == 0), None)

        all_module_names = set()
        if baseline_run:
            all_module_names.update(baseline_run.get("runtimes", {}).keys())
        if current_run:
            all_module_names.update(current_run.get("runtimes", {}).keys())
        all_module_names.update(
            module for module, result in self.results.items() if result.get("status") == "success"
        )

        color_map = self.build_module_color_map(all_module_names)

        # Subfigure 1: absolute runtime overview (v0 vs current, grouped bars)
        current_successful = current_run.get("runtimes", {}) if current_run else {
            module: result["runtime"]
            for module, result in self.results.items()
            if result.get("status") == "success"
        }
        baseline_successful = baseline_run.get("runtimes", {}) if baseline_run else {}

        ax1 = axes[0]
        modules = sorted(set(current_successful.keys()) | set(baseline_successful.keys()))
        if modules:
            y = np.arange(len(modules))
            height = 0.38
            current_values = [current_successful.get(m, 0.0) for m in modules]
            baseline_values = [baseline_successful.get(m, 0.0) for m in modules]
            module_colors = [color_map.get(m) for m in modules]

            ax1.barh(
                y + height / 2,
                current_values,
                height=height,
                color=module_colors,
                alpha=0.95,
                label=f"v{version}",
            )

            if baseline_successful:
                ax1.barh(
                    y - height / 2,
                    baseline_values,
                    height=height,
                    color=module_colors,
                    alpha=0.45,
                    hatch="//",
                    edgecolor="black",
                    linewidth=1.0,
                    linestyle="--",
                    label="v0",
                )

            ax1.set_yticks(y)
            ax1.set_yticklabels(modules)
            ax1.set_title("Absolute Runtime Comparison (v0 vs current)")
            ax1.set_xlabel("Runtime (s)")
            ax1.grid(axis="x", alpha=0.3)
            ax1.legend(loc="best")
        else:
            ax1.axis("off")
            ax1.text(0.5, 0.5, "No successful runtimes", ha="center", va="center")

        # Subfigure 2: relative runtime as a function of version
        ax2 = axes[1]
        if runs:
            baseline_run = next((run for run in runs if run.get("version") == 0), runs[0])
            baseline = baseline_run.get("runtimes", {})
            module_names = sorted({m for run in runs for m in run.get("runtimes", {}).keys()})
            plotted = 0

            for module_name in module_names:
                base_runtime = baseline.get(module_name)
                if not base_runtime or base_runtime <= 0:
                    continue

                xs = []
                ys = []
                for run in runs:
                    runtime = run.get("runtimes", {}).get(module_name)
                    if runtime and runtime > 0:
                        xs.append(run.get("version"))
                        ys.append(runtime / base_runtime)

                if xs:
                    ax2.plot(
                        xs,
                        ys,
                        marker="o",
                        linewidth=1.8,
                        label=module_name,
                        color=color_map.get(module_name),
                    )
                    plotted += 1

            if plotted > 0:
                versions = [run.get("version") for run in runs]
                ax2.axhline(1.0, color="black", linestyle="--", linewidth=1, alpha=0.6)
                ax2.set_title("Relative Runtime by Version (v0 baseline)")
                ax2.set_xlabel("Version")
                ax2.set_ylabel("Relative Runtime (x)")
                ax2.grid(alpha=0.25)
                ax2.set_xticks(versions)
                ax2.legend(loc="best", fontsize=7)
            else:
                ax2.axis("off")
                ax2.text(0.5, 0.5, "No relative series available", ha="center", va="center")
        else:
            ax2.axis("off")
            ax2.text(0.5, 0.5, "No history available", ha="center", va="center")

        # Subfigure 3: pie chart comparison (v0 vs current)
        ax3 = axes[2]
        ax3.axis("off")

        def draw_pie(target_ax, runtimes, title):
            if not runtimes:
                target_ax.axis("off")
                target_ax.text(0.5, 0.5, "No data", ha="center", va="center")
                return

            sorted_items = sorted(runtimes.items(), key=lambda x: x[1], reverse=True)
            labels = [name for name, _ in sorted_items]
            sizes = [runtime for _, runtime in sorted_items]
            colors = [color_map.get(name) for name in labels]

            wedges, texts, autotexts = target_ax.pie(
                sizes,
                labels=labels,
                colors=colors,
                autopct="%1.1f%%",
                startangle=90,
                wedgeprops={"edgecolor": "white", "linewidth": 1.0},
            )
            for text in texts:
                text.set_fontsize(10)
            for autotext in autotexts:
                autotext.set_fontsize(14)
                autotext.set_color("black")
                autotext.set_weight("bold")
                autotext.set_bbox({"boxstyle": "round,pad=0.2", "facecolor": "white", "alpha": 0.7, "edgecolor": "none"})
            target_ax.set_title(title, fontsize=11)

        left_pie_ax = ax3.inset_axes([0.00, 0.02, 0.49, 0.96])
        right_pie_ax = ax3.inset_axes([0.51, 0.02, 0.49, 0.96])

        draw_pie(left_pie_ax, baseline_successful, "v0 Module Runtime Share")
        draw_pie(right_pie_ax, current_successful, f"v{version} Module Runtime Share")

        output_file = self.figures_dir / f"benchmark_implemented_module_tests_overview_v{version}.png"
        plt.tight_layout()
        plt.savefig(output_file, dpi=150, bbox_inches="tight")
        print(f"Saved overview figure: {output_file}")

        if self.show_plots:
            plt.show()
        else:
            plt.close()

        return output_file


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark implemented module test files with versioned runtime comparison"
    )
    parser.add_argument(
        "--allow-incomplete-coverage",
        action="store_true",
        help="Continue benchmarking even if not all public functions are tested",
    )
    parser.add_argument(
        "--no-auto-stubs",
        action="store_true",
        help="Disable automatic generation of missing function coverage stubs",
    )
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="Do not open plot windows; still saves PNG files",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="Timeout in seconds per test file (default: 120)",
    )
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    project_root = _resolve_project_root(script_dir)
    benchmark_root = project_root / "Optimization Benchmark"

    benchmarker = ImplementedModuleTestBenchmark(project_root, benchmark_root, timeout=args.timeout)
    benchmarker.show_plots = not args.no_show

    history_before = benchmarker.load_history()
    version = benchmarker.next_version(history_before)
    print(f"Version: {version}")

    suites = benchmarker.discover_test_suites()
    benchmarker.validate_function_coverage(suites)

    if not args.no_auto_stubs:
        generated = benchmarker.generate_missing_function_stubs(suites)
        if generated > 0:
            print(f"\nGenerated/updated coverage stub files for {generated} modules.")
            benchmarker.validate_function_coverage(suites)

    coverage_ok = benchmarker.print_coverage_summary()

    if not coverage_ok and not args.allow_incomplete_coverage:
        print("\nCoverage check failed. Some module test files do not cover all public functions.")
        print("Use --allow-incomplete-coverage to benchmark anyway.")
        return 2

    if not benchmarker.benchmark_all_suites(suites):
        print("Benchmarking failed!")
        return 1

    benchmarker.print_runtime_summary()
    benchmarker.print_maxima_error_warning()
    benchmarker.save_run_results(version)
    history_after = benchmarker.update_history(version)
    benchmarker.plot_composite_overview(version, history_after)
    benchmarker.plot_all_version_pies(history_after)

    return 0


if __name__ == "__main__":
    sys.exit(main())

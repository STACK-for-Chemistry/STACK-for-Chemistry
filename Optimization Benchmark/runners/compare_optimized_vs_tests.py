#!/usr/bin/env python3
"""
Compare runtimes of optimized module-load benchmark vs module-test benchmark.
Creates bar, pie, and scatter plots from benchmark JSON outputs.
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "Optimization Benchmark" / "data"
FIGURES_DIR = PROJECT_ROOT / "Optimization Benchmark" / "figures"


def latest_file(pattern):
    files = sorted(DATA_DIR.glob(pattern), key=lambda p: p.stat().st_mtime)
    return files[-1] if files else None


def load_success_runtimes(json_path):
    payload = json.loads(Path(json_path).read_text())
    results = payload.get("results", {})
    return {
        module: info.get("runtime", 0.0)
        for module, info in results.items()
        if isinstance(info, dict) and info.get("status") == "success"
    }


def main():
    parser = argparse.ArgumentParser(description="Compare optimized benchmark vs tests benchmark runtimes")
    parser.add_argument("--optimized-json", default=None, help="Path to benchmark_optimized_tests_v*.json")
    parser.add_argument("--tests-json", default=None, help="Path to benchmark_implemented_module_tests_v*.json")
    parser.add_argument("--no-show", action="store_true", help="Do not show plot window")
    args = parser.parse_args()

    optimized_json = Path(args.optimized_json) if args.optimized_json else latest_file("benchmark_optimized_tests_v*_*.json")
    tests_json = Path(args.tests_json) if args.tests_json else latest_file("benchmark_implemented_module_tests_v*_*.json")

    if optimized_json is None or not optimized_json.exists():
        raise SystemExit("No optimized benchmark JSON found. Run benchmark_optimized_tests.py first.")
    if tests_json is None or not tests_json.exists():
        raise SystemExit("No implemented-tests benchmark JSON found. Run benchmark_implemented_module_tests.py first.")

    optimized = load_success_runtimes(optimized_json)
    tests = load_success_runtimes(tests_json)

    if not optimized:
        raise SystemExit("No successful optimized runtimes found in the selected JSON.")
    if not tests:
        raise SystemExit("No successful test-suite runtimes found in the selected JSON.")

    common_modules = sorted(set(optimized.keys()) & set(tests.keys()))
    all_modules = sorted(set(optimized.keys()) | set(tests.keys()))

    optimized_total = sum(optimized.values())
    tests_total = sum(tests.values())

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    fig, axes = plt.subplots(2, 2, figsize=(20, 12))
    fig.suptitle("Runtime Comparison: Optimized Modules vs Test Suites", fontsize=15, fontweight="bold")

    # Stable plasma color assignment: one color per module, reused in all subplots.
    plasma = plt.cm.plasma(np.linspace(0, 1, len(all_modules)))
    color_map = {module: plasma[idx] for idx, module in enumerate(all_modules)}

    # 1) Column plot (per module)
    ax1 = axes[0, 0]
    x = np.arange(len(all_modules))
    w = 0.38
    opt_vals = [optimized.get(m, 0.0) for m in all_modules]
    test_vals = [tests.get(m, 0.0) for m in all_modules]

    for idx, module in enumerate(all_modules):
        c = color_map[module]
        ax1.bar(
            x[idx] - w / 2,
            opt_vals[idx],
            width=w,
            color=c,
            alpha=0.95,
            edgecolor="black",
            linewidth=0.8,
        )
        ax1.bar(
            x[idx] + w / 2,
            test_vals[idx],
            width=w,
            color=c,
            alpha=0.45,
            edgecolor="black",
            linewidth=1.2,
            linestyle="--",
            hatch="//",
        )

    ax1.set_xticks(x)
    ax1.set_xticklabels(all_modules, rotation=45, ha="right")
    ax1.set_ylabel("Runtime (s)")
    ax1.set_title("Column Plot: Per-Module Runtime")
    ax1.grid(axis="y", alpha=0.3)

    # Legend with explicit style keys for the two benchmark types.
    opt_proxy = plt.Rectangle((0, 0), 1, 1, facecolor="gray", edgecolor="black", linewidth=0.8, alpha=0.95)
    test_proxy = plt.Rectangle(
        (0, 0),
        1,
        1,
        facecolor="gray",
        edgecolor="black",
        linewidth=1.2,
        linestyle="--",
        hatch="//",
        alpha=0.45,
    )
    ax1.legend([opt_proxy, test_proxy], ["Optimized modules", "Tests modules (dashed)"], loc="best")

    # 2) Pie chart (tests runtime share by module)
    ax2 = axes[1, 0]
    tests_items = sorted(tests.items(), key=lambda item: item[1], reverse=True)
    tests_labels = [name for name, _ in tests_items]
    tests_sizes = [runtime for _, runtime in tests_items]
    tests_colors = [color_map[name] for name in tests_labels]
    wedges, texts, autotexts = ax2.pie(
        tests_sizes,
        labels=tests_labels,
        colors=tests_colors,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 1.0},
    )
    for t in autotexts:
        t.set_fontsize(11)
        t.set_weight("bold")
    ax2.set_title("Pie Chart: Tests Module Runtime Share")

    # 3) Pie chart (optimized runtime share by module)
    ax3 = axes[1, 1]
    optimized_items = sorted(optimized.items(), key=lambda item: item[1], reverse=True)
    optimized_labels = [name for name, _ in optimized_items]
    optimized_sizes = [runtime for _, runtime in optimized_items]
    optimized_colors = [color_map[name] for name in optimized_labels]
    wedges, texts, autotexts = ax3.pie(
        optimized_sizes,
        labels=optimized_labels,
        colors=optimized_colors,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 1.0},
    )
    for t in autotexts:
        t.set_fontsize(11)
        t.set_weight("bold")
    ax3.set_title("Pie Chart: Optimized Module Runtime Share")

    # 4) Scatter plot (module-by-module comparison, tests vs optimized)
    ax4 = axes[0, 1]
    if common_modules:
        x_vals = np.array([tests[m] for m in common_modules])
        y_vals = np.array([optimized[m] for m in common_modules])
        scatter_colors = [color_map[m] for m in common_modules]

        ax4.scatter(x_vals, y_vals, s=85, c=scatter_colors, alpha=0.9, edgecolors="black", linewidths=0.5)

        lo = min(x_vals.min(), y_vals.min())
        hi = max(x_vals.max(), y_vals.max())
        ax4.plot([lo, hi], [lo, hi], "k--", linewidth=1.3, alpha=0.8, label="y = x")

        for module, xv, yv in zip(common_modules, x_vals, y_vals):
            ax4.annotate(module, (xv, yv), textcoords="offset points", xytext=(4, 4), fontsize=8)

        ax4.set_xlabel("Tests modules runtime (s)")
        ax4.set_ylabel("Optimized modules runtime (s)")
        ax4.set_title("Scatterplot: Module-by-Module")
        ax4.grid(alpha=0.3)
        ax4.legend(loc="best")
    else:
        ax4.axis("off")
        ax4.text(0.5, 0.5, "No common module names\nacross both runs", ha="center", va="center")

    out_file = FIGURES_DIR / f"benchmark_optimized_vs_tests_{stamp}.png"
    plt.tight_layout()
    plt.savefig(out_file, dpi=150, bbox_inches="tight")

    summary_file = DATA_DIR / f"benchmark_optimized_vs_tests_{stamp}.json"
    summary_file.write_text(
        json.dumps(
            {
                "timestamp": datetime.now().isoformat(),
                "optimized_json": str(optimized_json),
                "tests_json": str(tests_json),
                "optimized_total_runtime": optimized_total,
                "tests_total_runtime": tests_total,
                "common_modules": common_modules,
                "optimized_runtimes": optimized,
                "tests_runtimes": tests,
            },
            indent=2,
        )
    )

    print(f"Optimized JSON: {optimized_json}")
    print(f"Tests JSON: {tests_json}")
    print(f"Saved comparison figure: {out_file}")
    print(f"Saved comparison data: {summary_file}")

    if args.no_show:
        plt.close()
    else:
        plt.show()


if __name__ == "__main__":
    main()

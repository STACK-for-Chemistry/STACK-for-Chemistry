#!/usr/bin/env python3
"""
Chemistry Library Maxima Module Benchmarker
Runs tests for each module, tracks CAS runtime, and generates visualizations.
"""

import os
import subprocess
import time
import json
from pathlib import Path
from datetime import datetime
import sys

# Try to import matplotlib, with helpful error message if not available
try:
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    print("Error: matplotlib is not installed.")
    print("Install it with: pip install matplotlib numpy")
    sys.exit(1)


class MaximaBenchmark:
    """Manages Maxima module benchmarking and visualization."""
    
    def __init__(self, base_path):
        """Initialize benchmarker with base chemistry library path."""
        self.base_path = Path(base_path)
        self.test_path = self.base_path / "Module Test files"
        self.utilized_path = self.base_path / "Modules" / "Utilized"
        self.results = {}
        self.timestamps = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def find_test_files(self):
        """Discover all test files in module folders."""
        test_files = {}
        
        if not self.test_path.exists():
            print(f"Error: Test path not found: {self.test_path}")
            return test_files
            
        for module_dir in sorted(self.test_path.iterdir()):
            if module_dir.is_dir():
                module_name = module_dir.name
                test_file = module_dir / f"test_{module_name}.txt"
                
                if test_file.exists():
                    test_files[module_name] = test_file
                    print(f"✓ Found: {module_name}")
                else:
                    print(f"✗ Missing: test_{module_name}.txt")
                    
        return test_files
    
    def get_utilized_module(self, module_name):
        """Get path to the corresponding utilized module."""
        # Map test folder names to module files
        module_file = self.utilized_path / f"{module_name}.mac"
        
        if module_file.exists():
            return module_file
        return None
    
    def run_maxima_test(self, test_file):
        """Run a single test file with Maxima and measure runtime."""
        print(f"\n  Running Maxima test: {test_file.name}")
        
        start_time = time.time()
        
        try:
            # Prepare Maxima command to run the test file
            cmd = [
                "maxima",
                "-b", str(test_file),  # Batch mode
                "-q"  # Quiet mode
            ]
            
            # Run Maxima
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120  # 2-minute timeout per test
            )
            
            elapsed_time = time.time() - start_time
            
            if result.returncode == 0:
                print(f"    ✓ Completed in {elapsed_time:.3f}s")
                return {
                    "status": "success",
                    "runtime": elapsed_time,
                    "stdout_lines": len(result.stdout.split('\n')),
                    "stderr_lines": len(result.stderr.split('\n'))
                }
            else:
                print(f"    ✗ Failed with return code {result.returncode}")
                return {
                    "status": "failed",
                    "runtime": elapsed_time,
                    "error": result.stderr[:200]
                }
                
        except subprocess.TimeoutExpired:
            elapsed_time = time.time() - start_time
            print(f"    ✗ Timeout after {elapsed_time:.1f}s")
            return {
                "status": "timeout",
                "runtime": elapsed_time
            }
        except FileNotFoundError:
            print("    ✗ Maxima not found. Is it installed?")
            return {
                "status": "error",
                "error": "Maxima not found in PATH"
            }
        except Exception as e:
            elapsed_time = time.time() - start_time
            print(f"    ✗ Exception: {str(e)}")
            return {
                "status": "error",
                "runtime": elapsed_time,
                "error": str(e)
            }
    
    def benchmark_all_modules(self):
        """Run benchmarks for all discovered modules."""
        print("\n" + "="*70)
        print("CHEMISTRY LIBRARY MAXIMA MODULE BENCHMARK")
        print("="*70)
        
        test_files = self.find_test_files()
        
        if not test_files:
            print("No test files found!")
            return False
        
        print(f"\nFound {len(test_files)} modules to benchmark")
        print("\nStarting benchmarks...")
        
        for module_name, test_file in sorted(test_files.items()):
            print(f"\n[{module_name.upper()}]")
            print(f"  Test file: {test_file}")
            
            # Run the test and capture results
            result = self.run_maxima_test(test_file)
            self.results[module_name] = result
        
        return True
    
    def print_summary(self):
        """Print summary of benchmark results."""
        print("\n" + "="*70)
        print("BENCHMARK SUMMARY")
        print("="*70 + "\n")
        
        successful = []
        failed = []
        
        for module_name, result in sorted(self.results.items()):
            status = result.get("status", "unknown")
            runtime = result.get("runtime", 0)
            
            if status == "success":
                successful.append((module_name, runtime))
                print(f"✓ {module_name:20} {runtime:8.3f}s")
            else:
                failed.append((module_name, status))
                print(f"✗ {module_name:20} {status}")
        
        if successful:
            print(f"\n{'Module':<20} {'Runtime (s)':<12} {'Relative':<10}")
            print("-" * 42)
            
            min_time = min(t for _, t in successful)
            total_time = sum(t for _, t in successful)
            
            for module_name, runtime in sorted(successful, key=lambda x: x[1], reverse=True):
                relative = runtime / min_time if min_time > 0 else 0
                print(f"{module_name:<20} {runtime:>10.3f}   {relative:>8.1f}x")
            
            print("-" * 42)
            print(f"{'Total':<20} {total_time:>10.3f}s")
            print(f"{'Average':<20} {total_time/len(successful):>10.3f}s")
        
        print(f"\nSuccessful: {len(successful)}/{len(self.results)}")
        if failed:
            print(f"Failed: {', '.join(m for m, _ in failed)}")
    
    def save_results(self):
        """Save results to JSON file."""
        output_file = self.base_path / f"benchmark_results_{self.timestamps}.json"
        
        with open(output_file, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "results": self.results
            }, f, indent=2)
        
        print(f"\n✓ Results saved to: {output_file}")
        return output_file
    
    def plot_results(self):
        """Create visualizations of benchmark results."""
        successful = {
            name: result["runtime"]
            for name, result in self.results.items()
            if result.get("status") == "success"
        }
        
        if not successful:
            print("\nNo successful benchmarks to plot")
            return
        
        # Sort by runtime
        sorted_modules = sorted(successful.items(), key=lambda x: x[1], reverse=True)
        modules = [m[0] for m in sorted_modules]
        runtimes = [m[1] for m in sorted_modules]
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Chemistry Library Maxima Module Benchmarks', fontsize=16, fontweight='bold')
        
        # Plot 1: Runtime by module (bar chart)
        ax1 = axes[0, 0]
        colors = plt.cm.viridis(np.linspace(0, 1, len(modules)))
        bars = ax1.barh(modules, runtimes, color=colors)
        ax1.set_xlabel('Runtime (seconds)', fontweight='bold')
        ax1.set_title('Execution Time by Module', fontweight='bold')
        ax1.grid(axis='x', alpha=0.3)
        
        # Add value labels on bars
        for i, (bar, runtime) in enumerate(zip(bars, runtimes)):
            ax1.text(runtime, i, f' {runtime:.3f}s', va='center', fontsize=9)
        
        # Plot 2: Relative runtime (normalized to fastest)
        ax2 = axes[0, 1]
        min_time = min(runtimes)
        relative_times = [t / min_time for t in runtimes]
        bars2 = ax2.barh(modules, relative_times, color=colors)
        ax2.set_xlabel('Relative Runtime (×)', fontweight='bold')
        ax2.set_title('Runtime Relative to Fastest Module', fontweight='bold')
        ax2.grid(axis='x', alpha=0.3)
        ax2.axvline(x=1, color='red', linestyle='--', linewidth=2, alpha=0.5, label='Fastest')
        
        for i, (bar, rel_time) in enumerate(zip(bars2, relative_times)):
            ax2.text(rel_time, i, f' {rel_time:.1f}×', va='center', fontsize=9)
        ax2.legend()
        
        # Plot 3: Pie chart of total runtime
        ax3 = axes[1, 0]
        ax3.pie(runtimes, labels=modules, autopct='%1.1f%%', colors=colors, startangle=90)
        ax3.set_title('Runtime Distribution Across Modules', fontweight='bold')
        
        # Plot 4: Summary statistics
        ax4 = axes[1, 1]
        ax4.axis('off')
        
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
        
        ax4.text(0.05, 0.95, stats_text, transform=ax4.transAxes, 
                fontfamily='monospace', fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        # Save figure
        plot_file = self.base_path / f"benchmark_plot_{self.timestamps}.png"
        plt.tight_layout()
        plt.savefig(plot_file, dpi=150, bbox_inches='tight')
        print(f"✓ Plot saved to: {plot_file}")
        
        # Show plot
        plt.show()
        
        return plot_file


def main():
    """Main entry point."""
    # Get base path
    base_path = Path(__file__).parent
    
    # Create benchmarker
    benchmarker = MaximaBenchmark(base_path)
    
    # Run benchmarks
    if benchmarker.benchmark_all_modules():
        # Print summary
        benchmarker.print_summary()
        
        # Save results
        benchmarker.save_results()
        
        # Create plots
        try:
            benchmarker.plot_results()
        except Exception as e:
            print(f"\nWarning: Could not generate plots: {str(e)}")
            print("Results were still saved to JSON file.")
    else:
        print("Benchmarking failed!")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Individual Module Benchmarker
Run benchmarks for specific modules or get quick performance metrics.
"""

import argparse
import subprocess
import time
from pathlib import Path
import shutil
import sys


class ModuleBenchmark:
    """Simple benchmarking for individual modules."""
    
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.test_path = self.base_path / "Module Test files"

    @staticmethod
    def check_maxima_available():
        """Return True when Maxima executable is available in PATH."""
        return shutil.which("maxima") is not None

    def get_module_test_files(self, module_name):
        """Return all test files for a module, including split test suites."""
        module_dir = self.test_path / module_name
        if not module_dir.exists() or not module_dir.is_dir():
            return []
        return sorted(module_dir.glob(f"test_{module_name}*.txt"))
    
    def list_modules(self):
        """List all available modules."""
        modules = []
        for module_dir in sorted(self.test_path.iterdir()):
            if module_dir.is_dir():
                if self.get_module_test_files(module_dir.name):
                    modules.append(module_dir.name)
        return modules
    
    def benchmark_module(self, module_name, runs=1, verbose=True):
        """Benchmark a specific module multiple times across all its test files."""
        test_files = self.get_module_test_files(module_name)

        if not test_files:
            print(f"Error: No test files found for module '{module_name}'")
            return None
        
        runtimes = []
        
        for run in range(runs):
            if verbose and runs > 1:
                print(f"  Run {run+1}/{runs}...", end=" ", flush=True)
            
            start = time.time()
            
            try:
                for test_file in test_files:
                    result = subprocess.run(
                        ["maxima", "-b", str(test_file), "-q"],
                        capture_output=True,
                        text=True,
                        timeout=120
                    )
                    if result.returncode != 0:
                        if verbose:
                            stderr_snippet = (result.stderr or "").strip()
                            stdout_snippet = (result.stdout or "").strip()
                            details = stderr_snippet or stdout_snippet
                            print(f"\n  Failed in {test_file.name} (exit {result.returncode}).")
                            if details:
                                print(f"  Output: {details[-300:]}")
                        return None
                
                elapsed = time.time() - start
                
                runtimes.append(elapsed)
                if verbose and runs > 1:
                    print(f"{elapsed:.3f}s ✓")
                    
            except subprocess.TimeoutExpired:
                if verbose and runs > 1:
                    print(f"Timeout ✗")
                return None
            except FileNotFoundError:
                if verbose:
                    print("Maxima executable not found in PATH.")
                return None
            except Exception as e:
                if verbose and runs > 1:
                    print(f"Error: {e} ✗")
                return None
        
        return runtimes
    
    def format_result(self, runtimes):
        """Format benchmark results."""
        if not runtimes:
            return None
        
        result = {
            "runs": len(runtimes),
            "min": min(runtimes),
            "max": max(runtimes),
            "avg": sum(runtimes) / len(runtimes)
        }
        
        if len(runtimes) > 1:
            import statistics
            result["median"] = statistics.median(runtimes)
            result["stdev"] = statistics.stdev(runtimes)
        
        return result


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark individual Chemistry Library modules"
    )
    
    parser.add_argument(
        "-m", "--module",
        help="Module to benchmark (e.g., acidbase, thermodynamictables)"
    )
    
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="List all available modules"
    )
    
    parser.add_argument(
        "-r", "--runs",
        type=int,
        default=1,
        help="Number of times to run the benchmark (default: 1)"
    )
    
    parser.add_argument(
        "-a", "--all",
        action="store_true",
        help="Benchmark all modules once"
    )
    
    parser.add_argument(
        "--path",
        default=".",
        help="Path to STACK-for-Chemistry directory (default: current directory)"
    )
    
    args = parser.parse_args()

    if args.runs < 1:
        print("Error: --runs must be at least 1")
        return 1
    
    benchmarker = ModuleBenchmark(args.path)

    if not benchmarker.check_maxima_available():
        print("Error: Maxima is not installed or not in PATH.")
        print("Install Maxima and try again.")
        print("Ubuntu/Debian: sudo apt install maxima")
        print("Windows (winget): winget install MaximaTeam.Maxima")
        return 1
    
    # List modules
    if args.list:
        print("Available modules:")
        for module in benchmarker.list_modules():
            print(f"  - {module}")
        return 0
    
    # Benchmark all modules
    if args.all:
        print("Benchmarking all modules...")
        results = {}
        
        for module in benchmarker.list_modules():
            print(f"\n{module}:")
            times = benchmarker.benchmark_module(module, runs=1)
            
            if times:
                result = benchmarker.format_result(times)
                results[module] = result
                print(f"  Runtime: {result['min']:.3f}s")
            else:
                print(f"  Failed")
        
        # Summary
        print("\n" + "="*50)
        print("SUMMARY")
        print("="*50)
        
        if results:
            sorted_results = sorted(results.items(), key=lambda x: x[1]['min'], reverse=True)
            
            for module, result in sorted_results:
                print(f"{module:20} {result['min']:>8.3f}s")
            
            total_time = sum(r['min'] for r in results.values())
            print("-"*50)
            print(f"{'Total':<20} {total_time:>8.3f}s")
        
        return 0
    
    # Benchmark specific module
    if args.module:
        if args.module not in benchmarker.list_modules():
            print(f"Error: Module '{args.module}' not found")
            print("Use -l/--list to see available modules")
            return 1
        
        print(f"Benchmarking module: {args.module}")
        print(f"Number of runs: {args.runs}")
        print()
        
        runtimes = benchmarker.benchmark_module(args.module, runs=args.runs)
        
        if not runtimes:
            print("Benchmarking failed!")
            return 1
        
        result = benchmarker.format_result(runtimes)
        
        print("\nResults:")
        print("-"*50)
        print(f"  Min:     {result['min']:.4f}s")
        print(f"  Max:     {result['max']:.4f}s")
        print(f"  Average: {result['avg']:.4f}s")
        
        if 'median' in result:
            print(f"  Median:  {result['median']:.4f}s")
        if 'stdev' in result:
            print(f"  Std Dev: {result['stdev']:.4f}s")
        
        print("-"*50)
        print(f"  Total time: {sum(runtimes):.3f}s")
        
        return 0
    
    # No action specified
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())

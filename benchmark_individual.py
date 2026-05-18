#!/usr/bin/env python3
"""
Individual Module Benchmarker
Run benchmarks for specific modules or get quick performance metrics.
"""

import argparse
import subprocess
import time
from pathlib import Path
from datetime import datetime
import sys


class ModuleBenchmark:
    """Simple benchmarking for individual modules."""
    
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.test_path = self.base_path / "Module Test files"
    
    def list_modules(self):
        """List all available modules."""
        modules = []
        for module_dir in sorted(self.test_path.iterdir()):
            if module_dir.is_dir():
                test_file = module_dir / f"test_{module_dir.name}.txt"
                if test_file.exists():
                    modules.append(module_dir.name)
        return modules
    
    def benchmark_module(self, module_name, runs=1, verbose=True):
        """Benchmark a specific module multiple times."""
        test_file = self.test_path / module_name / f"test_{module_name}.txt"
        
        if not test_file.exists():
            print(f"Error: Test file not found: {test_file}")
            return None
        
        runtimes = []
        
        for run in range(runs):
            if verbose and runs > 1:
                print(f"  Run {run+1}/{runs}...", end=" ", flush=True)
            
            start = time.time()
            
            try:
                result = subprocess.run(
                    ["maxima", "-b", str(test_file), "-q"],
                    capture_output=True,
                    timeout=120
                )
                
                elapsed = time.time() - start
                
                if result.returncode == 0:
                    runtimes.append(elapsed)
                    if verbose and runs > 1:
                        print(f"{elapsed:.3f}s ✓")
                else:
                    if verbose and runs > 1:
                        print(f"Failed ✗")
                    return None
                    
            except subprocess.TimeoutExpired:
                if verbose and runs > 1:
                    print(f"Timeout ✗")
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
    
    benchmarker = ModuleBenchmark(args.path)
    
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

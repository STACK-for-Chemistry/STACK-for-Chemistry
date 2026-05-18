# Chemistry Library Module Benchmarker

A comprehensive benchmarking tool that automatically runs all Maxima module tests, measures their execution time, and generates detailed performance visualizations.

## Features

- ✅ **Automatic Module Discovery** — Finds and runs all test files in the Module Test files directory
- ✅ **Precise Runtime Tracking** — Measures CAS execution time down to milliseconds
- ✅ **Multi-format Output** — Saves results as JSON and generates PNG plots
- ✅ **Comprehensive Visualizations** — 4-panel dashboard with runtime comparisons, relative performance, distribution, and statistics
- ✅ **Detailed Logging** — Shows progress and status for each module
- ✅ **Error Handling** — Graceful handling of timeouts, missing files, and Maxima failures

## Requirements

### System Requirements

1. **Python 3.6+**
   ```bash
   python --version
   ```

2. **Maxima** (any recent version)
   - Installation: [Maxima Official Site](https://maxima.sourceforge.io/)
   - Verify: `maxima --version`

3. **Python Packages**
   - matplotlib
   - numpy
   
   Install with:
   ```bash
   pip install matplotlib numpy
   ```

## Usage

### Option 1: PowerShell Script (Recommended)

The easiest way on Windows:

```powershell
cd c:\STACK\STACK-for-Chemistry
.\run_benchmark.ps1
```

The script will:
- Check for Python installation
- Install missing dependencies
- Verify Maxima is available
- Run the full benchmark suite
- Generate visualizations

### Option 2: Direct Python Execution

```bash
cd c:\STACK\STACK-for-Chemistry
python benchmark_modules.py
```

### Option 3: From Python Code

```python
from benchmark_modules import MaximaBenchmark
from pathlib import Path

base_path = Path("c:/STACK/STACK-for-Chemistry")
benchmarker = MaximaBenchmark(base_path)

# Run all benchmarks
benchmarker.benchmark_all_modules()

# Print summary
benchmarker.print_summary()

# Save results and generate plots
benchmarker.save_results()
benchmarker.plot_results()
```

## Output Files

The benchmarker generates the following output files in the STACK-for-Chemistry directory:

### JSON Results File
**Filename:** `benchmark_results_YYYYMMDD_HHMMSS.json`

Contains structured data for programmatic use:
```json
{
  "timestamp": "2026-05-18T14:30:45.123456",
  "results": {
    "acidbase": {
      "status": "success",
      "runtime": 2.345,
      "stdout_lines": 150,
      "stderr_lines": 0
    },
    ...
  }
}
```

### PNG Visualization File
**Filename:** `benchmark_plot_YYYYMMDD_HHMMSS.png`

Contains 4 subplots:
1. **Execution Time by Module** (horizontal bar chart)
   - Shows absolute runtime for each module
   - Color-coded for easy comparison

2. **Runtime Relative to Fastest Module** (relative performance)
   - Shows how much slower each module is compared to the fastest
   - Helps identify performance outliers

3. **Runtime Distribution** (pie chart)
   - Shows what percentage of total time each module uses
   - Useful for identifying bottlenecks

4. **Summary Statistics Box**
   - Total time, averages, medians
   - Fastest/slowest modules
   - Standard deviation
   - Timestamp of benchmark run

## Console Output Example

```
======================================================================
CHEMISTRY LIBRARY MAXIMA MODULE BENCHMARK
======================================================================

Found 8 modules to benchmark

Starting benchmarks...

[ACIDBASE]
  Test file: c:\STACK\STACK-for-Chemistry\Module Test files\acidbase\test_acidbase.txt
  Running Maxima test: test_acidbase.txt
    ✓ Completed in 2.345s

[ELECTROCHEMISTRY]
  Test file: c:\STACK\STACK-for-Chemistry\Module Test files\electrochemistry\test_electrochemistry.txt
  Running Maxima test: test_electrochemistry.txt
    ✓ Completed in 1.234s

...

======================================================================
BENCHMARK SUMMARY
======================================================================

✓ thermodynamictables    3.456s
✓ acidbase               2.345s
✓ solubility             2.123s
✓ nuclidetable           1.987s
✓ reactions              1.876s
✓ numericops             1.234s
✓ electrochemistry       1.123s
✓ pse_masses             0.876s

Module               Runtime (s)    Relative
--------------------------------------------
thermodynamictables      3.456         3.9x
acidbase                 2.345         2.7x
...
thermodynamictables     19.654s
Average                  2.457s

Successful: 8/8

✓ Results saved to: benchmark_results_20260518_143045.json
✓ Plot saved to: benchmark_plot_20260518_143045.png
```

## Modules Benchmarked

The tool automatically discovers and benchmarks:

1. **acidbase** - Acid-base equilibrium calculations
2. **electrochemistry** - Electrochemistry functions
3. **nuclidetable** - Nuclide database access
4. **numericops** - Numeric operations (significant figures, decimal places)
5. **pse_masses** - Periodic table and molar mass calculations
6. **reactions** - Chemical reaction data
7. **solubility** - Solubility equilibrium calculations
8. **thermodynamictables** - Thermodynamic data retrieval

## Interpreting Results

### Runtime Interpretation

- **< 1 second** — Excellent, minimal overhead
- **1-2 seconds** — Very good, acceptable for interactive use
- **2-5 seconds** — Good, reasonable for batch processing
- **> 5 seconds** — Consider optimization opportunities

### Relative Performance

- **1-2x** — Module loads quickly relative to fastest
- **2-5x** — Module has moderate overhead
- **> 5x** — Module may benefit from optimization

## Troubleshooting

### "Maxima not found in PATH"

**Solution:** Ensure Maxima is installed and the installation directory is in your system PATH.

**Windows:**
1. Add Maxima bin directory to PATH environment variable
2. Restart terminal/PowerShell
3. Verify: `maxima --version`

### "matplotlib is not installed"

**Solution:** Install with pip:
```bash
pip install matplotlib numpy
```

### "Timeout after X seconds"

The script has a 2-minute timeout per test. If a module exceeds this, it's marked as failed.
- Check if your system is under heavy load
- Verify Maxima is working: `maxima -q -b test_file.txt`

### No plots generated

If plotting fails but results are saved as JSON:
- Verify matplotlib installation
- Check disk space
- Try running again without other applications

## Performance Optimization

If you notice slow modules, you can:

1. **Check Maxima performance:**
   ```bash
   time maxima -q -b test_module.txt
   ```

2. **Profile individual functions** in the test file

3. **Check system resources:**
   - CPU usage during testing
   - Available RAM
   - Disk I/O

4. **Optimize database queries** in slow modules

## Advanced Usage

### Custom Timeout

Edit `benchmark_modules.py`, line ~117:
```python
timeout=120  # Change 120 to desired seconds
```

### Filter Specific Modules

Edit the script's main function to skip modules:
```python
skip_modules = ["electrochemistry", "reactions"]
test_files = {k: v for k, v in test_files.items() if k not in skip_modules}
```

### Export Results to CSV

After running benchmarks:
```python
import json
import csv

with open("benchmark_results_*.json") as f:
    data = json.load(f)

with open("benchmark_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Module", "Status", "Runtime (s)"])
    for module, result in data["results"].items():
        writer.writerow([module, result["status"], result.get("runtime", "N/A")])
```

## Contributing

To add benchmarking for new modules:

1. Add test file to `Module Test files/{module_name}/test_{module_name}.txt`
2. Run benchmarker — it will automatically discover the new module
3. Results will be included in visualizations and JSON output

## License

Same as the STACK-for-Chemistry project

## Contact

For issues or improvements, see the main STACK-for-Chemistry repository.

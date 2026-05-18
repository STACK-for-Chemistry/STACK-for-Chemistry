# Chemistry Library Module Benchmarker
# Run this script to benchmark all Maxima modules and generate performance plots

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Chemistry Library Module Benchmarker" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "`n✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "`n✗ Python not found. Please install Python 3.6+" -ForegroundColor Red
    exit 1
}

# Check if matplotlib is installed
Write-Host "`nChecking dependencies..."
try {
    python -c "import matplotlib; import numpy" 2>&1 | Out-Null
    Write-Host "✓ matplotlib and numpy are installed" -ForegroundColor Green
} catch {
    Write-Host "`n⚠ matplotlib/numpy not installed. Installing..." -ForegroundColor Yellow
    python -m pip install matplotlib numpy
}

# Check if Maxima is installed
Write-Host "`nChecking Maxima installation..."
try {
    maxima --version 2>&1 | Out-Null
    Write-Host "✓ Maxima found" -ForegroundColor Green
} catch {
    Write-Host "`n✗ Maxima not found. Please ensure Maxima is installed and in your PATH" -ForegroundColor Red
    exit 1
}

# Run the benchmark
Write-Host "`n" 
Write-Host "Starting benchmarks..." -ForegroundColor Yellow
Write-Host "This may take a few minutes depending on your system.`n"

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$benchmarkScript = Join-Path $scriptPath "benchmark_modules.py"

python $benchmarkScript

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✓ Benchmarking completed successfully!" -ForegroundColor Green
} else {
    Write-Host "`n✗ Benchmarking failed with exit code $LASTEXITCODE" -ForegroundColor Red
    exit 1
}

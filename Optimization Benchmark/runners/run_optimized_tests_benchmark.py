#!/usr/bin/env python3
"""Launcher for optimized test module benchmark."""

import runpy
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "benchmark_optimized_tests.py"

runpy.run_path(str(SCRIPT), run_name="__main__")

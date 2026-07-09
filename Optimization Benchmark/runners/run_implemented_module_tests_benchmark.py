#!/usr/bin/env python3
"""Launcher for implemented module test benchmark."""

import runpy
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "benchmark_implemented_module_tests.py"

runpy.run_path(str(SCRIPT), run_name="__main__")

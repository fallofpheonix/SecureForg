#!/usr/bin/env python3
"""
Sentinel-Scribe CLI
Main entry point for the system.
"""

import sys
import argparse
import json
from pathlib import Path
from pipeline import SentinelScribePipeline
from llm import get_llm


def load_file(path: str) -> str:
    """Load file content."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Error loading file {path}: {e}")
        sys.exit(1)


def load_files_from_dir(directory: str) -> dict:
    """Load all Python files from directory."""
    files = {}
    path = Path(directory)
    
    for py_file in path.glob("*.py"):
        with open(py_file, 'r') as f:
            files[py_file.name] = f.read()
    
    return files


def main():
    parser = argparse.ArgumentParser(
        description="Sentinel-Scribe: Offline Adversarial Reasoning Engine"
    )
    
    parser.add_argument(
        "--file", "-f",
        help="Single Python file to analyze"
    )
    
    parser.add_argument(
        "--dir", "-d",
        help="Directory of Python files to analyze"
    )
    
    parser.add_argument(
        "--instruction", "-i",
        help="Custom analysis instruction"
    )
    
    parser.add_argument(
        "--check-ollama",
        action="store_true",
        help="Check if Ollama is available"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="Save report to JSON file"
    )
    
    args = parser.parse_args()
    
    # Check Ollama
    if args.check_ollama:
        llm = get_llm()
        if llm.is_available():
            print("✓ Ollama is available")
            sys.exit(0)
        else:
            print("✗ Ollama is not available")
            print("Start Ollama with: ollama serve")
            sys.exit(1)
    
    # Load files
    files = {}
    
    if args.file:
        files = {Path(args.file).name: load_file(args.file)}
    elif args.dir:
        files = load_files_from_dir(args.dir)
    else:
        parser.print_help()
        sys.exit(1)
    
    if not files:
        print("No Python files found")
        sys.exit(1)
    
    print(f"Loaded {len(files)} file(s)")
    
    # Run pipeline
    print("\nStarting Sentinel-Scribe analysis...\n")
    
    pipeline = SentinelScribePipeline()
    report = pipeline.run_full_pipeline(files, args.instruction)
    
    # Print report
    pipeline.print_report()
    
    # Save report if requested
    if args.output:
        try:
            with open(args.output, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"Report saved to {args.output}")
        except Exception as e:
            print(f"Error saving report: {e}")
    
    return 0 if report.get("status") == "complete" else 1


if __name__ == "__main__":
    sys.exit(main())

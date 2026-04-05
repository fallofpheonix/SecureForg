import argparse
import sys
import os

# Add root folder to sys.path since we're in app/
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline import run_pipeline
import json


def read_code_file(path: str) -> str:
    with open(path, "r") as handle:
        return handle.read()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to Python file to analyze")
    parser.add_argument("--patched-file", help="Path to manually patched Python file for re-execution validation")

    args = parser.parse_args()

    try:
        code = read_code_file(args.file)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    patched_code = None
    if args.patched_file:
        try:
            patched_code = read_code_file(args.patched_file)
        except Exception as e:
            print(f"Error reading patched file: {e}")
            sys.exit(1)

    result = run_pipeline(code, patched_code=patched_code)

    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()

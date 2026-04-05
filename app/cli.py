import argparse
import sys
import os

# Add root folder to sys.path since we're in app/
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline import run_pipeline
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to Python file to analyze")

    args = parser.parse_args()

    try:
        with open(args.file, "r") as f:
            code = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    result = run_pipeline(code)

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()

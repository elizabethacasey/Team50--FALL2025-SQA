"""
Small demo to prove Avery's forensic logging works.
Creates a tiny fake results CSV and calls some decorated functions.
"""

import os
import pandas as pd

from frequency import reportProportion, reportEventDensity
from report import reportProp, reportDensity


def make_dummy_files(out_dir: str):
    """
    Create a few tiny Python files so getAllSLOC() has real paths to read.
    Returns their full paths.
    """
    os.makedirs(out_dir, exist_ok=True)

    file_paths = []
    for name in ["file1.py", "file2.py", "file3.py"]:
        full_path = os.path.join(out_dir, name)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write("# dummy file used for forensic demo\nprint('hello from', {!r})\n".format(name))
        file_paths.append(full_path)

    return file_paths  


def make_dummy_csv(path: str):
    """
    Create a tiny CSV with the columns expected by the scripts.
    FILE_FULL_PATH will point to the dummy .py files we just created.
    """
    out_dir = os.path.dirname(path)
    file1, file2, file3 = make_dummy_files(out_dir)

    data = {
        "REPO_FULL_PATH": ["repo1", "repo1", "repo2"],
        "FILE_FULL_PATH": [file1, file2, file3],
        "DATA_LOAD_COUNT": [1, 0, 2],
        "MODEL_LOAD_COUNT": [0, 1, 0],
        "DATA_DOWNLOAD_COUNT": [0, 0, 1],
        "MODEL_LABEL_COUNT": [0, 0, 0],
        "MODEL_OUTPUT_COUNT": [1, 0, 0],
        "DATA_PIPELINE_COUNT": [0, 1, 0],
        "ENVIRONMENT_COUNT": [0, 0, 1],
        "STATE_OBSERVE_COUNT": [0, 0, 0],
        "TOTAL_EVENT_COUNT": [2, 2, 4],
        "CATEGORY": ["DATA_LOAD_COUNT", "MODEL_LOAD_COUNT", "TOTAL_EVENT_COUNT"],
        "PROP_VAL": [50.0, 33.3, 66.7],
        "EVENT_DENSITY": [0.5, 0.3, 0.8],
    }

    df = pd.DataFrame(data)
    df.to_csv(path, index=False)
    print(f"Dummy CSV written to: {path}")


def main():
    out_dir = "demo_outputs"
    os.makedirs(out_dir, exist_ok=True)

    dummy_results = os.path.join(out_dir, "dummy_results.csv")
    prop_csv = os.path.join(out_dir, "dummy_prop.csv")
    density_csv = os.path.join(out_dir, "dummy_density.csv")

    make_dummy_csv(dummy_results)

    print("\n=== Calling frequency.reportProportion ===")
    reportProportion(dummy_results, prop_csv)

    print("\n=== Calling frequency.reportEventDensity ===")
    reportEventDensity(dummy_results, density_csv)

    print("\n=== Calling report.reportProp ===")
    reportProp(prop_csv)

    print("\n=== Calling report.reportDensity ===")
    reportDensity(density_csv)

    print("\nDone. Check 'forensics.log' in the repo root to see logged events.")


if __name__ == "__main__":
    main()

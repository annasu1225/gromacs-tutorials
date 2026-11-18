#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt


def read_xvg_columns(path: Path, x_col: int, y_col: int) -> tuple[list[float], list[float]]:
    """Read 1-based columns from a GROMACS XVG file, skipping comments/meta lines."""
    xs: list[float] = []
    ys: list[float] = []

    # Convert 1-based input columns to 0-based indices.
    x_idx = x_col - 1
    y_idx = y_col - 1

    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or stripped.startswith("@"):
                continue

            parts = stripped.split()
            if len(parts) <= max(x_idx, y_idx):
                continue

            try:
                x_val = float(parts[x_idx])
                y_val = float(parts[y_idx])
            except ValueError:
                continue

            xs.append(x_val)
            ys.append(y_val)

    return xs, ys


def main() -> int:
    base_dir = Path(__file__).resolve().parent

    fast_file = base_dir / "pullf.xvg"
    slow_file = base_dir / "pullf_slow.xvg"

    if not fast_file.exists():
        print(f"Missing input file: {fast_file.name}")
        return 1
    if not slow_file.exists():
        print(f"Missing input file: {slow_file.name}")
        return 1

    # Equivalent to:
    # xmgrace -block pullf.xvg -bxy 1:2 -bxy 1:3 -block pullf_slow.xvg -bxy 1:2 -bxy 1:3
    series_specs = [
        (fast_file, 2, "pullf.xvg col2"),
        (fast_file, 3, "pullf.xvg col3"),
        (slow_file, 2, "pullf_slow.xvg col2"),
        (slow_file, 3, "pullf_slow.xvg col3"),
    ]

    plt.figure(figsize=(10, 6), dpi=150)

    for file_path, y_col, label in series_specs:
        x_vals, y_vals = read_xvg_columns(file_path, x_col=1, y_col=y_col)
        if not x_vals:
            print(f"No valid data for {label}; skipping.")
            continue
        plt.plot(x_vals, y_vals, linewidth=1.5, label=label)

    plt.xlabel("Column 1")
    plt.ylabel("Force")
    plt.title("Force Profiles: pullf.xvg and pullf_slow.xvg")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    out_path = base_dir / "pullf_profiles_compare_velocities.png"
    plt.savefig(out_path)
    plt.close()

    print(f"Saved {out_path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def parse_xvg(path: Path):
    """Return (title, x_label, y_label, series) for a GROMACS .xvg file."""
    title = path.stem.replace("_", " ").title()
    x_label = "Time"
    y_label = "Value"
    rows = []

    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("#"):
                continue
            if stripped.startswith("@"):
                lowered = stripped.lower()
                if "title" in lowered and '"' in stripped:
                    try:
                        title = stripped.split('"')[1]
                    except IndexError:
                        pass
                elif "xaxis" in lowered and "label" in lowered and '"' in stripped:
                    try:
                        x_label = stripped.split('"')[1]
                    except IndexError:
                        pass
                elif "yaxis" in lowered and "label" in lowered and '"' in stripped:
                    try:
                        y_label = stripped.split('"')[1]
                    except IndexError:
                        pass
                continue

            parts = stripped.split()
            if len(parts) < 2:
                continue

            try:
                values = [float(value) for value in parts]
            except ValueError:
                continue

            rows.append(values)

    if not rows:
        return None

    series = []
    max_cols = max(len(row) for row in rows)
    for col_index in range(1, max_cols):
        xs = []
        ys = []
        valid = True
        for row in rows:
            if len(row) <= col_index:
                valid = False
                break
            xs.append(row[0])
            ys.append(row[col_index])
        if valid and xs and ys:
            series.append((xs, ys))

    if not series:
        series = [([row[0] for row in rows], [row[1] for row in rows])]

    if len(series) == 1:
        return title, x_label, y_label, series

    return title, x_label, y_label, series


def render_series(path: Path):
    parsed = parse_xvg(path)
    if parsed is None:
        print(f"Skipping {path.name}: no valid numeric data found.")
        return

    title, x_label, y_label, series = parsed
    fig, ax = plt.subplots(figsize=(9, 6), dpi=300, constrained_layout=True)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    palette = [
        "#1f77b4", "#d62728", "#2ca02c", "#ff7f0e", "#9467bd",
        "#17becf", "#bcbd22", "#8c564b", "#e377c2", "#7f7f7f"
    ]

    for index, (xs, ys) in enumerate(series):
        color = palette[index % len(palette)]
        ax.plot(xs, ys, lw=2.2, color=color, label=f"Series {index + 1}" if len(series) > 1 else None)

    ax.set_title(title, fontsize=14, pad=10)
    ax.set_xlabel(x_label, fontsize=12)
    ax.set_ylabel(y_label, fontsize=12)
    ax.grid(True, which="major", linestyle="-", linewidth=0.7, alpha=0.35)
    ax.tick_params(labelsize=10)

    for spine in ax.spines.values():
        spine.set_linewidth(1.0)
        spine.set_color("#303030")

    if len(series) > 1:
        ax.legend(frameon=True, framealpha=0.9, fancybox=False, edgecolor="#d0d0d0")

    out_path = path.with_suffix(".png")
    fig.savefig(out_path, format="png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved {out_path.name}")


def main():
    directory = Path(__file__).resolve().parent
    xvg_files = sorted(directory.glob("*.xvg"))
    if not xvg_files:
        print(f"No .xvg files found in {directory}")
        return 1

    for xvg_file in xvg_files:
        render_series(xvg_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

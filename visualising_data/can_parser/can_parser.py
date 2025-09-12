import re
import sys
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go

# -------------------------------------------------------------
# Helpers
# -------------------------------------------------------------
def parse_start_time(line: str):
    """Parse line with 'Start time' and return datetime."""
    m = re.search(
        r"Start time:\s*([0-3]?\d\.[01]?\d\.\d{4})\s+([0-2]?\d:[0-5]\d:[0-5]\d(?:\.\d+)?)",
        line,
    )
    if not m:
        return None
    date_part, time_part = m.group(1), m.group(2)
    fmt = "%d.%m.%Y %H:%M:%S.%f" if "." in time_part else "%d.%m.%Y %H:%M:%S"
    return datetime.strptime(f"{date_part} {time_part}", fmt)


def signed_24_from_bytes(msb, mid, lsb):
    """Convert 3 bytes to signed 24-bit integer with sign extension."""
    v = (msb << 16) | (mid << 8) | lsb
    if v & 0x800000:  # if sign bit set
        v |= 0xFF000000
        if v >= 1 << 31:
            v = v - (1 << 32)
    return v


def parse_trc_file(path: str):
    """Parse Vector .trc file and return DataFrame."""
    rows = []
    start_time = None

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for ln in f:
            if "Start time" in ln and start_time is None:
                start_time = parse_start_time(ln)
                continue

            toks = ln.strip().split()
            if len(toks) < 6:
                continue

            # Find numeric time offset
            time_idx = None
            for i, t in enumerate(toks):
                if re.match(r"^\d+(\.\d+)?$", t):
                    time_idx = i
                    break
            if time_idx is None or len(toks) <= time_idx + 3:
                continue

            try:
                raw_time_ms = float(toks[time_idx])  # ms
                can_id = toks[time_idx + 2].upper()
                length = int(toks[time_idx + 3])
            except Exception:
                continue

            bytes_tokens = toks[time_idx + 4 : time_idx + 4 + length]
            if not all(re.match(r"^[0-9A-Fa-f]{2}$", b) for b in bytes_tokens):
                continue
            b = [int(bt, 16) for bt in bytes_tokens]
            b = b + [0] * (8 - len(b))  # pad to 8

            # Compute timestamp
            offset_seconds = raw_time_ms / 1000.0
            timestamp = start_time + timedelta(seconds=offset_seconds) if start_time else None

            # Decode values
            tns = signed_24_from_bytes(b[3], b[2], b[1])
            tnscal = signed_24_from_bytes(b[6], b[5], b[4])

            rows.append(
                {
                    "timestamp": timestamp,
                    "offset_s": offset_seconds,
                    "can_id": can_id,
                    "bytes": " ".join(f"{x:02X}" for x in b),
                    "tns_g": tns,
                    "tnscal_g": tnscal,
                    "tnscal_kg": tnscal / 1000.0,
                }
            )

    return pd.DataFrame(rows)


def plot_can(df: pd.DataFrame, out_html: str):
    """Plot CAN data with Plotly."""
    fig = go.Figure()

    for can_id, g in df.groupby("can_id"):
        fig.add_trace(
            go.Scatter(
                x=g["timestamp"],
                y=g["tnscal_kg"],
                mode="lines+markers",
                connectgaps=False,
                name=f"{can_id} - tnscal (kg)",
                yaxis="y2",
            )
        )

    fig.update_layout(
        title="CAN Data",
        xaxis_title="Time",
        yaxis2=dict(title="tnscal (kg)", overlaying="y", side="right"),
        legend=dict(orientation="h"),
    )

    fig.write_html(out_html, include_plotlyjs="cdn")
    print(f"Plot saved to {out_html}")


# -------------------------------------------------------------
# Main
# -------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python can_parser.py file1.trc [file2.trc ...]")
        sys.exit(1)

    all_df = []
    for path in sys.argv[1:]:
        df = parse_trc_file(path)
        print(f"Parsed {len(df)} rows from {path}")
        all_df.append(df)

    df_all = pd.concat(all_df, ignore_index=True)

    # Save to CSV
    df_all = df_all.sort_values("timestamp") # new line
    df_all.to_csv("can_data.csv", index=False)
    print("CSV saved to can_data.csv")

    # Save plot
    plot_can(df_all, "can_plot.html")

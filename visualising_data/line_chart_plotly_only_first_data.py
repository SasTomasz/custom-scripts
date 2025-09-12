import re
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Path to your log file
log_file = r"D:\PROJEKTY\Wagi\DEKO\Testy\Testy wpływu temperatury\Piwnica\test-13.txt"

# Regex to extract timestamp and weights
pattern = re.compile(r"(\d{2}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \| ST0=\[(.*)kg, (.*)kg\]")

records = []
with open(log_file, "r") as f:
    for line in f:
        m = pattern.search(line)
        if m:
            timestamp = datetime.strptime(m.group(1), "%y-%m-%d %H:%M:%S")
            w1 = float(m.group(2))
            w2 = float(m.group(3))
            records.append([timestamp, w1, w2])

# Create DataFrame
df = pd.DataFrame(records, columns=["timestamp", "weight1", "weight2"])

# Classification thresholds
def classify(w):
    if w < 100:
        return "min"
    elif 1000 < w < 1112:
        return "max"
    else:
        return None

def keep_first_of_blocks(data_frame, col):
    """
    Keep only the first row of consecutive blocks where `col` is not NaN.
    """
    mask = data_frame[col].notna()
    block_change = mask & ~mask.shift(fill_value=False)  # True when block starts
    return data_frame[block_change][["timestamp", col]]

# Split into four columns
df["max_weight_1"] = df.apply(lambda row: row["weight1"] if classify(row["weight1"])=="max" else None, axis=1)
df["max_weight_2"] = df.apply(lambda row: row["weight2"] if classify(row["weight2"])=="max" else None, axis=1)
df["min_weight_1"] = df.apply(lambda row: row["weight1"] if classify(row["weight1"])=="min" else None, axis=1)
df["min_weight_2"] = df.apply(lambda row: row["weight2"] if classify(row["weight2"])=="min" else None, axis=1)

# Example for your four series
max1 = keep_first_of_blocks(df, "max_weight_1")
max2 = keep_first_of_blocks(df, "max_weight_2")
min1 = keep_first_of_blocks(df, "min_weight_1")
min2 = keep_first_of_blocks(df, "min_weight_2")

# --- Plot with Plotly ---
fig = go.Figure()

# Max weights
fig.add_trace(go.Scatter(x=max1["timestamp"], y=max1["max_weight_1"], mode="lines+markers", name="max"))
fig.add_trace(go.Scatter(x=max2["timestamp"], y=max2["max_weight_2"], mode="lines+markers", name="max [compens.]"))

# Min weights
fig.add_trace(go.Scatter(x=min1["timestamp"], y=min1["min_weight_1"], mode="lines+markers", name="min"))
fig.add_trace(go.Scatter(x=min2["timestamp"], y=min2["min_weight_2"], mode="lines+markers", name="min [compens.]"))

# Layout
fig.update_layout(
    title="Zmiany min i max wagi w czasie",
    xaxis_title="Data i godzina",
    yaxis_title="Zmierzona waga (kg)",
    hovermode="x unified"  # show all values at the same timestamp
)

# Set custom y-axis range for min weights (~0 kg) if you like
# Example: zoom on min weights separately by using two y-axes or subplots
# fig.show()
fig.write_html("test-13_simplify.html")

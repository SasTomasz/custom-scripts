import re
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Path to your log file
log_file = "data.txt"

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
df.set_index("timestamp", inplace=True)

# Classification thresholds
def classify(w):
    if w < 100:
        return "min"
    elif w > 1000:
        return "max"
    else:
        return None

# Split into four columns
df["max_weight_1"] = df.apply(lambda row: row["weight1"] if classify(row["weight1"])=="max" else None, axis=1)
df["max_weight_2"] = df.apply(lambda row: row["weight2"] if classify(row["weight2"])=="max" else None, axis=1)
df["min_weight_1"] = df.apply(lambda row: row["weight1"] if classify(row["weight1"])=="min" else None, axis=1)
df["min_weight_2"] = df.apply(lambda row: row["weight2"] if classify(row["weight2"])=="min" else None, axis=1)

# ---- Plotting ----
fig, axes = plt.subplots(2, 1, figsize=(12,8), sharex=True)

# Max weights (~1111 kg)
line_max1, = axes[0].plot(df.index, df["max_weight_1"], label="max_bez_kompensacji", marker="o")
line_max2, = axes[0].plot(df.index, df["max_weight_2"], label="max_z_kompensacją", marker="o")
axes[0].set_ylabel("Waga (kg)")
axes[0].set_title("Maksymalna waga (~1111 kg)")
leg0 = axes[0].legend()
axes[0].grid(True)

# Min weights (~0 kg)
line_min1, = axes[1].plot(df.index, df["min_weight_1"], label="min_bez_kompensacji", marker="x")
line_min2, = axes[1].plot(df.index, df["min_weight_2"], label="min_z_kompensacją", marker="x")
axes[1].set_xlabel("Czas badania")
axes[1].set_ylabel("Waga (kg)")
axes[1].set_title("Waga minimalna (~0 kg)")
axes[1].set_ylim(0.00, 0.10)
leg1 = axes[1].legend()
axes[1].grid(True)

# --- Make legends clickable ---
def make_legend_pickable(legend, lines):
    for legline, origline in zip(legend.get_lines(), lines):
        legline.set_picker(True)   # make legend line clickable
        legline.set_pickradius(5)  # click tolerance
        legline._associated_line = origline

def on_pick(event):
    legline = event.artist
    origline = legline._associated_line
    vis = not origline.get_visible()
    origline.set_visible(vis)
    legline.set_alpha(1.0 if vis else 0.2)  # fade legend entry if hidden
    fig.canvas.draw()

make_legend_pickable(leg0, [line_max1, line_max2])
make_legend_pickable(leg1, [line_min1, line_min2])
fig.canvas.mpl_connect("pick_event", on_pick)

plt.tight_layout()
plt.show()

import re
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Path to your log file
log_file = "data.txt"

# Regex to extract fields
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

df = pd.DataFrame(records, columns=["timestamp", "weight1", "weight2"])
df.set_index("timestamp", inplace=True)

# Define threshold
def classify(w):
    if w < 100:
        return "min"
    elif w > 1110:
        return "max"
    else:
        return None

# Create separate columns
df["max_weight_1"] = df.apply(lambda row: row["weight1"] if classify(row["weight1"])=="max" else None, axis=1)
df["max_weight_2"] = df.apply(lambda row: row["weight2"] if classify(row["weight2"])=="max" else None, axis=1)
df["min_weight_1"] = df.apply(lambda row: row["weight1"] if classify(row["weight1"])=="min" else None, axis=1)
df["min_weight_2"] = df.apply(lambda row: row["weight2"] if classify(row["weight2"])=="min" else None, axis=1)

print(df)

# Plot
plt.figure(figsize=(12,6))
plt.plot(df.index, df["max_weight_1"], label="max_weight_1", marker="o")
plt.plot(df.index, df["max_weight_2"], label="max_weight_2", marker="o")
plt.plot(df.index, df["min_weight_1"], label="min_weight_1", marker="x")
plt.plot(df.index, df["min_weight_2"], label="min_weight_2", marker="x")

plt.xlabel("Time")
plt.ylabel("Weight (kg)")
plt.title("Min & Max Weights over Time")
plt.legend()
plt.grid(True)
plt.show()

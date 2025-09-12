import pandas as pd
import plotly.graph_objects as go


# Load your CSV file
df = pd.read_csv("filtered_0100.csv", parse_dates=["timestamp"])

df.set_index("timestamp", inplace=True)

# Classification thresholds
def classify(w):
    if w < 100:
        return "min"
    elif 1050 < w < 1112:
        return "max"
    else:
        return None

# Split into four columns
df["max_weight_1"] = df.apply(lambda row: row["tnscal_kg"] if classify(row["tnscal_kg"])=="max" else None, axis=1)
df["min_weight_1"] = df.apply(lambda row: row["tnscal_kg"] if classify(row["tnscal_kg"])=="min" else None, axis=1)

# --- Plot with Plotly ---
fig = go.Figure()

# Max weights
fig.add_trace(go.Scatter(x=df.index, y=df["max_weight_1"], mode="lines+markers", name="max"))

# Min weights
fig.add_trace(go.Scatter(x=df.index, y=df["min_weight_1"], mode="lines+markers", name="min"))

# Layout
fig.update_layout(
    title="Zmiany min i max wagi w czasie - CAN",
    xaxis_title="Data i godzina",
    yaxis_title="Zmierzona waga (kg)",
    hovermode="x unified"  # show all values at the same timestamp
)

# Set custom y-axis range for min weights (~0 kg) if you like
# Example: zoom on min weights separately by using two y-axes or subplots
# fig.show()
fig.write_html("CAN-01.html")

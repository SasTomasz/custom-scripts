import pandas as pd
from visualising_data.can_parser.can_parser import plot_can


# Load your CSV file
df = pd.read_csv("filtered_0100.csv", parse_dates=["timestamp"])
plot_can(df, "filtered_can.html")
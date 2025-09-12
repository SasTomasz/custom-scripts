import pandas as pd

df = pd.read_csv("can_data.csv", parse_dates=["timestamp"])

# Filter rows
filtered_df = df[
    (df["can_id"] == "0100") &
    (df["tnscal_kg"] > 1000) &
    (df["tnscal_kg"] < 1112)
    ]

# print(filtered_df)

# # Save to a new file
filtered_df.to_csv("filtered_0100.csv", index=False)

print("Saved filtered file with only can_id=0100 to filtered_0100.csv")

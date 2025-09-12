import pandas as pd

# Load your CSV file
df = pd.read_csv("can_data.csv", parse_dates=["timestamp"])
# print(df.dtypes)
# Show first 20 rows with ID 0100
# df_0100 = df[df["can_id"] == "0100"]
# print(df_0100[["timestamp", "tns_g", "tnscal_g", "tnscal_kg"]])

print(type(df["can_id"]))   # type of first value

# Filter rows where can_id == "0100"
filtered_df = df[
    (df["can_id"] == "0100") &
    (df["tnscal_kg"] > 1000) &
    (df["tnscal_kg"] < 1112)
    ]

# print(filtered_df)

# # Save to a new file
filtered_df.to_csv("filtered_0100.csv", index=False)

print("Saved filtered file with only can_id=0100 to filtered_0100.csv")

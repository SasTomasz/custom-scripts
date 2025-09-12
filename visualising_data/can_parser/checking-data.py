import pandas as pd

df = pd.read_csv("can_data.csv", parse_dates=["timestamp"])

# Show first 20 rows with ID 0100
df_0100 = df[df["can_id"] == 0x100].head(20)
print(df_0100[["timestamp", "tns_g", "tnscal_g", "tnscal_kg"]])

# print(df["can_id"].head(10))
# print(df_0100)

import pandas as pd
import numpy as np

df = pd.read_excel("data/starbucks_uncleaned.xlsx")

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Remove duplicate rows
df.drop_duplicates(inplace=True)

# Replace invalid values
df.replace(["", "NA", "N/A", "null", "NULL", "-", "?"], np.nan, inplace=True)

# Fill missing values
for col in df.columns:
    if df[col].dtype == "object":
        df[col] = df[col].fillna("Unavailable")
    else:
        df[col] = df[col].fillna(df[col].median())

# ==========================
# ADD THE NEW CODE HERE
# ==========================

df["category"] = df["category"].astype(str).str.strip().str.title()
df["order_channel"] = df["order_channel"].astype(str).str.strip().str.title()
df["payment_method"] = df["payment_method"].astype(str).str.strip().str.title()
df["loyalty_member"] = df["loyalty_member"].astype(str).str.strip().str.title()

df["customer_rating"] = pd.to_numeric(df["customer_rating"], errors="coerce")
df["customer_rating"] = df["customer_rating"].fillna(df["customer_rating"].median())

df["total_amount_inr"] = pd.to_numeric(df["total_amount_inr"], errors="coerce")
df["total_amount_inr"] = df["total_amount_inr"].fillna(
    df["quantity"] * df["unit_price_inr"] * (1 - df["discount_percent"] / 100)
)

# ==========================
# SAVE FILE
# ==========================

df.to_csv("data/starbucks_cleaned.csv", index=False)

print("Cleaned file saved!")
print(df.head())
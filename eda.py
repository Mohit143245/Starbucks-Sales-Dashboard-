import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs("images", exist_ok=True)

df = pd.read_csv("data/starbucks_cleaned.csv")

df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

numeric_cols = [
    "quantity",
    "unit_price_inr",
    "discount_percent",
    "total_amount_inr",
    "customer_rating"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

sns.set_theme(style="whitegrid")

# 1. Correlation Heatmap
plt.figure(figsize=(8, 6))
corr = df[numeric_cols].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", linewidths=1)
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("images/correlation_heatmap.png")
plt.show()

# 2. Sales by City
plt.figure(figsize=(10, 6))
city_sales = df.groupby("city")["total_amount_inr"].sum().sort_values(ascending=False)
sns.barplot(x=city_sales.values, y=city_sales.index)
plt.title("Sales by City")
plt.xlabel("Total Sales INR")
plt.ylabel("City")
plt.tight_layout()
plt.savefig("images/sales_by_city.png")
plt.show()

# 3. Sales by Category
plt.figure(figsize=(8, 5))
category_sales = df.groupby("category")["total_amount_inr"].sum().sort_values(ascending=False)
sns.barplot(x=category_sales.index, y=category_sales.values)
plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Total Sales INR")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("images/sales_by_category.png")
plt.show()

# 4. Customer Rating Distribution
plt.figure(figsize=(8, 5))
sns.histplot(df["customer_rating"], bins=10, kde=True)
plt.title("Customer Rating Distribution")
plt.xlabel("Customer Rating")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("images/customer_rating_distribution.png")
plt.show()

# 5. Discount Distribution
plt.figure(figsize=(8, 5))
sns.histplot(df["discount_percent"], bins=15, kde=True)
plt.title("Discount Distribution")
plt.xlabel("Discount Percent")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("images/discount_distribution.png")
plt.show()

# 6. Quantity Distribution
plt.figure(figsize=(8, 5))
sns.histplot(df["quantity"], bins=10, kde=True)
plt.title("Quantity Distribution")
plt.xlabel("Quantity")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("images/quantity_distribution.png")
plt.show()

# 7. Boxplot: Sales by Category
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x="category", y="total_amount_inr")
plt.title("Sales Spread by Category")
plt.xlabel("Category")
plt.ylabel("Total Amount INR")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("images/sales_boxplot_category.png")
plt.show()

# 8. Payment Method Count
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x="payment_method")
plt.title("Payment Method Count")
plt.xlabel("Payment Method")
plt.ylabel("Number of Orders")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("images/payment_method_count.png")
plt.show()

# 9. Loyalty Member Count
plt.figure(figsize=(6, 5))
sns.countplot(data=df, x="loyalty_member")
plt.title("Loyalty Member Count")
plt.xlabel("Loyalty Member")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("images/loyalty_member_count.png")
plt.show()

# 10. Monthly Sales Trend
monthly_sales = (
    df.dropna(subset=["order_date"])
    .groupby(df["order_date"].dt.to_period("M"))["total_amount_inr"]
    .sum()
)

monthly_sales.index = monthly_sales.index.astype(str)

plt.figure(figsize=(12, 6))
sns.lineplot(x=monthly_sales.index, y=monthly_sales.values, marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales INR")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("images/monthly_sales_trend.png")
plt.show()

# 11. Top 10 Products
top_products = (
    df.groupby("product_name")["total_amount_inr"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 6))
sns.barplot(x=top_products.values, y=top_products.index)
plt.title("Top 10 Products by Sales")
plt.xlabel("Total Sales INR")
plt.ylabel("Product")
plt.tight_layout()
plt.savefig("images/top_10_products.png")
plt.show()

# 12. Discount vs Sales
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x="discount_percent", y="total_amount_inr", hue="category")
plt.title("Discount vs Sales")
plt.xlabel("Discount Percent")
plt.ylabel("Total Amount INR")
plt.tight_layout()
plt.savefig("images/discount_vs_sales.png")
plt.show()

print("EDA completed. Charts saved in images folder.")
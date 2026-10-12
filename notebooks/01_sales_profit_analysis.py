from pathlib import Path
import pandas as pd

# Project folder का रास्ता
project_folder = Path(__file__).resolve().parent.parent

# CSV file पढ़ना
csv_file = project_folder / "data" / "sales_data.csv"
df = pd.read_csv(csv_file)

# डेटा की शुरुआती जाँच
print("\n--- FIRST 5 ROWS ---")
print(df.head())

print("\n--- DATA SHAPE ---")
print(df.shape)

print("\n--- COLUMN NAMES ---")
print(df.columns.tolist())

print("\n--- DATA INFORMATION ---")
df.info()

print("\n--- MISSING VALUES ---")
print(df.isnull().sum())
# DATA CLEANING

print("\n--- DATA CLEANING ---")

# 1. Date column ko datetime mein convert karna
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# 2. Duplicate rows check karna
print("Duplicate rows:", df.duplicated().sum())

# 3. Duplicate rows remove karna
df = df.drop_duplicates()

# 4. Cleaned data check karna
print("\n--- CLEANED DATA ---")
print(df.head())

# 5. Rows aur columns dobara check karna
print("\nCleaned Data Shape:", df.shape)

# 6. Data types check karna
print("\n--- DATA TYPES ---")
print(df.dtypes)

# 7. Missing values dobara check karna
print("\n--- MISSING VALUES AFTER CLEANING ---")
print(df.isnull().sum())
# DATA CLEANING

print("\n--- DATA CLEANING ---")

# 1. Date column ko date format mein convert karna
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# 2. Duplicate rows check karna
print("Duplicate rows:", df.duplicated().sum())

# 3. Duplicate rows remove karna
df = df.drop_duplicates()

# 4. Cleaned data check karna
print("\n--- CLEANED DATA ---")
print(df.head())

# 5. Rows aur columns dobara check karna
print("\nCleaned Data Shape:", df.shape)

# 6. Data types check karna
print("\n--- DATA TYPES ---")
print(df.dtypes)

# 7. Missing values dobara check karna
print("\n--- MISSING VALUES AFTER CLEANING ---")
print(df.isnull().sum())
# SALES AND PROFIT ANALYSIS

print("\n========== SALES & PROFIT ANALYSIS ==========")

# 1. Total Sales aur Total Profit
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()

print("\nTotal Sales:", total_sales)
print("Total Profit:", total_profit)

# 2. Profit Margin percentage
profit_margin = (total_profit / total_sales) * 100

print("Profit Margin:", round(profit_margin, 2), "%")

# 3. Region ke hisaab se Sales aur Profit
print("\n--- REGION ANALYSIS ---")

region_analysis = df.groupby("Region").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Total_Quantity=("Quantity", "sum")
)

region_analysis = region_analysis.sort_values(
    by="Total_Profit",
    ascending=False
)

print(region_analysis)

# 4. Category ke hisaab se Sales aur Profit
print("\n--- CATEGORY ANALYSIS ---")

category_analysis = df.groupby("Category").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Average_Discount=("Discount", "mean")
)

category_analysis = category_analysis.sort_values(
    by="Total_Profit",
    ascending=False
)

print(category_analysis.round(2))

# 5. Sabse zyada Profit dene wale Products
print("\n--- TOP PROFITABLE PRODUCTS ---")

product_analysis = df.groupby("Product").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum")
)

product_analysis = product_analysis.sort_values(
    by="Total_Profit",
    ascending=False
)

print(product_analysis.head(5))

# DISCOUNT ANALYSIS & PROFIT LEAKAGE

print("\n========== DISCOUNT ANALYSIS ==========")

# 1. Discount ke hisaab se sales aur profit
discount_analysis = df.groupby("Discount").agg(
    Order_Count=("Order_ID", "count"),
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Average_Profit=("Profit", "mean")
)

print("\n--- DISCOUNT-WISE REPORT ---")
print(discount_analysis.round(2))

# 2. High discount wale orders ki janch
# Yahan 15% practice ke liye threshold hai
high_discount_threshold = 0.15

high_discount_orders = df[
    df["Discount"] >= high_discount_threshold
]

print("\n--- HIGH DISCOUNT ORDERS (15% OR MORE) ---")

print(
    high_discount_orders[
        ["Order_ID", "Product", "Discount", "Sales", "Profit"]
    ].to_string(index=False)
)

# 3. High discount orders ka total profit
high_discount_sales = high_discount_orders["Sales"].sum()
high_discount_profit = high_discount_orders["Profit"].sum()

print("\nHigh Discount Sales:", high_discount_sales)
print("High Discount Profit:", high_discount_profit)

# 4. Overall profit se comparison
print("\nOverall Profit:", df["Profit"].sum())


# DATA VISUALIZATION

import matplotlib.pyplot as plt

# Reports folder banana
reports_folder = project_folder / "reports"
reports_folder.mkdir(parents=True, exist_ok=True)


# 1. Region-wise Sales Chart
sales_by_region = (
    df.groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(8, 5))
sales_by_region.plot(kind="bar")

plt.title("Total Sales by Region")
plt.xlabel("Region")
plt.ylabel("Total Sales")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(reports_folder / "sales_by_region.png", dpi=150)
plt.close()


# 2. Category-wise Profit Chart
profit_by_category = (
    df.groupby("Category")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(8, 5))
profit_by_category.plot(kind="bar")

plt.title("Total Profit by Category")
plt.xlabel("Category")
plt.ylabel("Total Profit")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(reports_folder / "profit_by_category.png", dpi=150)
plt.close()


# 3. Discount vs Profit Chart
plt.figure(figsize=(8, 5))

plt.scatter(
    df["Discount"] * 100,
    df["Profit"]
)

plt.title("Discount vs Profit")
plt.xlabel("Discount (%)")
plt.ylabel("Profit")
plt.tight_layout()

plt.savefig(reports_folder / "discount_vs_profit.png", dpi=150)
plt.close()


print("\n--- CHARTS CREATED SUCCESSFULLY ---")
print("Saved in:", reports_folder)
print("1. sales_by_region.png")
print("2. profit_by_category.png")
print("3. discount_vs_profit.png")


# BUSINESS INSIGHTS & RECOMMENDATIONS

print("\n========== BUSINESS INSIGHTS ==========")

# 1. Region-wise performance
region_summary = df.groupby("Region").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum")
)

best_region = region_summary["Total_Profit"].idxmax()

print("\nMost Profitable Region:", best_region)
print(region_summary.sort_values(
    by="Total_Profit", ascending=False
))


# 2. Category-wise performance
category_summary = df.groupby("Category").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum")
)

best_category = category_summary["Total_Profit"].idxmax()

print("\nMost Profitable Category:", best_category)
print(category_summary.sort_values(
    by="Total_Profit", ascending=False
))


# 3. Most profitable product
product_profit = df.groupby("Product")["Profit"].sum()

best_product = product_profit.idxmax()

print("\nMost Profitable Product:", best_product)
print("Product Profit:", product_profit.max())


# 4. High discount orders ki jaanch
high_discount_orders = df[df["Discount"] >= 0.15]

print("\nOrders with 15% or Higher Discount:")
print(
    high_discount_orders[
        ["Order_ID", "Product", "Discount", "Sales", "Profit"]
    ].to_string(index=False)
)


# 5. Business recommendations
print("\n========== RECOMMENDATIONS ==========")

print(
    f"1. {best_region} Region ki performance ko samjhein "
    "aur uski successful practices ko investigate karein."
)

print(
    f"2. {best_category} Category ke sales aur profit "
    "ko monitor karein."
)

print(
    f"3. {best_product} Product ki profitability ko "
    "samjhein aur uske results ko monitor karein."
)

print(
    "4. High-discount orders ki cost aur profit margin "
    "check karein, taaki pata chale discount profitable tha ya nahi."
)

# DATA VISUALIZATION & REPORTS

import matplotlib.pyplot as plt

# Reports folder banana
reports_folder = project_folder / "reports"
reports_folder.mkdir(parents=True, exist_ok=True)


# 1. Region-wise Sales Chart
sales_by_region = df.groupby("Region")["Sales"].sum()

plt.figure(figsize=(8, 5))
sales_by_region.plot(kind="bar")
plt.title("Total Sales by Region")
plt.xlabel("Region")
plt.ylabel("Total Sales")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(reports_folder / "sales_by_region.png", dpi=150)
plt.close()


# 2. Category-wise Profit Chart
profit_by_category = df.groupby("Category")["Profit"].sum()

plt.figure(figsize=(8, 5))
profit_by_category.plot(kind="bar")
plt.title("Total Profit by Category")
plt.xlabel("Category")
plt.ylabel("Total Profit")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(reports_folder / "profit_by_category.png", dpi=150)
plt.close()


# 3. Discount vs Profit Chart
plt.figure(figsize=(8, 5))
plt.scatter(df["Discount"] * 100, df["Profit"])
plt.title("Discount vs Profit")
plt.xlabel("Discount (%)")
plt.ylabel("Profit")
plt.tight_layout()
plt.savefig(reports_folder / "discount_vs_profit.png", dpi=150)
plt.close()


print("\n--- CHARTS CREATED ---")
print("Reports folder:", reports_folder)
print("sales_by_region.png")
print("profit_by_category.png")
print("discount_vs_profit.png")

# FINAL BUSINESS REPORT

from pathlib import Path

reports_folder = project_folder / "reports"
reports_folder.mkdir(parents=True, exist_ok=True)

# Overall business summary
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
profit_margin = (
    total_profit / total_sales * 100
    if total_sales != 0 else 0
)

# Region-wise results
region_report = df.groupby("Region").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum")
).sort_values("Total_Profit", ascending=False)

# Category-wise results
category_report = df.groupby("Category").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum")
).sort_values("Total_Profit", ascending=False)

# Product-wise results
product_report = df.groupby("Product").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum")
).sort_values("Total_Profit", ascending=False)

# High-discount orders
high_discount = df[df["Discount"] >= 0.15]

# Build the report
report_text = f"""
SALES & PROFIT INTELLIGENCE SYSTEM
==================================

1. OVERALL SUMMARY

Total Orders/Records: {len(df)}
Total Sales: {total_sales}
Total Profit: {total_profit}
Profit Margin: {profit_margin:.2f}%

2. REGION-WISE PERFORMANCE

{region_report.to_string()}

3. CATEGORY-WISE PERFORMANCE

{category_report.to_string()}

4. TOP 5 PRODUCTS BY PROFIT

{product_report.head(5).to_string()}

5. HIGH-DISCOUNT REVIEW (15% OR MORE)

Number of Orders: {len(high_discount)}
Sales from These Orders: {high_discount["Sales"].sum()}
Profit from These Orders: {high_discount["Profit"].sum()}

6. BUSINESS NOTE

High-discount orders should be reviewed alongside product
costs and expected margins. A high discount alone does not
prove that a business has lost profit.

This report was generated using the available project dataset.
"""

# Save the report
report_file = reports_folder / "business_analysis_report.txt"
report_file.write_text(report_text, encoding="utf-8")

print("\n--- FINAL BUSINESS REPORT CREATED ---")
print("Report saved at:", report_file)
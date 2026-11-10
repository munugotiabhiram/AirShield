
import pandas as pd
import numpy as np

# 1. Load the dataset
df = pd.read_excel("pollution.xlsx")

# 2. Display original dataset
print("Original Dataset:")
print(df.head())

# 3. Remove extra spaces from column names
df.columns = df.columns.str.strip()

# 4. Remove extra spaces from text columns
for col in df.select_dtypes(include=["object", "string"]).columns:
    df[col] = df[col].str.strip()

# 5. Convert Date column to datetime
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(
        df["Date"], errors="coerce"
    )

# 6. Convert pollution values into numeric format
numeric_columns = [
    "AQI", "PM2.5", "PM10",
    "NO2", "SO2", "CO", "O3"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(
            df[col], errors="coerce"
        )

# 7. Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# 8. Remove duplicate records
df = df.drop_duplicates()

# 9. Check dataset information
print("\nCleaned Dataset Information:")
print(df.info())

# 10. Display cleaned dataset
print("\nCleaned Dataset:")
print(df.head())

# 11. Save cleaned dataset
df.to_excel("pollution_cleaned.xlsx", index=False)

print("\nDataset cleaned successfully!")
print("Cleaned dataset saved as pollution_cleaned.xlsx")


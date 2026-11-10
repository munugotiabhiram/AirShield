
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Load dataset
df = pd.read_excel("pollution_cleaned.xlsx")

# 2. Prepare dataset
df.columns = df.columns.str.strip()
df["City"] = df["City"].astype(str).str.strip()
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

pollutants = ["AQI", "PM2.5", "PM10",
              "NO2", "SO2", "CO", "O3"]

for col in pollutants:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.drop_duplicates()

# 3. Basic analytics
print("DATASET INFORMATION")
print(df.info())

print("\nSTATISTICAL ANALYSIS")
print(df[pollutants].describe())

print("\nCITY WISE AQI")
city_avg = df.groupby("City")["AQI"].mean()
print(city_avg.sort_values(ascending=False))

# 4. Average AQI by city
plt.figure(figsize=(9, 5))
city_avg.sort_values().plot(kind="barh")
plt.title("Average AQI by City")
plt.xlabel("Average AQI")
plt.ylabel("City")
plt.tight_layout()
plt.show()

# 5. Monthly AQI trend
monthly_aqi = (
    df.set_index("Date")["AQI"]
    .resample("MS").mean()
)

plt.figure(figsize=(10, 5))
plt.plot(monthly_aqi.index, monthly_aqi.values,
         marker="o")
plt.title("Monthly AQI Trend")
plt.xlabel("Month")
plt.ylabel("Average AQI")
plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()
plt.show()

# 6. AQI distribution
plt.figure(figsize=(8, 5))
plt.hist(df["AQI"].dropna(), bins=20,
         edgecolor="black")
plt.title("AQI Distribution")
plt.xlabel("AQI")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# 7. Correlation analysis
corr = df[pollutants].corr()

print("\nCORRELATION MATRIX")
print(corr.round(2))

plt.figure(figsize=(8, 6))
plt.imshow(corr, vmin=-1, vmax=1)
plt.colorbar(label="Correlation")

plt.xticks(range(len(pollutants)),
           pollutants, rotation=45)
plt.yticks(range(len(pollutants)),
           pollutants)

plt.title("Pollutant Correlation Heatmap")

for i in range(len(pollutants)):
    for j in range(len(pollutants)):
        plt.text(j, i, round(corr.iloc[i, j], 2),
                 ha="center", va="center")

plt.tight_layout()
plt.show()

# 8. Pollutant comparison by city
city_pollution = df.groupby("City")[
    ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"]
].mean()

city_pollution.plot(kind="bar", figsize=(11, 6))
plt.title("Pollutant Levels by City")
plt.xlabel("City")
plt.ylabel("Average Pollutant Level")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

# 9. Highest and lowest AQI
print("\nHIGHEST AQI")
print(df.loc[df["AQI"].idxmax()])

print("\nLOWEST AQI")
print(df.loc[df["AQI"].idxmin()])

# 10. Save analytics results
with pd.ExcelWriter("pollution_analytics_report.xlsx") as writer:
    df.to_excel(writer, sheet_name="Cleaned_Data",
                index=False)
    df[pollutants].describe().to_excel(
        writer, sheet_name="Statistics")
    city_pollution.to_excel(
        writer, sheet_name="City_Pollution")
    corr.to_excel(writer, sheet_name="Correlation")
    monthly_aqi.to_frame().to_excel(
        writer, sheet_name="Monthly_AQI")

print("\nDATA ANALYSIS COMPLETED!")
print("Charts generated successfully!")
print("Analytics report saved successfully!")

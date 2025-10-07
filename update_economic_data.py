from fredapi import Fred
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# --- 1. Connect to FRED API ---
# Use GitHub secret if available, fallback to manual key (for local testing)
api_key = os.getenv("FRED_API_KEY", "d30c886c3feb7735e7bd72c3016cecac")
fred = Fred(api_key=api_key)

# --- 2. Define FRED economic indicators ---
fred_series = {
    "GDP Growth QoQ": "A191RL1Q225SBEA",
    "CPI YoY": "CPIAUCSL",
    "Unemployment Rate": "UNRATE",
    "Nonfarm Payrolls": "PAYEMS",
    "PPI YoY": "PPIACO",
    "Core PCE YoY": "PCEPILFE"
}

# --- 3. Fetch latest data from FRED ---
data = {}
for name, code in fred_series.items():
    try:
        series = fred.get_series_latest_release(code)
        df = series.tail(12)  # get last 12 months/quarters
        data[name] = df
    except Exception as e:
        print(f"Error fetching {name}: {e}")

# --- 4. Convert to one DataFrame ---
df_all = pd.DataFrame(data)
df_all.index = pd.to_datetime(df_all.index)
df_all = df_all.sort_index()

# --- 5. Save to CSV ---
today = datetime.today().strftime("%Y-%m-%d")
filename = f"economic_data_{today}.csv"
df_all.to_csv(filename, encoding="utf-8-sig")
print(f"✅ Data saved to {filename}")

# --- 6. Visualize key indicators ---
plt.figure(figsize=(12, 8))
for col in df_all.columns:
    plt.plot(df_all.index, df_all[col], label=col)

plt.title("U.S. Key Economic Indicators (Last 12 Periods)")
plt.xlabel("Date")
plt.ylabel("Value")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("economic_data_chart.png")  # also save chart
plt.close()

print("📊 Chart saved as economic_data_chart.png")

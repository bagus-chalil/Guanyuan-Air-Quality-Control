import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load data
guanyuan_df = pd.read_csv('https://raw.githubusercontent.com/marceloreis/HTI/master/PRSA_Data_20130301-20170228/PRSA_Data_Guanyuan_20130301-20170228.csv')

# Convert to datetime and set as index
guanyuan_df['date'] = pd.to_datetime(guanyuan_df[['year', 'month', 'day', 'hour']])
guanyuan_df.set_index('date', inplace=True)

# Prepare data
numeric_columns = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3", "TEMP", "PRES", "DEWP", "RAIN", "WSPM"]

# Start Streamlit app
st.title('Air Quality monitoring')

# Add year filter in the sidebar
with st.sidebar:
    st.title("Guanyuan air quality dashboard")
    st.text("Filter Year")
    selected_year = st.selectbox('Year', list(range(guanyuan_df.index.year.min(), guanyuan_df.index.year.max() + 1)))

# Filter data based on selected year
filtered_data = guanyuan_df[guanyuan_df.index.year == selected_year]
monthly_data = filtered_data[numeric_columns].resample('ME').mean()

# Plot trend of air quality indicators over time
st.subheader('Trend of Air Quality Indicators Over Time')
fig, ax = plt.subplots()
for column in numeric_columns:
    ax.plot(monthly_data.index, monthly_data[column], label=column)
ax.set_xlabel('Time')
ax.set_ylabel('Air Quality Indicator Value')
ax.legend()
st.pyplot(fig)

# Plot correlation between temperature, pressure, dew point, rain and air quality indicators
st.subheader('Correlation between Temperature, Pressure, Dew Point, Rain and Air Quality Indicators')
# Calculate correlation
corr = filtered_data[['TEMP', 'PRES', 'DEWP', 'RAIN', 'PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].corr()

# Plot heatmap of correlation
fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

st.caption('Copyright (c) M Bagus Chalil A 2024')

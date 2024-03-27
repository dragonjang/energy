import streamlit as st
import pandas as pd
import requests
import io
from datetime import datetime, timedelta

# 다운로드 URL
url = "https://thedocs.worldbank.org/en/doc/5d903e848db1d1b83e0ec8f744e55570-0350012021/related/CMO-Historical-Data-Monthly.xlsx"
df = pd.ExcelFile(url)
sheet_name = 'Monthly Prices'
df = df.parse(sheet_name)

# Add the 4th row data to the 3rd row
df.iloc[3] += df.iloc[4]

# Set the column names of the dataframe to the values in the 3rd row
df.columns = df.iloc[3]

# Delete rows 0 to 2 (inclusive)
df = df.drop(df.index[:6])

# Rename the first column of df to 'date'
df.rename(columns={df.columns[0]: 'date'}, inplace=True)

# Convert the column to datetime format
df['date'] = pd.to_datetime(df['date'], format='%YM%m')

# Set index as date column
df.set_index('date', inplace=True)

# Create a chart
st.subheader("Chart")
columns_to_chart = st.multiselect("Select columns to chart", df.columns)

if columns_to_chart:
    # Drop rows with missing values
    df = df.dropna(subset=columns_to_chart)

    # Replace non-numeric values with NaN
    df[columns_to_chart] = df[columns_to_chart].apply(lambda x: pd.to_numeric(x, errors='coerce'))

    # Convert dates to Unix timestamps
    min_date = df.index.min().timestamp()
    max_date = df.index.max().timestamp()

    # Create a slider to control the x-axis scale
    # x_scale_values = st.slider("X-axis scale", min_date, max_date, (min_date, max_date), step=timedelta(days=30).total_seconds(), format="%Y-%m-%d")
    x_scale_values = st.slider("X-axis scale", min_date, max_date, (min_date, max_date), step=timedelta(days=30).total_seconds(), format="YYY-MM-DD")

    # Convert Unix timestamps back to datetime objects
    start_date = datetime.fromtimestamp(x_scale_values[0])
    end_date = datetime.fromtimestamp(x_scale_values[1])

    # Create a line chart using st.line_chart
    chart_data = df.loc[start_date:end_date, columns_to_chart]
    st.line_chart(chart_data)
import streamlit as st
import pandas as pd
import numpy as np


st.title("Uber pickups in NYC")

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


# Create a text element and let the reader know the data is loading.
load_data_state = st.text("Loading data...")

# Load 10,000 rows of data into the dataframe.
data = load_data(10000)

# Notify the reader that the data was successfully loaded.
load_data_state.text("Done! (using st.cache_data)")

if st.checkbox('Show raw data?'):
    st.subheader("Raw data")
    st.write(data)

# Draw a histogram
st.subheader("Number of pickups by hour")

# Use numpy to generate a histogram than breaks down pickup times binned by hour
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

st.bar_chart(hist_values)   # Draws the histogram

#   Plot data on map
# st.subheader("Map of all pickups")
# st.map(data)


#   Map of all pickups at 5:00'
hour_to_filter = hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h

filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)


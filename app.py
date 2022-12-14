import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title('Credit Card Fraud Detection')

#DATE_COLUMN = 'date/time'
#DATA_URL = ('https://drive.google.com/file/d/1HiFyESnf22FeI2FBNR29z6Oq0C9zoQiC/view?usp=sharing')

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    st.write(bytes_data)

    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    st.write(stringio)

    # To read file as string:
    string_data = stringio.read()
    st.write(string_data)

    # Can be used wherever a "file-like" object is accepted:
    data = pd.read_csv(uploaded_file)
    st.write(data)

@st.cache
def load_data(nrows):
    data = pd.read_csv(uploaded_file)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data 

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(284315)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')

st.subheader('Raw data')
st.write(data)

st.subheader('Data Visualization of 100 transactions')
data1 = data[['class','amount']]

st.bar_chart(data1[:100])


fraudData = data.loc[data['class'] == 1]
normalData = data.loc[data['class'] == 0]
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
fig.suptitle('Transaction time vs Amount')

ax1.scatter(fraudData.time, fraudData.amount)
ax1.set_title('Fraud')

ax2.scatter(normalData.time, normalData.amount)
ax2.set_title('Normal')

plt.xlabel('Time(in s)')
plt.ylabel('Amount(in $)')
st.pyplot(fig)



fig, (ax1, ax2) = plt.subplots(1,2, sharex=True)
fig.suptitle('Amount per transaction by class')

bins = 5

ax2.hist(normalData.amount, bins = bins)
ax2.set_title('Normal')

ax1.hist(fraudData.amount, bins = bins)
ax1.set_title('Fraud')

plt.xlabel('Amount($)')
plt.ylabel('No. of Transactions')
plt.xlim((0, 20000))
plt.yscale('log')
st.pyplot(fig)

import streamlit as st
import fsspec
import boto3
import botocore
import pandas as pd

# Connect to S3
s3 = boto3.client('s3')

# st.set_page_config(page_title="My S3 App", page_icon=":guardsman:", layout="wide")

# Get parquet file from S3
file = 'trades2021.parquet'

# Read data from S3
data = pd.read_parquet(f"s3://schiff-trades-2021/{file}")

def calculate_mean(data):
    return data.mean()

def calculate_sum(data):
    return data.sum()


st.title("Options Data")
if st.button("Calculate Mean"):
    mean_result = calculate_mean(data.head(200))
    st.write("Mean:", mean_result)
if st.button("Calculate Sum"):
    sum_result = calculate_sum(data.head(200))
    st.write("Sum:", sum_result)

import streamlit as st
import fsspec
import boto3
import botocore
import pandas as pd
import numpy as np
# Connect to S3
s3 = boto3.client('s3')

st.set_page_config(page_title="My S3 App", page_icon=":guardsman:", layout="wide")

delta=st.slider('Select differnce points from market value',-50,50,0,10)

open_time=st.selectbox('Choose Opening time',[10,11,12])

close_time=st.selectbox('Choose Closing time',[13,14,15,16])

months = st.multiselect(
    'Select Months',
    [1, 2, 3, 4,5,6,7,8,9,10,11,12],)

all_options = st.checkbox("Select whole Year",1)
if all_options:
    months = [1, 2, 3, 4,5,6,7,8,9,10,11,12]


# Get parquet file from S3
file = 'trades2021.parquet'

# Read data from S3
df = pd.read_parquet(f"s3://schiff-trades-2021/{file}")

#Create timestamp for date and time columns
df['timestamp'] = df['date'] + pd.to_timedelta(df['time'])


def Day_Night_Result_table(df,buy_morning=True,open_time=open_time,close_time=close_time,
                           delta=delta,months=months):
    months = [months] if type(months) == int else months

    open_trades= df[(df['timestamp'].dt.hour < open_time)&
                    (df['diff_mimush']==delta)&
                    (df['timestamp'].dt.month.isin(months))]
    
    close_trades =  df[(df['timestamp'].dt.hour > close_time)&
             (df['diff_mimush']==delta)&
             (df['timestamp'].dt.month.isin(months))]

    full_trades = pd.concat([open_trades, close_trades], ignore_index=True).sort_values(by=['timestamp','mispar_hoze']).reset_index(drop=True)

    grouped = full_trades.groupby(['date', 'mispar_hoze'])
    first_trade = grouped.first().reset_index()
    last_trade = grouped.last().reset_index()

    if buy_morning:
        first_trade['trade_type'] = 'buy'
        last_trade['trade_type'] = 'sell'
    else:
        first_trade['trade_type'] = 'sell'
        last_trade['trade_type'] = 'buy'

    df_final = pd.concat([first_trade, last_trade], ignore_index=True)
    df_final['buy_sell'] = np.where(df_final.trade_type=='buy',-df_final['p'],df_final['p'])
    # number_of_trades = df_final.shape[0]
    # result= df_final.groupby(['call','month'])['buy_sell'].sum().reset_index().rename(columns={'call': 'option_type'})
    # result['option_type'] = result['option_type'].map({0.0: 'Put', 1.0: 'Call'})

    return(df_final)

a =Day_Night_Result_table(df)

def Output_Table(df):
    df_final = Day_Night_Result_table(df)
    number_of_trades = df_final.shape[0]
    result= df_final.groupby(['call','month'])['buy_sell'].sum().reset_index().rename(columns={'call': 'option_type'})
    result['option_type'] = result['option_type'].map({0.0: 'Put', 1.0: 'Call'})
    result['month'] = result['month'].astype(int)
    return result



# def calculate_mean(df):
#     return df.mean()

# def calculate_sum(data):
#     return df.sum()


st.title("Options Data")
if st.button("Calculate Mean"):
    mean_result = Output_Table(df)
    st.write("Mean:", mean_result)



# if st.button("Calculate Sum"):
#     sum_result = calculate_sum(df.head(200))
#     st.write("Sum:", sum_result)



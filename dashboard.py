import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime

st.set_page_config(page_title='Real-Time Dashboard', layout='wide')
st.title('Real-Time Data Analytics Dashboard')
st.markdown('**Project 3 - Navyan Data Analytics Internship**')

st.sidebar.title('Settings')
refresh = st.sidebar.slider('Auto Refresh (seconds)', 10, 60, 30)
choice = st.sidebar.selectbox('Select Data', ['Cryptocurrency', 'Both'])

st.sidebar.markdown('---')
st.sidebar.markdown('Last Updated: ' + datetime.now().strftime('%H:%M:%S'))

st.header('Live Cryptocurrency Prices')
try:
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,dogecoin,cardano,solana&vs_currencies=usd&include_24hr_change=true'
    response = requests.get(url, timeout=10)
    data = response.json()
    col1, col2, col3, col4, col5 = st.columns(5)
    coins = [('bitcoin','Bitcoin','BTC'), ('ethereum','Ethereum','ETH'), ('dogecoin','Dogecoin','DOGE'), ('cardano','Cardano','ADA'), ('solana','Solana','SOL')]
    cols = [col1, col2, col3, col4, col5]
    for i, (coin_id, name, symbol) in enumerate(coins):
        price = data[coin_id]['usd']
        change = data[coin_id]['usd_24h_change']
        arrow = '' if change > 0 else ''
        cols[i].metric(label=f'{arrow} {name} ({symbol})', value=f'${price:,.2f}', delta=f'{change:.2f}%')
    prices = [data[c[0]]['usd'] for c in coins]
    names = [c[1] for c in coins]
    df = pd.DataFrame({'Coin': names, 'Price (USD)': prices})
    st.bar_chart(df.set_index('Coin'))
except Exception as e:
    st.error(f'Error fetching crypto data: {e}')

st.markdown('---')
st.info(f'Dashboard refreshes every {refresh} seconds. Last updated: {datetime.now().strftime("%H:%M:%S")}')
time.sleep(refresh)
st.rerun()
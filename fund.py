# read in csv using pandas and create 


import pandas as pd
import numpy as np
from utils import get_btc,get_price,get_eth
from time import sleep


prices = get_price()
# print(data)
p_btc = prices['BTCUSDT']
p_eth = prices['ETHUSDT']


df = pd.read_csv('CryptoAddresses.csv')
Ex = pd.read_csv('ex.csv')


df_funds = pd.DataFrame(columns=['Platform', 'BTC', 'ETH','Stables'])
df = df[df['Type'] == 'fund']
df = df.reset_index(drop=True)
df.drop(columns=['Sol'], inplace=True)
df.dropna(axis=0, inplace=True)

df_funds["Platform"] = df["Platform"]



# wallets
for row in df.iterrows():
    wallet_address_btc = row[1]['BTC']
        
    btc = get_btc(wallet_address_btc)
    df_funds.loc[row[0], 'BTC'] = btc
    
    wallet_address_eth = row[1]['ETH']
    eth_tokens = get_eth(wallet_address_eth)
  
  
    if eth_tokens is not None:
        df_funds.loc[row[0], 'ETH'] = eth_tokens['ETH']
        df_funds.loc[row[0], 'Stables'] = int(eth_tokens['DAI'])
    

df_funds['BTC_USD'] = int(df_funds['BTC'] * p_btc)
df_funds['ETH_USD'] = int(df_funds['ETH'] * p_eth)
df_funds['Total_USD'] = int(df_funds['BTC_USD'] + df_funds['ETH_USD'] + df_funds['Stables'])

print(df_funds)

df_funds.to_html('funds.html', index=False)    


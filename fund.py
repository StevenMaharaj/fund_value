# read in csv using pandas and create


import asyncio
import pandas as pd
import numpy as np
from utils import get_btc, get_price, get_eth
from time import sleep
import deribit
from dotenv import load_dotenv
import os

load_dotenv()

wallet_address_btc = os.getenv('WALLET_ADDRESS_BTC')
wallet_address_eth = os.getenv('WALLET_ADDRESS_ETH')

prices = get_price()
# print(data)
p_btc = prices['BTCUSDT']
p_eth = prices['ETHUSDT']


df_funds = pd.DataFrame(columns=['Platform', 'BTC', 'ETH', 'Stables'])

# wallets
# Exodus

btc = get_btc(wallet_address_btc)
eth_tokens = get_eth(wallet_address_eth)

df_funds.loc[0, 'Platform'] = 'Exodus'
df_funds.loc[0, 'BTC'] = btc
df_funds.loc[0, 'ETH'] = eth_tokens['ETH']
df_funds.loc[0, 'Stables'] = int(eth_tokens['DAI'])


# Deribit
deribit_info = asyncio.get_event_loop().run_until_complete(deribit.call_api())
df_funds.loc[1, 'Platform'] = 'Deribit'
df_funds.loc[1, 'BTC'] = deribit_info['BTC']
df_funds.loc[1, 'ETH'] = deribit_info['ETH']
df_funds.loc[1, 'Stables'] = int(deribit_info['USDC'])


df_funds['BTC_USD'] = (df_funds['BTC'] * p_btc).astype(int)
df_funds['ETH_USD'] = (df_funds['ETH'] * p_eth).astype(int)
df_funds['Total_USD'] = (df_funds['BTC_USD'] +
                         df_funds['ETH_USD'] + df_funds['Stables']).astype(int)

df_funds.set_index('Platform', inplace=True)
print(df_funds)


# df_funds.to_html('funds.html', index=False)

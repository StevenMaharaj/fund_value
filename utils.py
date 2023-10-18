
import re
import requests
from pprint import pprint

def get_btc(wallet_address):
# URL for the Blockchain.info API to fetch wallet information
    url = f'https://chain.api.btc.com/v3/address/{wallet_address}'

    try:
        response = requests.get(url)
        data = response.json()

        # Check if the request was successful
        if response.status_code == 200:
            # total_received = data['total_received']
            return data['data']['balance']/100000000.0
        else:
            print(f'Error: Unable to fetch wallet information. Status Code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')


def get_eth(wallet_address:str):
    url = f'https://api.ethplorer.io/getAddressInfo/{wallet_address}?apiKey=freekey'

    res: dict[str,float] = {}
    
    try:
        response = requests.get(url)
        data = response.json()

        # Check if the request was successful
        if response.status_code == 200:
            # total_received = data['total_received']
            # pprint(data)
            res['ETH'] = data['ETH']['balance']
            
            for token in data['tokens']:
                if token['tokenInfo']['symbol'] == 'DAI':
                    res['DAI'] = token['balance']/1000000000000000000.0
            
            return res
        else:
            print(f'Error: Unable to fetch wallet information. Status Code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')

    

def get_price() -> dict[str, float]:
    url = 'https://api.binance.com/api/v3/ticker/price?symbols=%5B%22BTCUSDT%22,%22ETHUSDT%22%5D'
    response = requests.get(url)
    data = response.json()
    prices = {e['symbol'] : float(e['price']) for e in data}
    return prices



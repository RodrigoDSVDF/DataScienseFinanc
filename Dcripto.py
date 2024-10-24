import ccxt
import pandas as pd
import os
import time

# Conexão com a Binance utilizando variáveis de ambiente
exchange = ccxt.binance({
    'apiKey': 'i4QeU6dT1xo2kKQYDnw3tqr5VATR4DcdEt3l6dInrmM9pfv9IHPczv7CGDRPZDTi',
    'secret': 'Mt1LVBB2N8hTgFIKmG50uwGKUxIYgiejhwJr8ozHw5xvhMJDC6bu4kq6iIdS5943',
})

# Lista das moedas que você quer importar
moedas = [
    "BTC/USDT", "ETH/USDT", "DOGE/USDT",
    "SOL/USDT", "AAVE/USDT", "SHIB/USDT",  "ADA/USDT",
]

# Função para importar dados históricos da Binance
def importar_dados(moeda):
    data = exchange.fetch_ohlcv(moeda, '1d')
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['moeda'] = moeda  # Adicionando a coluna moeda
    return df

# Definindo a função para importar e salvar os dados periodicamente
def atualizar_dados():
    dadosdf = pd.concat([importar_dados(moeda) for moeda in moedas], ignore_index=True)
    dadosdf.rename(columns={
        'timestamp': 'tempo',
        'open': 'abertura',
        'high': 'alto',
        'low': 'baixo',
        'close': 'fechamento',
        'volume': 'volume',
        'moeda': 'moeda'
    }, inplace=True)
    dadosdf.to_csv('dadospg_cripto.csv', index=False)
    print("Dados atualizados e salvos em dadosdf_cripto.csv")

# Executar a função de atualização a cada 10 minutos
while True:
    atualizar_dados()
    time.sleep(86000)  # Pausa o script por 10 minutos (600 segundos)

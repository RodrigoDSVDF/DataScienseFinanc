import yfinance as yf
import pandas as pd

# Empresas brasileiras (B3) e americanas (NYSE/NASDAQ)
brasil_empresas = ['VALE3.SA', 'PETR4.SA', 'ITUB4.SA', 'BBDC4.SA', 'ABEV3.SA', 'MGLU3.SA', 'BBAS3.SA']
usa_empresas = ['AAPL', 'MSFT', 'AMZN', 'TSLA', 'GOOGL', 'META', 'KO']

# Função para resgatar dados de uma lista de empresas
def get_stock_data(empresas, mercado):
    frames = []
    for empresa in empresas:
        stock = yf.Ticker(empresa)
        historico = stock.history(period="2y")  # Último ano de dados
        historico['Empresa'] = empresa  # Adiciona o nome da empresa
        historico['Mercado'] = mercado  # Adiciona o mercado (Brasil ou EUA)
        frames.append(historico)
    return pd.concat(frames)

# Resgatar dados para as empresas brasileiras e salvar em um arquivo CSV
dados_brasil = get_stock_data(brasil_empresas, 'Brasil')

# Reiniciar o índice para incluir a coluna de tempo
dados_brasil.reset_index(inplace=True)

# Renomear as colunas
dados_brasil = dados_brasil.rename(columns={
    'Date': 'tempo',  # Renomeia 'Date' para 'tempo'
    'Open': 'abertura',
    'High': 'alto',
    'Low': 'baixo',
    'Close': 'fechamento',
    'Volume': 'volume',
    'Empresa': 'moeda',  # Renomeado de 'Empresa' para 'moeda'
    'Mercado': 'mercado'
})

# Salvar em um arquivo CSV
dados_brasil.to_csv('dados_brasil.csv', index=False)
print("Dados do Brasil salvos em 'dados_brasil.csv'")

# Resgatar dados para as empresas americanas e salvar em um arquivo CSV
dados_usa = get_stock_data(usa_empresas, 'EUA')

# Reiniciar o índice para incluir a coluna de tempo
dados_usa.reset_index(inplace=True)

# Renomear as colunas
dados_usa = dados_usa.rename(columns={
    'Date': 'tempo',  # Renomeia 'Date' para 'tempo'
    'Open': 'abertura',
    'High': 'alto',
    'Low': 'baixo',
    'Close': 'fechamento',
    'Volume': 'volume',
    'Empresa': 'moeda',  # Renomeado de 'Empresa' para 'moeda'
    'Mercado': 'mercado'
})

# Salvar em um arquivo CSV
dados_usa.to_csv('dados_usa.csv', index=False)
print("Dados dos EUA salvos em 'dados_usa.csv'")

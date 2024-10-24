import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from scipy.stats import norm
import altair as alt

# Configuração da página
st.set_page_config(page_title='Dashboard Interativa', layout='wide')

# Função para download de relatório PDF
def download_relatorio_pdf():
    try:
        with open(r"C:\Users\Rodrigo_df\OneDrive\Documentos\Curriculo122024.pdf", 'rb') as f:
            st.sidebar.download_button(
                label='Baixar Relatório Completo (PDF)',
                data=f,
                file_name='relatorio_completo.pdf',
                mime='application/pdf'
            )
    except Exception as e:
        st.sidebar.error(f"Erro ao gerar relatório: {e}")

st.sidebar.image(r'C:\Users\Rodrigo_df\Downloads\Alpha-Wave-Analytics---Logo.jpg', use_column_width=True)

# Função para carregar dados com cache e tratamento de erros
@st.cache_data
def importar_dados(tipo_mercado):
    try:
        if tipo_mercado == 'Criptomoedas':
            caminho_csv = "dadospg_cripto.csv"
        elif tipo_mercado == 'Bolsa Brasileira':
            caminho_csv = "dados_brasil.csv"
        else:
            caminho_csv = "dados_usa.csv"

        df = pd.read_csv(caminho_csv)
        df['tempo'] = pd.to_datetime(df['tempo'])

        if 'fechamento' not in df.columns or 'moeda' not in df.columns:
            return None, "O arquivo CSV não contém as colunas necessárias."

        df['retorno_diario'] = df.groupby('moeda')['fechamento'].pct_change()
        df.dropna(subset=['retorno_diario'], inplace=True)
        return df, None  # Retorna os dados e nenhum erro
    except Exception as e:
        return None, f"Erro ao carregar dados: {e}"

# Função para calcular o MACD
def calculate_macd(df, span1=12, span2=26, signal=9):
    df['MACD_line'] = df['fechamento'].ewm(span=span1, adjust=False).mean() - df['fechamento'].ewm(span=span2, adjust=False).mean()
    df['MACD_signal'] = df['MACD_line'].ewm(span=signal, adjust=False).mean()
    return df

# Menu de navegação na barra lateral
menu = st.sidebar.radio(
    "MENU DE NAVEGAÇÃO",
    ['Apresentação', 'Criptomoedas', 'Bolsa Brasileira', 'Bolsa Americana']
)

# Página de apresentação
if menu == 'Apresentação':
    st.title("Análise de Mercados: Decisões Informadas e Estratégicas")
    st.image(r'C:\Users\Rodrigo_df\Downloads\gettyimages-1458179196-1- (1).jpg', use_column_width=True)
    
    st.subheader("""
    Bem-vindo ao seu aplicativo de Ciências de Dados para o mercado financeiro.
    Este é um ambiente robusto, criado para oferecer análises detalhadas e insights críticos que permitem uma compreensão aprofundada dos movimentos e tendências de diversos mercados.
    """)
    
    st.markdown("""
    ### Funcionalidades Principais:
    - **Análises Customizadas**: Relatórios personalizados para criptomoedas, ações da bolsa brasileira e americana.
    - **Indicadores Técnicos Avançados**: Cálculo de médias móveis, RSI, MACD, entre outros.
    - **Visualização de Dados Interativa**: Gráficos interativos e visualizações dinâmicas.
    - **Relatórios Downloadáveis**: Baixe relatórios completos com análises detalhadas.
    """)

    # Exibe o botão para download do relatório PDF
    download_relatorio_pdf()

# Páginas de análises separadas
else:
    st.sidebar.header('Análise de Ativos')

    # Carrega os dados baseados na seleção de mercado
    df, erro = importar_dados(menu)
    
    if erro:
        st.error(erro)
    else:
        st.subheader(f'Análise de {menu}')
        st.write("Dados carregados com sucesso.")
        
        # Seletor de análise
        opcoes = ['Visualização', 'Análise']
        escolha = st.sidebar.selectbox("Escolha uma análise", opcoes)

        # Visualização dos dados
        if escolha == 'Visualização':
            st.write(f'Visualização de dados para {menu}')
            criptomoedas = df['moeda'].unique()
            for moeda in criptomoedas:
                df_moeda = df[df['moeda'] == moeda]
                fig = px.line(df_moeda, x='tempo', y='fechamento', title=f'Preço de Fechamento ao Longo do Tempo para {moeda}')
                st.plotly_chart(fig)

        # Análise de indicadores e correlações
        elif escolha == 'Análise':
            st.subheader('Análise de Correlação e Indicadores de Mercado')
            criptomoedas = df['moeda'].unique()

            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Correlação Geral", "Médias Móveis", "MACD", "Probabilidade de Variação", "Gráfico de Dispersão", "Análise de Volume de Negociação"])

         # Aba 1: Correlação Geral
            with tab1:
                for moeda in criptomoedas:
                    df_moeda = df[df['moeda'] == moeda]
                    correlacao = df_moeda[['volume', 'fechamento']].corr().iloc[0, 1]
                    st.write(f'Correlação entre Volume e Preço de Fechamento para {moeda}: {correlacao:.2f}')
                    fig = px.scatter(df_moeda, x='volume', y='fechamento', trendline="ols",
                                     labels={'volume': 'Volume de Negociação', 'fechamento': 'Preço de Fechamento'},
                                     title=f'Correlação entre Volume e Preço de Fechamento para {moeda}')
                    st.plotly_chart(fig)

            # Aba 2: Médias Móveis
            with tab2:
                for moeda in criptomoedas:
                    st.write(f"Médias móveis para {moeda}")
                    df_moeda = df[df['moeda'] == moeda]
                    df_moeda['MA50'] = df_moeda['fechamento'].rolling(window=50).mean()
                    df_moeda['MA200'] = df_moeda['fechamento'].rolling(window=200).mean()
                    fig = px.line(df_moeda, x='tempo', y=['fechamento', 'MA50', 'MA200'], title=f'Médias Móveis para {moeda}')
                    st.plotly_chart(fig)

            # Aba 3: MACD
            with tab3:
                st.write("Indicador MACD para análise técnica")
                for moeda in criptomoedas:
                    df_moeda = calculate_macd(df[df['moeda'] == moeda])
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=df_moeda['tempo'], y=df_moeda['MACD_line'], mode='lines', name='MACD Line'))
                    fig.add_trace(go.Scatter(x=df_moeda['tempo'], y=df_moeda['MACD_signal'], mode='lines', name='MACD Signal'))
                    fig.update_layout(title=f"MACD para {moeda}", xaxis_title='Tempo', yaxis_title='MACD')
                    st.plotly_chart(fig)

         # Probabilidade de Variação (Distribuição Normal)
            with tab4:
                for moeda in criptomoedas:
                    df_moeda = df[df['moeda'] == moeda]
                    mu, std = norm.fit(df_moeda['retorno_diario'])
                    x = np.linspace(df_moeda['retorno_diario'].min(), df_moeda['retorno_diario'].max(), 100)
                    p = norm.pdf(x, mu, std)
                    df_normal = pd.DataFrame({'x': x, 'p': p})
                    histogram = alt.Chart(df_moeda).transform_density(
                        'retorno_diario',
                        as_=['retorno_diario', 'density'],
                        extent=[df_moeda['retorno_diario'].min(), df_moeda['retorno_diario'].max()]
                    ).mark_area(opacity=0.5).encode(
                        alt.X('retorno_diario:Q'),
                        alt.Y('density:Q'),
                    )
                    normal_curve = alt.Chart(df_normal).mark_line(color='red').encode(
                        alt.X('x'),
                        alt.Y('p')
                    )
                    st.altair_chart(histogram + normal_curve, use_container_width=True)
                    st.write(f"{moeda} - Retorno Médio: {df_moeda['retorno_diario'].mean()}, Risco: {df_moeda['retorno_diario'].std()}")
              

            with tab5:
                fig = go.Figure()
                for moeda in criptomoedas:
                    df_moeda = df[df['moeda'] == moeda]
                    fig.add_trace(go.Scatter(x=[df_moeda['retorno_diario'].mean()], y=[df_moeda['retorno_diario'].std()], mode='markers', name=moeda))
                fig.update_xaxes(title='Média esperada retorno diário', showgrid=True)
                fig.update_yaxes(title='Risco diário', showgrid=True)
                st.plotly_chart(fig)
                # Aba 6: Análise de Volume de Negociação
            # Volume de Negociação
            with tab6:
                for moeda in criptomoedas:
                    df_moeda = df[df['moeda'] == moeda]
                    fig = px.bar(df_moeda, x='tempo', y='volume', title=f'Volume de Negociação para {moeda}')
                    st.plotly_chart(fig)

        # Download do relatório PDF
        download_relatorio_pdf()

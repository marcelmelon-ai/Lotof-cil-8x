import streamlit as st import pandas as pd import numpy as np import requests from bs4 import BeautifulSoup from tensorflow.keras.models import Sequential from tensorflow.keras.layers import LSTM, Dense from sklearn.preprocessing import MinMaxScaler import io

st.set_page_config(page_title="Lotofácil Inteligente 8X", layout="wide") st.title("Lotofácil Inteligente - Previsão com IA")

Função para obter dados atualizados da Caixa

def obter_resultados_lotofacil(): url = "https://loterias.caixa.gov.br/Paginas/Lotofacil.aspx" resposta = requests.get(url) soup = BeautifulSoup(resposta.content, 'html.parser')

# Exemplo de scraping simples (a estrutura da página deve ser analisada com inspeção no navegador)
resultados = soup.find_all("div", class_="resultado-loteria")
if not resultados:
    return pd.DataFrame()

concursos = []
for r in resultados:
    try:
        titulo = r.find("h2").text.strip()
        numeros = r.find("ul").text.strip().split("\n")
        concursos.append({
            "Concurso": titulo,
            "Dezenas": [int(n) for n in numeros if n.isdigit()]
        })
    except:
        continue
return pd.DataFrame(concursos)

Função para carregar o Excel personalizado

def carregar_concursos_excel(arquivo): df = pd.read_excel(arquivo) colunas_esperadas = ['Concurso', 'data sorteio'] + [f'd{i}' for i in range(1, 16)] + ['ganhadores'] if not all(col in df.columns for col in colunas_esperadas): st.error("O arquivo Excel não possui as colunas corretas. Verifique o padrão: Concurso, data sorteio, d1...d15, ganhadores") return None return df

Função para preparar os dados para IA

def preparar_dados(df): dados = df[[f'd{i}' for i in range(1, 16)]].values scaler = MinMaxScaler() dados_normalizados = scaler.fit_transform(dados)

X = []
y = []
for i in range(1, len(dados_normalizados)):
    X.append(dados_normalizados[i - 1])
    y.append(dados_normalizados[i])

X = np.array(X).reshape((len(X), 1, 15))
y = np.array(y)
return X, y, scaler

Função para criar e treinar modelo LSTM

def treinar_modelo(X, y): model = Sequential() model.add(LSTM(64, return_sequences=True, input_shape=(1, 15))) model.add(LSTM(32)) model.add(Dense(15)) model.compile(optimizer='adam', loss='mse') model.fit(X, y, epochs=100, batch_size=8, verbose=0) return model

Upload do arquivo Excel

st.sidebar.header("Carregar Resultados da Lotofácil") uploaded_file = st.sidebar.file_uploader("Upload do Excel personalizado", type=[".xlsx"])

Botão para carregar resultados do site

if st.sidebar.button("Atualizar via Site da Caixa"): df_site = obter_resultados_lotofacil() if not df_site.empty: st.success("Resultados obtidos com sucesso!") st.dataframe(df_site.tail()) else: st.error("Falha ao obter resultados da Caixa. Tente novamente mais tarde.")

Processamento do Excel e previsão

if uploaded_file is not None: df = carregar_concursos_excel(uploaded_file) if df is not None: st.subheader("Resultados Carregados") st.dataframe(df.tail())

st.subheader("Análise com IA")
    X, y, scaler = preparar_dados(df)
    model = treinar_modelo(X, y)

    previsao_normalizada = model.predict(X[-1].reshape(1, 1, 15))
    previsao_denormalizada = scaler.inverse_transform(previsao_normalizada)

    sugestao = sorted([int(round(num)) for num in previsao_denormalizada[0]])
    sugestao = [n if 1 <= n <= 25 else min(max(n, 1), 25) for n in sugestao]

    st.markdown("### Sugestão de jogo com IA:")
    st.write(sorted(set(sugestao)))

    # Exibir gráfico de frequência
    st.subheader("Estatísticas")
    freq = pd.Series(df[[f'd{i}' for i in range(1, 15)]].values.ravel()).value_counts().sort_index()
    st.bar_chart(freq)

    st.success("Jogo sugerido gerado com sucesso com base em IA e histórico!")



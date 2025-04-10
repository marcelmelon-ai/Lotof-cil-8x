import streamlit as st
import pandas as pd
import numpy as np
import requests
import io
import re
from bs4 import BeautifulSoup
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MultiLabelBinarizer

# Configurações iniciais
st.set_page_config(page_title="Lotofácil IA - 8X", layout="centered")
st.title("Gerador Inteligente de Jogos - Lotofácil 8X")

# Função para carregar os concursos a partir do arquivo Excel
def carregar_concursos_excel(uploaded_file):
    try:
        # Leitura do arquivo Excel
        df = pd.read_excel(uploaded_file, sheet_name="Resultados")
        
        # Limpeza e reorganização dos dados
        df.columns = ['Concurso', 'Data', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'Ganhadores']
        df['Dezenas'] = df[['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12', 'D13', 'D14', 'D15']].values.tolist()
        
        return df[['Concurso', 'Data', 'Dezenas', 'Ganhadores']]
    except Exception as e:
        st.error(f"Erro ao processar o arquivo. Verifique se a aba se chama 'Resultados' e se o formato está correto. Detalhes: {e}")
        return None

# Função para carregar os concursos diretamente da URL da Caixa Econômica
@st.cache_data
def carregar_concursos_url():
    url = 'https://loterias.caixa.gov.br/Paginas/App/Lotofacil.aspx'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        tabela = soup.find_all('table')[0]
        
        # Processa a tabela e converte para DataFrame
        df = pd.read_html(str(tabela))[0]
        df.columns = ['Concurso', 'Data', 'Dezenas']
        return df
    else:
        st.error("Erro ao carregar os dados diretamente da Caixa Econômica.")
        return None

# Função para treinar o modelo de IA (Random Forest)
def treinar_modelo(df):
    # Convertendo as dezenas em variáveis binárias para o modelo
    mlb = MultiLabelBinarizer()
    X = mlb.fit_transform(df['Dezenas'])
    
    # Usando os resultados de ganhadores como target
    y = df['Ganhadores'].apply(lambda x: 1 if x > 0 else 0)  # 1 para ganhadores, 0 para não ganhadores
    
    # Divisão de dados em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Treinando o modelo RandomForest
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Predição e avaliação
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    st.success(f"Modelo treinado com sucesso! Acurácia: {accuracy:.2f}")
    return model, mlb

# Função para sugerir os próximos resultados com base no modelo treinado
def sugerir_resultados(model, mlb):
    # Geração de um conjunto de possíveis combinações de jogos (15 números)
    jogos_gerados = [sorted(np.random.choice(range(1, 26), 15, replace=False)) for _ in range(10)]
    
    # Convertendo os jogos gerados para o formato necessário para a predição
    X_novos_jogos = mlb.transform(jogos_gerados)
    
    # Predizendo os resultados
    predicoes = model.predict(X_novos_jogos)
    
    # Exibindo jogos com as previsões
    jogos_sugeridos = []
    for i, predicao in enumerate(predicoes):
        if predicao == 1:  # Jogo com ganhadores
            jogos_sugeridos.append(jogos_gerados[i])
    
    return jogos_sugeridos

# Carregar os dados a partir do arquivo Excel
uploaded_file = st.file_uploader("Carregar arquivo de resultados (Excel)", type="xlsx")

if uploaded_file:
    df = carregar_concursos_excel(uploaded_file)
    if df is not None:
        st.dataframe(df)  # Exibe os dados carregados
        
        # Treinamento do modelo IA
        model, mlb = treinar_modelo(df)
        
        # Gerar novos resultados
        st.subheader("Sugerir próximos resultados")
        jogos_sugeridos = sugerir_resultados(model, mlb)
        
        if jogos_sugeridos:
            st.write("Jogos sugeridos com possibilidade de ganhadores:")
            st.write(jogos_sugeridos)
        else:
            st.write("Nenhum jogo sugerido com alta probabilidade de ganhadores.")

else:
    st.warning("Por favor, carregue um arquivo para começar.")

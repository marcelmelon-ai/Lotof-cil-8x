app.py

import streamlit as st import pandas as pd import numpy as np import requests import io import re from bs4 import BeautifulSoup from datetime import datetime from sklearn.ensemble import RandomForestClassifier from sklearn.model_selection import train_test_split from sklearn.metrics import accuracy_score from sklearn.preprocessing import MultiLabelBinarizer

Configurações iniciais

df = None st.set_page_config(page_title="Lotofácil IA - 8X", layout="centered") st.title("Gerador Inteligente de Jogos - Lotofácil 8X")

Função para buscar os resultados atualizados da Caixa

def baixar_dados_caixa(): url = 'https://loterias.caixa.gov.br/Paginas/Lotofacil.aspx' response = requests.get(url) soup = BeautifulSoup(response.text, 'html.parser') scripts = soup.find_all("script")

for script in scripts:
    if 'var resultados' in script.text:
        resultados_texto = script.text
        break
else:
    return None

matches = re.findall(r'"concurso":(\d+),"dataApuracao":"(\d+/\d+/\d+)","dezenasSorteadasOrdemSorteio":([\d,"]+)', resultados_texto)
concursos = []
for concurso, data, dezenas in matches:
    dezenas = list(map(int, re.findall(r'\d+', dezenas)))
    concursos.append([int(concurso), data, dezenas])

df = pd.DataFrame(concursos, columns=['Concurso', 'Data', 'Dezenas'])
return df

Função alternativa para carregar Excel do usuário

@st.cache_data def carregar_concursos_excel(arquivo): df = pd.read_excel(arquivo) colunas = [col.lower().strip() for col in df.columns] dezenas_cols = [col for col in colunas if col.startswith("d") and col[1:].isdigit()] dezenas = df[[c for c in df.columns if c.lower() in dezenas_cols]].values.tolist() df_final = pd.DataFrame({ 'Concurso': df[df.columns[0]], 'Data': pd.to_datetime(df[df.columns[1]], errors='coerce'), 'Dezenas': dezenas }) return df_final

Seção para upload ou atualização dos dados

opcao_dados = st.radio("Escolha a origem dos dados:", ("Atualizar via site da Caixa", "Carregar arquivo Excel"))

if opcao_dados == "Atualizar via site da Caixa": df = baixar_dados_caixa() else: uploaded_file = st.file_uploader("Envie o arquivo Excel com os resultados", type=[".xlsx"]) if uploaded_file: df = carregar_concursos_excel(uploaded_file)

if df is not None: st.success(f"Concursos carregados: {df.shape[0]}")

# Estatísticas por Linhas
st.subheader("Estatísticas por Linhas (1–5, 6–10...)")
linhas = {
    '1-5': list(range(1, 6)),
    '6-10': list(range(6, 11)),
    '11-15': list(range(11, 16)),
    '16-20': list(range(16, 21)),
    '21-25': list(range(21, 26))
}
contagem = {linha: [] for linha in linhas}
for dezenas in df['Dezenas']:
    for nome, faixa in linhas.items():
        contagem[nome].append(len([d for d in dezenas if d in faixa]))

df_linhas = pd.DataFrame(contagem)
st.bar_chart(df_linhas.mean())

# Redes neurais e IA para sugestão
st.subheader("Previsão Inteligente com IA")
mlb = MultiLabelBinarizer(classes=list(range(1, 26)))
y = mlb.fit_transform(df['Dezenas'])
X = []
for i in range(len(y) - 1):
    X.append(y[i])
y_train = y[1:]

X_train, X_test, y_train, y_test = train_test_split(X, y_train, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc = accuracy_score(np.array(y_test).argmax(axis=1), y_pred.argmax(axis=1))
st.info(f"Acurácia da IA: {acc:.2f}")

pred_prox = model.predict([y[-1]])[0]
dezenas_previstas = [i+1 for i, val in enumerate(pred_prox) if val == 1][:15]
st.success(f"Sugestão inteligente para o próximo concurso: {sorted(dezenas_previstas)}")

# Geração de Jogos Aleatórios
st.subheader("Gerador de Jogos Aleatórios")
num_jogos = st.slider("Número de jogos a gerar:", 1, 20, 5)
def gerar_jogo():
    return sorted(np.random.choice(range(1, 26), 15, replace=False))

jogos = [gerar_jogo() for _ in range(num_jogos)]
df_jogos = pd.DataFrame(jogos)
st.dataframe(df_jogos)
st.download_button("Baixar Jogos (.csv)", df_jogos.to_csv(index=False).encode(), file_name="jogos_lotofacil.csv")

else: st.error("Erro ao carregar os dados. Verifique se o arquivo ou a fonte está correta.")

st.caption("Desenvolvido por 8X Agro - Marcel Melon")

                                   

import streamlit as st
import pandas as pd
from random import sample
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações do Streamlit
st.set_page_config(page_title="Lotofácil IA - 8X", layout="centered")
st.title("Gerador Inteligente de Jogos - Lotofácil 8X")

# Função para carregar os dados dos concursos a partir de um arquivo Excel
@st.cache_data
def carregar_concursos_excel(uploaded_file):
    # Lê o arquivo Excel carregado
    df = pd.read_excel(uploaded_file, sheet_name="Resultados")
    
    # Verifica se as colunas esperadas existem
    if 'Concurso' in df.columns and 'Data' in df.columns and 'Dezenas' in df.columns:
        # Limpeza dos dados: ajustando colunas
        df['Dezenas'] = df['Dezenas'].apply(lambda x: [int(d) for d in str(x).split()])  # Converte as dezenas em lista de inteiros
        return df
    else:
        st.error("O arquivo Excel não contém as colunas necessárias: Concurso, Data e Dezenas.")
        return None

# Carregar o arquivo Excel
uploaded_file = st.file_uploader("Carregue o arquivo Excel com os resultados da Lotofácil", type=["xlsx"])

# Se o usuário fizer o upload do arquivo
if uploaded_file is not None:
    df = carregar_concursos_excel(uploaded_file)

    # Verifica se o DataFrame foi carregado corretamente
    if df is not None:
        st.success(f"Total de concursos carregados: {df.shape[0]}")
        
        # Estatísticas por LINHAS (1-5, 6-10, 11-15, 16-20, 21-25)
        st.subheader("Estatísticas por Linhas (1–5, 6–10...)")
        linhas = {
            '1-5': list(range(1, 6)),
            '6-10': list(range(6, 11)),
            '11-15': list(range(11, 16)),
            '16-20': list(range(16, 21)),
            '21-25': list(range(21, 26))
        }

        contagem = {linha: [] for linha in linhas}

        # Contagem de ocorrências das dezenas por linha
        for index, row in df.iterrows():
            dezenas = row['Dezenas']
            for nome, faixa in linhas.items():
                contagem[nome].append(len([d for d in dezenas if d in faixa]))

        df_linhas = pd.DataFrame(contagem)
        st.bar_chart(df_linhas.mean())

        # Geração de JOGOS
        st.subheader("Gerar Jogos Inteligentes")
        num_jogos = st.slider("Quantos jogos deseja gerar?", 1, 20, 5)

        # Função para gerar um jogo aleatório
        def gerar_jogo():
            return sorted(sample(range(1, 26), 15))

        # Função para gerar um jogo balanceado, com base nas estatísticas
        def gerar_jogo_balanceado():
            escolha_dezenas = []
            for linha in linhas.values():
                escolha_dezenas.extend(sorted(sample(linha, 3)))  # Seleciona 3 números de cada linha
            return sorted(escolha_dezenas[:15])

        # Geração dos jogos
        jogos = [gerar_jogo() for _ in range(num_jogos)]  # Jogos aleatórios
        jogos_balanceados = [gerar_jogo_balanceado() for _ in range(num_jogos)]  # Jogos balanceados
        
        df_jogos = pd.DataFrame(jogos)
        df_jogos_balanceados = pd.DataFrame(jogos_balanceados)
        
        st.write("Jogos Aleatórios Gerados:")
        st.dataframe(df_jogos)
        
        st.write("Jogos Balanceados Gerados:")
        st.dataframe(df_jogos_balanceados)

        # Botões para download dos jogos gerados
        st.download_button("Baixar Jogos Aleatórios (.csv)", df_jogos.to_csv(index=False).encode(), file_name="jogos_aleatorios.csv")
        st.download_button("Baixar Jogos Balanceados (.csv)", df_jogos_balanceados.to_csv(index=False).encode(), file_name="jogos_balanceados.csv")

    else:
        st.error("Erro ao carregar os dados do arquivo Excel.")
else:
    st.info("Carregue um arquivo Excel contendo os resultados da Lotofácil para continuar.")

# Footer
st.caption("Powered by 8X Agro - Marcel Melon")

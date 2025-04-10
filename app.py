import streamlit as st
import pandas as pd
from random import sample

# Configuração da interface
st.set_page_config(page_title="Lotofácil IA - 8X", layout="centered")
st.title("Gerador Inteligente de Jogos - Lotofácil 8X")
st.caption("Desenvolvido por Marcel Melon - 8X Agro")

# Upload do arquivo Excel
uploaded_file = st.file_uploader("Faça o upload do arquivo Excel com os resultados da Lotofácil (.xlsx)", type="xlsx")

@st.cache_data
def carregar_concursos_excel(file):
    df = pd.read_excel(file, sheet_name="Resultados")
    
    # Assume que as colunas de dezenas começam na coluna 'D1'
    col_dezenas = [col for col in df.columns if str(col).startswith('D')]
    df['Dezenas'] = df[col_dezenas].values.tolist()
    
    return df[['Concurso', 'Data', 'Dezenas']]

if uploaded_file:
    try:
        df = carregar_concursos_excel(uploaded_file)
        st.success(f"{df.shape[0]} concursos carregados com sucesso!")
        
        # --- Estatísticas por Linhas ---
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
        
        # --- Estatísticas de Frequência Geral ---
        st.subheader("Frequência das Dezenas")
        todas_dezenas = sum(df['Dezenas'], [])
        freq = pd.Series(todas_dezenas).value_counts().sort_index()
        st.bar_chart(freq)

        # --- Geração de Jogos ---
        st.subheader("Gerar Jogos Inteligentes")
        num_jogos = st.slider("Quantos jogos deseja gerar?", 1, 20, 5)

        def gerar_jogo_inteligente():
            # Usa as 20 dezenas mais frequentes para montar o jogo
            top_dezenas = freq.sort_values(ascending=False).head(20).index.tolist()
            return sorted(sample(top_dezenas, 15))

        jogos = [gerar_jogo_inteligente() for _ in range(num_jogos)]
        df_jogos = pd.DataFrame(jogos, columns=[f"D{i+1}" for i in range(15)])
        st.dataframe(df_jogos)

        st.download_button("Baixar Jogos (.csv)", df_jogos.to_csv(index=False).encode(), file_name="jogos_lotofacil.csv")

    except Exception as e:
        st.error("Erro ao processar o arquivo. Verifique se a aba se chama 'Resultados' e se o formato está correto.")
        st.exception(e)

else:
    st.warning("Por favor, envie um arquivo Excel com os dados da Lotofácil para começar.")

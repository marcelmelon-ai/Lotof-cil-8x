# Lotofácil 8X - App Inteligente de Previsões e Estatísticas

Este é um aplicativo completo desenvolvido com **Streamlit**, que utiliza dados da Lotofácil da **Caixa Econômica Federal** e técnicas de **Inteligência Artificial**, **Redes Neurais (LSTM)** e **Análises Estatísticas** para prever e gerar jogos otimizados.

## Funcionalidades

- Upload de arquivo Excel com dados históricos
- Leitura direta dos concursos da Caixa pela web
- Análise estatística por faixas (1-5, 6-10...)
- Geração inteligente de jogos
- Previsão de dezenas com rede neural LSTM
- Download dos jogos gerados

## Como Rodar Localmente

### 1. Clone o projeto

```bash
git clone https://github.com/seu-usuario/lotofacil-8x.git
cd lotofacil-8x
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Execute o app

```bash
streamlit run app.py
```

### 4. Atualização de dados

Você pode usar a URL oficial da Caixa:  
[https://loterias.caixa.gov.br/Paginas/App/Lotofacil.aspx](https://loterias.caixa.gov.br/Paginas/App/Lotofacil.aspx)  
Ou fazer upload de um arquivo Excel contendo as colunas:

- Concurso
- Data Sorteio
- d1, d2, ..., d15
- Ganhadores

## Estrutura de Arquivos

- `app.py`: Aplicativo principal em Streamlit
- `requirements.txt`: Lista de dependências
- `README.md`: Este manual

---

Desenvolvido por **Marcel Melon** - 8X Agro
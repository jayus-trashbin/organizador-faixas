# 🪥 Colgate Foco - Organizador de Itens Foco

Ferramenta B2B de alta performance para vendedores da Colgate-Palmolive facilitarem a gestão de portfólio por faixas de loja.

## 🚀 Guia de Deploy (Recomendado)

O Streamlit exige uma conexão persistente via WebSockets para funcionar corretamente. Por isso, **não recomendamos o deploy no Vercel** (que é focado em funções Serverless).

### Opção 1: Streamlit Community Cloud (Grátis e Oficial)

Esta é a opção "estilo Vercel" oficial para Streamlit:

1. Suba este código para o seu GitHub (feito! ✅).
2. Acesse [share.streamlit.io](https://share.streamlit.io).
3. Conecte sua conta do GitHub.
4. Selecione o repositório `organizador-faixas`.
5. Clique em **Deploy**.

### Opção 2: Render ou Railway (Produção)

Se precisar de mais performance ou controle:
1. Crie um novo "Web Service".
2. Use o comando de inicialização: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

---

## 🛠️ Tecnologias Utilizadas

- **Framework:** [Streamlit](https://streamlit.io)
- **Análise de Dados:** Pandas & PyArrow (Parquet para persistência ultrarrápida)
- **Extração de PDF:** pdfplumber
- **Geração de Relatórios:** fpdf2
- **Visualização:** Plotly

## 💻 Instalação Local

1. Clone o repositório:
   ```bash
   git clone https://github.com/jayus-trashbin/organizador-faixas.git
   ```

2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute o app:
   ```bash
   streamlit run app.py
   ```

---
Desenvolvido para máxima produtividade em campo.

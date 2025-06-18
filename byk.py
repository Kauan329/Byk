import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from io import StringIO


#cd C:\Users\I\Desktop\IMBEROY
#streamlit run byk.py
#pip install pandas openpyxl
#streamlit run byk.py --server.address=0.0.0.0

#cat
CATEGORIAS_FIXAS = ["Insumos", "Infraestrutura", "Cabos", "Ferramentas", "Aparelhos"]

# ========== Autenticação e Conexão com Google Sheets ==========
escopo = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
json_keyfile = json.loads(st.secrets["google"])
credenciais = ServiceAccountCredentials.from_json_keyfile_dict(json_keyfile, escopo)

cliente = gspread.authorize(credenciais)
planilha = cliente.open("bykplanilha")
estoque_sheet = planilha.worksheet("estoque")
historico_sheet = planilha.worksheet("historico")

# ========== Configuração Streamlit ==========
st.set_page_config(page_title="Controle de Estoque", layout="wide")
st.title("📦 Sistema de Controle de Estoque")
aba = st.sidebar.radio("Menu", [
    "📋 Visualizar Estoque",
    "📤 Retirada de Itens",
    "📥 Adicionar Itens",
    "📉 Remover Quantidade",
    "📜 Histórico"
])

tecnicos = ["Moraes", "Candido", "Lemes", "Outros"]
categorias = ["Insumos", "Infraestrutura", "Cabos", "Ferramentas", "Aparelhos"]

# ========== Funções ==========
def carregar_estoque():
    return estoque_sheet.get_all_records()

def atualizar_estoque_google(estoque_atualizado):
    estoque_sheet.clear()
    colunas = ["nome", "categoria", "quantidade_inicial", "quantidade"]
    estoque_sheet.append_row(colunas)
    for item in estoque_atualizado:
        estoque_sheet.append_row([item[col] for col in colunas])

def registrar_movimentacao(tipo, tecnico, item, qtd, qtd_final):
    historico_sheet.append_row([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        tipo,
        tecnico,
        item,
        qtd,
        qtd_final
    ])

def atualizar_estoque():
    dados = estoque_sheet.get_all_records()
    st.session_state.estoque = dados

# ========== Inicialização ==========
estoque_data = estoque_sheet.get_all_records()
st.session_state.estoque = estoque_data
# ========== Interfaces ==========
if aba == "📋 Visualizar Estoque":
    st.header("📋 Estoque Atual")
    df = pd.DataFrame(st.session_state.estoque)
    st.dataframe(df, use_container_width=True)

elif aba == "📤 Retirada de Itens":
    st.header("📤 Retirada de Itens")
    categoria = st.selectbox("Selecione a categoria", categorias)
    itens_categoria = [i for i in st.session_state.estoque if i["categoria"] == categoria]

    tecnico = st.selectbox("Selecione o técnico", tecnicos)
    for item in itens_categoria:
        st.markdown(f"**{item['nome']}** — Disponível: {item['quantidade']}")
        qtd = st.number_input(f"Quantidade a retirar de {item['nome']}", 0, item["quantidade"], key=item["nome"])
        if st.button(f"Retirar {item['nome']}", key=f"btn_{item['nome']}"):
            for i in st.session_state.estoque:
                if i["nome"] == item["nome"]:
                    i["quantidade"] -= qtd
                    registrar_movimentacao("Saída", tecnico, i["nome"], qtd, i["quantidade"])
                    atualizar_estoque_google(st.session_state.estoque)
                    st.success(f"{qtd} unidade(s) de {item['nome']} retiradas.")
                    break

elif aba == "📥 Adicionar Itens":
    st.header("📥 Adicionar Itens ao Estoque")

    # 🔹 CARD 1 - Adicionar Novo Item (sem duplicar)
    st.subheader("➕ Adicionar Novo Item")
    nome_item = st.text_input("Nome do Item", key="novo_item_nome")
    categoria_item = st.selectbox("Categoria", CATEGORIAS_FIXAS, key="nova_categoria")
    quantidade_item = st.number_input("Quantidade Inicial", 1, step=1, key="nova_qtd")

    if st.button("Adicionar Novo Item"):
        if not nome_item.strip():
            st.error("Digite o nome do item.")
        else:
            duplicado = any(item["nome"].lower() == nome_item.lower() and item["categoria"] == categoria_item
                            for item in st.session_state.estoque)
            if duplicado:
                st.warning("Esse item já existe. Use o card abaixo para adicionar mais unidades.")
            else:
                novo = {
                    "nome": nome_item,
                    "categoria": categoria_item,
                    "quantidade_inicial": quantidade_item,
                    "quantidade": quantidade_item
                }
                # Adiciona o item na planilha
                estoque_sheet.append_row([
                        nome_item,
                        categoria_item,
                        quantidade_item,
                        quantidade_item
                    ])

                    # Recarrega o estoque da planilha para refletir a mudança
                atualizar_estoque()

                    # Mostra sucesso
                st.success(f'Item **"{nome_item}"** adicionado com sucesso!')

elif aba == "📉 Remover Quantidade":
    st.header("📉 Remover Quantidade Manualmente")
    nomes = [i["nome"] for i in st.session_state.estoque]
    nome = st.selectbox("Escolha o item", nomes)
    item = next((i for i in st.session_state.estoque if i["nome"] == nome), None)
    if item:
        qtd = st.number_input("Quantidade a remover", 0, item["quantidade"])
        if st.button("Remover"):
            item["quantidade"] -= qtd
            registrar_movimentacao("Remoção Manual", "-", nome, qtd, item["quantidade"])
            atualizar_estoque_google(st.session_state.estoque)
            st.success("Quantidade removida com sucesso.")

elif aba == "📜 Histórico":
    st.header("📜 Histórico de Movimentações")
    dados = historico_sheet.get_all_records()
    df = pd.DataFrame(dados)
    st.write("Colunas do DataFrame:", df.columns.tolist())
    st.dataframe(df.sort_values("data/hora", ascending=False), use_container_width=True)
    
    if "data/hora" in df.columns:
        df = df.sort_values("data/hora", ascending=False)
    st.dataframe(df, use_container_width=True)

    #IMAGEM SIDEBAR INFERIOR ESQUERDA
with st.sidebar:
    st.markdown(
    """
    <style>
        /* Espaço para empurrar o logo para o fim da sidebar */
        .sidebar-content:after {
            content: "";
            display: block;
            height: 200px; /* Aumente ou diminua conforme necessário */
        }

        /* Estilo do contêiner da logo */
        .logo-inferior {
            position: fixed;
            bottom: 20px;  /* Distância do rodapé */
            left: 10px;    /* Distância da lateral esquerda */
        }

        /* Imagem da logo */
        .logo-inferior img {
            width: 50px;  /* Ajuste conforme sua logo */
        }
    </style>
    <div class="logo-inferior">
        <img src="https://speednetworktelecom.s3.sa-east-1.amazonaws.com/logos/logo_royal.png">
    </div>
    """,
    unsafe_allow_html=True
)

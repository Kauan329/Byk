import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime

#cd C:\Users\I\Desktop\IMBEROY
#streamlit run byk.py
#pip install pandas openpyxl
#streamlit run byk.py --server.address=0.0.0.0

st.set_page_config(page_title="Controle de Estoque", layout="wide")
st.title("📦 Sistema de Controle de Estoque")

ARQUIVO_REGISTRO = "registro_retiradas.xlsx"
ARQUIVO_ESTOQUE_JSON = "estoque.json"
tecnicos = ["Moraes", "Candido", "Lemes", "Outros"]
CATEGORIAS_FIXAS = ["Insumos", "Infraestrutura", "Cabos", "Ferramentas", "Aparelhos"]

# --------- Funções ---------
def carregar_estoque():
    if os.path.exists(ARQUIVO_ESTOQUE_JSON):
        with open(ARQUIVO_ESTOQUE_JSON, "r") as f:
            return json.load(f)
    else:
        estoque_padrao = [
        #Aparelhos 
        #Nokia
        {"nome": "Nokia 1425G-A", "categoria": "Aparelhos", "quantidade_inicial": 73, "quantidade": 73},
        {"nome": "Nokia 2425G-H", "categoria": "Aparelhos", "quantidade_inicial": 9, "quantidade": 9},
        {"nome": "Nokia 140w-H", "categoria": "Aparelhos", "quantidade_inicial": 18, "quantidade": 18},


        #Huawei
        {"nome": "Huawei HG8245Q2", "categoria": "Aparelhos", "quantidade_inicial": 6, "quantidade": 6}, 
        {"nome": "Huawei HG8145V5 ", "categoria": "Aparelhos", "quantidade_inicial": 6, "quantidade": 6},
        {"nome": "Huawei EG8145X6-10", "categoria": "Aparelhos", "quantidade_inicial": 3, "quantidade": 3},


        #Ferramentas
        {"nome": "Fibra Ativa", "categoria": "Ferramentas", "quantidade_inicial": 2, "quantidade": 2},
        {"nome": "Máquina de Fusão", "categoria": "Ferramentas", "quantidade_inicial": 2, "quantidade": 2},
        {"nome": "Estilete", "categoria": "Ferramentas", "quantidade_inicial": 100, "quantidade": 100},
        
        # Insumos
        {"nome": "Conector RJ45", "categoria": "Insumos", "quantidade_inicial": 00, "quantidade": 00},
        {"nome": "Conector", "categoria": "Insumos", "quantidade_inicial": 22, "quantidade": 22},
        {"nome": "Gabarito", "categoria": "Insumos", "quantidade_inicial": 7, "quantidade": 7},
        {"nome": "Arame de Espinar", "categoria": "Insumos", "quantidade_inicial": 7, "quantidade": 7},

        # Infraestrutura
        {"nome": "Cto's", "categoria": "Infraestrutura", "quantidade_inicial": 00, "quantidade": 00},
        {"nome": "Ceo's", "categoria": "Infraestrutura", "quantidade_inicial": 00, "quantidade": 00},
        {"nome": "Mantas", "categoria": "Infraestrutura", "quantidade_inicial": 00, "quantidade": 00},
        {"nome": "Rodanas", "categoria": "Infraestrutura", "quantidade_inicial": 00, "quantidade": 00},
        {"nome": "Unhas", "categoria": "Infraestrutura", "quantidade_inicial": 00, "quantidade": 00},

        # Cabos

            #CABOS DE 6FO
            {"nome": "6FO 1892M", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "6FO 80M", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

                #CABOS DE 6FO RASPADOS
                    {"nome": "6FO Raspado - 1 ", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

                    {"nome": "6FO Raspado - 2", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},


            #CABOS DE 12 FO
            {"nome": "12FO 2358M", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "12FO 43M - 1", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "12FO 3008M", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "12FO 27M", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "12FO 43M - 2", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "12FO 17M - 1", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "12FO 17M - 2", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "12FO 67M", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "12FO 78M", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "12FO 30M", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "12FO 90M", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "12FO 130M", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "12FO 16M", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "12FO 38M", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "12FO 344M", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "12FO 557M", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

                #CABO DE 12FO RAPADOS
                {"nome": "12FO Raspado - 1", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

                {"nome": "12FO RASPADO - 2", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

                {"nome": "12FO RASPADO - 3", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

                {"nome": "12FO RASPADO - 4", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

                {"nome": "12FO RASPADO - 5", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

                {"nome": "12FO RASPADO - 6", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},
        
                {"nome": "12FO RASPADO - 7", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

                {"nome": "12FO RASPADO - 8", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},
        
                {"nome": "12FO RASPADO - 9", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

             #CABO DE 24FO
            {"nome": "24FO 3000M", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

                 #CABO DE 24FO RASPADOS

            #CABO DE 36FO
            {"nome": "36FO 16M", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "36FO 1008M", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "36FO 1084 M", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "36FO 30M", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "36FO 336M", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "36FO 228m", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "36FO 19M", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "36FO 315M", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

                #CABO DE 36FO RASPADOS
                {"nome": "36FO RASPADO", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

             #CABO DE 48FO 
            {"nome": "48FO 3059M", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

                #CABO DE 48FO RASPADOS
                {"nome": "48FO RASPADO", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

             #CABO DE 72FO
            {"nome": "72FO 256M", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "72FO 220M", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "72FO 19M", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "72FO 244M", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "72FO 140M", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "72FO 102M", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

                #CABO DE 72FO RASPADOS
                {"nome": "72FO RASPADO", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

             #CORDOALHA
            {"nome": "Cordoalha 502M", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "Cordoalha 500M - 1", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "Cordoalha 500m - 2", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "Cordoalha 17m", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},

            {"nome": "Cordoalha 14M", "categoria": "Cabos", "quantidade_inicial": 1, "quantidade": 1},
    ]
        # E já salva o arquivo para uso futuro
        with open(ARQUIVO_ESTOQUE_JSON, "w") as f:
            json.dump(estoque_padrao, f, indent=4)
        return estoque_padrao

def salvar_estoque():
    with open(ARQUIVO_ESTOQUE_JSON, "w") as f:
        json.dump(st.session_state.estoque, f, indent=4)

def registrar_saida_excel(tecnico, item_nome, qtd_retirada, qtd_restante):
    registro = {
        "Data/Hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Técnico": tecnico,
        "Item": item_nome,
        "Quantidade Retirada": qtd_retirada,
        "Quantidade Restante": qtd_restante
    }
    if os.path.exists(ARQUIVO_REGISTRO):
        df_existente = pd.read_excel(ARQUIVO_REGISTRO)
        df_novo = pd.concat([df_existente, pd.DataFrame([registro])], ignore_index=True)
    else:
        df_novo = pd.DataFrame([registro])
    df_novo.to_excel(ARQUIVO_REGISTRO, index=False)

# --------- Inicialização ---------
if "estoque" not in st.session_state:
    st.session_state.estoque = carregar_estoque()

# --------- Interface ---------
aba = st.sidebar.radio("Menu", ["👷 Técnicos", "📤 Retirada de Itens", "📥 Adicionar Itens", "📋 Visualizar Estoque"])

if aba == "👷 Técnicos":
    st.header("👷 Técnicos Cadastrados")
    for t in tecnicos:
        st.markdown(f"- {t}")

elif aba == "📤 Retirada de Itens":
    st.header("📤 Retirada de Itens do Estoque")
    categoria_escolhida = st.selectbox("Selecione a categoria", CATEGORIAS_FIXAS)
    itens_categoria = [item for item in st.session_state.estoque if item["categoria"] == categoria_escolhida]

    st.subheader("Selecione o técnico responsável:")
    coltec = st.columns(len(tecnicos))
    for i, t in enumerate(tecnicos):
        with coltec[i]:
            if st.button(t.title(), key=f"tec_{t}"):
                st.session_state.tecnico_selecionado = t

    if "tecnico_selecionado" in st.session_state:
        st.success(f"Técnico selecionado: **{st.session_state.tecnico_selecionado}**")
    else:
        st.warning("Nenhum técnico selecionado.")

    for item in itens_categoria:
        st.markdown(f"### {item['nome']}")
        st.markdown(f"- Quantidade Inicial: {item['quantidade_inicial']}")
        st.markdown(f"- Quantidade Disponível: {item['quantidade']}")

        col1, col2 = st.columns([2, 1])
        with col1:
            qtd = st.number_input(f"Qtd a retirar ({item['nome']})", 0, item["quantidade"], step=1, key=f"qtd_{item['nome']}")
        with col2:
            if st.button(f"Retirar - {item['nome']}", key=f"btn_{item['nome']}"):
                if "tecnico_selecionado" not in st.session_state:
                    st.error("Selecione um técnico.")
                elif qtd <= 0 or qtd > item["quantidade"]:
                    st.error("Quantidade inválida.")
                else:
                    for i in range(len(st.session_state.estoque)):
                        if st.session_state.estoque[i]["nome"] == item["nome"]:
                            st.session_state.estoque[i]["quantidade"] -= qtd
                            break

                    salvar_estoque()
                    registrar_saida_excel(st.session_state.tecnico_selecionado, item["nome"], qtd, item["quantidade"])
                    st.success(f"{qtd} unidade(s) de **{item['nome']}** retiradas.")

    if os.path.exists(ARQUIVO_REGISTRO):
        with open(ARQUIVO_REGISTRO, "rb") as f:
            st.download_button("📥 Baixar Registro de Retiradas", f, file_name="registro_retiradas.xlsx")

elif aba == "📥 Adicionar Itens":
    st.header("📥 Adicionar Novo Item")

    nome_item = st.text_input("Nome do Item")
    categoria_item = st.selectbox("Categoria", CATEGORIAS_FIXAS)
    quantidade_item = st.number_input("Quantidade Inicial", 1, step=1)

    if st.button("Adicionar Item"):
        existente = next((i for i in st.session_state.estoque if i["nome"].lower() == nome_item.lower()), None)
        if existente:
            st.warning("Esse item já existe no estoque.")
        else:
            novo = {
                "nome": nome_item,
                "categoria": categoria_item,
                "quantidade_inicial": quantidade_item,
                "quantidade": quantidade_item
            }
            st.session_state.estoque.append(novo)
            salvar_estoque()
            st.success(f'Item "{nome_item}" adicionado com sucesso!')

elif aba == "📋 Visualizar Estoque":
    st.header("📋 Estoque Atual")
    if st.session_state.estoque:
        df = pd.DataFrame(st.session_state.estoque)
        st.dataframe(df)
    else:
        st.info("Nenhum item no estoque ainda.")

    if st.button("🔄 Resetar Estoque"):
        del st.session_state.estoque
        st.experimental_rerun()
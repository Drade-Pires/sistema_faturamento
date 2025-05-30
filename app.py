import streamlit as st
import pandas as pd
from login import validar_login
from utils.faturamento import calcular_fatura
from utils.excel import gerar_relatorio_excel_por_cliente

st.set_page_config(page_title="Sistema de Faturamento", layout="centered")
st.title("🔐 Sistema de Faturamento")

# Estado da sessão
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

# Tela de login
if not st.session_state.autenticado:
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if validar_login(usuario, senha):
            st.session_state.autenticado = True
            st.success(f"✅ Bem-vindo, {usuario}!")
            st.rerun()

        else:
            st.error("❌ Usuário ou senha inválidos.")
else:
    st.success("✅ Login realizado com sucesso!")

    st.subheader("📤 Upload de Planilha de Impressões")
    arquivo = st.file_uploader("Escolha um arquivo Excel (.xlsx)", type="xlsx")

    if arquivo:
        try:
            df = pd.read_excel(arquivo)
            st.success("✅ Arquivo carregado com sucesso!")
            st.write("📄 Visualização dos dados:")
            st.dataframe(df)

            resultado = calcular_fatura(df)

            resultado = calcular_fatura(df)
            relatorios = gerar_relatorio_excel_por_cliente(resultado)

            st.subheader("📊 Relatório de Faturas:")
            st.dataframe(resultado)

            st.subheader("🔎 Buscar Cliente para Baixar Relatório")

            clientes = list(relatorios.keys())
            cliente_escolhido = st.selectbox("Selecione o cliente", clientes, index=None, placeholder="Digite o nome do cliente...")

            if cliente_escolhido:
                buffer = relatorios[cliente_escolhido]
                st.download_button(
                    label=f"📥 Baixar Relatório de {cliente_escolhido}",
                    data=buffer,
                    file_name=f"Relatorio_{cliente_escolhido}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


        except Exception as e:
            st.error(f"❌ Erro ao processar o arquivo: {e}")

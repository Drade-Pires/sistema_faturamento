import streamlit as st
import pandas as pd
import io
from login import validar_login

st.set_page_config(page_title="Sistema de Faturamento", layout="centered")

st.title("🔐 Sistema de Faturamento - Login")

# Inicializa o estado da sessão para autenticação
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if validar_login(usuario, senha):
            st.session_state.autenticado = True
            st.experimental_rerun()  # CHAMADA CORRETA: só dentro do clique no botão
        else:
            st.error("Usuário ou senha inválidos.")
else:
    st.success("✅ Login realizado com sucesso!")
    st.write(f"Bem-vindo, usuário!")

    # Parâmetros fixos do sistema
    VALOR_FRANQUIA = 100.0
    FRANQUIA_CREDITOS = 1000
    VALOR_A4 = 0.10
    VALOR_A3 = 0.20
    EQUIVALENCIA_A3_EM_A4 = 2

    def calcular_fatura(df):
        resultados = []

        for cliente in df['Cliente'].unique():
            dados_cliente = df[df['Cliente'] == cliente]
            total_a4 = dados_cliente[dados_cliente['Tipo_Impressao'] == 'A4']['Quantidade'].sum()
            total_a3 = dados_cliente[dados_cliente['Tipo_Impressao'] == 'A3']['Quantidade'].sum()

            total_creditos = total_a4 + (total_a3 * EQUIVALENCIA_A3_EM_A4)

            excedente = max(0, total_creditos - FRANQUIA_CREDITOS)

            excedente_valor = 0.0
            excedente_restante = excedente

            if excedente_restante <= total_a4:
                excedente_valor = excedente_restante * VALOR_A4
            else:
                excedente_valor += total_a4 * VALOR_A4
                excedente_restante -= total_a4
                excedente_valor += (excedente_restante / EQUIVALENCIA_A3_EM_A4) * VALOR_A3

            total_fatura = VALOR_FRANQUIA + excedente_valor

            resultados.append({
                "Cliente": cliente,
                "A4": total_a4,
                "A3": total_a3,
                "Total Créditos": total_creditos,
                "Excedente": excedente,
                "Valor Excedente": excedente_valor,
                "Valor Total": total_fatura
            })

        return pd.DataFrame(resultados)

    def gerar_relatorio_excel(cliente, total_a4, total_a3, total_creditos, excedente, excedente_valor, total_fatura):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_relatorio = pd.DataFrame({
                "Descrição": [
                    "Cliente", "Total A4", "Total A3", "Créditos Totais",
                    "Excedente", "Valor Excedente", "Valor da Franquia", "Valor Total"
                ],
                "Valor": [
                    cliente, total_a4, total_a3, total_creditos,
                    excedente, f"R$ {excedente_valor:.2f}", f"R$ {VALOR_FRANQUIA:.2f}", f"R$ {total_fatura:.2f}"
                ]
            })

            df_relatorio.to_excel(writer, sheet_name="Fatura", index=False)
        
        output.seek(0)
        return output

    st.subheader("📤 Upload de Planilha de Impressões")

    arquivo = st.file_uploader("Escolha um arquivo Excel (.xlsx)", type="xlsx")

    if arquivo:
        df = pd.read_excel(arquivo)
        st.success("Arquivo carregado com sucesso!")
        st.write("📄 Visualização dos dados:")
        st.dataframe(df)

        resultado = calcular_fatura(df)
        st.subheader("📊 Relatório de Faturas:")
        st.dataframe(resultado)

        st.subheader("📥 Relatórios por Cliente")
        for index, row in resultado.iterrows():
            excel_file = gerar_relatorio_excel(
                cliente=row['Cliente'],
                total_a4=row['A4'],
                total_a3=row['A3'],
                total_creditos=row['Total Créditos'],
                excedente=row['Excedente'],
                excedente_valor=row['Valor Excedente'],
                total_fatura=row['Valor Total']
            )

            st.download_button(
                label=f"📄 Baixar fatura de {row['Cliente']}",
                data=excel_file,
                file_name=f"Fatura_{row['Cliente'].replace(' ', '_')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

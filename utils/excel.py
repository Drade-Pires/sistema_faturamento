import pandas as pd
import io

def gerar_relatorio_excel_por_cliente(df_resultado):
    arquivos = {}

    for _, row in df_resultado.iterrows():
        nome_cliente = row["Cliente"]
        buffer = io.BytesIO()
        writer = pd.ExcelWriter(buffer, engine='xlsxwriter')
        row.to_frame().T.to_excel(writer, index=False, sheet_name="Fatura")
        writer.close()
        buffer.seek(0)
        arquivos[nome_cliente] = buffer

    return arquivos

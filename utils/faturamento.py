# utils/faturamento.py

VALOR_FRANQUIA = 100.0
FRANQUIA_CREDITOS = 1000
VALOR_A4 = 0.10
VALOR_A3 = 0.20
EQUIVALENCIA_A3_EM_A4 = 2

import pandas as pd

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
            "Valor Excedente": f"R$ {excedente_valor:.2f}",
            "Valor Total": f"R$ {total_fatura:.2f}"
        })

    return pd.DataFrame(resultados)
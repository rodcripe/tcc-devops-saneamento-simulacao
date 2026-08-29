"""
03_gerar_planilha_graficos_excel.py
Projeto: TCC - Estratégias DevOps em Sistemas de Saneamento
Autor: Rodrigo Crisostomo Pereira
Descrição: Gera a planilha TCC_Graficos_Resultados.xlsx contendo tabelas
           formatadas e gráficos combinados editáveis para a redação do TCC.
"""

import pandas as pd
import xlsxwriter

def gerar_dashboard_excel():
    nome_arquivo = 'TCC_Graficos_Resultados.xlsx'
    
    # DADOS ATUALIZADOS PARA ESPELHAR EXATAMENTE A TABELA 4 DO TCC
    dados = {
        "Fase de Maturidade": ["Baseline (Legado)", "Fase 1 (Observabilidade)", "Fase 2 (Automação)", "Fase 3 (CI/CD)"],
        "MTTR (Horas)": [336.0, 48.0, 24.0, 4.0],
        "CFR": [0.550, 0.500, 0.180, 0.100],
        "QD003 (Horas)": [7.9, 3.2, 2.1, 0.8],
        "IN013": [0.313, 0.280, 0.185, 0.120]
    }
    df = pd.DataFrame(dados)

    writer = pd.ExcelWriter(nome_arquivo, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Dashboard_Resultados', index=False, startrow=1, startcol=1)

    workbook = writer.book
    worksheet = writer.sheets['Dashboard_Resultados']
    worksheet.hide_gridlines(2)

    # Formatação das Células
    header_fmt = workbook.add_format({'bold': True, 'font_color': 'white', 'bg_color': '#2B547E', 'border': 1, 'align': 'center', 'valign': 'vcenter'})
    cell_fmt = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter'})
    pct_fmt = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter', 'num_format': '0.0%'})

    worksheet.set_column('B:B', 28)
    worksheet.set_column('C:C', 18, cell_fmt)
    worksheet.set_column('D:D', 18, pct_fmt)
    worksheet.set_column('E:E', 18, cell_fmt)
    worksheet.set_column('F:F', 18, pct_fmt)

    for col_num, value in enumerate(df.columns.values):
        worksheet.write(1, col_num + 1, value, header_fmt)

    # Gráfico 1: MTTR vs CFR
    chart_dora = workbook.add_chart({'type': 'column'})
    chart_dora.add_series({
        'name': ['Dashboard_Resultados', 1, 2],
        'categories': ['Dashboard_Resultados', 2, 1, 5, 1],
        'values': ['Dashboard_Resultados', 2, 2, 5, 2],
        'fill': {'color': '#4A90E2'},
        'data_labels': {'value': True, 'num_format': '0.0'}
    })

    line_cfr = workbook.add_chart({'type': 'line'})
    line_cfr.add_series({
        'name': ['Dashboard_Resultados', 1, 3],
        'categories': ['Dashboard_Resultados', 2, 1, 5, 1],
        'values': ['Dashboard_Resultados', 2, 3, 5, 3],
        'y2_axis': True,
        'line': {'color': '#E67E22', 'width': 2.5},
        'marker': {'type': 'circle', 'size': 7, 'fill': {'color': '#E67E22'}},
        'data_labels': {'value': True, 'num_format': '0.0%'}
    })
    chart_dora.combine(line_cfr)
    chart_dora.set_title({'name': 'Métricas Técnicas (DORA): MTTR vs CFR'})
    chart_dora.set_x_axis({'name': 'Fases do Roadmap DevOps'})
    chart_dora.set_y_axis({'name': 'MTTR (Horas)'})
    chart_dora.set_y2_axis({'name': 'Taxa de Falhas - CFR (%)'})
    chart_dora.set_size({'width': 720, 'height': 380})
    worksheet.insert_chart('H2', chart_dora)

    # Gráfico 2: QD003 vs IN013
    chart_neg = workbook.add_chart({'type': 'column'})
    chart_neg.add_series({
        'name': ['Dashboard_Resultados', 1, 4],
        'categories': ['Dashboard_Resultados', 2, 1, 5, 1],
        'values': ['Dashboard_Resultados', 2, 4, 5, 4],
        'fill': {'color': '#27AE60'},
        'data_labels': {'value': True, 'num_format': '0.0'}
    })

    line_in013 = workbook.add_chart({'type': 'line'})
    line_in013.add_series({
        'name': ['Dashboard_Resultados', 1, 5],
        'categories': ['Dashboard_Resultados', 2, 1, 5, 1],
        'values': ['Dashboard_Resultados', 2, 5, 5, 5],
        'y2_axis': True,
        'line': {'color': '#C0392B', 'width': 2.5},
        'marker': {'type': 'circle', 'size': 7, 'fill': {'color': '#C0392B'}},
        'data_labels': {'value': True, 'num_format': '0.0%'}
    })
    chart_neg.combine(line_in013)
    chart_neg.set_title({'name': 'Métricas de Negócio: Paralisações (QD003) vs Perdas (IN013)'})
    chart_neg.set_x_axis({'name': 'Fases do Roadmap DevOps'})
    chart_neg.set_y_axis({'name': 'Paralisações - QD003 (Horas)'})
    chart_neg.set_y2_axis({'name': 'Perda de Faturamento - IN013 (%)'})
    chart_neg.set_size({'width': 720, 'height': 380})
    worksheet.insert_chart('H22', chart_neg)

    writer.close()
    print(f"Planilha '{nome_arquivo}' gerada com sucesso!")

if __name__ == "__main__":
    gerar_dashboard_excel()

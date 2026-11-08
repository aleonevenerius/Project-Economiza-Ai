from flask import Flask, render_template
from datetime import date, timedelta

app = Flask(__name__)

# ==========================================
# 1. MATRIZ DE DADOS
# ==========================================

matriz = [
    ["Recurso", "Mês", "Ano", "Valor (R$)", "Data"]
]

meses = {
    7: "Julho",
    8: "Agosto",
    9: "Setembro"
}

# Período: julho a setembro de 2026
data_atual = date(2026, 7, 1)
data_final = date(2026, 9, 30)

while data_atual <= data_final:

    dia = data_atual.day
    mes = data_atual.month
    ano = data_atual.year

    # Valores fictícios de gastos diários
    valor_agua = round(
        4.00 + ((dia * 3 + mes) % 9) * 1.15, 2
    )

    valor_energia = round(
        7.50 + ((dia * 5 + mes * 2) % 11) * 1.80, 2
    )

    # Registrar gasto de água
    matriz.append([
        "Água",
        meses[mes],
        ano,
        valor_agua,
        data_atual.strftime("%d/%m/%Y")
    ])

    # Registrar gasto de energia
    matriz.append([
        "Energia",
        meses[mes],
        ano,
        valor_energia,
        data_atual.strftime("%d/%m/%Y")
    ])

    data_atual += timedelta(days=1)


# ==========================================
# 2. CALCULAR OS GASTOS TOTAIS
# ==========================================

contas = matriz[1:]

total_agua = round(
    sum(
        linha[3] for linha in contas
        if linha[0] == "Água"
    ),
    2
)

total_energia = round(
    sum(
        linha[3] for linha in contas
        if linha[0] == "Energia"
    ),
    2
)

total_geral = round(total_agua + total_energia, 2)


# ==========================================
# 3. CALCULAR OS GASTOS MENSAIS
# ==========================================

meses_trimestre = ["Julho", "Agosto", "Setembro"]

resumo_mensal = []

for mes in meses_trimestre:

    gastos_agua = round(
        sum(
            linha[3] for linha in contas
            if linha[0] == "Água"
            and linha[1] == mes
        ),
        2
    )

    gastos_energia = round(
        sum(
            linha[3] for linha in contas
            if linha[0] == "Energia"
            and linha[1] == mes
        ),
        2
    )

    resumo_mensal.append({
        "mes": mes,
        "agua": gastos_agua,
        "energia": gastos_energia,
        "total": round(gastos_agua + gastos_energia, 2)
    })


# ==========================================
# 4. EXIBIR O DASHBOARD
# ==========================================

@app.route("/")
def inicio():
    #return "FLASK OK"
    
    return render_template(
        "index.html",
        contas=contas,
        total_agua=total_agua,
        total_energia=total_energia,
        total=total_geral,
        resumo_mensal=resumo_mensal
    )


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
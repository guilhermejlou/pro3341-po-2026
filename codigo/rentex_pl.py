"""
PRO3341 -- Projeto Rentex: Otimizacao do Mix de Producao
Trade-off entre margem de contribuicao e parcerias de longo prazo
Disciplina: PRO3341 - Modelagem e Otimizacao de Sistemas de Producao
Professora: Profa. Dra. Celma O. Ribeiro
Grupo: Guilherme de Jesus Lourencao (11260300)
       Emilly C C de Oliveira (15520464)
       Addison Fischer Borges (11375100)
"""
import pulp

produtos  = ['Sarja_Barcelos', 'Sarja_Joy', 'Forro_Padrao', 'Forro_Premium']
recursos  = ['Teares', 'Fio_Algodao', 'Fio_Poliester', 'Elastano', 'MOD']
contratos = ['Forro_Padrao', 'Forro_Premium']

MC    = {'Sarja_Barcelos':700,'Sarja_Joy':1000,'Forro_Padrao':220,'Forro_Premium':350}
b     = {'Teares':380,'Fio_Algodao':400,'Fio_Poliester':500,'Elastano':12,'MOD':1200}
a     = {
    'Teares':       {'Sarja_Barcelos':0.85,'Sarja_Joy':1.40,'Forro_Padrao':0.50,'Forro_Premium':0.70},
    'Fio_Algodao':  {'Sarja_Barcelos':1.35,'Sarja_Joy':0.95,'Forro_Padrao':0.00,'Forro_Premium':0.00},
    'Fio_Poliester':{'Sarja_Barcelos':0.00,'Sarja_Joy':0.35,'Forro_Padrao':1.60,'Forro_Premium':1.55},
    'Elastano':     {'Sarja_Barcelos':0.00,'Sarja_Joy':0.07,'Forro_Padrao':0.00,'Forro_Premium':0.08},
    'MOD':          {'Sarja_Barcelos':0.40,'Sarja_Joy':0.65,'Forro_Padrao':0.25,'Forro_Premium':0.35},
}
d_min  = {'Sarja_Barcelos':0,'Sarja_Joy':0,'Forro_Padrao':60,'Forro_Premium':20}
d_max  = {'Sarja_Barcelos':200,'Sarja_Joy':80,'Forro_Padrao':160,'Forro_Premium':60}
d_pref = {'Forro_Padrao':130,'Forro_Premium':45}


def resolver(rho, b_ov=None):
    """
    Resolve o modelo PL aprimorado com penalidade de relacionamento.

    Parametros
    ----------
    rho   : dict {produto_contrato: R$/lote de shortfall abaixo do preferido}
    b_ov  : dict de overrides de capacidade (para analise de sensibilidade)

    Retorno
    -------
    prob, x (variaveis de producao), s (variaveis de shortfall)
    """
    _b = {**b, **(b_ov or {})}
    prob = pulp.LpProblem("Rentex_Mix", pulp.LpMaximize)

    x = {j: pulp.LpVariable(f"x_{j}", lowBound=0) for j in produtos}
    s = {j: pulp.LpVariable(f"s_{j}", lowBound=0) for j in contratos}

    # Funcao objetivo: MC bruta menos custo de relacionamento
    prob += (pulp.lpSum(MC[j]*x[j] for j in produtos)
             - pulp.lpSum(rho[j]*s[j] for j in contratos))

    # Restricoes de capacidade
    for i in recursos:
        prob += (pulp.lpSum(a[i][j]*x[j] for j in produtos) <= _b[i], f"Cap_{i}")

    # Restricoes de demanda
    for j in produtos:
        prob += x[j] >= d_min[j], f"Min_{j}"
        prob += x[j] <= d_max[j], f"Max_{j}"

    # Soft constraints: nivel preferido (pode ser violado a custo rho)
    for j in contratos:
        prob += x[j] + s[j] >= d_pref[j], f"Pref_{j}"

    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    return prob, x, s


if __name__ == '__main__':
    # --- Cenario base ---
    rho_base = {'Forro_Padrao': 200, 'Forro_Premium': 300}
    prob, x, s = resolver(rho_base)

    print("="*65)
    print("SOLUCAO OTIMA -- Rentex Mix de Producao")
    print(f"Cenario base: rho_FP={rho_base['Forro_Padrao']}, rho_FPr={rho_base['Forro_Premium']}")
    print("="*65)
    print(f"Status: {pulp.LpStatus[prob.status]}")
    print(f"Z*    : R$ {pulp.value(prob.objective):,.2f}/semana\n")

    print(f"{'Produto':<20} {'x*':>7} {'d_pref':>8} {'shortfall':>10} {'MC_total':>12}")
    print("-"*60)
    for j in produtos:
        xv = pulp.value(x[j])
        sv = pulp.value(s[j]) if j in contratos else 0.0
        dp = d_pref.get(j, '---')
        print(f"{j:<20} {xv:>7.1f} {str(dp):>8} {sv:>10.1f} {MC[j]*xv:>12,.2f}")

    print(f"\n{'Recurso':<16} {'Uso':>8} {'Cap':>7} {'Folga':>8} {'Ocup%':>7} {'Pi':>10}")
    print("-"*58)
    for name, c in prob.constraints.items():
        if 'Cap' not in name: continue
        rec = name.replace('Cap_','')
        uso = sum(a[rec][j]*pulp.value(x[j]) for j in produtos)
        pi  = -c.pi if c.pi is not None else 0.0
        print(f"{rec:<16} {uso:>8.1f} {b[rec]:>7} {b[rec]-uso:>8.1f} {100*uso/b[rec]:>6.1f}% {pi:>10.2f}")

    # --- Fronteira de decisao ---
    print("\n=== Fronteira de decisao: threshold de rho_FP ===")
    print(f"{'rho_FP':>8} {'x_FP':>7} {'s_FP':>7} {'Z_liq':>14}")
    for r3 in [0, 25, 29, 30, 50, 200]:
        p2, x2, s2 = resolver({'Forro_Padrao': r3, 'Forro_Premium': 300})
        print(f"{r3:>8} {pulp.value(x2['Forro_Padrao']):>7.1f} {pulp.value(s2['Forro_Padrao']):>7.1f} "
              f"{pulp.value(p2.objective):>14,.2f}")

    # --- Ranging dos teares ---
    print("\n=== Ranging RHS -- Teares ===")
    z0 = pulp.value(prob.objective)
    for delta in [-80,-40,0,+20,+40,+60]:
        p2, _, _ = resolver(rho_base, b_ov={'Teares': b['Teares']+delta})
        zv = pulp.value(p2.objective)
        print(f"  Teares={b['Teares']+delta}h: Z={zv:,.2f} (delta={zv-z0:+,.2f})")

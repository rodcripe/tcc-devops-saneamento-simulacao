"""
02_analise_sensibilidade.py
Projeto: TCC - Estratégias DevOps em Sistemas de Saneamento
Autor: Rodrigo Crisostomo Pereira
Descrição: Análise de sensibilidade estocástica sob cenários de estresse
           de carga operacional para validação de robustez da Fase 3.
"""

import numpy as np
import pandas as pd

def pert_random(a: float, m: float, b: float, size: int = 5000) -> np.ndarray:
    mu = (a + 4 * m + b) / 6.0
    sigma = (b - a) / 6.0
    alpha = ((mu - a) / (b - a)) * (((mu - a) * (b - mu) / (sigma ** 2)) - 1)
    beta_param = alpha * (b - mu) / (mu - a)
    return a + np.random.beta(alpha, beta_param, size) * (b - a)

def executar_analise_sensibilidade():
    np.random.seed(42)
    n_iter = 5000
    
    print("=" * 70)
    print("EXECUTANDO ANÁLISE DE SENSIBILIDADE ESTOCÁSTICA (FASE 3 SOB ESTRESSE)")
    print("=" * 70)
    
    # 1. Cenário Conservador (Sobrecarga / Carga +50%)
    mttr_cons = pert_random(a=4.0, m=8.0, b=15.0, size=n_iter)
    cfr_cons = pert_random(a=8.0, m=15.0, b=22.0, size=n_iter)
    inc_cons = np.random.poisson(lam=2.0, size=n_iter)
    in013_cons = 0.55 * cfr_cons + 6.2 + np.random.normal(0, 0.5, n_iter)
    qd003_cons = (mttr_cons * inc_cons) / 9.0

    # 2. Cenário Moderado (Regime Padrão da Fase 3)
    mttr_mod = pert_random(a=2.0, m=4.0, b=6.0, size=n_iter)
    cfr_mod = pert_random(a=5.0, m=10.0, b=15.0, size=n_iter)
    inc_mod = np.random.poisson(lam=1.0, size=n_iter)
    in013_mod = 0.55 * cfr_mod + 6.5 + np.random.normal(0, 0.5, n_iter)
    qd003_mod = (mttr_mod * inc_mod) / 5.0

    # 3. Cenário Otimista (Carga -20% / Alta Elasticidade Nuvem)
    mttr_otim = pert_random(a=1.0, m=2.0, b=3.0, size=n_iter)
    cfr_otim = pert_random(a=2.0, m=5.0, b=8.0, size=n_iter)
    inc_otim = np.random.poisson(lam=0.5, size=n_iter)
    in013_otim = 0.55 * cfr_otim + 7.0 + np.random.normal(0, 0.5, n_iter)
    qd003_otim = (mttr_otim * inc_otim) / 2.5

    tabela_sensibilidade = pd.DataFrame({
        "MTTR (Horas)": [np.mean(mttr_cons), np.mean(mttr_mod), np.mean(mttr_otim)],
        "CFR (%)": [np.mean(cfr_cons), np.mean(cfr_mod), np.mean(cfr_otim)],
        "Perdas IN013 (%)": [np.mean(in013_cons), np.mean(in013_mod), np.mean(in013_otim)],
        "Duração QD003 (Horas)": [np.mean(qd003_cons), np.mean(qd003_mod), np.mean(qd003_otim)]
    }, index=["Cenário Conservador (+50%)", "Cenário Moderado (Baseline Fase 3)", "Cenário Otimista (-20%)"])

    print("\nTABELA DE ANÁLISE DE SENSIBILIDADE (Fase 3):")
    print(tabela_sensibilidade.round(1))
    
    return tabela_sensibilidade

if __name__ == "__main__":
    executar_analise_sensibilidade()

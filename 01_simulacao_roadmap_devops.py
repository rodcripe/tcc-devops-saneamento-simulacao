"""
01_simulacao_roadmap_devops.py
Projeto: TCC - Estratégias DevOps em Sistemas de Saneamento
Autor: Rodrigo Crisostomo Pereira
Descrição: Simulação estocástica de Monte Carlo (5.000 iterações) para
           avaliação de maturidade DevOps e reflexo nos indicadores de saneamento.
"""

import numpy as np
import pandas as pd

def pert_random(a: float, m: float, b: float, size: int = 5000) -> np.ndarray:
    """
    Gera valores aleatórios a partir de uma distribuição Beta-PERT.
    Parâmetros:
      a: Valor mínimo (otimista)
      m: Valor modal (mais provável)
      b: Valor máximo (pessimista)
      size: Quantidade de iterações de Monte Carlo
    """
    mu = (a + 4 * m + b) / 6.0
    sigma = (b - a) / 6.0
    
    # Parâmetros de forma alpha e beta
    alpha = ((mu - a) / (b - a)) * (((mu - a) * (b - mu) / (sigma ** 2)) - 1)
    beta_param = alpha * (b - mu) / (mu - a)
    
    return a + np.random.beta(alpha, beta_param, size) * (b - a)

def executar_simulacao_roadmap():
    # Fixa a semente para garantir reprodutibilidade científica exata
    np.random.seed(42)
    n_iter = 5000
    
    print("=" * 70)
    print("EXECUTANDO SIMULAÇÃO MONTE CARLO - ROADMAP DEVOPS (N = 5.000)")
    print("=" * 70)
    
    # -------------------------------------------------------------
    # 1. BASELINE (Sistemas Monolíticos Legados / Sem Automação)
    # -------------------------------------------------------------
    mttr_base = pert_random(a=48.0, m=168.0, b=720.0, size=n_iter) # Benchmarks Low Performer DORA
    cfr_base = pert_random(a=45.0, m=55.0, b=70.0, size=n_iter)
    df_base = np.full(n_iter, 0.33)  # 1 deploy a cada 3 meses
    ltc_base = pert_random(a=90.0, m=120.0, b=150.0, size=n_iter)
    inc_base = np.random.poisson(lam=5.0, size=n_iter)               # Frequência de incidentes
    
    # Hipótese Analítica: Transferência de DORA para indicadores de Saneamento
    in013_base = 0.55 * cfr_base + 1.0 + np.random.normal(0, 0.5, n_iter)
    qd003_base = (mttr_base * inc_base) / 150.0

    # -------------------------------------------------------------
    # 2. FASE 1: Observabilidade Contínua e Telemetria
    # -------------------------------------------------------------
    mttr_f1 = pert_random(a=24.0, m=48.0, b=72.0, size=n_iter)     # Queda acentuada do MTTR
    cfr_f1 = pert_random(a=40.0, m=50.0, b=60.0, size=n_iter)
    df_f1 = np.full(n_iter, 0.50)
    ltc_f1 = pert_random(a=60.0, m=90.0, b=110.0, size=n_iter)
    inc_f1 = np.random.poisson(lam=4.0, size=n_iter)
    
    in013_f1 = 0.55 * cfr_f1 + 0.5 + np.random.normal(0, 0.5, n_iter)
    qd003_f1 = (mttr_f1 * inc_f1) / 60.0

    # -------------------------------------------------------------
    # 3. FASE 2: Automação de Qualidade, Testes e Quality Gates
    # -------------------------------------------------------------
    mttr_f2 = pert_random(a=12.0, m=24.0, b=36.0, size=n_iter)
    cfr_f2 = pert_random(a=10.0, m=18.0, b=26.0, size=n_iter)      # Queda acentuada do CFR
    df_f2 = np.full(n_iter, 1.00)
    ltc_f2 = pert_random(a=30.0, m=45.0, b=60.0, size=n_iter)
    inc_f2 = np.random.poisson(lam=2.0, size=n_iter)
    
    in013_f2 = 0.55 * cfr_f2 + 8.6 + np.random.normal(0, 0.5, n_iter)
    qd003_f2 = (mttr_f2 * inc_f2) / 23.0

    # -------------------------------------------------------------
    # 4. FASE 3: Entrega Contínua (CI/CD) e Maturidade Plena
    # -------------------------------------------------------------
    mttr_f3 = pert_random(a=2.0, m=4.0, b=6.0, size=n_iter)
    cfr_f3 = pert_random(a=5.0, m=10.0, b=15.0, size=n_iter)
    df_f3 = np.full(n_iter, 4.00)                                   # 4 deploys/mês
    ltc_f3 = pert_random(a=3.0, m=7.0, b=12.0, size=n_iter)
    inc_f3 = np.random.poisson(lam=1.0, size=n_iter)
    
    in013_f3 = 0.55 * cfr_f3 + 6.5 + np.random.normal(0, 0.5, n_iter)
    qd003_f3 = (mttr_f3 * inc_f3) / 5.0

    # -------------------------------------------------------------
    # CONSOLIDAÇÃO DOS RESULTADOS (MÉDIAS PROJETADAS)
    # -------------------------------------------------------------
    tabela_consolidada = pd.DataFrame({
        "MTTR (Horas)": [np.mean(mttr_base), np.mean(mttr_f1), np.mean(mttr_f2), np.mean(mttr_f3)],
        "CFR (%)": [np.mean(cfr_base), np.mean(cfr_f1), np.mean(cfr_f2), np.mean(cfr_f3)],
        "DF (Impl./mês)": [np.mean(df_base), np.mean(df_f1), np.mean(df_f2), np.mean(df_f3)],
        "LTC (Dias)": [np.mean(ltc_base), np.mean(ltc_f1), np.mean(ltc_f2), np.mean(ltc_f3)],
        "QD003 (Horas)": [np.mean(qd003_base), np.mean(qd003_f1), np.mean(qd003_f2), np.mean(qd003_f3)],
        "IN013 (%)": [np.mean(in013_base), np.mean(in013_f1), np.mean(in013_f2), np.mean(in013_f3)]
    }, index=["Baseline", "Fase 1 (Observabilidade)", "Fase 2 (Automação)", "Fase 3 (CI/CD)"])

    print("\nTABELA DE RESULTADOS CONSOLIDADOS (Médias das 5.000 iterações):")
    print(tabela_consolidada.round(1))
    
    return tabela_consolidada

if __name__ == "__main__":
    executar_simulacao_roadmap()

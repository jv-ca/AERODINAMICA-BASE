import pandas as pd
import CoolProp.CoolProp as cp
import matplotlib.pyplot as plt
import backend as BE
import os
import numpy as np
import math
# Dados do INMET
T_amb = 18.4  # Temperatura (°C)
T_amb_K = T_amb + 273.15  # Temperatura (K)
P_atm = 919.5 * 100  # Pressão (Pa)

# Diretórios dos dados experimentais
caminhos_arquivos = [
    (r"C:\Users\joaov\OneDrive\Desktop\AERODINAMICA FELIPE\Ang -6.txt", "df_neg6"),
    (r"C:\Users\joaov\OneDrive\Desktop\AERODINAMICA FELIPE\Ang -4.txt", "df_neg4"),
    (r"C:\Users\joaov\OneDrive\Desktop\AERODINAMICA FELIPE\Ang -2.txt", "df_neg2"),
    (r"C:\Users\joaov\OneDrive\Desktop\AERODINAMICA FELIPE\Ang 0.txt", "df_0"),
    (r"C:\Users\joaov\OneDrive\Desktop\AERODINAMICA FELIPE\Ang 2.txt", "df_2"),
    (r"C:\Users\joaov\OneDrive\Desktop\AERODINAMICA FELIPE\Ang 4.txt", "df_4"),
    (r"C:\Users\joaov\OneDrive\Desktop\AERODINAMICA FELIPE\Ang 6.txt", "df_6"),
    (r"C:\Users\joaov\OneDrive\Desktop\AERODINAMICA FELIPE\Ang 16.txt", "df_16")
]

# Lista de valores para o eixo x (x_plot)
x_plot = [
    1.00000, 0.95140, 0.91097, 0.87134, 0.83004, 0.79115, 0.75148, 0.71040,
    0.67169, 0.63259, 0.59060, 0.55130, 0.51171, 0.47011, 0.42901, 0.38841,
    0.34661, 0.30653, 0.26551, 0.22694, 0.18680, 0.14648, 0.10693, 0.07151,
    0.04308, 0.02591, 0.01500, 0.00945, 0.00355, 0.00000, 0.00045, 0.00269,
    0.00820, 0.01639, 0.02909, 0.04887, 0.07633, 0.10697, 0.13992, 0.17461,
    0.21219, 0.24868, 0.28715, 0.32497, 0.36279, 0.40019, 0.44102, 0.48034,
    0.51996, 0.55911, 0.59763, 0.63770, 0.67665, 0.71623, 0.75741, 0.79420,
    0.83447, 0.87542, 0.91421, 0.95076, 0.98576
]

# Convertendo x_plot para um DataFrame chamado df_X
df_X = pd.DataFrame(x_plot, columns=['x_plot'])

# Valores de x_plot que devem ser desconsiderados
x_plot_correcoes = [0.91097, 0.83004, 0.75148, 0.48034, 0.42901]

# Loop para ler e processar cada arquivo
for caminho_arquivo, nome_df in caminhos_arquivos:
    # Ler o conteúdo do arquivo
    with open(caminho_arquivo, 'r') as file:
        texto = file.read()

    # Dividir o texto em linhas
    linhas = texto.strip().split("\n")

    # Separar os termos de cada linha pelo delimitador ";"
    dados = [linha.split(";") for linha in linhas]

    # Criar o DataFrame original
    df = pd.DataFrame(dados)

    # Remover a primeira coluna
    df_modificado = df.drop(df.columns[0], axis=1)

    # Trocar a última coluna com a antepenúltima (para organizar as colunas de pressão dinâmica)
    df_modificado[df_modificado.columns[-1]], df_modificado[df_modificado.columns[-3]] = df_modificado[df_modificado.columns[-3]], df_modificado[df_modificado.columns[-1]]

    # Remover as duas primeiras linhas
    df_modificado = df_modificado.drop([0, 1])

    # Resetar o índice
    df_modificado = df_modificado.reset_index(drop=True)

    # Substituir vírgulas por pontos em todo o DataFrame
    df_modificado = df_modificado.replace(',', '.', regex=True)

    # Converter os valores das colunas para float
    df_modificado = df_modificado.apply(pd.to_numeric, errors='coerce')

    # Atribuir o DataFrame modificado à variável correspondente
    globals()[nome_df] = df_modificado

    # Criar o DataFrame df_P (com as colunas de pressão, exceto as últimas duas)
    df_P = df_modificado.iloc[:, :-2]  # Seleciona todas as colunas exceto as últimas duas
    nome_df_P = f"{nome_df}__P"
    globals()[nome_df_P] = df_P

# Loop para gerar os gráficos
for caminho_arquivo, nome_df in caminhos_arquivos:
    file = caminho_arquivo
    p_dinamica = BE.ler_dados_apos_cabecalho(file)
    # Nome do DataFrame com o final __P
    nome_df_P = f"{nome_df}__P"
    
    # Recuperar o DataFrame com o final __P
    if nome_df_P in globals():
        df_P = globals()[nome_df_P]
    else:
        print(f"Atenção: O DataFrame {nome_df_P} não foi encontrado.")
        continue
    
    # Ajustar os dados para que o gráfico comece da segunda coluna
    y_values = df_P.iloc[0, 1:].values  # Ignora a primeira coluna (índice)

    # Desconsiderar os valores associados aos valores de x_plot a serem ignorados
    indices_para_remover = df_X[df_X['x_plot'].isin(x_plot_correcoes)].index
    x_filtered = df_X.drop(indices_para_remover)['x_plot'].values
    y_filtered = [y for i, y in enumerate(y_values) if i not in indices_para_remover]

    # Definir o título com base no nome do DataFrame (e corrigir o símbolo do grau)
    if nome_df == "df_neg6": 
        titulo = 'Alpha = -6°'
    elif nome_df == "df_neg4": 
        titulo = 'Alpha = -4°'
    elif nome_df == "df_neg2": 
        titulo = 'Alpha = -2°'
    elif nome_df == "df_0": 
        titulo = 'Alpha = 0°'
    elif nome_df == "df_2": 
        titulo = 'Alpha = 2°'
    elif nome_df == "df_4": 
        titulo = 'Alpha = 4°'
    elif nome_df == "df_6": 
        titulo = 'Alpha = 6°'
    elif nome_df == "df_16": 
        titulo = 'Alpha = 16°'

    # y_filtered --> pressões medidas
    # x_filtered --> pontos da corda certos
    pressão_dinamica = np.mean([p_dinamica[60],p_dinamica[61]])
    rho = cp.PropsSI('D', 'T', T_amb_K, 'P', P_atm, 'Air')
    C_p = [i/pressão_dinamica for i in y_filtered]
    C_n_trapz = BE.integrar_cp_trapezio(x_filtered,C_p)
    C_n_simps = BE.integrar_cp_simpson(x_filtered,C_p)
    v_inf = math.sqrt(2*pressão_dinamica/rho)
    print(f'v_inf: {v_inf}')
    print(f'C_n_simps: {C_n_simps}')
    print(f'C_n_trapz: {C_n_trapz}')
    print('-----------')
    # Criar o gráfico
    plt.figure(figsize=(10, 6))

    # Plotar os primeiros 29 pontos com cor azul
    plt.plot(x_filtered[:29], C_p[:29], 'bo-', label="Intradorso")

    # Plotar os últimos pontos com cor preta
    plt.plot(x_filtered[29:], C_p[29:], 'ko-', label="Extradorso")

    # Configurações do gráfico
    plt.title(titulo)
    plt.xlabel('x/c')
    plt.ylabel('Cp')
    plt.legend()
    plt.grid(True)

    # Inverter o sentido positivo do eixo Y
    plt.gca().invert_yaxis()

    # Exibir o gráfico
    plt.show()
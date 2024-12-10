import pandas as pd
import CoolProp.CoolProp as cp

# Função para calcular a área com a Regra de Simpson
def regra_simpson(x, y):
    h = (x[-1] - x[0]) / (len(x) - 1)
    area = y[0] + y[-1]
    for i in range(1, len(x) - 1, 2):
        area += 4 * y[i]
    for i in range(2, len(x) - 2, 2):
        area += 2 * y[i]
    area *= h / 3
    return area

# Dados do INMET
T_amb = 18.4  # Temperatura (°C)
T_amb_K = T_amb + 273.15  # Temperatura (K)
P_atm = 919.5 * 100  # Pressão (Pa)
rho = cp

# Diretórios dos dados experimentais
caminhos_arquivos = [
    (r"C:\Users\filip\Desktop\2024.2\Aerodinâmica\Ang -6.txt", "df_neg6"),
    (r"C:\Users\filip\Desktop\2024.2\Aerodinâmica\Ang -4.txt", "df_neg4"),
    (r"C:\Users\filip\Desktop\2024.2\Aerodinâmica\Ang -2.txt", "df_neg2"),
    (r"C:\Users\filip\Desktop\2024.2\Aerodinâmica\Ang 0.txt", "df_0"),
    (r"C:\Users\filip\Desktop\2024.2\Aerodinâmica\Ang 2.txt", "df_2"),
    (r"C:\Users\filip\Desktop\2024.2\Aerodinâmica\Ang 4.txt", "df_4"),
    (r"C:\Users\filip\Desktop\2024.2\Aerodinâmica\Ang 6.txt", "df_6"),
    (r"C:\Users\filip\Desktop\2024.2\Aerodinâmica\Ang 16.txt", "df_16")
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

# Criar o DataFrame df_areas_simp para armazenar as áreas (sem título de colunas no início)
df_areas_simp = pd.DataFrame(index=["Intradorso", "Extradorso", "Total"])

# Loop para ler e processar cada arquivo
for caminho_arquivo, nome_df in caminhos_arquivos:
    # Nome do ângulo a partir do nome do arquivo
    if nome_df == "df_neg6": 
        angulo = "-6"
    elif nome_df == "df_neg4": 
        angulo = "-4"
    elif nome_df == "df_neg2": 
        angulo = "-2"
    elif nome_df == "df_0": 
        angulo = "0"
    elif nome_df == "df_2": 
        angulo = "2"
    elif nome_df == "df_4": 
        angulo = "4"
    elif nome_df == "df_6": 
        angulo = "6"
    elif nome_df == "df_16": 
        angulo = "16"
    
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

    # Criar o DataFrame df_P (com as colunas de pressão, exceto as últimas duas)
    df_P = df_modificado.iloc[:, :-2]  # Seleciona todas as colunas exceto as últimas duas
    nome_df_P = f"{nome_df}__P"
    globals()[nome_df_P] = df_P

    # Ajustar os dados para que o gráfico comece da segunda coluna
    y_values = df_P.iloc[0, 1:].values  # Ignora a primeira coluna (índice)
    y_values_ajustado = y_values / 1000

    # Desconsiderar os valores associados aos valores de x_plot a serem ignorados
    indices_para_remover = df_X[df_X['x_plot'].isin(x_plot_correcoes)].index
    x_filtered = df_X.drop(indices_para_remover)['x_plot'].values
    y_filtered = [y for i, y in enumerate(y_values_ajustado) if i not in indices_para_remover]

    # Calcular as áreas utilizando a regra de Simpson
    area_intra_simps = regra_simpson(x_filtered[:29], y_filtered[:29])
    area_extra_simps = regra_simpson(x_filtered[29:], y_filtered[29:])

    # Adicionar as áreas no DataFrame df_areas_simp
    df_areas_simp[angulo] = [area_intra_simps, area_extra_simps, area_intra_simps - area_extra_simps]

    # Exibir as áreas calculadas
    #print(f"Área do intradorso ({angulo}°): {area_intra_simps:.6f}")
    #print(f"Área do extradorso ({angulo}°): {area_extra_simps:.6f}")

# Exibir o DataFrame final com as áreas calculadas
print("\nDataFrame com áreas calculadas:")
print(df_areas_simp)

c = 320*10**(-3) # Corda em metros

# Definir a função para calcular os valores de CN
def calcular_CN(df_areas_simp, c):
    # Criar um DataFrame vazio para armazenar os valores de CN, com uma única linha
    df_CN = pd.DataFrame(columns=df_areas_simp.columns)
    
    # Para cada coluna (ângulo) em df_areas_simp, calcular CN e armazenar
    df_CN.loc[0] = df_areas_simp.loc["Total"] / c  # Dividir a linha "Total" pela corda c
    
    return df_CN

# Variável da corda
c = 320 * 10**(-3)  # Corda em metros

# Calcular os valores de CN e armazenar no DataFrame df_CN
df_CN = calcular_CN(df_areas_simp, c)

# Exibir o DataFrame com os valores de CN
print("\nDataFrame com os valores de CN:")
print(df_CN)

import pandas as pd
import CoolProp.CoolProp as cp
import numpy as np

# Função para aplicar a regra de Simpson
def regra_simpson(x, y):
    """
    Aplica a regra de Simpson para calcular a área sob a curva definida por (x, y).
    x: Valores do eixo x (distâncias ou pontos)
    y: Valores do eixo y (valores das pressões ou outras grandezas)
    """
    # Converter y para um array NumPy
    y = np.array(y)
    
    # Número de intervalos
    n = len(x) - 1
    h = (x[-1] - x[0]) / n

    # Cálculo pela regra de Simpson
    soma_par = sum(y[2*i+1] for i in range((n-1)//2))
    soma_impar = sum(y[2*i+2] for i in range((n-1)//2))
    area = (h / 3) * (y[0] + y[-1] + 4 * soma_par + 2 * soma_impar)
    
    return area

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

# Criar o DataFrame df_areas_simp para armazenar as áreas (sem título de colunas no início)
df_areas_simp = pd.DataFrame(index=["Intradorso", "Extradorso", "Total"])

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

    # Calcular a área para Intradorso (linha 1)
    y_intrad = df_modificado.iloc[0, :-2].values  # Converte para um array NumPy
    area_intrad = regra_simpson(x_plot, y_intrad)

    # Calcular a área para Extradorso (linha 2)
    y_extrad = df_modificado.iloc[1, :-2].values  # Converte para um array NumPy
    area_extrad = regra_simpson(x_plot, y_extrad)

    # Preencher o DataFrame df_areas_simp com as áreas calculadas
    df_areas_simp[nome_df] = [area_intrad, area_extrad, area_intrad - area_extrad]  # Total é a diferença entre Intradorso e Extradorso

# Exibir o DataFrame final com as áreas calculadas
print('Integração por Regra de Simpson: ')
print(df_areas_simp)
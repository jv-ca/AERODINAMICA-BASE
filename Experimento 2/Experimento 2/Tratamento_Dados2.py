# Código para Prática 2 da disciplina Aerodinâmica
# Autor: Filipe Oliveira + GPTysson
# Criação: 31/02/2025
# última correção: 01/02/2025

import pandas as pd
import xlwings as xw
import os

# Diretório base
diretorio_base = r"C:\Users\joaov\OneDrive\Desktop\AERODINAMICA\Experimento 2\Experimento 2"

# Função para abrir múltiplos arquivos do Excel e extrair a coluna B
def abrir_planilhas(nomes_arquivos, nomes_colunas, diretorio):
    dados = {coluna: [] for coluna in nomes_colunas}
    
    app = xw.App(visible=False)  # Abre uma única instância do Excel
    try:
        max_linhas = 0  # Para alinhar tamanhos das colunas
        for nome_arquivo, nome_coluna in zip(nomes_arquivos, nomes_colunas):
            caminho = os.path.join(diretorio, nome_arquivo)
            if not os.path.exists(caminho):
                print(f"Erro: O arquivo {caminho} não foi encontrado.")
                continue
            
            try:
                wb = xw.Book(caminho)
                sheet = wb.sheets[0]
                valores = sheet.range("B2").expand("down").value
                
                # Se apenas um valor for lido, converte para lista
                valores = valores if isinstance(valores, list) else [valores]
                
                max_linhas = max(max_linhas, len(valores))
                dados[nome_coluna] = valores
                wb.close()

                #print(f"Dados da coluna B do arquivo {nome_arquivo} carregados com sucesso!")

            except Exception as e:
                print(f"Erro ao carregar {caminho}: {e}")

        # Padronizar o tamanho das colunas
        for coluna in dados:
            while len(dados[coluna]) < max_linhas:
                dados[coluna].append(None)

    finally:
        app.quit()  # Fecha a instância do Excel

    return pd.DataFrame.from_dict(dados, orient='index').transpose()

# Função para limpar os dados
def limpar_dados(df, remover_primeiros=30, manter_primeiros=50):
    df = df.replace({',': '.'}, regex=True).astype(float)  # Substitui vírgula por ponto e converte para float
    
    # Remove os primeiros valores e mantém apenas os primeiros 50
    df = df.iloc[remover_primeiros:].reset_index(drop=True).iloc[:manter_primeiros].reset_index(drop=True)
    
    return df

# Função para calcular a média das colunas
def calcular_media(df):
    return pd.DataFrame([df.mean()])

# ------------ Primeira parte: Correção do gráfico de tensão ------------
nomes_arquivos_correcao = ["v10_2025.xlsx", "v20_2025.xlsx", "v25_2025.xlsx", "v30_2025.xlsx", "v35_2025.xlsx"]
nomes_colunas_correcao = ["V10", "V20", "V25", "V30", "V35"]

df_dados_calibracao = abrir_planilhas(nomes_arquivos_correcao, nomes_colunas_correcao, diretorio_base)
df_dados_calibracao = limpar_dados(df_dados_calibracao)
df_correcao = calcular_media(df_dados_calibracao)

print('Valores de Correção: ')
print(df_correcao)

# ------------ Segunda parte: Dados da Aeronave ------------
nomes_arquivos_aeronave = ["Aeronave_v15.xlsx", "Aeronave_v20.xlsx", "Aeronave_v25.xlsx", "Aeronave_v30.xlsx", "Aeronave_v35.xlsx"]
df_aeronave_Volt = abrir_planilhas(nomes_arquivos_aeronave, nomes_colunas_correcao, diretorio_base)
df_aeronave_Volt = limpar_dados(df_aeronave_Volt)
df_aeronave_final = calcular_media(df_aeronave_Volt)

print("DataFrame final com as médias das Tensões para para Aeronave: ")
print(df_aeronave_final)

# ------------ Terceira parte: Dados das Esferas ------------
# Arquivos
dados_bolas = {
    "Golfe": ["Golfe_v10.xlsx", "Golfe_v20.xlsx", "Golfe_v35.xlsx"],
    "Lisa": ["Esferalisa_v10.xlsx", "Esferalisa_v20.xlsx", "Esferalisa_v35.xlsx"],
    "Vórtice": ["Esferavortice_v10.xlsx", "Esferavortice_v20.xlsx", "Esferavortice_v35.xlsx"]
}

# Criar DFs para cada tipo de esfera
dfs_bolas = {}
medias_esferas = {}

for tipo, arquivos in dados_bolas.items():
    df_temp = abrir_planilhas(arquivos, ["V10", "V20", "V35"], diretorio_base)
    df_temp = limpar_dados(df_temp)
    df_media = calcular_media(df_temp)
    
    dfs_bolas[tipo] = df_media
    medias_esferas[tipo] = df_media.values.flatten()  # Salva as médias no dicionário
    
    #print(f"Médias {tipo}:\n", df_media)

# Criando o DataFrame final com as médias de cada esfera
df_esferas_medias = pd.DataFrame.from_dict(
    medias_esferas, 
    orient="index", 
    columns=["V10", "V20", "V35"]
)

# Printando o DataFrame final
print("DataFrame final com as médias das Tensões para cada uma das esferas:")
print(df_esferas_medias)

# ------------ Quarta parte: Cálculo da Força ------------
g = 9.81

# Criando o DataFrame df_slope_mass com a fórmula dada
df_slope_mass = pd.DataFrame(
    {col: 5 / (4.91 - df_correcao[col].values[0]) for col in df_correcao.columns}, 
    index=["Slope_Mass"]
)

# Printando o novo DataFrame
print("DataFrame Slope Mass:")
print(df_slope_mass)

# Criando o DataFrame df_Forca_aeronave com a fórmula dada
df_Forca_aeronave = pd.DataFrame(
    {col: [(df_slope_mass[col].values[0] * (df_aeronave_final[col].values[0] - df_correcao[col].values[0])) * g]   #Os valores utilizados também são corrigidos a partir de df_correcao
     for col in df_slope_mass.columns}
)

# Printando o novo DataFrame
print("DataFrame Força Aeronave:")
print(df_Forca_aeronave)

# Encontrar colunas em comum entre df_slope_mass e df_esferas_medias
colunas_comuns = df_slope_mass.columns.intersection(df_esferas_medias.columns)

# Criar df_Forcas_esferas apenas com as colunas em comum
df_Forcas_esferas = pd.DataFrame(
    {
        col: (df_slope_mass[col].values[0] * (df_esferas_medias[col] - df_correcao[col].values[0])) * g          #Os valores utilizados também são corrigidos a partir de df_correcao
        for col in colunas_comuns
    },
    index=df_esferas_medias.index  # Mantendo a indexação de linhas de df_esferas_medias
)

# Printando o novo DataFrame
print("DataFrame Forças Esferas:")
print(df_Forcas_esferas)

# ------------ Quinta parte: Cálculo do Cd ------------
# Definir variáveis para dimensões e densidade do ar (rho)
rho = 1.079512  # Densidade do ar em kg/m³
df_dimensoes = [5.9514*10**-3, 5.0265*10**-3, 8.4949*10**-3, 8.4949*10**-3]
df_p_din = [0.5 * rho * (v**2) for v in [10, 20, 25, 30, 35]]  # Dinâmica de pressão para as velocidades

# Criar o DataFrame df_CD_aeronave
df_CD_aeronave = pd.DataFrame(
    {
        col: df_Forca_aeronave[col] / (df_p_din[i] * df_dimensoes[0]) 
        for i, col in enumerate(df_Forca_aeronave.columns)
    },
    index=df_Forca_aeronave.index
)

# Criar o DataFrame df_CD_esferas para Golfe, Lisa e Vórtice
df_CD_esferas = pd.DataFrame({
    col: df_Forcas_esferas[col] / (df_p_din[i] * df_dimensoes[j]) 
    for i, col in enumerate(df_Forcas_esferas.columns)
    for j, esfera in enumerate(['Golfe', 'Lisa', 'Vórtice'])
}, index=df_Forcas_esferas.index)

# Printando os DataFrames
print("Coeficiente de Arrasto da Aeronave (df_CD_aeronave):")
print(df_CD_aeronave)

print("Coeficiente de Arrasto das Esferas (df_CD_esferas):")
print(df_CD_esferas)

print("Pressão Dinâmica (10, 20, 25, 30, 35 m/s): ")
print(df_p_din)
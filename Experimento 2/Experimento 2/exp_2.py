import os
import pandas as pd
# ============================== ATT DADOS =========================== #
S_aeronave=5.9514 * (10**(-3))
S_esfera=8.4949 * (10**(-3))
S_golfe=5.0265 * (10**(-3))
q10=53.956
q15=121.401
q20=215.824
q25=337.225
q30=485.604
q35=660.961

# ============================== PARTE ORIGINAL =========================== #
velocidade = 35  # 10, 15, 20, 25, 30, 35
calibration_text = f'v{velocidade}'
aeronave_text = f'Aeronave_v{velocidade}'
esfera_lisa_text = f'Esferalisa_v{velocidade}'
esfera_vortice_text = f'Esferavortice_v{velocidade}'
golfe_text = f'Golfe_v{velocidade}'

# Função para ler arquivos e retornar os dados, se o arquivo existir
def ler_arquivo(arquivo):
    if os.path.exists(arquivo):
        return pd.read_excel(arquivo)
    else:
        print(f"Arquivo {arquivo} não encontrado.")
        return None

# ================ LEITURA DO ARQUIVO DE CALIBRAÇÃO ======================== #
calibration_file = ler_arquivo(f'{calibration_text}_2025.xlsx')

if calibration_file is not None:
    sum_calibration = calibration_file['Voltage_0'].sum()
    num_linhas = len(calibration_file['Voltage_0'])
    a = sum_calibration / num_linhas
else:
    sum_calibration = num_linhas = a = 0

# =============== LEITURA DO ARQUIVO DA AERONAVE ========================== #
exp_file_aeronave = ler_arquivo(f'{aeronave_text}.xlsx')

if exp_file_aeronave is not None:
    sum_calibration_exp_aeronave = exp_file_aeronave['Voltage_0'].sum()
    num_linhas_exp_aeronave = len(exp_file_aeronave['Voltage_0'])
    tensão_aeronave = sum_calibration_exp_aeronave / num_linhas_exp_aeronave
else:
    sum_calibration_exp_aeronave = num_linhas_exp_aeronave = tensão_aeronave = 0

# ============== LEITURA DO ARQUIVO DA ESFERA LISA ======================= #
exp_file_esfera_lisa = ler_arquivo(f'{esfera_lisa_text}.xlsx')

if exp_file_esfera_lisa is not None:
    sum_calibration_exp_esfera_lisa = exp_file_esfera_lisa['Voltage_0'].sum()
    num_linhas_exp_esfera_lisa = len(exp_file_esfera_lisa['Voltage_0'])
    tensão_esfera_lisa = sum_calibration_exp_esfera_lisa / num_linhas_exp_esfera_lisa
else:
    sum_calibration_exp_esfera_lisa = num_linhas_exp_esfera_lisa = tensão_esfera_lisa = 0

# ================ LEITURA DO ARQUIVO DA ESFERA COM GERADOR DE VÓRTICE ============== #
exp_file_esfera_vortice = ler_arquivo(f'{esfera_vortice_text}.xlsx')

if exp_file_esfera_vortice is not None:
    sum_calibration_exp_esfera_vortice = exp_file_esfera_vortice['Voltage_0'].sum()
    num_linhas_exp_esfera_vortice = len(exp_file_esfera_vortice['Voltage_0'])
    tensão_esfera_vortice = sum_calibration_exp_esfera_vortice / num_linhas_exp_esfera_vortice
else:
    sum_calibration_exp_esfera_vortice = num_linhas_exp_esfera_vortice = tensão_esfera_vortice = 0

# =============== LEITURA DO ARQUIVO DA BOLA DE GOLFE ============================ #
exp_file_golfe = ler_arquivo(f'{golfe_text}.xlsx')

if exp_file_golfe is not None:
    sum_calibration_exp_golfe = exp_file_golfe['Voltage_0'].sum()
    num_linhas_exp_golfe = len(exp_file_golfe['Voltage_0'])
    tensão_golfe = sum_calibration_exp_golfe / num_linhas_exp_golfe
else:
    sum_calibration_exp_golfe = num_linhas_exp_golfe = tensão_golfe = 0

# Calcular os valores de m e b
if a != 0:
    m = 48.919 / (4.91 - a)
    b = -(48.919 / (4.91 - a)) * a
else:
    m = b = 0

# Calcular a força de arrasto se os dados estiverem disponíveis
forca_de_arrasto_aeronave = m * tensão_aeronave + b if exp_file_aeronave is not None else 0
forca_de_arrasto_esfera_lisa = m * tensão_esfera_lisa + b if exp_file_esfera_lisa is not None else 0
forca_de_arrasto_esfera_vortice = m * tensão_esfera_vortice + b if exp_file_esfera_vortice is not None else 0
forca_de_arrasto_golfe = m * tensão_golfe + b if exp_file_golfe is not None else 0

# ============================== ATT CD =========================== #
q = q35
CD_aeronave = forca_de_arrasto_aeronave/(S_aeronave*q35)
CD_esfera_lisa = forca_de_arrasto_esfera_lisa/(S_esfera*q35)
CD_esfera_vortice = forca_de_arrasto_esfera_vortice/(S_esfera*q35)
CD_golfe = forca_de_arrasto_golfe/(S_golfe*q35)
print("CD_aeronave: ", CD_aeronave)
print("CD_esfera_lisa: ", CD_esfera_lisa)
print("CD_esfera_vortice: ", CD_esfera_vortice)
print("CD_golfe: ", CD_golfe)

# ============================== VERIFICAR RESULTADOS =========================== #
print(f"{'DADOS DA CALIBRAÇÃO':<30}")
print(f"Soma dos valores: {'':<5}{sum_calibration:<10}| N° de linhas: {'':<5}{num_linhas:<10}| Média(a): {'':<5}{a:<10}")
print(f"{'DADOS DO EXPERIMENTO (AERONAVE)':<30}")
print(f"Soma dos valores: {'':<5}{sum_calibration_exp_aeronave:<10}| N° de linhas: {'':<5}{num_linhas_exp_aeronave:<10}| Média: {'':<5}{tensão_aeronave:<10}")
if exp_file_aeronave is not None:
    print(f"Força de arrasto: {'':<5}{forca_de_arrasto_aeronave:<10} N | Conversão em peso: {'':<5}{forca_de_arrasto_aeronave / 9.7838:<10} kg")
else:
    print("Força de arrasto: Não disponível devido à ausência do arquivo")

print(f"{'DADOS DO EXPERIMENTO (ESFERA LISA)':<30}")
print(f"Soma dos valores: {'':<5}{sum_calibration_exp_esfera_lisa:<10}| N° de linhas: {'':<5}{num_linhas_exp_esfera_lisa:<10}| Média: {'':<5}{tensão_esfera_lisa:<10}")
if exp_file_esfera_lisa is not None:
    print(f"Força de arrasto: {'':<5}{forca_de_arrasto_esfera_lisa:<10} N | Conversão em peso: {'':<5}{forca_de_arrasto_esfera_lisa / 9.7838:<10} kg")
else:
    print("Força de arrasto: Não disponível devido à ausência do arquivo")

print(f"{'DADOS DO EXPERIMENTO (ESFERA COM GERADOR DE VÓRTICE)':<30}")
print(f"Soma dos valores: {'':<5}{sum_calibration_exp_esfera_vortice:<10}| N° de linhas: {'':<5}{num_linhas_exp_esfera_vortice:<10}| Média: {'':<5}{tensão_esfera_vortice:<10}")
if exp_file_esfera_vortice is not None:
    print(f"Força de arrasto: {'':<5}{forca_de_arrasto_esfera_vortice:<10} N | Conversão em peso: {'':<5}{forca_de_arrasto_esfera_vortice / 9.7838:<10} kg")
else:
    print("Força de arrasto: Não disponível devido à ausência do arquivo")

print(f"{'DADOS DO EXPERIMENTO (BOLA DE GOLFE)':<30}")
print(f"Soma dos valores: {'':<5}{sum_calibration_exp_golfe:<10}| N° de linhas: {'':<5}{num_linhas_exp_golfe:<10}| Média: {'':<5}{tensão_golfe:<10}")
if exp_file_golfe is not None:
    print(f"Força de arrasto: {'':<5}{forca_de_arrasto_golfe:<10} N | Conversão em peso: {'':<5}{forca_de_arrasto_golfe / 9.7838:<10} kg")
else:
    print("Força de arrasto: Não disponível devido à ausência do arquivo")

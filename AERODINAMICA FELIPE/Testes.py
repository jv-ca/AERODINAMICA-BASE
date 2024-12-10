import backend as BE
import os
import CoolProp.CoolProp as cp
import numpy as np
import math

# Configuração de diretório
workdir = os.getcwd() # Não mudar
angle_of_attack = 0 # Mudar para os ângulos de ataque da prática (0,2,4,6,16,-2,-4,-6)
workfile = f'/Ang {angle_of_attack}.txt' # Não mudar

# Dados da corda e dados a serem retirados da corda
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

x_plot_correcoes = [0.91097, 0.83004, 0.75148, 0.48034, 0.42901]
x_indices_correcoes = [2,4,6,14]

# Dados do INMET
T_amb = 18.4  # Temperatura (°C)
T_amb_K = T_amb + 273.15  # Temperatura (K)
P_atm = 919.5 * 100  # Pressão (Pa) -> 919500

# Download do arquivo de dados
file = f"{workdir}{workfile}"
raw_data = BE.ler_dados_apos_cabecalho(file) # hPa
indices_pressao_dinamica = [61,62]
indices_raw_data_correção = [2,4,6,47,14]

pressoes_dinamica = [raw_data[61],raw_data[62]]
pressoes_dinamica = [raw_data[61],raw_data[62]]
pressão_dinamica = np.mean(pressoes_dinamica)
print(pressão_dinamica)
'''
############# CÁLCULO DO CP ##############

Formula:

C_p = (p - p_inf)/q_inf

q_inf -> pressão dinamica (dados dos canais 60 e 61) -> q_inf = (rho*V_inf**2)/2
p_inf -> Pressão do escoamento livre
p -> pressão no ponto (dados obtidos)
'''
rho = cp.PropsSI('D', 'T', T_amb_K, 'P', P_atm, 'Air')
pressão_dinamica = np.mean(pressoes_dinamica) #
v_inf = math.sqrt(2*pressão_dinamica/rho)

C_p = [i/pressão_dinamica for i in raw_data]
print(len(C_p))
print(pressão_dinamica)
print(rho)
print(v_inf)


C_n_trapz = BE.integrar_cp_trapezio(x_plot,C_p)
C_n_simps = BE.integrar_cp_simpson(x_plot,C_p)

a = 1
while a < len(C_p):
    print(f'a: {a}')
    print(BE.integrar_cp_trapezio(x_plot[:a],C_p[:a]))
    print(BE.integrar_cp_simpson(x_plot[:a],C_p[:a]))
    a = a +1

BE.plot_gráfico(x_plot,C_p)

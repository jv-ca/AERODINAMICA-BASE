import matplotlib.pyplot as plt
import numpy as np
from uncertainties import ufloat
import CoolProp.CoolProp as CP
from CoolProp.CoolProp import PropsSI
import math
from math import pi,sqrt,exp 
from uncertainties import ufloat
import re
from scipy.integrate import simps

def process_line_to_list(line):
    """
    Converte uma linha de dados delimitada por ';' em uma lista.

    Args:
        line (str): Uma linha de texto no formato delimitado por ';'.

    Returns:
        list: Uma lista com os elementos da linha.
    """
    # Dividir a linha pelo delimitador ';'
    values = line.split(';')
    # Retorna a lista com os valores
    return values

def read_first_line_from_file(file_path):
    """
    Lê o arquivo especificado e retorna a primeira linha.

    Args:
        file_path (str): Caminho do arquivo.

    Returns:
        list: A primeira linha do arquivo, ou None se o arquivo estiver vazio.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            first_line = file.readline().strip()  # Lê e remove espaços/brancos extras
            first_line = process_line_to_list(first_line)
            return first_line if first_line else None
    except FileNotFoundError:
        print(f"Erro: Arquivo '{file_path}' não encontrado.")
        return None
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return None

def ler_dados_apos_cabecalho(caminho_arquivo):
    """
    Localiza o cabeçalho "Dados:" em um arquivo e lê a linha seguinte,
    removendo o primeiro e o segundo elemento e convertendo os restantes para float.

    Parâmetros:
    - caminho_arquivo (str): Caminho para o arquivo.

    Retorno:
    - list: Lista com os dados da linha de dados (após remoção dos dois primeiros elementos e conversão para float).
    """
    # Abrir e ler o arquivo
    with open(caminho_arquivo, 'r') as file:
        linhas = file.readlines()

    # Procurar pela linha que contém "Dados:"
    for i, linha in enumerate(linhas):
        if linha.strip() == "Dados:":
            # Verificar se existe uma linha logo após "Dados:"
            if i + 1 < len(linhas):
                linha_dados = linhas[i + 1].strip()
                break
            else:
                raise ValueError("Não há linha de dados após 'Dados:' no arquivo.")
    else:
        raise ValueError("Cabeçalho 'Dados:' não encontrado no arquivo.")

    # Dividir a linha pelo delimitador ";"
    dados = linha_dados.split(";")

    # Remover o 1° e 2° elemento e converter o restante para float
    dados_convertidos = [float(dado.replace(",", ".")) for dado in dados[2:]]

    return dados_convertidos

def plot_gráfico(x, y, titulo='Gráfico', xlabel='x/c', ylabel='Cp', limite=27):
    """
    Função para plotar um gráfico com duas curvas distintas, utilizando diferentes cores para o gráfico.

    Parâmetros:
    - x: Dados para o eixo X (lista ou array).
    - y: Dados para o eixo Y (lista ou array).
    - titulo: Título do gráfico.
    - xlabel: Rótulo do eixo X.
    - ylabel: Rótulo do eixo Y.
    - limite: Índice para separar os dois conjuntos de dados.
    """
    
    # Criar o gráfico
    plt.figure(figsize=(10, 6))

    # Plotar os primeiros 'limite' pontos com cor azul
    plt.plot(x[:limite], y[:limite], 'bo-', label="Intradorso")

    # Plotar os últimos pontos com cor preta
    plt.plot(x[limite:], y[limite:], 'ko-', label="Extradorso")

    # Configurações do gráfico
    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)

    # Inverter o sentido positivo do eixo Y
    plt.gca().invert_yaxis()

    # Exibir o gráfico
    plt.show()


def integrar_cp_trapezio(x, cp_values):
    """
    Função para calcular o valor de C_n (força normal) a partir de C_p usando o método dos trapézios.
    
    :param x_plot: Lista ou array de valores de x/c (abscissas).
    :param cp_values: Lista ou array de valores de C_p (coeficiente de pressão).
    :return: Lista de valores de C_n integrados.
    """
    # Verificando se os arrays de x_plot e cp_values têm o mesmo tamanho
    if len(x) != len(cp_values):
        raise ValueError("x_plot e cp_values devem ter o mesmo tamanho")
    
    # Calculando a integral de C_p usando o método dos trapézios
    cn_values = np.trapz(cp_values, x)
    
    # Retornando a integral de C_p (C_n)
    return cn_values

def integrar_cp_simpson(x_values, cp_values):
    """
    Calcula o coeficiente C_n integrando os valores de Cp ao longo de x/c usando o método de Simpson.
    
    Parâmetros:
        x_values (list ou ndarray): Valores de x/c (posição relativa ao longo da corda do perfil).
        cp_values (list ou ndarray): Valores de Cp (coeficiente de pressão) correspondentes.
    
    Retorno:
        float: Valor do coeficiente C_n.
    """
    # Verificação de entrada
    if len(x_values) != len(cp_values):
        raise ValueError("As listas x_values e cp_values devem ter o mesmo tamanho.")
    
    # Realiza a integração com Simpson
    cn = simps(cp_values, x_values)
    
    return cn
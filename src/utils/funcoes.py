import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import os
import time
from .dicionario_categorias import categorias_palavras_chave as contagem_palavras


df = pd.read_excel("C:/Users/Usuario/Desktop/bot_cadastrar/src/PRODUTOS.xlsx") # PC casa

# Função para categorizar o produto
def categorizar_produto(nome_produto):
    nome_produto = nome_produto.lower()  # Converter o nome do produto para letras minúsculas
    
    # Inicializa uma nova contagem de palavras para este produto
    contagem = {categoria: 0 for categoria in contagem_palavras.keys()}
    
    # Percorre o dicionário de categorias e palavras-chave
    for categoria, palavras in contagem_palavras.items():
        for palavra in palavras:
            if palavra in nome_produto:
                contagem[categoria] += 1  # Incrementa a contagem para a categoria

    # Filtra as categorias que têm pelo menos uma palavra-chave no nome do produto
    categorias_encontradas = {cat: count for cat, count in contagem.items() if count > 0}
    
    if len(categorias_encontradas) == 0:
        return "OUTROS"  # Nenhuma categoria encontrada
    
    # Se houver mais de uma categoria com palavras-chave encontradas
    if len(categorias_encontradas) > 1:
        # Ordena as categorias pela contagem de palavras-chave em ordem decrescente
        categorias_ordenadas = sorted(categorias_encontradas.items(), key=lambda x: x[1], reverse=True)
        
        # Verifica se há empate nas categorias mais relevantes
        if categorias_ordenadas[0][1] == categorias_ordenadas[1][1]:
            return "OUTROS"  # Empate entre categorias, retorna "OUTROS"
        else:
            return categorias_ordenadas[0][0]  # Retorna a categoria com mais palavras-chave
    else:
        # Se apenas uma categoria tiver palavras-chave, retorna essa categoria
        return list(categorias_encontradas.keys())[0]

# Função para localizar elementos com tentativa de recuperação
def localizar_elemento(navegador,xpath_elemento, timeout=10):
    # elemento_presente = navegador.find_elements(By.XPATH, xpath_elemento)
    # if len(elemento_presente) == 0:
    #     print(f"Elemento {xpath_elemento} não encontrado no DOM.")
    # else:
    #     print(f"Elemento {xpath_elemento} encontrado no DOM.")
    for _ in range(3):  # Tenta 3 vezes
        try:
            elemento = WebDriverWait(navegador, timeout).until(
                EC.visibility_of_element_located((By.XPATH, xpath_elemento))
            )
            # print('elemento...',elemento)
            return elemento
        except Exception as e:
            print(f"Tentativa falhou: {e}. Tentando novamente...")
            time.sleep(2)
    raise Exception(f"Falha ao localizar o elemento: {xpath_elemento}") 

# # Função para localizar elementos com tentativa de recuperação e maior detalhe de erro
# def localizar_elemento(xpath, timeout=15):
#     for tentativa in range(3):  # Tenta 3 vezes
#         try:
#             # Adiciona uma espera explícita para verificar se o elemento está visível e clicável
#             elemento = WebDriverWait(navegador, timeout).until(
#                 EC.element_to_be_clickable((By.XPATH, xpath))
#             )
#             print(f"Elemento localizado com sucesso na tentativa {tentativa + 1}")
#             return elemento
#         except Exception as e:
#             print(f"Tentativa {tentativa + 1} falhou: {e}. Tentando novamente em 2 segundos...")
#             time.sleep(2)  # Espera um pouco antes de tentar novamente
#     raise Exception(f"Falha ao localizar o elemento após 3 tentativas: {xpath}")


# Função para localizar e interagir com elementos com tentativas de relocalização
def interagir_com_elemento(navegador,xpath, acao, tentativas=3):
    for tentativa in range(tentativas):
        try:
            # Localiza o elemento
            elemento = WebDriverWait(navegador, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            
            # Executa a ação desejada no elemento
            acao(elemento)
            break  # Se a interação foi bem-sucedida, sai do loop
        except StaleElementReferenceException:
            print(f"Tentativa {tentativa + 1} falhou devido ao erro 'stale element'. Tentando novamente...")
            time.sleep(2)  # Espera um pouco antes de tentar novamente
        except Exception as e:
            print(f"Erro ao tentar interagir com o elemento: {e}")
            break  # Sai do loop se outro erro ocorrer

# def aguardar_loading_desaparecer(timeout=30):
#     try:
#         # Aguarda até que o elemento com id="loading" apareça com display="block"
#         WebDriverWait(navegador, timeout).until(
#             EC.presence_of_element_located((By.ID, "loading"))
#         )
        
#         # Aguarda até que o display do elemento com id="loading" seja "none"
#         WebDriverWait(navegador, timeout).until(
#             lambda driver: driver.execute_script("return document.getElementById('loading').style.display") == "none"
#         )
#         print("Carregamento completo.")
#     except Exception as e:
#         print(f"Erro ao aguardar o desaparecimento do loading: {e}")

def aguardar_loading_desaparecer(navegador,timeout=30):
    try:
        WebDriverWait(navegador, timeout).until(
            lambda driver: driver.execute_script("""
                var loading = document.getElementById('loading');
                if (loading) {
                    return loading.style.display === 'none';
                }
                return true;
            """)
        )
        print("Carregamento completo.")
    except Exception as e:
        print(f"Erro ao aguardar o desaparecimento do loading: {e}")


def inserir_codigo_barras(navegador, codigo_barras):
    try:
        # Localiza o campo de código de barras e insere o código
        campo_codigo_barras = navegador.find_element(By.XPATH, '/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[1]/div[1]/div[3]/input')
        campo_codigo_barras.clear()
        campo_codigo_barras.send_keys(codigo_barras)
        
        # Clica no campo do grupo de produto (ou qualquer campo para avançar no processo)
        campo_grupo_produto = navegador.find_element(By.XPATH, '/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[1]/div[1]/div[4]/div/input')
        campo_grupo_produto.click()
        
        # Aguarda um tempo para verificar se aparece o pop-up de erro
        time.sleep(2)
        
         # Espera explícita para verificar se o pop-up aparece
        try:
            # Aguarda até que o pop-up apareça por até 5 segundos
            popup_mensagem = WebDriverWait(navegador, 5).until(
                EC.visibility_of_element_located((By.XPATH, '//*[contains(text(),"Já existe um produto utilizando este código de barra!")]'))
            )

            if popup_mensagem:
                print("Código de barras já cadastrado. Fechando pop-up.")
            
                # Fecha o pop-up clicando no botão "OK"
                botao_ok = navegador.find_element(By.XPATH, '/html/body/div[6]/div[1]/div/div/footer/button')
                botao_ok.click()
                return True
            
            # Espera o pop-up desaparecer antes de continuar
            time.sleep(1)
            
            # Reinterage com o campo do grupo de produto
            campo_grupo_produto = navegador.find_element(By.XPATH, '//*[@id="grupo_produto"]')
            campo_grupo_produto.click()
            return True

        except TimeoutException:
            # Se o pop-up não aparecer, continua normalmente
            print("Código de barras inserido com sucesso. Nenhum pop-up encontrado.")
        # if popup_mensagem:
        #     # Fecha o pop-up clicando no botão "OK"
        #     botao_ok = navegador.find_element(By.XPATH, '/html/body/div[5]/div[1]/div/div/footer/button')
        #     botao_ok.click()
            
        #     # Espera o pop-up desaparecer antes de continuar
        #     time.sleep(2)
            
        #     # Reinterage com o campo do grupo de produto
        #     campo_grupo_produto = navegador.find_element(By.XPATH, '/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[1]/div[1]/div[4]/div/input')
        #     campo_grupo_produto.click()
            
        #     time.sleep(1)

        #     campo_codigo_barras.click()
        #     campo_codigo_barras.clear()
        #     time.sleep(1)
            
    except NoSuchElementException:
        # Se não encontrar o pop-up, continua o fluxo normalmente
        time.sleep(2)
        pass
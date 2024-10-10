import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
import os
import time
from .dicionario_categorias import categorias_palavras_chave as contagem_palavras



# df = pd.read_excel("C:/Users/Usuario/Desktop/bot_cadastrar/src/cadastro_produtos_matriz.xlsx") # PC casa
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


# Função para localizar elementos com tentativa de recuperação
def localizar_elemento(navegador, xpath_elemento, timeout=10):
    for _ in range(3):  # Tenta 3 vezes
        try:
            elemento = WebDriverWait(navegador, timeout).until(
                EC.visibility_of_element_located((By.XPATH, xpath_elemento))
            )
            return elemento
        except TimeoutException:
            print(f"Tentativa falhou: Timeout ao localizar o elemento. Tentando novamente...")
            time.sleep(2)
        except StaleElementReferenceException as e:
            print(f"Tentativa falhou: {e}. Tentando novamente...")
            time.sleep(2)
    raise NoSuchElementException(f"Falha ao localizar o elemento após várias tentativas: {xpath_elemento}")

# Função para interagir com elemento com múltiplas tentativas
def interagir_com_elemento(navegador, xpath, acao, tentativas=3):
    for tentativa in range(tentativas):
        try:
            elemento = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            acao(elemento)
            print(f"Interação com o elemento {xpath} realizada com sucesso.")
            return True  # Retorna True se a interação foi bem-sucedida
        except (StaleElementReferenceException, ElementClickInterceptedException) as e:
            print(f"Erro na tentativa {tentativa + 1}: {e}. Tentando novamente...")
            time.sleep(2)  # Espera um pouco antes de tentar novamente
        except Exception as e:
            print(f"Erro ao tentar interagir com o elemento: {e}")
            return False
    return False  # Retorna False se falhar após todas as tentativas

# Função para localizar elemento visível e clicável com tentativa de recuperação
def localizar_elemento_visivel_e_clicavel(navegador, xpath_elemento, timeout=10):
    for tentativa in range(3):  # Tenta 3 vezes
        try:
            elemento = WebDriverWait(navegador, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath_elemento))  # Espera até estar clicável
            )
            # Rola para o elemento para garantir que está visível na tela
            navegador.execute_script("arguments[0].scrollIntoView(true);", elemento)
            return elemento
        except TimeoutException:
            print(f"Tentativa {tentativa + 1} falhou: Timeout ao localizar o elemento. Tentando novamente...")
            time.sleep(2)
        except StaleElementReferenceException as e:
            print(f"Tentativa {tentativa + 1} falhou: {e}. Tentando novamente...")
            time.sleep(2)
    raise NoSuchElementException(f"Falha ao localizar o elemento após várias tentativas: {xpath_elemento}")

# Função para interagir com elemento visível e clicável
def interagir_com_elemento_visivel(navegador, xpath, acao, tentativas=3):
    for tentativa in range(tentativas):
        try:
            # Localiza o elemento visível e clicável
            elemento = localizar_elemento_visivel_e_clicavel(navegador, xpath)
            acao(elemento)
            print(f"Interação com o elemento {xpath} realizada com sucesso.")
            return True  # Retorna True se a interação foi bem-sucedida
        except (StaleElementReferenceException, ElementClickInterceptedException) as e:
            print(f"Erro na tentativa {tentativa + 1}: {e}. Tentando novamente...")
            time.sleep(2)  # Espera um pouco antes de tentar novamente
        except Exception as e:
            print(f"Erro ao tentar interagir com o elemento: {e}")
            return False
    return False  # Retorna False se falhar após todas as tentativas


def interagir_com_elemento_forcado(navegador, xpath, tentativas=3):
    """
    Função que tenta interagir com um elemento, forçando a interação via JavaScript em caso de falha.
    """
    for tentativa in range(tentativas):
        try:
            # Localiza o elemento
            elemento = WebDriverWait(navegador, 10).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            # Tenta clicar no elemento normalmente
            elemento.click()
            print(f"Interação com o elemento {xpath} realizada com sucesso.")
            return True
        except Exception as e:
            print(f"Tentativa {tentativa + 1} falhou: {e}. Tentando novamente com JavaScript...")
            try:
                # Força o clique via JavaScript
                elemento_js = navegador.find_element(By.XPATH, xpath)
                navegador.execute_script("arguments[0].click();", elemento_js)
                print(f"Interação forçada via JavaScript com sucesso no elemento: {xpath}")
                return True
            except Exception as e_js:
                print(f"Erro ao tentar forçar a interação com o elemento via JavaScript: {e_js}")
                time.sleep(2)
    return False  # Retorna False se falhar após todas as tentativas

# Função para inserir código de barras
def inserir_codigo_barras(navegador, codigo_barras):
    try:
        # Localiza o campo de código de barras pelo ID e insere o código
        campo_codigo_barras = navegador.find_element(By.ID, 'codigo_barra')
        campo_codigo_barras.clear()
        campo_codigo_barras.send_keys(codigo_barras)
        
        # Clica no campo do grupo de produto usando o ID
        campo_grupo_produto = navegador.find_element(By.ID, 'grupo')
        campo_grupo_produto.click()
        
        # Aguarda um tempo para verificar se aparece o pop-up de erro
        time.sleep(2)

        # Verifica se aparece a mensagem de "Digite um código válido"
        try:
            mensagem_invalida = WebDriverWait(navegador, 5).until(
                EC.visibility_of_element_located((By.XPATH, '//div[@class="d-block invalid-feedback" and contains(text(),"Digite um código válido")]'))
            )
            if mensagem_invalida:
                print("Código de barras inválido detectado.")
                campo_codigo_barras.clear()
                return False
                
        except TimeoutException:
            print("Código de barras válido. Nenhuma mensagem de erro de código inválido detectada.")
        
        while True:
            try:
                # Verifica se o popup aparece
                # localizar_elemento(navegador, '//*[contains(text(),"Já existe um produto utilizando este código de barra!")]')

                popup_mensagem = WebDriverWait(navegador, 5).until(
                EC.visibility_of_element_located((By.XPATH, '//*[contains(text(),"Já existe um produto utilizando este código de barra!")]'))
            )
                
                    
                print('Popup de código de barras já existente detectado.')

                # Fecha o popup clicando no botão OK
                botao_ok = navegador.execute_script("""
                    return document.querySelector('button.btn.btn-primary[type="button"][value="true"]');
                """)
                botao_ok.click()

                # Espera o popup desaparecer antes de continuar
                WebDriverWait(navegador, 5).until(
                    EC.invisibility_of_element_located((By.XPATH, '//*[contains(text(),"Já existe um produto utilizando este código de barra!")]'))
                )
                print('Popup desapareceu.')

                campo_codigo_barras = navegador.find_element(By.ID, 'codigo_barra')
                campo_codigo_barras.clear()

                # Reinterage com o campo do grupo de produto
                campo_grupo_produto = navegador.find_element(By.ID, 'grupo')
                campo_grupo_produto.click()
                break  # Sai do loop se tudo ocorrer bem
                

            except TimeoutException:
                print("Código de barras inserido com sucesso. Nenhum pop-up encontrado.")
                break  # Sai do loop quando não há popup

            except Exception as e:
                print(f'Erro ao lidar com o popup: {e}')
                time.sleep(1)  # Tenta novamente após um curto intervalo

    except NoSuchElementException:
        time.sleep(2)
        pass



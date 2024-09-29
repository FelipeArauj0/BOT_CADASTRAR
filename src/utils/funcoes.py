import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import os
import time
from .dicionario_categorias import categorias_palavras_chave as contagem_palavras

navegador = webdriver.Chrome()
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
def localizar_elemento(xpath, timeout=10):
    for _ in range(3):  # Tenta 3 vezes
        try:
            return WebDriverWait(navegador, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        except Exception as e:
            print(f"Tentativa falhou: {e}. Tentando novamente...")
            time.sleep(2)
    raise Exception(f"Falha ao localizar o elemento: {xpath}")

# Função para localizar e interagir com elementos com tentativas de relocalização
def interagir_com_elemento(xpath, acao, tentativas=3):
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

def aguardar_loading_desaparecer(timeout=30):
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


def processo_cadastrar_produtos():
    for index, row in df.iterrows():
        nome_produto = row['nome']
        preco_produto = row['valor de venda']
        estoque_min = row['estoque-min']
        estoque_max = row['estoque-max']
        estoque_atual = row['estoque-atual']
    
        # Verifica se o produto existe
        try:
            # Determina a categoria do produto
            categoria_produto = categorizar_produto(nome_produto)

            aguardar_loading_desaparecer()
            time.sleep(1)

            #clica no campo buscar produto
            campo_busca = localizar_elemento('/html/body/div[2]/div/div/aside[2]/div/div/section/div/div[1]/div/div[2]/form/div/input')
            campo_busca.clear()
            campo_busca.send_keys(nome_produto)
            campo_busca.send_keys(Keys.RETURN)
            
            # Aguarda
            aguardar_loading_desaparecer()
            time.sleep(1)
            
            mensagem_nao_encontrado = navegador.find_elements(By.XPATH, '/html/body/div[2]/div/div/aside[2]/div/div/section/div/div[2]/div[2]/h3')
            if len(mensagem_nao_encontrado) > 0 and mensagem_nao_encontrado[0].text == "Nenhum produto foi encontrado!":
                print(f'Produto "{nome_produto}" não está cadastrado. Procedendo com o cadastro...')
                
                # Aguarda
                aguardar_loading_desaparecer()
                time.sleep(1)

                # Clica no botão para adicionar um novo produto
                adicionar_produtos = localizar_elemento('/html/body/div[2]/div/div/aside[2]/div/div/section/div/div[1]/div/div[1]/a')
                adicionar_produtos.click()

                # Aguarda
                aguardar_loading_desaparecer()
                time.sleep(1)

                # Preenche o NOME do produto
                adicionar_nome_produto = localizar_elemento('/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[1]/div[1]/div[1]/input')
                adicionar_nome_produto.send_keys(nome_produto)
                
                # Aguarda
                time.sleep(1)

                # Clica para GERAR o código interno
                gerar_codigoInterno = localizar_elemento('/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[1]/div[1]/div[2]/div/div/button')
                gerar_codigoInterno.click()

                # Aguarda
                time.sleep(1)

                # Seleciona a categoria do produto
                campo_grupo_produto = localizar_elemento('//*[@id="grupo"]')
                campo_grupo_produto.send_keys(categoria_produto)

                # Aguarda
                time.sleep(1)


                # Aba "Valores"
                aba_valores = localizar_elemento('//*[text()="Valores"]')
                aba_valores.click()

                time.sleep(1)

                # Preenche o valor de venda
                campo_valor_venda = localizar_elemento('/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[3]/div/div[2]/div/div[2]/div[2]/table/tbody/tr/td[4]/input')
                campo_valor_venda.clear()
                campo_valor_venda.send_keys(str(preco_produto))

                # Aguarda
                time.sleep(1)

                # Aba "Estoque"
                aba_estoque = localizar_elemento('//*[text()="Estoque"]')
                aba_estoque.click()

                # Aguarda
                time.sleep(1)

                # Preenche campos de estoque
                campo_estoque_min = localizar_elemento('/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[4]/div/div[1]/div[1]/input')
                campo_estoque_min.clear()
                campo_estoque_min.send_keys(str(estoque_min))



                campo_estoque_max = localizar_elemento('/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[4]/div/div[1]/div[2]/input')
                campo_estoque_max.clear()
                campo_estoque_max.send_keys(str(estoque_max))

                campo_estoque_atual = localizar_elemento('/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[4]/div/div[1]/div[3]/input')
                campo_estoque_atual.clear()
                campo_estoque_atual.send_keys(str(estoque_atual))

                # Aguarda
                time.sleep(1)

                # Cadastra o produto
                cadastrar_produto = localizar_elemento('/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[2]/button')
                cadastrar_produto.click()

                # Aguarda loading desaparecer
                aguardar_loading_desaparecer()
                time.sleep(1)


                
            else:
                print(f'Produto "{nome_produto}" já está cadastrado. Pulando para o próximo produto...')
                interagir_com_elemento('//*[@id="app"]/div/div/aside[1]/section/ul/li[2]/ul/li[1]/a', lambda elem: elem.click())
                # aguardar_loading_desaparecer()
                # navegador.refresh()
                # aguardar_loading_desaparecer()
                time.sleep(1)


        except Exception as e:
            print(f"Erro ao verificar se o produto está cadastrado: {e}")
            continue
    
        # Atualiza a página
        navegador.refresh()
        aguardar_loading_desaparecer()
        time.sleep(1)

        print("Produto cadastrado com sucesso!")
    print("Todos os produtos foram cadastrados com sucesso!")


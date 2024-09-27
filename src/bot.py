import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from utils.funcoes import categorizar_produto
from utils.funcoes import verificar_produto

navegador = webdriver.Chrome()

navegador.get("https://gestaoclick.com/inicio")
print("Diretório de trabalho atual:", os.getcwd())
# df = pd.read_excel("C:/Users/AlgoMais/Documents/BOT_CADASTRAR/src/PRODUTOS.xlsx") #loja pc esquerdo
df = pd.read_excel("C:/Users/Usuario/Desktop/bot_cadastrar/src/PRODUTOS.xlsx") # PC casa
# df = pd.read_excel("C:/Users/Usuario/Desktop/bot_cadastrar/src/cadastro_produtos_matriz.xlsx")
# print(df)

#efetuar login no site
campo_email = navegador.find_element(By.XPATH, '//*[@id="email"]')
campo_email.send_keys("algomais.com2012@gmail.com")

campo_senha = navegador.find_element(By.XPATH, '//*[@id="senha"]')
campo_senha.send_keys("Algomais2012@")

campo_senha.send_keys(Keys.RETURN)

# Aguarda um pouco
time.sleep(2)

try:
    # Navega até a página de produtos
    menu_produtos = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/aside[1]/section/ul/li[2]/a'))
    )
    menu_produtos.click()

    time.sleep(2)
    
    # Localiza e clica na opção "Gerenciar Produtos"
    gerenciar_produtos = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/aside[1]/section/ul/li[2]/ul/li[1]/a'))
    )
    gerenciar_produtos.click()

    time.sleep(2)

    
    # Verifica se o produto está cadastrado
    print('Produto não cadastrado. Iniciando o cadastro...')
    for index, row in df.iterrows():
        nome_produto = row['nome']
        preco_produto = row['valor de venda']
        estoque_min = row['estoque-min']
        estoque_max = row['estoque-max']
        estoque_atual = row['estoque-atual']
       

        # Determina a categoria do produto
        categoria_produto = categorizar_produto(nome_produto)

        #clica no campor buscar produto
        campo_busca = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/aside[2]/div/div/section/div/div[1]/div/div[2]/form/div/input'))
            )
        campo_busca.send_keys(nome_produto)
        campo_busca.send_keys(Keys.RETURN)

        # Aguarda os resultados da busca
        time.sleep(2)

        produto_na_lista = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/aside[2]/div/div/section/div/div[2]/div[1]/table/tbody/tr/td[2]'))  # XPATH correto
        )
        if produto_na_lista:
            print(f'Produto "{nome_produto}" já está cadastrado. Pulando para o próximo...')
            continue  # Produto encontrado, pula para o próximo produto

        # Verifica se a mensagem de "Nenhum produto foi encontrado" aparece
        
        mensagem_nao_encontrado = navegador.find_element(By.XPATH, '/html/body/div[2]/div/div/aside[2]/div/div/section/div/div[2]/div[2]/h3')
        if mensagem_nao_encontrado:
            print(f'Produto "{nome_produto}" não está cadastrado. Procedendo com o cadastro...')
            # Produto não encontrado, proceder com o cadastro

            time.sleep(2)

            try:
                # Clica no botão para adicionar um novo produto
                adicionar_produtos = WebDriverWait(navegador, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/aside[2]/div/div/section/div/div[1]/div/div[1]/a'))
                )
                adicionar_produtos.click()

                # Verifica se o botão foi clicado com sucesso
                WebDriverWait(navegador, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="nome"]'))
                )
                print("Página de cadastro aberta com sucesso. Preenchendo os dados...")
            except Exception as e:
                print(f"Erro ao tentar adicionar produto: {e}")
                continue  # Pule para o próximo produto em caso de erro

            # Clica para gerar o código interno
            gerar_codigoInterno = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[1]/div[1]/div[2]/div/div/button'))
            )
            gerar_codigoInterno.click()

            campo_grupo_produto = WebDriverWait(navegador, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="grupo"]')) 
            )
            campo_grupo_produto.send_keys(categoria_produto)

            time.sleep(2)
            
            # Aba "Valores"
            aba_valores = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[text()="Valores"]'))
            )
            aba_valores.click()

            # Preenche o campo de valor de venda
            campo_valor_venda = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[3]/div/div[2]/div/div[2]/div[2]/table/tbody/tr/td[4]/input'))
            )
            campo_valor_venda.clear()
            campo_valor_venda.send_keys((str(preco_produto)))

            time.sleep(2)

            # Aba "Estoque"
            aba_estoque = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[text()="Estoque"]'))
            )
            aba_estoque.click()

            # Preenche campos de estoque
            campo_estoque_min = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[4]/div/div[1]/div[1]/input'))
            )
            campo_estoque_min.clear()
            campo_estoque_min.send_keys((str(estoque_min)))

            campo_estoque_max = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[4]/div/div[1]/div[2]/input'))
            )
            campo_estoque_max.clear()
            campo_estoque_max.send_keys((str(estoque_max)))

            campo_estoque_atual = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[4]/div/div[1]/div[3]/input'))
            )
            campo_estoque_atual.clear()
            campo_estoque_atual.send_keys((str(estoque_atual)))

            # Cadastra o produto
            cadastrar_produto = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[2]/button'))
            )
            cadastrar_produto.click()

            time.sleep(1)

            # Atualiza a página para adicionar o próximo produto
            navegador.refresh()

            time.sleep(2)
                # except:
                #     print(f"Erro ao verificar a existência do produto {nome_produto}.")
                #     continue

        # except Exception as e:
        #     print(f"Erro ao buscar o produto: {e}")
        #     continue

        # Retorna True se todos os produtos já estão cadastrados


        

        print("Todos os produtos foram cadastrados com sucesso!")

except Exception as e:
    print(f"Erro: {e}")

# Mantém a janela aberta até o usuário decidir fechar
input("Pressione enter para fechar...")
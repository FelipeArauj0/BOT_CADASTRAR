import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import os
import time
from utils.funcoes import categorizar_produto
from utils.funcoes import localizar_elemento
from utils.funcoes import interagir_com_elemento
from utils.funcoes import aguardar_loading_desaparecer
# from utils.funcoes import processo_cadastrar_produtos
from utils.navegador import iniciar_navegador
from utils.funcoes import inserir_codigo_barras
import math



navegador = iniciar_navegador()
navegador.get('https://gestaoclick.com/')
# print("Diretório de trabalho atual:", os.getcwd())
# df = pd.read_excel("C:/Users/Usuario/Desktop/bot_cadastrar/src/cadastro_produtos_matriz.xlsx") # PC casa
df = pd.read_excel("C:/Users/Usuario/Desktop/bot_cadastrar/src/PRODUTOS.xlsx") # PC casa

#efetuar login no site
campo_email = navegador.find_element(By.XPATH, '//*[@id="email"]')
campo_email.send_keys("algomais.com2012@gmail.com")

campo_senha = navegador.find_element(By.XPATH, '//*[@id="senha"]')
campo_senha.send_keys("Algomais2012@")

campo_senha.send_keys(Keys.RETURN)

# Aguarda
time.sleep(2)
aguardar_loading_desaparecer(navegador)

try:
    # menu loja
    menu_loja = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/aside[1]/section/div/div[2]/ul/li/a'))
    )
    menu_loja.click()

    time.sleep(2)

    # clicla loja nordeste
    loja_nordeste = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/aside[1]/section/div/div[2]/ul/li/ul/li[1]/a'))
    )
    loja_nordeste.click()
    
    aguardar_loading_desaparecer(navegador)
    time.sleep(1)

    mensagem_logado_nordeste = navegador.find_elements(By.XPATH, '/html/body/div[5]/div[1]/div/div/div/div')
    if mensagem_logado_nordeste[0].text == "Você já está logado na loja ALGO+ NORDESTE!":
        #clica botao ok
        botao_ok = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[1]/div/div/footer/button'))
        )
        botao_ok.click()

        time.sleep(1)

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

        MAX_tentativas = 3
        # processo_cadastrar_produtos()
        for index, row in df.iterrows():
            nome_produto = row['nome']
            codigo_barras = row['codigo de barra']
            preco_produto = row['valor de venda']
            estoque_min = row['estoque-min']
            estoque_max = row['estoque-max']
            estoque_atual = row['estoque-atual']
            print('codigo barras.....',str(codigo_barras).strip())
            
            tentativas = 0
            sucess = False

            while tentativas < MAX_tentativas and not sucess:

                # Verifica se o produto existe
                try:
                    # Determina a categoria do produto
                    categoria_produto = categorizar_produto(nome_produto)

                    aguardar_loading_desaparecer(navegador)
                    time.sleep(1)

                    

                    # #clica no campo buscar produto
                    campo_busca = localizar_elemento(navegador,'/html/body/div[2]/div/div/aside[2]/div/div/section/div/div[1]/div/div[2]/form/div/input')
                    campo_busca.clear()
                    campo_busca.send_keys(nome_produto)
                    campo_busca.send_keys(Keys.RETURN)
                    
                    # Aguarda
                    aguardar_loading_desaparecer(navegador)
                    time.sleep(1)
                    
                    mensagem_nao_encontrado = navegador.find_elements(By.XPATH, '/html/body/div[2]/div/div/aside[2]/div/div/section/div/div[2]/div[2]/h3')
                    if len(mensagem_nao_encontrado) > 0 and mensagem_nao_encontrado[0].text == "Nenhum produto foi encontrado!":
                        print(f'Produto "{nome_produto}" não está cadastrado. Procedendo com o cadastro...')
                        
                        # Aguarda
                        time.sleep(1)

                        # Clica no botão para adicionar um novo produto
                        adicionar_produtos = localizar_elemento(navegador,'/html/body/div[2]/div/div/aside[2]/div/div/section/div/div[1]/div/div[1]/a')
                        adicionar_produtos.click()

                        # Aguarda
                        aguardar_loading_desaparecer(navegador)
                        time.sleep(1)

                        # Preenche o NOME do produto
                        adicionar_nome_produto = localizar_elemento(navegador,'/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[1]/div[1]/div[1]/input')
                        adicionar_nome_produto.send_keys(nome_produto)
                        
                        # Aguarda
                        time.sleep(1)

                        # Clica para GERAR o código interno
                        gerar_codigoInterno = localizar_elemento(navegador,'/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[1]/div[1]/div[2]/div/div/button')
                        gerar_codigoInterno.click()

                        # Aguarda
                        time.sleep(1)                       
                        
                        #se tiver codigo de barras adiciona se nao pula para categoria
                        if codigo_barras and str(codigo_barras).strip() and str(codigo_barras).lower() != "nan":  
                            try:
                                inserir_codigo_barras(navegador, str(codigo_barras).split('.')[0])
                            except Exception as e:
                                print(f"Erro ao inserir o código de barras: {e}")
                        
                        print('passei pelo if....')
                    
                        # Aguarda
                        time.sleep(1)
                    
                        

                        # Insere a categoria do produto
                        inserir_grupo_produto = localizar_elemento(navegador,'/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[1]/div[1]/div[4]/div/input')
                        inserir_grupo_produto.clear()
                        inserir_grupo_produto.send_keys(categoria_produto)

                        # Aguarda
                        time.sleep(1)

                        # Aba "Valores"
                        aba_valores = localizar_elemento(navegador,'//*[text()="Valores"]')
                        aba_valores.click()

                        time.sleep(1)
                        print('campo valor venda')
                        print(preco_produto)
                        print('campo valor venda igual a nan => ')
                        print(str(preco_produto).lower())
                        if preco_produto and str(preco_produto).lower() != "nan":
                            # Preenche o valor de venda
                            campo_valor_venda = localizar_elemento(navegador,'/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[3]/div/div[2]/div/div[2]/div[2]/table/tbody/tr/td[4]/input')
                            campo_valor_venda.clear()
                            campo_valor_venda.send_keys(int(preco_produto))
                            
                            # Aguarda
                            time.sleep(1)

                            # Aba "Estoque"
                            aba_estoque = localizar_elemento(navegador,'//*[text()="Estoque"]')
                            aba_estoque.click()

                            # Aguarda
                            time.sleep(1)

                            # Preenche campos de estoque
                            campo_estoque_min = localizar_elemento(navegador,'/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[4]/div/div[1]/div[1]/input')
                            campo_estoque_min.clear()
                            campo_estoque_min.send_keys(str(estoque_min))



                            campo_estoque_max = localizar_elemento(navegador,'/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[4]/div/div[1]/div[2]/input')
                            campo_estoque_max.clear()
                            campo_estoque_max.send_keys(str(estoque_max))

                            campo_estoque_atual = localizar_elemento(navegador,'/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[4]/div/div[1]/div[3]/input')
                            campo_estoque_atual.clear()
                            campo_estoque_atual.send_keys(str(estoque_atual))

                            # Aguarda
                            time.sleep(1)

                            menu_lojas = localizar_elemento(navegador, '/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[1]/ul/li[9]/a')
                            menu_lojas.click()

                            # Aguarda
                            time.sleep(1)

                            # # Aguarda até que a checkbox esteja visível e clicável
                            # try:
                            #     retirar_loja_vale = WebDriverWait(navegador, 10).until(
                            #         EC.element_to_be_clickable((By.ID, '__BVID__656'))
                            #     )
                            #     print("Checkbox localizada.")
    
                            #     # Usa JavaScript para verificar se a checkbox está marcada
                            #     is_checked = navegador.execute_script("return arguments[0].checked;", retirar_loja_vale)
                                
                            #     if is_checked:
                            #         # Clica usando JavaScript para desmarcar
                            #         navegador.execute_script("arguments[0].click();", retirar_loja_vale)
                            #         print("Caixinha 'ALGO+VALE' desmarcada.")
                            #     else:
                            #         print("Caixinha 'ALGO+VALE' já estava desmarcada.")
                            # except Exception as e:
                            #     print(f"Erro ao tentar desmarcar a checkbox: {e}")
                            
                            # Aguarda
                            time.sleep(2)

                            # Cadastra o produto
                            cadastrar_produto = localizar_elemento(navegador,'/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[2]/button')
                            cadastrar_produto.click()

                            # Aguarda loading desaparecer
                            aguardar_loading_desaparecer(navegador)
                            time.sleep(1)
                        else:
                            # Aguarda
                            time.sleep(1)

                            # Aba "Estoque"
                            aba_estoque = localizar_elemento(navegador,'//*[text()="Estoque"]')
                            aba_estoque.click()

                            # Aguarda
                            time.sleep(1)

                            # Preenche campos de estoque
                            campo_estoque_min = localizar_elemento(navegador,'/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[4]/div/div[1]/div[1]/input')
                            campo_estoque_min.clear()
                            campo_estoque_min.send_keys(str(estoque_min))



                            campo_estoque_max = localizar_elemento(navegador,'/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[4]/div/div[1]/div[2]/input')
                            campo_estoque_max.clear()
                            campo_estoque_max.send_keys(str(estoque_max))

                            campo_estoque_atual = localizar_elemento(navegador,'/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[4]/div/div[1]/div[3]/input')
                            campo_estoque_atual.clear()
                            campo_estoque_atual.send_keys(str(estoque_atual))


                            # Aguarda
                            time.sleep(1)

                            menu_lojas = localizar_elemento(navegador, '/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[1]/ul/li[9]/a')
                            menu_lojas.click()

                            # Aguarda
                            time.sleep(1)

                            # # Aguarda até que a checkbox esteja visível e clicável
                            # try:
                            #     retirar_loja_vale = WebDriverWait(navegador, 10).until(
                            #         EC.element_to_be_clickable((By.ID, '__BVID__656'))
                            #     )
                            #     print("Checkbox localizada.")
    
                            #     # Usa JavaScript para verificar se a checkbox está marcada
                            #     is_checked = navegador.execute_script("return arguments[0].checked;", retirar_loja_vale)
                                
                            #     if is_checked:
                            #         # Clica usando JavaScript para desmarcar
                            #         navegador.execute_script("arguments[0].click();", retirar_loja_vale)
                            #         print("Caixinha 'ALGO+VALE' desmarcada.")
                            #     else:
                            #         print("Caixinha 'ALGO+VALE' já estava desmarcada.")
                            # except Exception as e:
                            #     print(f"Erro ao tentar desmarcar a checkbox: {e}")
                            
                            # Aguarda
                            time.sleep(2)

                            # Cadastra o produto
                            cadastrar_produto = localizar_elemento(navegador,'/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[2]/button')
                            cadastrar_produto.click()

                            # Aguarda loading desaparecer
                            aguardar_loading_desaparecer(navegador)
                            time.sleep(1)

                            sucess = True


                        
                    else:
                        print(f'Produto "{nome_produto}" já está cadastrado. Pulando para o próximo produto...')
                        time.sleep(1)

                        sucess = False


                except Exception as e:
                    tentativas += 1
                    print(f"Erro ao cadastrar '{nome_produto}', tentativa {tentativas} de {MAX_tentativas}. Erro: {e}")
    
            # Atualiza a página
            aguardar_loading_desaparecer(navegador)
            time.sleep(1)

            print("Produto cadastrado com sucesso!")
        print("Todos os produtos foram cadastrados com sucesso!")
    else:
        # clicla botao sim
        botao_sim = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[1]/div/div/footer/button[2]'))
        )
        botao_sim.click()
        time.sleep(1)

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

        MAX_tentativas = 3

        # processo_cadastrar_produtos()
        for index, row in df.iterrows():
            nome_produto = row['nome']
            codigo_barras = row['codigo de barra']
            preco_produto = row['valor de venda']
            estoque_min = row['estoque-min']
            estoque_max = row['estoque-max']
            estoque_atual = row['estoque-atual']

            tentativas = 0
            sucess = False
            # print('codigo barras.....',str(codigo_barras).strip())
            while tentativas < MAX_tentativas and not sucess:
                # Verifica se o produto existe
                try:
                    # Determina a categoria do produto
                    categoria_produto = categorizar_produto(nome_produto)

                    aguardar_loading_desaparecer(navegador)
                    time.sleep(1)

                    #clica no campo buscar produto
                    campo_busca = localizar_elemento(navegador,'/html/body/div[2]/div/div/aside[2]/div/div/section/div/div[1]/div/div[2]/form/div/input')
                    campo_busca.clear()
                    campo_busca.send_keys(nome_produto)
                    campo_busca.send_keys(Keys.RETURN)
                    
                    # Aguarda
                    aguardar_loading_desaparecer(navegador)
                    time.sleep(1)
                    
                    mensagem_nao_encontrado = navegador.find_elements(By.XPATH, '/html/body/div[2]/div/div/aside[2]/div/div/section/div/div[2]/div[2]/h3')
                    if len(mensagem_nao_encontrado) > 0 and mensagem_nao_encontrado[0].text == "Nenhum produto foi encontrado!":
                        print(f'Produto "{nome_produto}" não está cadastrado. Procedendo com o cadastro...')
                        
                        time.sleep(1)

                        # Clica no botão para adicionar um novo produto
                        adicionar_produtos = localizar_elemento(navegador,'/html/body/div[2]/div/div/aside[2]/div/div/section/div/div[1]/div/div[1]/a')
                        adicionar_produtos.click()

                        time.sleep(1)

                        # Preenche o NOME do produto
                        adicionar_nome_produto = localizar_elemento(navegador,'/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[1]/div[1]/div[1]/input')
                        adicionar_nome_produto.send_keys(nome_produto)
                        
                        # Aguarda
                        time.sleep(1)

                        # Clica para GERAR o código interno
                        gerar_codigoInterno = localizar_elemento(navegador,'/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[1]/div[1]/div[2]/div/div/button')
                        gerar_codigoInterno.click()
                        
                        # Aguarda
                        time.sleep(1)
                        campo_codigo_barras = localizar_elemento(navegador, '/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[1]/div[1]/div[3]/input')

                        # Aguarda
                        time.sleep(1)
                        campo_grupo_produto = localizar_elemento(navegador,'//*[@id="grupo"]')

                        #se tiver codigo de barras adiciona se nao pula para categoria
                        if codigo_barras and str(codigo_barras).strip() and str(codigo_barras).lower() != "nan":
                            try:
                               inserir_codigo_barras(navegador, str(codigo_barras).split('.')[0])
                            except Exception as e:
                                print(f"Erro ao inserir o código de barras: {e}")
                        
                        
                        print('passei pelo if....')
                        time.sleep(1)

                        # Insere a categoria do produto
                        inserir_grupo_produto = localizar_elemento(navegador,'/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[1]/div[1]/div[4]/div/input')
                        inserir_grupo_produto.clear()
                        inserir_grupo_produto.send_keys(categoria_produto)
                    

                        # Aguarda
                        time.sleep(1)


                        # Aba "Valores"
                        aba_valores = localizar_elemento(navegador,'//*[text()="Valores"]')
                        aba_valores.click()

                        time.sleep(1)


                        print('campo valor venda')
                        print(preco_produto)
                        print('campo valor venda igual a nan => ')
                        print(str(preco_produto).lower())

                        if preco_produto and str(preco_produto).lower() != "nan":
                            # Preenche o valor de venda
                            campo_valor_venda = localizar_elemento(navegador,'/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[3]/div/div[2]/div/div[2]/div[2]/table/tbody/tr/td[4]/input')
                            campo_valor_venda.clear()
                            campo_valor_venda.send_keys(int(preco_produto))
                            
                            # Aguarda
                            time.sleep(1)

                            # Aba "Estoque"
                            aba_estoque = localizar_elemento(navegador,'//*[text()="Estoque"]')
                            aba_estoque.click()

                            # Aguarda
                            time.sleep(1)

                            # Preenche campos de estoque
                            campo_estoque_min = localizar_elemento(navegador,'/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[4]/div/div[1]/div[1]/input')
                            campo_estoque_min.clear()
                            campo_estoque_min.send_keys(str(estoque_min))



                            campo_estoque_max = localizar_elemento(navegador,'/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[4]/div/div[1]/div[2]/input')
                            campo_estoque_max.clear()
                            campo_estoque_max.send_keys(str(estoque_max))

                            campo_estoque_atual = localizar_elemento(navegador,'/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[4]/div/div[1]/div[3]/input')
                            campo_estoque_atual.clear()
                            campo_estoque_atual.send_keys(str(estoque_atual))

                            # Aguarda
                            time.sleep(1)

                            menu_lojas = localizar_elemento(navegador, '/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[1]/ul/li[9]/a')
                            menu_lojas.click()

                             # Aguarda
                            time.sleep(2)

                            # # Aguarda até que a checkbox esteja visível e clicável
                            # try:
                            #     retirar_loja_vale = WebDriverWait(navegador, 10).until(
                            #         EC.element_to_be_clickable((By.ID, '__BVID__656'))
                            #     )
                            #     print("Checkbox localizada.")
    
                            #     # Usa JavaScript para verificar se a checkbox está marcada
                            #     is_checked = navegador.execute_script("return arguments[0].checked;", retirar_loja_vale)
                                
                            #     if is_checked:
                            #         # Clica usando JavaScript para desmarcar
                            #         navegador.execute_script("arguments[0].click();", retirar_loja_vale)
                            #         print("Caixinha 'ALGO+VALE' desmarcada.")
                            #     else:
                            #         print("Caixinha 'ALGO+VALE' já estava desmarcada.")
                            # except Exception as e:
                            #     print(f"Erro ao tentar desmarcar a checkbox: {e}")
                            
                            # Aguarda
                            time.sleep(2)
                            
                            # Cadastra o produto
                            cadastrar_produto = localizar_elemento(navegador,'/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[2]/button')
                            cadastrar_produto.click()

                            # Aguarda loading desaparecer
                            aguardar_loading_desaparecer(navegador)
                            time.sleep(1)
                        else:
                            # Aguarda
                            time.sleep(1)

                            # Aba "Estoque"
                            aba_estoque = localizar_elemento(navegador,'//*[text()="Estoque"]')
                            aba_estoque.click()

                            # Aguarda
                            time.sleep(1)

                            # Preenche campos de estoque
                            campo_estoque_min = localizar_elemento(navegador,'/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[4]/div/div[1]/div[1]/input')
                            campo_estoque_min.clear()
                            campo_estoque_min.send_keys(str(estoque_min))



                            campo_estoque_max = localizar_elemento(navegador,'/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[4]/div/div[1]/div[2]/input')
                            campo_estoque_max.clear()
                            campo_estoque_max.send_keys(str(estoque_max))

                            campo_estoque_atual = localizar_elemento(navegador,'/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[4]/div/div[1]/div[3]/input')
                            campo_estoque_atual.clear()
                            campo_estoque_atual.send_keys(str(estoque_atual))

                            # Aguarda
                            time.sleep(1)

                            menu_lojas = localizar_elemento(navegador, '/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[1]/ul/li[9]/a')
                            menu_lojas.click()

                             # Aguarda
                            time.sleep(2)

                            # # Aguarda até que a checkbox esteja visível e clicável
                            # try:
                            #     retirar_loja_vale = WebDriverWait(navegador, 10).until(
                            #         EC.element_to_be_clickable((By.ID, '__BVID__656'))
                            #     )
                            #     print("Checkbox localizada.")
    
                            #     # Usa JavaScript para verificar se a checkbox está marcada
                            #     is_checked = navegador.execute_script("return arguments[0].checked;", retirar_loja_vale)
                                
                            #     if is_checked:
                            #         # Clica usando JavaScript para desmarcar
                            #         navegador.execute_script("arguments[0].click();", retirar_loja_vale)
                            #         print("Caixinha 'ALGO+VALE' desmarcada.")
                            #     else:
                            #         print("Caixinha 'ALGO+VALE' já estava desmarcada.")
                            # except Exception as e:
                            #     print(f"Erro ao tentar desmarcar a checkbox: {e}")
                            # Aguarda
                            time.sleep(2)

                            # Cadastra o produto
                            cadastrar_produto = localizar_elemento(navegador,'/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[2]/button')
                            cadastrar_produto.click()

                            # Aguarda loading desaparecer
                            aguardar_loading_desaparecer(navegador)
                            time.sleep(1)
                        
                    else:
                        print(f'Produto "{nome_produto}" já está cadastrado. Pulando para o próximo produto...')
                        # interagir_com_elemento(navegador,'//*[@id="app"]/div/div/aside[1]/section/ul/li[2]/ul/li[1]/a', lambda elem: elem.click())
                        # aguardar_loading_desaparecer()
                        # navegador.refresh()
                        # aguardar_loading_desaparecer()
                        sucess = False
                        time.sleep(1)


                except Exception as e:
                    tentativas += 1
                    print(f"Erro ao cadastrar '{nome_produto}', tentativa {tentativas} de {MAX_tentativas}. Erro: {e}")
                
    
            # Atualiza a página
            navegador.refresh()
            time.sleep(1)
            aguardar_loading_desaparecer(navegador)

            print("Produto cadastrado com sucesso!")
        print("Todos os produtos foram cadastrados com sucesso!")

except Exception as e:
    print(f"Erro: {e}")

finally:
    navegador.quit()
# Mantém a janela aberta até o usuário decidir fechar
# input("Pressione enter para fechar...")
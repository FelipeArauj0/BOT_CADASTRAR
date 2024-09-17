import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

navegador = webdriver.Chrome()

navegador.get("https://gestaoclick.com/inicio")
print("Diretório de trabalho atual:", os.getcwd())
df = pd.read_excel("C:/Users/Usuario/Desktop/bot_cadastrar/src/PRODUTOS.xlsx")
# df = pd.read_excel("C:/Users/Usuario/Desktop/bot_cadastrar/src/cadastro_produtos_matriz.xlsx")
# print(df)

campo_email = navegador.find_element(By.XPATH, '//*[@id="email"]')
campo_email.send_keys("algomais.com2012@gmail.com")

campo_senha = navegador.find_element(By.XPATH, '//*[@id="senha"]')
campo_senha.send_keys("Algomais2012@")

campo_senha.send_keys(Keys.RETURN)

try:
    menu_produtos = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/aside[1]/section/ul/li[2]/a'))
    )
    menu_produtos.click()
    
    time.sleep(2)
    # Localiza e clica na opção "Gerenciar Produtos" dentro do submenu
    gerenciar_produtos = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/aside[1]/section/ul/li[2]/ul/li[1]/a'))
    )
    gerenciar_produtos.click()
    
    time.sleep(2)


    # .columns lista as colunas da tabela
    # print(df.columns) 

    # iloc.[numero] seleciona de acordo a linha solicitada.
    # linha_selecionada = df.iloc[1]
    # nome_produto = linha_selecionada['nome']
    # print(f'Nome do produto: {nome_produto}')

    for index, row in df.iterrows():
        nome_produto = row['nome']
        preco_produto = row['valor de venda']
        estoque_min = row['estoque-min']
        estoque_max = row['estoque-max']
        estoque_atual = row['estoque-atual']
        
        # Clica no botão para adicionar um novo produto
        adicionar_produtos = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="botao-adicionar"]'))
        )
        adicionar_produtos.click()

        # Preenche o formulário de cadastro de produto
        campo_nome = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="nome"]')) 
        )
        campo_nome.send_keys(nome_produto)

        gerar_codigoInterno = navegador.find_element(By.XPATH, '//*[@id="__BVID__2400"]/div[1]/div[2]/div/div/button')  
        gerar_codigoInterno.click()  

        # campo_quantidade = navegador.find_element(By.XPATH, '//*[@id="campo-quantidade-produto"]')  # Substituir pelo XPATH correto
        # campo_quantidade.send_keys(str(quantidade_produto))  # Convertendo a quantidade para string

        # # Submete o formulário (botão de salvar)
        # botao_salvar = navegador.find_element(By.XPATH, '//*[@id="botao-salvar-produto"]')  # Substituir pelo XPATH correto
        # botao_salvar.click()

        # Aguarda um pouco antes de cadastrar o próximo produto
        time.sleep(2)
    
    print("Todos os produtos foram cadastrados com sucesso!")
    
    
    



except Exception as e:
    print(f"Erro: {e}")

input("pressione enter para fechar...")
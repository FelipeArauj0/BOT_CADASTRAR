import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time


# Dicionário de categorias com palavras-chave
categorias_palavras_chave = {
    "SUPORTE": ["suporte", "base"],
    "PAPELARIA": ["papel", "caneta", "caderno", "apontador", "borracha"],
    "ACESSÓRIO": ["chaveiro","pulseira", "capa"],
    "ELETRÔNICOS": ["antena", "controle", "fone", "cabo", "adaptador", "carregador"],
    "INFORMÁTICA": ["mouse", "teclado", "monitor", "impressora", "usb", "pendrive"]
}


# Função para categorizar o produto
def categorizar_produto(nome_produto):
    nome_produto = nome_produto.lower()  # Converter o nome do produto para letras minúsculas
    for categoria, palavras in categorias_palavras_chave.items():
        for palavra in palavras:
            if palavra in nome_produto:
                return categoria
    return "OUTROS"  # Retorna uma categoria padrão

navegador = webdriver.Chrome()

navegador.get("https://gestaoclick.com/inicio")
# print("Diretório de trabalho atual:", os.getcwd())
df = pd.read_excel("C:/Users/Usuario/Desktop/bot_cadastrar/src/PRODUTOS.xlsx")
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
    # click menu
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

        # Determina a categoria do produto
        categoria_produto = categorizar_produto(nome_produto)
        print(f'Produto: {nome_produto} | Categoria: {categoria_produto}')
        
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

        #clicar botao gerar codigo interno
        gerar_codigoInterno = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[1]/div[1]/div[2]/div/div/button'))
        )
        gerar_codigoInterno.click()

        campo_grupo_produto = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="grupo"]')) 
        )
        campo_grupo_produto.send_keys(categoria_produto)

        # campo_quantidade = navegador.find_element(By.XPATH, '//*[@id="campo-quantidade-produto"]')  # Substituir pelo XPATH correto
        # campo_quantidade.send_keys(str(quantidade_produto))  # Convertendo a quantidade para string

        # # Submete o formulário (botão de salvar)
        # botao_salvar = navegador.find_element(By.XPATH, '//*[@id="botao-salvar-produto"]')  # Substituir pelo XPATH correto
        # botao_salvar.click()

        # Aguarda um pouco antes de adicionar valor produto
        time.sleep(2)
        
         # Aguarde até que o botão da aba "Valores" esteja visível e clique
        aba_valores = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[text()="Valores"]'))
        )
        aba_valores.click()
        

        #clicar botao valor de venda
        campo_valor_venda = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[3]/div/div[2]/div/div[2]/div[2]/table/tbody/tr[1]/td[5]/input'))
        )
        campo_valor_venda.clear()
        campo_valor_venda.send_keys((str(preco_produto)))

        # Aguarda um pouco
        time.sleep(2)

        # Aguarde até que o botão da aba "Estoque" esteja visível e clique
        aba_estoque = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[text()="Estoque"]'))
        )
        aba_estoque.click()

        #clicar botao estoque min
        campo_estoque_min = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[4]/div/div[1]/div[1]/input'))
        )
        campo_estoque_min.clear()
        campo_estoque_min.send_keys((str(estoque_min)))

        #clicar botao estoque max
        campo_estoque_max = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[4]/div/div[1]/div[2]/input'))
        )
        campo_estoque_max.clear()
        campo_estoque_max.send_keys((str(estoque_max)))

        #clicar botao estoque atual
        campo_estoque_atual = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[1]/div[2]/div[4]/div/div[1]/div[3]/input'))
        )
        campo_estoque_atual.clear()
        campo_estoque_atual.send_keys((str(estoque_atual)))

        # CADASTRAR PRODUTO
        cadastrar_produto = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/aside[2]/div/div/section/form/div[2]/button'))
        )
        cadastrar_produto.click()

        # Aguarda um pouco
        time.sleep(1)

        # Voltar à página de "Adicionar Produto" para cadastrar o próximo produto
        navegador.refresh()

        # Aguarda um pouco
        time.sleep(2)

        
    
    print("Todos os produtos foram cadastrados com sucesso!")
    
    
    



except Exception as e:
    print(f"Erro: {e}")

input("pressione enter para fechar...")
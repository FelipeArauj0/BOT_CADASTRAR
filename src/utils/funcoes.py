from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from .dicionario_categorias import categorias_palavras_chave as contagem_palavras

navegador = webdriver.Chrome()


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
    
# verificar se o produto já foi cadastrado
def verificar_produto(df_planilha):
    for index, row in df_planilha.iterrows():
        nome_produto = row['nome']
        preco_produto = row['valor de venda']
        estoque_min = row['estoque-min']
        estoque_max = row['estoque-max']
        estoque_atual = row['estoque-atual']

        # Realiza a busca do produto no sistema
        campo_busca = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/aside[2]/div/div/section/div/div[1]/div/div[2]/form/div/input"]'))  
        )
        campo_busca.clear()
        campo_busca.send_keys(nome_produto)
        campo_busca.send_keys(Keys.RETURN)

        # Aguarda os resultados da busca
        time.sleep(2)

        try:
            # Verifica se o produto está na tabela (substituir o XPATH pela localização real do produto)
            produto_na_lista = WebDriverWait(navegador, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="produto-tabela"]'))  # Substituir pelo XPATH da tabela de produtos encontrados
            )
            print(f'Produto "{nome_produto}" já está cadastrado. Pulando para o próximo...')
            continue  # Se o produto for encontrado, pula para o próximo produto

        except:
            # Verifica se a mensagem de "Nenhum produto foi encontrado" aparece (substituir o XPATH pelo correto)
            mensagem_nao_encontrado = navegador.find_element(By.XPATH, '//*[@class="row no-result"]')
            if mensagem_nao_encontrado:
                print(f'Produto "{nome_produto}" não está cadastrado. Procedendo com o cadastro...')
                # Se não encontrou o produto, prossegue com o cadastro
                cadastrar_produto(navegador, nome_produto, preco_produto, estoque_min, estoque_max, estoque_atual)
            else:
                print(f"Erro ao verificar a existência do produto {nome_produto}.")
                continue
    


# Função + loop pesquisar produto se existe na base de dados do sistema

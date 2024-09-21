## BOT - CADASTRAR PRODUTOS  

irá ser capaz de ler uma planilha com diversos produtos para cadastrar no sistema da loja.  
  
* nome  
* clicar em gerar codigo interno;  
* colar codigo de barra se tiver;  
* selecionar o grupo do produto;  
* selecionar **VALOR DE VENDA UTILIZADO (R$)** e colocar valor do produto;  
* atualizar estoque **MINIMO**, **MAXIMO** e **ATUAL**;  
* adicionar foto do produto;  

## instalar dependencias

```
pip3 install pandas
pip install openpyxl

```
## TESTAR CODIGO  
Exemplo de código para verificar a existência do produto: 

```
# Código que já está presente para navegar até a página

for index, row in df.iterrows():
    nome_produto = row['nome']
    preco_produto = row['valor de venda']
    estoque_min = row['estoque-min']
    estoque_max = row['estoque-max']
    estoque_atual = row['estoque-atual']

    # Realiza a busca do produto no sistema
    campo_busca = WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="search-bar"]'))  # Substituir pelo XPATH real do campo de busca
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

```



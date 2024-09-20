# Função para categorizar o produto com base nas regras especificadas
def categorizar_produto(nome_produto):
    nome_produto = nome_produto.lower()  # Converter o nome do produto para letras minúsculas
    contagem_palavras = {}  # Dicionário para contar as ocorrências de palavras-chave por categoria
    
    # Percorre o dicionário de categorias e palavras-chave
    for categoria, palavras in categorias_palavras_chave.items():
        contagem_palavras[categoria] = 0  # Inicializa a contagem da categoria
        for palavra in palavras:
            if palavra in nome_produto:
                contagem_palavras[categoria] += 1  # Incrementa a contagem para a categoria

    # Filtra as categorias que têm pelo menos uma palavra-chave no nome do produto
    categorias_encontradas = {cat: count for cat, count in contagem_palavras.items() if count > 0}
    
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
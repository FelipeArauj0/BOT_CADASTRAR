from selenium import webdriver

# Função para criar e retornar a instância do navegador
def iniciar_navegador():
    # Aqui você pode configurar as opções do Chrome, se necessário
    options = webdriver.ChromeOptions()
    # Exemplo de configuração: executar o Chrome em modo headless
    # options.add_argument('--headless')
    
    # Cria uma única instância do navegador
    navegador = webdriver.Chrome(options=options )
    return navegador

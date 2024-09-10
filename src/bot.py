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
print(df)

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
    
    time.sleep(3)
    # Localiza e clica na opção "Gerenciar Produtos" dentro do submenu
    gerenciar_produtos = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/aside[1]/section/ul/li[2]/ul/li[1]/a'))
    )
    gerenciar_produtos.click()

except Exception as e:
    print(f"Erro: {e}")

input("pressione enter para fechar...")
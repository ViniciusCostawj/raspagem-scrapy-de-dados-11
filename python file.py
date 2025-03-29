from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys
import json
from datetime import datetime

# Corrigimdo problema de codificação no Windows
sys.stdout.reconfigure(encoding='utf-8')

# Configuração do WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

# Inicializando o WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# URL do site
url = "https://portaldatransparencia.gov.br/servidores/consulta"
driver.get(url)

# espera 15 segundos para garantir que a página carregue completamente
WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

# 📌 ACEITAR OS COOKIES
try:
    time.sleep(2)
    botao_aceitar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Aceitar') or contains(., 'Concordar')]"))
    )
    botao_aceitar.click()
    print("✅ Aceitou os cookies básicos")
    
    time.sleep(3)
    try:
        botao_salvar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Salvar') or contains(., 'Confirmar')]"))
        )
        botao_salvar.click()
        print("✅ Configurações de cookies salvas")
    except:
        print("⚠️ Página de configuração não apareceu - continuando...")
        
except Exception as e:
    print(f"⚠️ Não foi possível aceitar cookies: {str(e)[:100]}...")

driver.implicitly_wait(5)

def search_employee(driver, name):
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "lista"))
        )
        
        header_cells = driver.find_elements(By.XPATH, "//table[@id='lista']//th")
        nome_index = None
        
        for index, cell in enumerate(header_cells):
            if "Nome" in cell.text:
                nome_index = index + 1
                break
                
        if nome_index is None:
            raise Exception("Coluna 'Nome' não encontrada na tabela")
        
        search_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, 
                f"//table[@id='lista']//tr[@class='filtro']/td[{nome_index}]/input"))
        )
        
        search_input.clear()
        search_input.send_keys(name)
        search_input.send_keys(Keys.RETURN)
        print(f"🔍 Pesquisa por '{name}' realizada com sucesso")
        return True
        
    except Exception as e:
        print(f"❌ Erro na pesquisa: {str(e)}")
        return False

# Espera a tabela carregadar
try:
    tabela = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//table[@id='lista']"))
    )
    print("✅ Tabela encontrada com sucesso!")
except Exception as e:
    print("❌ Erro ao encontrar a tabela:", e)
    driver.quit()
    exit()

# Aguarda os dados carregarem
time.sleep(5)

# Captura os servidores
servidores = tabela.find_elements(By.XPATH, ".//tbody/tr")

# Lista para armazenar os dados em JSON
dados_json = []
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Salvar em TXT e JSON
with open("resultado.txt", "w", encoding="utf-8") as file_txt, \
     open("resultado.json", "w", encoding="utf-8") as file_json:
    
    for servidor in servidores:
        try:
            # Extrai os dados
            servidor_data = {
                "detalhar": servidor.find_element(By.XPATH, ".//td[1]").text.strip(),
                "tipo": servidor.find_element(By.XPATH, ".//td[2]").text.strip(),
                "cpf": servidor.find_element(By.XPATH, ".//td[3]").text.strip(),
                "nome": servidor.find_element(By.XPATH, ".//td[4]").text.strip(),
                "orgao_lotacao": servidor.find_element(By.XPATH, ".//td[5]").text.strip(),
                "matricula": servidor.find_element(By.XPATH, ".//td[6]").text.strip(),
                "situacao": servidor.find_element(By.XPATH, ".//td[7]").text.strip(),
                "funcao": servidor.find_element(By.XPATH, ".//td[8]").text.strip(),
                "cargo": servidor.find_element(By.XPATH, ".//td[9]").text.strip(),
                "quantidade": servidor.find_element(By.XPATH, ".//td[10]").text.strip(),
                "data_consulta": timestamp
            }
            
            # Adiciona ao JSON
            dados_json.append(servidor_data)
            
            # Escreve no TXT
            file_txt.write(
                f"Detalhar: {servidor_data['detalhar']}\n"
                f"Tipo: {servidor_data['tipo']}\n"
                f"CPF: {servidor_data['cpf']}\n"
                f"Nome: {servidor_data['nome']}\n"
                f"Órgão de Lotação: {servidor_data['orgao_lotacao']}\n"
                f"Matrícula: {servidor_data['matricula']}\n"
                f"Situação: {servidor_data['situacao']}\n"
                f"Função: {servidor_data['funcao']}\n"
                f"Cargo: {servidor_data['cargo']}\n"
                f"Quantidade: {servidor_data['quantidade']}\n"
                f"{'-' * 50}\n"
            )
            
        except Exception as e:
            print("❌ Erro ao extrair dados:", e)
    
    # Salva o JSON
    json.dump(dados_json, file_json, ensure_ascii=False, indent=2)

print("\n✅ Resultados salvos em:")
print("- resultado.txt (formato texto)")
print("- resultado.json (formato JSON)")

driver.quit()
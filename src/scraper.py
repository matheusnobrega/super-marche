# src/scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from utils import ITENS
import time


# Configurações do Selenium
def init_webdriver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Executar sem interface gráfica
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service("C:\Program Files (x86)\chromedriver.exe")  # Atualize para o caminho do seu chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Função para scraping
def scrape_website(url):
    driver = init_webdriver()
    driver.get(url)

    # Aguarde até que o elemento esteja presente
    wait = WebDriverWait(driver, 2)
    

    page_source = driver.page_source
    
    for item, codigo in ITENS.items():
        search_box = wait.until(EC.presence_of_element_located((By.ID, "input-search")))
        search_box.send_keys(item)
        search_box.send_keys(Keys.RETURN)
        catch_info(driver, codigo)
        driver.get(url)

    
    # soup = BeautifulSoup(page_source, "html.parser")

    # # Extraia informações desejadas (exemplo: título da página)
    # page_title = soup.title.string

    # Fechar o navegador
    driver.quit()

def catch_info(driver, codigo):
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    card_item = soup.find('button',{'data-product-id':codigo}).parent.parent

    price_boilerplate = soup.find('span', {'class': 'product-variation__final-price'})

    price_per_kg_boilerplate = soup.find('div', {'class': 'product-variation__fractional-desc'})

    price = price_boilerplate.getText().split()[1].replace(',', '.')

    if price_per_kg_boilerplate:
        price_per_kg = price_per_kg_boilerplate.text.strip().split()[-1].replace(',', '.')
    else:
        price_per_kg = None

    print(price, price_per_kg)


if __name__ == "__main__":
    url = "https://minhacooper.com.br/loja/garcia-bnu" 
    scrape_website(url)

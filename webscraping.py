# Importações
import pandas as pd
from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Selenium
service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Função: capturar_pagina()
def capturar_pagina():
    tituloLista = []
    imgLista = []
    pdfLista = []
    dataLista = []
    horaLista = []
    noticiaLista = []
    urlLista = []
  
    n_noticias = len(driver.find_elements(By.CLASS_NAME, 'views-row')) + 1
    
    for e in range(1, n_noticias):
        driver.find_elements(By.TAG_NAME, 'h2')[e].click()

        
        # Titulo
        titulo = driver.find_element(By.TAG_NAME, 'h1').text
        tituloLista.append(titulo)
    
        # Imagem
        img =  driver.find_elements(By.TAG_NAME, 'img')[5].get_attribute('src')
        imgLista.append(img)
        
        # Todos os PDF's
        def capturar_pdfs():
            pdfLista_dentro = []
            lista_link = driver.find_elements(By.TAG_NAME, "a")
            
            for link in lista_link:
                pdf = str(link.get_attribute("href"))
                if 'pdf' in pdf:
                    pdfLista_dentro.append(pdf)
            return pdfLista_dentro
            
        pdfLista_fora = capturar_pdfs()

        pdfLista.append(pdfLista_fora)
        
        
        # Data
        data = driver.find_elements(By.CLASS_NAME, 'submitted')[0].text[31:].split()[0]
        dataLista.append(data)
        
        # Hora
        hora = driver.find_elements(By.CLASS_NAME, 'submitted')[0].text[31:].split()[2]
        horaLista.append(hora)
    
        
        # Noticia
        noticia = driver.find_element(By.ID, "main-content-inner").text
        noticiaLista.append(noticia)

        # Url
        url = driver.current_url
        urlLista.append(url)
        
        # Volta para página
        # sleep(2)
        driver.back()

        
    
    # return tituloLista, imgLista,  pdfLista, dataLista, horaLista, noticiaLista
    
    df = pd.DataFrame({
                        'tituloLista': tituloLista, 
                        'imgLista': imgLista, 
                        'pdfLista': pdfLista, 
                        'dataLista': dataLista,
                        'horaLista': horaLista,
                        'noticiaLista': noticiaLista,
                        'urlLista': urlLista})
    # Fechar
    return df

# Função: capturar_todas_noticiais()

def capturar_todas_noticiais():
    url = 'https://proext.ufba.br/noticias?page=0'
    driver.get(url)
    driver.find_element(By.CLASS_NAME, "pager-last").click()
    ultima_pagina = int(driver.find_element(By.CLASS_NAME, "pager-current").text)
    driver.get(url)

    
    df_pagina1 = pd.DataFrame()
    dfs = []
    
    for i in range(0, ultima_pagina):
        url2 = f'https://proext.ufba.br/noticias?page={i}'
        driver.get(url2)
        df = capturar_pagina()
        dfs.append(df)
        sleep(5)
        
    
    df_raw = pd.concat(dfs, axis=0)
    
    df_pagina1 = pd.concat([df_pagina1, df_raw], axis=0)


    df_pagina1.reset_index(drop=True, inplace=True)
        
    return df_pagina1

# Execução
df1 = capturar_todas_noticiais()

# DataFrame Final
# data atual
data = f'{datetime.now().year}{datetime.now().month}{datetime.now().day}_{datetime.now().hour}-{datetime.now().minute}'

# Resetar Index
df1.reset_index(drop=True, inplace=True)

df1.to_csv(f'{data}_out.csv')

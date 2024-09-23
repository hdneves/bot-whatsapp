from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import time
import requests
from constants import API_KEY, agent

def start_driver():
    '''Função com todas as configurações do browser'''

    path_dir = os.getcwd()
    options = Options()
    #options.add_argument('--headless') 
    options.add_argument(r"user-data-dir=" + path_dir + "profile/zap")
    options.add_argument('start-maximized')
    
    driver = webdriver.Edge(options=options)
    return driver

def getApi(api_key=API_KEY, agent=agent):
    # Faz a requisição à API
    api_response = requests.get(api_key, headers=agent)
    time.sleep(1)  # Aguarda 1 segundo

    # Processa a resposta
    api_text = api_response.text
    api_parts = api_text.split(".n.")

    # Extrai os dados desejados e remove espaços em branco
    bolinha_notificacao = api_parts[3].strip()
    contato_cliente = api_parts[4].strip()
    caixa_msg = api_parts[5].strip()
    msg_cliente = api_parts[6].strip()
    caixa_msg2 = api_parts[7].strip()
    caixa_pesquisa = api_parts[8].strip()

    return {
        'notify_ball': bolinha_notificacao,
        'number_client': contato_cliente,
        'box_msg': caixa_msg,
        'client_msg': msg_cliente,
        'box_msg_2': caixa_msg2,
        'search_box': caixa_pesquisa
    }


def bot(driver, element):

    try:
        
        #CAPTURAR A BOLINHA
        green_ball = driver.find_element(By.CLASS_NAME,element['notify_ball'])
        green_ball = driver.find_elements(By.CLASS_NAME,element['notify_ball'])
        click_ball = green_ball[-1]
        action_ball = webdriver.common.action_chains.ActionChains(driver)
        action_ball.move_to_element_with_offset(click_ball,0,-20)
        action_ball.click()
        action_ball.perform()
        action_ball.click()
        action_ball.perform()
        time.sleep(1)

        #PEGAR O TELEFONE
        client_number = driver.find_element(By.XPATH,element['number_client'])
        final_number = client_number.text 
        print(f'Número: {final_number}')
        time.sleep(2)

        #PEGAR A MSG DO CLIENTE
        all_msg_element = driver.find_elements(By.CLASS_NAME,element['client_msg'])
        all_msg = [e.text for e in all_msg_element]
        msg = all_msg[-1]
        print(f'Mensagem: {msg}')
        time.sleep(2)

        #RESPONDENDO CLIENTE
        box_msg_element = driver.find_element(By.XPATH,element['box_msg'])
        box_msg_element.click()
        time.sleep(1)
        box_msg_element.send_keys('Olá aqui é o Nagore. Como posso ajudar?', Keys.ENTER)


        #FECHAR CONTATO
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()


    except Exception as e:
        pass

if __name__ == '__main__':
    driver = start_driver()
    driver.get('https://web.whatsapp.com/')
    time.sleep(20)
    element = getApi()
    while True:
        bot(driver=driver, element=element)
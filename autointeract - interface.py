import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.common.exceptions import NoSuchElementException


# Função que será chamada quando o botão "Iniciar" for clicado
def iniciar_script():
    # Obtém o valor dos campos de entrada
    username = username_entry.get()
    password = password_entry.get()
    interacao = interacao_var.get()

    # Verifica se a opção selecionada foi "Romc"
    if interacao == "Romc":
        # Retorna uma mensagem informando que a ferramenta ainda não foi implementada
        mensagem_label.config(text="Ferramenta ainda não implementada")
    # Verifica se a opção selecionada foi "amzd"
    else:
        # faz conversões para utilizar o driver do navegador mais atual, com a função webdriver e renomeia a
        # variavel navegador para driver
        servico = Service(ChromeDriverManager().install())
        navegador = webdriver.Chrome(service=servico)
        driver = navegador

        ##acessa o site principal
        driver.get('https://www.footmundo.com/')

        # aguarda pagina carregar
        time.sleep(1)
        # faz login no site
        campo_email = driver.find_element(By.ID, 'usernameInput')
        time.sleep(0.5)
        campo_email.send_keys(username)
        campo_senha = driver.find_element(By.ID, 'passwordInput')  # Encontra o elemento novamente
        time.sleep(0.5)
        campo_senha.send_keys(password)
        btn_submit = driver.find_element(By.CLASS_NAME, 'btn.btn-primary.btn-large.span')
        time.sleep(0.5)
        btn_submit.click()
        # aguarda a pagina carregar
        time.sleep(1)
        # Acesse a página de relacionamentos
        link_relacionamentos = driver.find_element(By.LINK_TEXT, 'Relacionamentos')
        link_relacionamentos.click()

        time.sleep(1)

        # Encontra todos os links com a ID "link_padrao" e guarda em uma lista
        links = driver.find_elements(By.XPATH, '//a[@id="link_padrao"]')
        links = [link.get_attribute("href") for link in links]

        # Dicionário para armazenar as informações das opções
        opcoes_dict = {}

        # Loop para abrir cada link e coletar as informações das opções
        for link in links:
            driver.execute_script("window.open(arguments[0])", link)
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(3)
            try:
                select_interacao = driver.find_element(By.NAME, 'interacao')
            except NoSuchElementException:
                print(f"Elemento 'select_interacao' não foi encontrado no link {link}")
                continue
            opcoes_interacao = select_interacao.find_elements(By.TAG_NAME, 'option')
            opcoes_interacao = [opcao.get_attribute('value') for opcao in opcoes_interacao]
            opcoes_dict[link] = opcoes_interacao
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            # Imprime as informações coletadas
            print(opcoes_dict)
        return


#Cria a janela
janela = tk.Tk()
janela.title("Ligação e interação automatica - Footmundo")

#Cria os widgets da janela
username_label = tk.Label(janela, text="Usuário:")
username_entry = tk.Entry(janela)
password_label = tk.Label(janela, text="Senha:")
password_entry = tk.Entry(janela, show="*")
interacao_label = tk.Label(janela, text="Tipo de Interação:")
interacao_var = tk.StringVar(value="Selecione...")
interacao_optionmenu = tk.OptionMenu(janela, interacao_var, "Selecione...", "Romc","Amzd")
iniciar_button = tk.Button(janela, text="Iniciar", command=iniciar_script)
mensagem_label = tk.Label(janela, text="")

#Posiciona os widgets na janela
username_label.grid(row=0, column=0)
username_entry.grid(row=0, column=1)
password_label.grid(row=1, column=0)
password_entry.grid(row=1, column=1)
interacao_label.grid(row=2, column=0)
interacao_optionmenu.grid(row=2, column=1)
iniciar_button.grid(row=3, column=0, columnspan=2)
mensagem_label.grid(row=4, column=0, columnspan=2)

#Inicia a janela
janela.mainloop()

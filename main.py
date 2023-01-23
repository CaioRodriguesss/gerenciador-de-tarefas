import subprocess
import threading as thr
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from endereco import e_host, e_porta

# Host e porta que forma o endereço
endereco_app = "http://" + str(e_host) + ":" + str(e_porta)


class RodarApp:
    def __init__(self):
        self.subprocesso = None
        self.thrr = thr
        self.opcoes = Options()
        self.opcoes.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        self.driver = webdriver.Chrome(
            service=Service(executable_path="C:/Users/caior/OneDrive/Área de Trabalho/git projetos/gerenciador de tarefas browser v1.0/chromedriver.exe"),
            options=self.opcoes
        )
        self.mensagem_desconexao = "Unable to evaluate script: no such window: target window already closed\nfrom unknown error: web view not found\n"

    def iniciar_app(self):
        self.subprocesso = subprocess.Popen("py app.py", shell=False)

    def iniciar_threading(self):
        iniciar = self.thrr.Thread(target=self.iniciar_app())
        time.sleep(2)
        iniciar.start()

    def abrir_navegador(self):
        self.driver.get(endereco_app)
        #self.driver.get("http://127.0.0.1:8050/")

    def manter_app(self):
        while True:
            if self.driver.get_log("driver") != []:
                if self.driver.get_log("driver")[0]["message"] == self.mensagem_desconexao: # Leva 3 segundos para encerrar os processos.
                    self.subprocesso.kill()
                    break
            time.sleep(3)

    
    
rodar_app = RodarApp()

if __name__ == "__main__":
    rodar_app.iniciar_threading()
    rodar_app.abrir_navegador()
    rodar_app.manter_app()

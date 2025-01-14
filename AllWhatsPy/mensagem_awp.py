from .decorators_awp import aprovarConexao
from .errors_awp import AWPContatoNaoEncontrado
import os
import re
import time
import requests
import pyperclip
from urllib import parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    UnexpectedAlertPresentException,
    NoSuchElementException)


class AWPMensagem():
    
    def __init__(self, objeto):
        self.objeto_awp = objeto
        self.objeto_awp._get_logging(f'{__class__.__name__} obteve êxito.')
        self.endereco = Endereco
        self.anexo = Anexo(self.objeto_awp)
        self.analise = Analise(self.objeto_awp)


    @aprovarConexao
    def enviar_mensagem_isolada(self, mensagem: str):
        try:
            if self.objeto_awp.InferenciaAWP.contato_acessivel:
                if isinstance(mensagem, int) or isinstance(mensagem, float):
                    mensagem = str(mensagem)

                self.objeto_awp.InferenciaAWP.mensagem = mensagem
                textbox = self.objeto_awp._ArmazemXPATH.textbox_xpath

                if isinstance(mensagem, list):        
                    mensagem = '\n'.join(mensagem)
                    
                self.objeto_awp._drive.find_element(By.XPATH,textbox).send_keys(mensagem,Keys.ENTER)         
                self.objeto_awp._get_logging(f'   Mensagem enviada para {self.objeto_awp.InferenciaAWP.contato}')

                if len(self.objeto_awp.InferenciaAWP.mensagem) > 50:
                    self.objeto_awp._get_logging(f'   Mensagem: {self.objeto_awp.InferenciaAWP.mensagem[:50]}[...]')
                else:
                    self.objeto_awp._get_logging(f'   Mensagem: {self.objeto_awp.InferenciaAWP.mensagem[:50]}')
                self._exitoEnvio()
                
            else:
                self.objeto_awp._get_logging(f'    Não foi possível enviar mensagem por se tratar de um contato inacessível.')
                
        except (NoSuchElementException, AttributeError):
            raise AWPContatoNaoEncontrado


    @aprovarConexao
    def enviar_mensagem_paragrafada(self, mensagem: str):
        try:
            if self.objeto_awp.InferenciaAWP.contato_acessivel:
                self.objeto_awp.InferenciaAWP.mensagem = mensagem

                textbox = self.objeto_awp._marktime_func(self.objeto_awp._ArmazemXPATH.textbox_xpath)
                textbox.click()

                if isinstance(mensagem, list):
                    mensagem = '\n'.join(mensagem)
                    
                for linha in mensagem.split('\n'):
                    textbox.send_keys(linha)
                    ActionChains(self.objeto_awp._drive).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).perform()
                    
                textbox.send_keys(Keys.ENTER)
                self.objeto_awp._get_logging(f'   Mensagem enviada para {self.objeto_awp.InferenciaAWP.contato}')
                
                if len(self.objeto_awp.InferenciaAWP.mensagem) > 50:
                    self.objeto_awp._get_logging(f'   Mensagem: {self.objeto_awp.InferenciaAWP.mensagem[:50]}[...]')
                else:
                    self.objeto_awp._get_logging(f'   Mensagem: {self.objeto_awp.InferenciaAWP.mensagem[:50]}')
                    
                self._exitoEnvio()
                
            else:
                self.objeto_awp._get_logging(f'    Não foi possível enviar mensagem por se tratar de um contato inacessível.')
                
        except (NoSuchElementException, AttributeError):
            raise AWPContatoNaoEncontrado       
        
        
    @aprovarConexao
    def enviar_mensagem_compulsiva(self, repeticao: int, iter_msg:list = []):
        try:
            if self.objeto_awp.InferenciaAWP.contato_acessivel:
                self.objeto_awp.InferenciaAWP.mensagem = iter_msg
                textbox = self.objeto_awp._ArmazemXPATH.textbox_xpath
                
                for i in range(repeticao):
                    for msg in iter_msg:
                        self.objeto_awp._drive.find_element(By.XPATH,textbox).send_keys(msg)
                
                self.objeto_awp._get_logging(f'   Mensagem enviada para {self.objeto_awp.InferenciaAWP.contato}')
                if len(self.objeto_awp.InferenciaAWP.mensagem) > 50:
                    self.objeto_awp._get_logging(f'   Mensagem: {self.objeto_awp.InferenciaAWP.mensagem[:50]}[...]')
                else:
                    self.objeto_awp._get_logging(f'   Mensagem: {self.objeto_awp.InferenciaAWP.mensagem[:50]}')
                self._exitoEnvio()
            
            else:
                self.objeto_awp._get_logging(f'    Não foi possível enviar mensagem por se tratar de um contato inacessível.')
                
        except (NoSuchElementException, AttributeError):
            raise AWPContatoNaoEncontrado
        

    @aprovarConexao
    def enviar_mensagemCP(self, mensagem:str):
        try:
            if self.objeto_awp.InferenciaAWP.contato_acessivel:
                
                self.objeto_awp.InferenciaAWP.mensagem = mensagem
                textbox = self.objeto_awp._ArmazemXPATH.textbox_xpath
                
                pyperclip.copy(mensagem)
                self.objeto_awp._drive.find_element(By.XPATH,textbox).send_keys(Keys.CONTROL, 'v')
                self.objeto_awp._drive.find_element(By.XPATH,textbox).send_keys(Keys.ENTER)
                pyperclip.copy('')
                

                self.objeto_awp._get_logging(f'   Mensagem enviada para {self.objeto_awp.InferenciaAWP.contato}')
                if len(self.objeto_awp.InferenciaAWP.mensagem) > 50:
                    self.objeto_awp._get_logging(f'   Mensagem: {self.objeto_awp.InferenciaAWP.mensagem[:50]}[...]')
                else:
                    self.objeto_awp._get_logging(f'   Mensagem: {self.objeto_awp.InferenciaAWP.mensagem[:50]}')
                self._exitoEnvio()
                
            else:
                self.objeto_awp._get_logging(f'    Não foi possível enviar mensagem por se tratar de um contato inacessível.')
                
        except (NoSuchElementException, AttributeError):
            raise AWPContatoNaoEncontrado
        

    @aprovarConexao
    def enviar_mensagem_por_link(self, numero, texto):
        self.objeto_awp.InferenciaAWP.mensagem = texto

        texto =  parse.quote(texto)
        link = f'https://web.whatsapp.com/send?phone={numero}&text={texto}'
        self.objeto_awp._drive.get(link)
        
        textbox = self.objeto_awp._marktime_func(self.objeto_awp._ArmazemXPATH.textbox_xpath)
        textbox.send_keys(Keys.ENTER)

        next(self.objeto_awp._generator_info_contato_acessado)
        next(self.objeto_awp._generator_info_contato_acessado)
        self._exitoEnvio()


    @aprovarConexao
    def enviar_mensagem_direta(self, contato, mensagem: str, selecionar_funcao: int = 1, salvo: bool = True):

        if salvo:
            self.objeto_awp.ctt.encontrar_contato(contato)
        else:        
            self.objeto_awp.ctt.encontrar_usuario(contato)
            
        
        metodos_envio:dict ={
            1:'self.objeto_awp.msg.enviar_mensagem_isolada(mensagem)',
            2:'self.objeto_awp.msg.enviar_mensagem_paragrafada(mensagem)',
        }
        
        try:
            eval(metodos_envio[selecionar_funcao])
        except Exception as e:
            print(e)
            raise ValueError('Valor informado incoerente.')
        
            
    def _exitoEnvio(self):
        try:
            # match case mensagem
            self.objeto_awp._marktime_func('//*[@id="main"]//*[@data-icon="msg-time"]')
            self.objeto_awp._marktime_func_not_until('//*[@id="main"]//*[@data-icon="msg-time"]')
            #match case imagem
            
            #match case arquivo
            
        except (NoSuchElementException, Exception) as e:
            self.objeto_awp._get_logging(f"Não foi obtido êxito no envio da mensagem ao contato {self.objeto_awp.InferenciaAWP.contato} - {e}")



class __TratarAnalise():
    
    def __init__(self, t_util) -> None:
        self.__t_util = t_util
        self.get = {
            'USER':self.__identificar_user(),
            'MSG':self.__identificar_mensagem(),
            'TIME':self.__identificar_hora(),
            'ALL':self.__t_util,
            }
        

    def __identificar_user(self):
        return ''
    
    
    def __identificar_mensagem(self):
        return ''


    def __identificar_hora(self):
        return ''
        
    

class Analise:
    
    def __init__(self, objeto) -> None:
        self.objeto_awp = objeto
            
    
    @aprovarConexao
    def ultima_mensagem_chat(self): #verifica se a mensagem foi enviada.
        quadro_interacao = self.objeto_awp._drive.find_element(By.XPATH, '/html/body/div[1]/div/div/div[5]/div/div[2]/div/div[2]/div[3]') #pelo quadro onde ficar as msgs
        caixa_mensagens_objeto = quadro_interacao.find_elements(By.XPATH, '//*[@role="row"]')
        caixa_mensagens = caixa_mensagens_objeto[-1].text
        
        return __TratarAnalise(caixa_mensagens)  #depois aprimorar caixa_mensagens.find_element(By.XPATH, '...')
        
    
    
        


class Enquete():
    
    def __init__(self) -> None:
        ...



class Endereco():

    def __init__(self, cep: int):
        self.link = 'https://viacep.com.br/ws/{}/json/'
        self.cep = Endereco.tratamento_cep(cep)
        self.dados = None
        self.run()
    

    @staticmethod
    def tratamento_cep(item):
        item = str(item)
        if '-' in item:
            item =  item.replace('-','')
        
        if '.' in item:
            item = item.replace('.','')

        if len(item) == 8:
            return item


    def run(self):
        try:
            requisicao = requests.get(self.link.format(self.cep)).json()
            rua = requisicao['logradouro'] 
            cidade = requisicao['localidade'] 
            bairro = requisicao['bairro'] 
            uf = requisicao['uf'] 

            self.dados = requisicao, rua, cidade, bairro, uf
            
        except requests.JSONDecodeError:
            raise ValueError("Insira um CEP válido")


    def retornar(self):
        self.dados = ', '.join(self.dados[1:])
        return self.dados
    


class Anexo():

    def __init__(self, objeto) -> None:
        self.objeto_awp = objeto
        self.__metodo_anexo = None


    @aprovarConexao
    def imagem(self, nome_arquivo, mensagem=''):
        try:
            if self.objeto_awp.InferenciaAWP.contato_acessivel:
                
                self.__metodo_anexo = 'imagem'
                item = os.path.realpath(nome_arquivo)
                self.__encontrar_botao_anexo_XPATH()
                    
                arquivo = self.objeto_awp._drive.find_elements(By.CSS_SELECTOR, "input[type='file']") #metodo "elements" porque tanto a seleção de arquivo, quanto de imagem em o parâmetro "type" como "file"
                arquivo[1].send_keys(item)
                time.sleep(2)

                self.__enviar_anexo_XPATH(mensagem)
                time.sleep(2)
                # self.objeto_awp.msg._exitoEnvio()

            else:
                self.objeto_awp._get_logging(f'    Não foi possível enviar a imagem por se tratar de um contato inacessível.')

        except (NoSuchElementException, AttributeError):
            raise AWPContatoNaoEncontrado
        
    
    @aprovarConexao
    def arquivo(self, nome_arquivo, mensagem=''):  
        try:
            if self.objeto_awp.InferenciaAWP.contato_acessivel:  
                self.__metodo_anexo = 'arquivo'
                item = os.path.realpath(nome_arquivo)
                self.__encontrar_botao_anexo_XPATH()
                    
                arquivo = self.objeto_awp._drive.find_elements(By.CSS_SELECTOR, "input[type='file']") #metodo "elements" porque tanto a seleção de arquivo, quanto de imagem em o parâmetro "type" como "file"
                arquivo[0].send_keys(item)
                time.sleep(2)

                self.__enviar_anexo_XPATH(mensagem)
                time.sleep(2)
                # self.objeto_awp.msg._exitoEnvio()
            else:
                self.objeto_awp._get_logging(f'    Não foi possível enviar o arquivo por se tratar de um contato inacessível.')

        
        except (NoSuchElementException, AttributeError):
            raise AWPContatoNaoEncontrado
    

    @aprovarConexao
    def __encontrar_botao_anexo_XPATH(self):
        botão_anexo_xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div'
        self.objeto_awp._drive.find_element(By.XPATH, botão_anexo_xpath).click()
        time.sleep(1)
        
        
    @aprovarConexao
    def __enviar_anexo_XPATH(self, msg):
        dict_delinear = {'arquivo': '//*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[1]/div[3]/div/div/div[1]/div[1]/p',
                         'imagem': '//*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/p'
                         }
        inputbox_xpath = dict_delinear.get(self.__metodo_anexo)

        if msg:
            self.objeto_awp._drive.find_element(By.XPATH, inputbox_xpath).send_keys(msg, Keys.ENTER)
        else:
            self.objeto_awp._drive.find_element(By.XPATH, inputbox_xpath).send_keys(Keys.ENTER)
        time.sleep(1)

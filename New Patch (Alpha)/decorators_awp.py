from errors_awp import AWPConnectionError
import time
import string
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    UnexpectedAlertPresentException,
    NoSuchElementException,
)


def eventual_erro(func):
    def wrapper(self, *args, **kwargs):
        try:
            f = func(self, *args, **kwargs)
            return f
            
        except AWPConnectionError:
            raise AWPConnectionError

        except (Exception, NoSuchElementException, UnexpectedAlertPresentException) as e:
            self.objeto_awp._get_logging(f'Ocorreu um erro durante a execução de {f"{self.objeto_awp.atual_funcao}"} — Erro: {e}. Tempo de Execução AWP: {self.objeto_awp.tempo_execucao}')
            self.objeto_awp._get_logging(f"{'':=^40}")
            raise
    return wrapper


def aprovarConexao(func):
    @eventual_erro
    def wrapper(self, *args, **kwargs):
        if self.objeto_awp._flag_status():
            self.objeto_awp._alterar_funcao_em_execucao(f'AllWhatsPy.{func.__name__}()')
            
            self.objeto_awp._get_logging(f'AllWhatsPy.{func.__name__}() inicializou.')
            f = func(self, *args, **kwargs)
            self.objeto_awp._get_logging(f'{self.objeto_awp._tratamento_log_func(func)} finalizou sua execução.')
            return f
        raise AWPConnectionError
    return wrapper


def executarOrdemTeclas(func):
    def _ordenacao(self, ordem):
        acao = ActionChains(self.objeto_awp._drive)
        for t in ordem:
            acao.key_down(t)
        
        time.sleep(0.5)
        acao.perform()
        time.sleep(0.5)    
            
    def wrapper(self, *args, **kwargs):
        run = func(self, *args, **kwargs)
        _ordenacao(self, run)
        
        next(self.objeto_awp._generator_info_contato_acessado)
        next(self.objeto_awp._generator_info_contato_acessado)
        
    return wrapper


def PseudoAWP(func):
    def _deteccao_metodo(obj, item):
        metodo_resolucao = {
                "EM" : obj.msg.enviar_mensagem,
                "EMP" : obj.msg.enviar_mensagem_paragrafada,
                }
        try:
            return metodo_resolucao[item]
            
        except KeyError:
            raise KeyError(f"Método não aceito. Opções: {', '.join(list(metodo_resolucao.keys()))}") 


    def validacao_dados(dicio: dict):
        relacao = {
                "objeto" : None,
                "iter_ctt": None,
                "mensagem" : None,
                "metodo" : None,
                "calibragem" : [True, 10],
                "server_host" : True,
                "anexo" : None,  #a criar...
        }
        if isinstance(dicio, dict):
            objeto = dicio.get('objeto')
            relacao['metodo'] = _deteccao_metodo(objeto, "EMP")

            relacao.update(dicio)
            return relacao
            
        else:
            raise TypeError(f'O objeto {dicio.__name__} do tipo {type(dicio)} é inválido. Passe um objeto do tipo dict para o parâmetro requisitado.')
        
    def _validar_alfabeto_em_contato(contato):   
        try:
            alfabeto = [l for l in string.ascii_lowercase]
            alfabeto_maiusculo = [l for l in string.ascii_uppercase]
            alfabeto.extend(alfabeto_maiusculo)
            contato = [l for l in contato]

            for l in contato:
                if l in alfabeto:
                    return True
            return False
        
        except TypeError as e:
            return False
        
    def wrapper(*args, **kwargs):
        inf = func(*args, **kwargs)
        dict_info = validacao_dados(inf)        
        dict_info['metodo'] = _deteccao_metodo(dict_info['objeto'], dict_info['metodo'])
        dict_info['objeto'].conexao(server_host=dict_info['server_host'], popup=False, calibragem=dict_info['calibragem'])

        for ctt in dict_info['iter_ctt']:
            if _validar_alfabeto_em_contato(ctt):
                dict_info['objeto'].ctt.encontrar_contato(ctt)    
            else:
                dict_info['objeto'].ctt.encontrar_usuario(ctt)
                
            if dict_info['objeto'].InferenciaAWP.contato_acessivel:
                dict_info['metodo'](dict_info['mensagem'])
                
    return wrapper


def aguardeCooldown(func):
    def wrapper(self, *args, **kwargs):
        bool_status, quantidade_realizacao, int_tempo_aguarde  = self._status_aguarde.values()
        f = func(*args, **kwargs)
        
        if bool_status:
            if self.contador > quantidade_realizacao:
                self.contador = 0
                time.sleep(int_tempo_aguarde)
                return f
            self.contador += 1
       
        return f
    return wrapper


def AWPC_Analytics(func):
    def wrapper(self, *args, **kwargs):
        f = func(self, *args, **kwargs)
        var_aux = self.log_get()
        self.objeto_logawp_log(f'AWPCriptografia.{var_aux[1]}: {var_aux[0]}')
        return f
    return wrapper
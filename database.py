# -*- coding: utf-8 -*-
"""
Created on Mon May  8 14:52:53 2017

@author: Dylan N. Sugimoto
"""
import pickle


class arquivo():
    """
        É a classe que trabalha com arquivos.
        Salvar arquivos e ler arquivos salvos.
    """
    def salvar(self, nome_arquivo, banco_dados):
        """
            Salvar arquivo com nome igual ao nome_arquivo sendo os dados do 
            arquivo salvo, o saldo da carteira do jogador e seu progresso.
        """
        #abrir arquivos
        arquivo_saldo = open("imgTeste/"+nome_arquivo+"saldo","wb")
        arquivo_progresso = open("imgTeste/"+nome_arquivo+"progresso","wb")
        arquivo_string_imagem_aviao = open("imgTeste/"+nome_arquivo+"img_aviao","wb")
        arquivo_string_imagem_aviao_inv = open("imgTeste/"+nome_arquivo+
                                               "img_aviao_inv","wb")
        arquivo_XP = open("imgTeste/"+nome_arquivo+"XP","wb")
        #pegar saldo da carteira
        saldo = banco_dados.getCarteira()
        #pegar progresso do jogo
        progresso = banco_dados.getProgresso()
        #pegar a lista de skin de aviao do Jogador
        _string_imagem_aviao = banco_dados.getStringAviao()[0]
        _string_imagem_aviao_inv = banco_dados.getStringAviao()[1]
        #pegar experiencia
        XP = banco_dados.getXP()
        #salvar saldo 
        pickle.dump(saldo,arquivo_saldo)
        #salvar progresso
        pickle.dump(progresso,arquivo_progresso)
        #salvar lista de skin de aviao do Jogador
        pickle.dump(_string_imagem_aviao, arquivo_string_imagem_aviao)
        pickle.dump(_string_imagem_aviao_inv,arquivo_string_imagem_aviao_inv)
        #salvar experiencia
        pickle.dump(XP,arquivo_XP)
        #fechar arquivos
        arquivo_saldo.close()
        arquivo_progresso.close()
        arquivo_string_imagem_aviao.close()
        arquivo_string_imagem_aviao_inv.close()
        arquivo_XP.close()
        
        
    def ler(self, nome_arquivo):
        """
            Ler o arquivo salvo que tem nome dado pela variavel nome_arquivo,
            e retornar as informacoes lidas.
        """
        #abrir arquivos
        arquivo_saldo = open("imgTeste/"+nome_arquivo+"saldo","rb")
        arquivo_progresso = open("imgTeste/"+nome_arquivo+"progresso","rb")
        arquivo_string_imagem_aviao = open("imgTeste/"+nome_arquivo+"img_aviao","rb")
        arquivo_string_imagem_aviao_inv = open("imgTeste/"+nome_arquivo+
                                               "img_aviao_inv","rb")
        arquivo_XP = open("imgTeste/"+nome_arquivo+"XP","rb")
        #pegar saldo da carteira salvo
        saldo = pickle.load(arquivo_saldo)
        #pegar o progresso salvo
        progresso = pickle.load(arquivo_progresso)
        #pegar a lista de skin de aviao do Jogador salvada.
        _string_imagem_aviao = pickle.load(arquivo_string_imagem_aviao)
        _string_imagem_aviao_inv = pickle.load(arquivo_string_imagem_aviao_inv)
        #ler experiencia
        XP = pickle.load(arquivo_XP)
        #fechar arquivos
        arquivo_saldo.close()
        arquivo_progresso.close()
        arquivo_string_imagem_aviao.close()
        arquivo_string_imagem_aviao_inv.close()
        arquivo_XP.close()
        #retornar valor do saldo e do progresso
        return (progresso,saldo, _string_imagem_aviao,_string_imagem_aviao_inv,XP)
        




class BancoDados():
    """
        É classe que guarda informacoes de progresso no jogo.
    """
    def __init__(self,progresso = None, saldo = 0):
        """
            progresso: é uma lista de tuplas. O primeiro argumento da tupla é a
                       quantidade de operacoes concluidas e o segundo é a 
                       quantidade de missoes concluidas daquela operacao.
            carteira:  guarda a quantidade de pontos obtido pelo jogador.
            _string_imagem_aviao: é uma lista de string de imagens.
            _skinAtual: é um inteiro que indica uma posicao na lista de string
                        imagens de aviao.
            _objetivo: é um dicionario que guarda o nome do inimigo que deve 
                        ser abatido e a quantidade deles que deve ser abatida.
            _progresso_objetivo: dicionario que contabiliza os abates.
            _experiencia: guarda a quantidade de pontos de experiencia do 
                          Jogador.
        """
        if progresso == None:
            progresso = [(1,0)]
        self._carteira = saldo
        self._progresso = progresso
        self._objetivo = {}
        self._progresso_objetivo = {}
        self._progresso_objetivo["AviaoInimigo"] = 0
        self._progresso_objetivo["TorreInimiga"] = 0
        self._string_imagem_aviao = ["imgTeste/hellcat2.png"]
        self._string_imagem_aviao_invertido = ["imgTeste/hellcat-2.png"]
        self._skinAtual = 0
        self._experiencia = 0
    
    def MudarSkinAtual(self):
        """
            mudar a string da imagem do aviao do Jogador.
        """
        self._skinAtual += 1
        if self._skinAtual >= len(self._string_imagem_aviao):
            self._skinAtual = 0  
    
    def addStringAviao(self,string_img):
        """
            adiciona uma string na lista.
        """
        self._string_imagem_aviao.append(string_img[0])
        self._string_imagem_aviao_invertido.append(string_img[1])
        
    def getStringAviao(self):
        """
            Pegar a lista de string de imagens de avioes do Jogador.
            Metodo usado para salvar as listas.
        """
        return (self._string_imagem_aviao,self._string_imagem_aviao_invertido)
    
    def getTamListaSkinAviao(self):
        """
            Retorna o tamanho da lista de skins de aviao do jogador
        """
        return len(self._string_imagem_aviao)
        
    def getSkinAtual(self):
        """
            Passar a string imagem da skin atual do aviao do Jogador.
        """
        return (self._string_imagem_aviao[self._skinAtual]
                ,self._string_imagem_aviao_invertido[self._skinAtual])
    
    def setStringAviao(self,string_img):
        """
            Define novas listas de string imagem.
            Metodo usado quando ler um arquivo salvo.
            string_img: é uma tupla de listas de string
        """
        self._string_imagem_aviao = string_img[0]
        self._string_imagem_aviao_invertido = string_img[1]
    
    def setCarteira(self,carteira):
        """
            Define uma nova carteira. 
            Metodo usado quando ler um arquivo salvo.
        """
        self._carteira = carteira
        
    def setExperiencia(self,experiencia):
        """
            Define um novo valor de pontos de experiencia. 
            Metodo usado quando ler um arquivo salvo.
        """
        self._experiencia = experiencia
    
    def setProgresso(self,progresso):
        """
            Define uma nova lista de progresso.
            Metodo usado quando ler um arquivo salvo
        """
        self._progresso = progresso
    
    def getXP(self):
        """
            retorna o saldo de pontos de experiencia do jogador
        """
        return self._experiencia
    
    def getCarteira(self):
        """
            retorna o saldo de pontos do jogador
        """
        return self._carteira
    
    
    def getProgresso(self):
        """
            retorna a lista de progresso
        """
        return self._progresso
    
    
    def acrescimoSaldo(self, acrescimo):
        """
            acrescenta pontos na carteira do jogador
        """
        self._carteira += acrescimo
        
    def acrescimoXP(self, acrescimo):
        """
            acrescenta pontos de experiencia do jogador
        """
        self._experiencia += acrescimo
        
    def passouMissao(self,operacao):
        """
            Atualiza o progresso de missoes naquela operacao.
        """
        tupla_progresso = self._progresso[operacao]
        tupla_passouMissao = (operacao,tupla_progresso[1]+1)
        self._progresso[operacao] = tupla_passouMissao
        
        
    def passouOperacao(self):
        """
            Atualiza o progresso das operacoes
        """
        ultimaOperacao = self.getProgressoOperacao
        self._progresso.append((ultimaOperacao+1,0))
        
        
    def getProgressoOperacao(self):
        """
            retorna o progresso das operacoes
        """
        ultimaOperacao = len(self._progresso)
        return ultimaOperacao
    
    
    def getProgressoMissao(self,Operacao):
        """
            retorna o progresso das missoes naquela operacao
        """
        tupla_progresso = self._progresso[Operacao-1]
        return tupla_progresso[1]
    
    
    def setObjetivo(self,string_objetivo,objetivo):
        """
            armazena qual é o objetivo
        """
        self._objetivo[string_objetivo] = objetivo 
        self.string_objetivo = string_objetivo
        self._progresso_objetivo[string_objetivo] = 0
        
        
    def verificarObjetivo(self):
        """
            verifica se o objetivo foi completado
        """
        if self._progresso_objetivo.get(self.string_objetivo)>=\
            self._objetivo.get(self.string_objetivo):
                completou_objetivo = True
        else:
            completou_objetivo = False
        return completou_objetivo
    
    
    def contabilizarAbate(self,string_abatido):
        """
            contabiliza a quantidade de inimigos abatidos
        """
        self._progresso_objetivo[string_abatido] = \
        self._progresso_objetivo.get(string_abatido)+1
        
        
#-----------------------------Fim da Classe Banco de Dados---------------------
banco_dados = BancoDados()
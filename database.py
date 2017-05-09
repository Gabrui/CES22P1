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
        #pegar saldo da carteira
        saldo = banco_dados.getCarteira()
        #pegar progresso do jogo
        progresso = banco_dados.getProgresso()
        #salvar saldo 
        pickle.dump(saldo,arquivo_saldo)
        #salvar progresso
        pickle.dump(progresso,arquivo_progresso)
        #fechar arquivos
        arquivo_saldo.close()
        arquivo_progresso.close()
        
        
    def ler(self, nome_arquivo):
        """
            Ler o arquivo salvo que tem nome dado pela variavel nome_arquivo,
            e retornar o valor do saldo e a lista de progresso.
        """
        #abrir arquivos
        arquivo_saldo = open("imgTeste/"+nome_arquivo+"saldo","rb")
        arquivo_progresso = open("imgTeste/"+nome_arquivo+"progresso","rb")
        #pegar saldo da carteira salvo
        saldo = pickle.load(arquivo_saldo)
        #salvar progresso salvo
        progresso = pickle.load(arquivo_progresso)
        #fechar arquivos
        arquivo_saldo.close()
        arquivo_progresso.close()
        #retornar valor do saldo e do progresso
        return (progresso,saldo)
        




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
        """
        if progresso == None:
            progresso = [(1,0)]
        self._carteira = saldo
        self._progresso = progresso
        self._objetivo = {}
        self._progresso_objetivo = {}
        self._progresso_objetivo["AviaoInimigo"] = 0
        self._progresso_objetivo["TorreInimiga"] = 0
    
    
    def setCarteira(self,carteira):
        """
            Define uma nova carteira. 
            Metodo usado quando ler um arquivo salvo.
        """
        self._carteira = carteira
    
    
    def setProgresso(self,progresso):
        """
            Define uma nova lista de progresso.
            Metodo usado quando ler um arquivo salvo
        """
        self._progresso = progresso
    
    
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
        print(string_abatido)
        print(self._progresso_objetivo[string_abatido])
        
#-----------------------------Fim da Classe Banco de Dados---------------------
banco_dados = BancoDados()
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 14:52:53 2017

@author: Dylan N. Sugimoto
"""
import pickle

class arquivo():
    
    def salvar(self, nome_arquivo, banco_dados):
        
        arquivo_saldo = open("imgTeste/"+nome_arquivo+"saldo","wb")
        arquivo_progresso = open("imgTeste/"+nome_arquivo+"progresso","wb")
        saldo = banco_dados.getCarteira()
        progresso = banco_dados.getProgresso()
        pickle.dump(saldo,arquivo_saldo)
        pickle.dump(progresso,arquivo_progresso)
        arquivo_saldo.close()
        arquivo_progresso.close()
        
    def ler(self, nome_arquivo):
        
        arquivo_saldo = open("imgTeste/"+nome_arquivo+"saldo","wb")
        arquivo_progresso = open("imgTeste/"+nome_arquivo+"progresso","wb")
        saldo = pickle.dump(arquivo_saldo)
        progresso = pickle.dump(arquivo_progresso)
        arquivo_saldo.close()
        arquivo_progresso.close()
        
        return BancoDados(progresso,saldo)
        
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
        print(self._carteira)
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
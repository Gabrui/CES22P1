# -*- coding: utf-8 -*-
"""
Created on Mon May  1 13:14:34 2017

@author: Dylan N. Sugimoto
"""

import aviao
import motor
import Projetil
import IA
class Simulador(motor.Camada):
    """
        Realiza operacoes de fundo do gameplay, como verificar colisoes.
    """
    def __init__(self, posChao):
        """
            posChao: é a posicao do chao (int).
        """
        self.posChao = posChao
        self.even.escutar("Atirar",self.adicionaFilho)
    
    def verificarColisao(self):
        
        """
            Verifica colisoes.
        """
        #Coletando objetos existentes no gameplay
        figuras, textos = self._observaFilhos()
        for filhos in figuras:
            for irmao in figuras:
                #comparar objetos diferentes
                if filhos != irmao:
                    #definindo ponto canto superior esquerdo
                    filhosTopo = motor.Ponto(filhos[1][0],filhos[1][1])
                    #definindo ponto canto inferior direito
                    filhosFundo = motor.Ponto(filhos[1][2],filhos[1][3])
                    #criando retangulo de referencia
                    referencia = motor.Retangulo(filhosTopo,filhosFundo)
                    #canto superior esquerdo
                    canto1Irmao = motor.Ponto(irmao[1][0],irmao[1][1])
                    #canto inferior direito
                    canto4Irmao = motor.Ponto(irmao[1][2],irmao[1][3])
                    #canto superior direito
                    canto2Irmao = motor.Ponto(irmao[1][2],irmao[1][1])
                    #canto inferior esquerdo
                    canto3Irmao = motor.Ponto(irmao[1][0],irmao[1][3])
                    #cantos: lista dos cantos da Figura
                    cantos = [canto1Irmao,canto2Irmao,canto3Irmao,canto4Irmao]
                    for pontos in cantos:
                        #verifica colisao
                        colisao = referencia.estaDentro(pontos)
                        if colisao:
                            #se houver colisao entre projeteis, remove os dois
                            #projeteis do gameplay
                            if isinstance(filhos,Projetil.Projetil) and isinstance(irmao,Projetil.Projetil):
                                self.removeFilho(filhos[10])
                                self.removeFilho(irmao[10])
                            elif (isinstance(filhos,Projetil.Projetil) and isinstance(irmao, aviao.Aviao)):
                                #Se houver colisao entre Jogador e projetil,
                                #reduz os pontos de vida do Jogador
                                irmao[10].reduzPV(filhos[10].getDano())
                                #chama animacao de fisica de impacto do projetil
                                filhos[10].fisicaDeImpacto()
                                #remove o projetil do gameplay
                                self.removeFilho(filhos[10])
                                #verifica se o Jogador esta vivo
                                if irmao[10].getPV() <= 0:
                                    if isinstance(irmao,aviao.Jogador):
                                        #se nao tiver vivo, chama tela de G.O.
                                        self.even.lancar("GameOver",True)
                            elif(isinstance(filhos, aviao.Aviao) and isinstance(irmao,Projetil.Projetil)):
                                #o mesmo que a anterior
                                filhos[10].reduzPV(filhos[10].getDano())
                                irmao[10].fisicaDeImpacto()
                                self.removeFilho(irmao[10])
                                if filhos[10].getPV() <= 0:
                                    if isinstance(filhos,aviao.Jogador):
                                        self.even.lancar("GameOver",True)
                                       
                            elif (isinstance(filhos,Projetil.Projetil) and isinstance(irmao,IA.IA)):
                                 #Se houver colisao entre projetil e IA
                                 #reduz os pontos de vida da IA
                                 irmao[10].reduzPV(filhos[10].getDano())
                                 #Chama animacao de impacto do projetil
                                
                                 filhos[10].fisicaDeImpacto()
                                 #remove o projetil do gameplay
                                 self.removeFilho(filhos[10])
                                 if irmao[10].getPV() <= 0:
                                     irmao[10].explosao()
                                     #Se IA esvier morta, remove do gameplay
                                     self.removeFilho(irmao[10])
                            elif(isinstance(filhos, IA.IA) and isinstance(irmao,Projetil.Projetil)):
                                #o mesmo que a anterior
                                filhos[10].reduzPV(filhos[10].getDano())
                                irmao[10].fisicaDeImpacto()
                                self.removeFilho(irmao[10])
                                if filhos[10].getPV() <= 0:
                                    filhos[10].explosao()
                                    self.removeFilho(filhos[10])
                                   
            if filhos[1][3] >= self.posChao:
                #verifica colisao com o chao
                if isinstance(filhos, Projetil.Projetil):
                   #Se for projetil ou IA, remove do gameplay
                   self.removeFilho(filhos[10])
                elif isinstance(filhos, aviao.Aviao):
                    #Se for Jogador, chama tela de G.O.
                    filhos[10].explosao()
                    self.even.lancar("GameOver", True)
                elif isinstance(filhos, IA.AviaoInimigo):
                    filhos[10].explosao()
                    self.removeFilho(filhos[10])
                    
                    
                               
                               
                               
                               
                               
                               
                               
                               
                               
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 18:57:11 2017

@author: Dylan N. Sugimoto
"""

class Projetil():
    """
     Representa a ideia abstrata de projetil
    """
    def __init__(self,Imagem,Som,Dano,pos = (0,0),Dono = None):
        """
        Imagem: referencia a imagem do projetil
        Som:    referencia o som do impacto do projetil
        Dano:   Quantidade de dano causado
        Dono:   Quem atirou
        """
        self._Imagem = Imagem
        self._Som = Som
        self._Dano = Dano
        self.Dono = Dono
        self.Pos = pos
        
    def getImagem(self):
        return self._Imagem
    def getSom(self):
        return self._Som
    def getDano(self):
        return self._Dano
    def getDono(self):
        return self.Dono
    def getPos(self):
        return self.Pos
    def getRotacao(self):
        return self.Angulo
    def definirDono(self,Dono):
        self.Dono = Dono
    def fisicaDeVoo(self,posI,velI,acelI):
        """
        Algoritmo da fisica de voo. Calcula posicao final
        ,velocidade final e aceleracao final.
        """
    def fisicaDeImpacto(self, posI,velI,acelI):
        """
        Algoritmo da fisica de impacto. 
        """
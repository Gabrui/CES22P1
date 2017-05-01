# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 18:57:11 2017

@author: Dylan N. Sugimoto
"""
import motor

class Projetil(motor.Figura):
    """
     Representa a ideia abstrata de projetil
    """
    def __init__(self,Imagem,Som,Dano, veli = 0,pos = motor.Ponto(0,0),Dono = None):
        """
        Imagem: referencia a imagem do projetil
        Som:    referencia o som do impacto do projetil
        Dano:   Quantidade de dano causado
        Dono:   Quem atirou
        """
        self._string_imagem = Imagem
        self._Som = Som
        self._Dano = Dano
        self.Dono = Dono
        self.Pos = pos
        self.veli = veli
        
    def clonarProjetil(self):
        return Projetil(self._string_imagem, self._Som, self._Dano, self.Pos, self.Dono)
    def getSom(self):
        return self._Som
    def getDano(self):
        return self._Dano
    def getDono(self):
        return self.Dono
    def definirDono(self,Dono):
        self.Dono = Dono
    def fisicaDeVoo(self,posI,velI):
        """
        Algoritmo da fisica de voo. Calcula posicao final
        ,velocidade final e aceleracao final.
        """
        pass
    def fisicaDeImpacto(self, posI,velI,acelI):
        """
        Algoritmo da fisica de impacto. 
        """
        self.even.lancar("tocarEfeito",self._Som)
    def Disparo(self, posI,direcao):
        self.Pos = posI
        self.direcao = direcao
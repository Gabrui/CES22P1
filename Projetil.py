# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 18:57:11 2017

@author: Dylan N. Sugimoto
"""
import motor
import math

class Projetil(motor.Figura):
    """
     Representa a ideia abstrata de projetil
    """
    def __init__(self,Imagem,Som,Dano,pos, veli = 0,Dono = None):
        """
        Imagem: referencia a imagem do projetil
        Som:    referencia o som do impacto do projetil
        Dano:   Quantidade de dano causado
        Dono:   Quem atirou
        veli:   modulo da velocidade do projetil
        """
        if pos is None:
            pos = motor.Ponto(0,0)
        
        self.direcao = motor.Angulo(0)
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
    def atualiza(self,dt):
        """
        Algoritmo da fisica de voo. Calcula posicao final
        """ 
        #Calula a velocidade X e Y
        velX = math.cos(self.direcao.getAngulo(False))*self.veli
        velY = math.sin(self.direcao.getAngulo(False))*self.veli
        #Truncamento
        VelocidadeX = int(velX)
        VelocidadeY = int(velY)
        #Arredondamento
        if velX - VelocidadeX >=0.5:
            VelocidadeX = VelocidadeX+1
        elif VelocidadeX - velX >= 0.5:
            VelocidadeX = VelocidadeX-1
        if velY - VelocidadeY >= 0.5:
            VelocidadeY = VelocidadeY+1
        elif VelocidadeY - velY >= 0.5:
            VelocidadeY = VelocidadeY-1
        #calcula nova posicao
        posX = self.Pos.getX() + VelocidadeX
        posY = self.Pos.getY() + VelocidadeY
        #atualiza posicao
        self.Pos.setXY( posX, posY)
    def fisicaDeImpacto(self, posI,velI,acelI):
        """
        Algoritmo da fisica de impacto. 
        """
        self.even.lancar("tocarEfeito",self._Som)
    def Disparo(self, posI,direcao):
        self.Pos.setXY( posI.getX(), posI.getY())
        self.direcao = motor.Angulo(direcao)
        
        
        
        
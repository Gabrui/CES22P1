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

    def __init__(self, imagem: object, som: object, dano: object, pos0: object, veli: object = 400,
                 dono: object = None) -> object:
        motor.Figura.__init__(self, imagem, pos = pos0)
        """
        Imagem: referencia a imagem do projetil
        som:    referencia o som do impacto do projetil
        dano:   Quantidade de dano causado
        dono:   Quem atirou
        veli:   modulo da velocidade do projetil
        """
        self._som = som
        self._dano = dano
        self.dono = dono
        self.veli = veli
        
        
    def clonarProjetil(self):
        return Projetil(self._string_imagem, self._som, self._dano, self.pos,
                        self.veli, self.dono)
    
    
    def getSom(self):
        return self._som
    
    
    def getDano(self):
        return self._dano
    
    
    def getDono(self):
        return self.dono
    
    
    def definirDono(self,dono):
        self.dono = dono
    
    
    def atualiza(self, dt):
        """
        Algoritmo da fisica de voo. Calcula posicao final
        """ 
        #Calula a velocidade X e Y
        velX = math.cos(self.rot.getAngulo(False))*self.veli
        velY = - math.sin(self.rot.getAngulo(False))*self.veli
        posX = self.pos.getX() + velX * dt
        posY = self.pos.getY() + velY * dt
        #atualiza posicao
        self.pos.setXY(posX, posY)
    
    
    def fisicaDeImpacto(self):
        """
        Algoritmo da fisica de impacto. 
        """
        self.even.lancar("tocarEfeito",self._som)
    
    
    def Disparo(self, posI, rotacao):
        self.pos.setXY(posI.getX(), posI.getY())
        self.rot.setAngulo(rotacao)
        
        
        
        
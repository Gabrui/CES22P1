# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 19:14:38 2017

@author: Dylan N. Sugimoto
"""

class Vida():
    """
    Representa os pontos de vida
    """
    def __init__(self, Max):
        """
        Max: Quantidade maxima de pontos de vida
        """
        self._MaxVida = Max
        self.Vida = Max
    def getPV(self):
        return self.Vida
    def reduzPV(self, Dano):
        """
        Dano: Quantidade de dano sofrido
        """
        self.Vida -=Dano
        if self.Vida <0:
            self.Vida = 0
            

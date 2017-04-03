# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 18:48:42 2017

@author: Dylan N. Sugimoto
"""

class Arma():
    """Representa a ideia abstrata de arma"""
    
    def __init__(self,Som, Projetil, Dono = None):
        """
        Som:        referencia o som da arma
        Projetil:   nome do projetil que a arma usa
        Dono:       nome da instancia que possui essa arma
        """
        self._Som = Som
        self._Projetil = Projetil
        self.Dono = Dono
        
    def getSom(self):
        return self._Som
    def getProjetil(self):
        return self._Projetil
    def getDono(self):
        return self._Dono
    def setDono(self,Dono):
        self.Dono = Dono
        
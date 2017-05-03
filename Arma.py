# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 18:48:42 2017

@author: Dylan N. Sugimoto
"""
import Projetil

class Arma():
    """Representa a ideia abstrata de arma"""
    
    def __init__(self,Som, projetil, Dono = None):
        """
        Som:        referencia o som da arma
        Projetil:   nome do projetil que a arma usa
        Dono:       nome da instancia que possui essa arma
        """
        
        if projetil is None:
            projetil = Projetil.Projetil()
        
        self._Som = Som
        self._Projetil = projetil
        self.Dono = Dono
        
    def getSom(self):
        return self._Som
    def getProjetil(self):
        projetil = self._Projetil.clonarProjetil()
        return projetil
    def getDono(self):
        return self._Dono
    def setDono(self,Dono):
        self.Dono = Dono
        
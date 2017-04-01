# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 18:48:42 2017

@author: Dylan N. Sugimoto
"""

class Arma():
    """Representa a ideia abstrata de arma"""
    
    def __init__(self,Som, Projetil, Imagem, Dono = None):
        """
        Som:        referencia o som da arma
        Imagem:     referencia a imagem da arma
        Projetil:   nome do projetil que a arma usa
        Dono:       nome da instancia que possui essa arma
        """
        self._Som = Som
        self._Projetil = Projetil
        self._Imagem = Imagem
        self.Dono = Dono
        
    def getSom(self):
        return self._Som
    def getImagem(self):
        return self._Imagem
    def getProjetil(self):
        return self._Projetil
    def getDono(self):
        return self._Dono
    def comprou(self,Dono):
        self.Dono = Dono
        
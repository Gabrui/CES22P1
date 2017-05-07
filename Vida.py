# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 19:14:38 2017

@author: Dylan N. Sugimoto
"""
from motor import Figura
from IA import IA
from aviao import Jogador

class Vida(Figura):
    """
    Representa os pontos de vida
    """
    def __init__(self, Max,string_imagem = None,Dono = None):
        """
        Max: Quantidade maxima de pontos de vida
        pos: é um ponto com a posicao inicial da Vida
        string_imagem: é uma lista de string com o caminho para a imagem da Barra de Vida
        Dono: é o objeto de qual a Vida vai representar a sua barra de vida.
        VidaAtual: é a quantidade de vida que o dono possui atualmente
        """
        Figura.__init__(self,string_imagem[0])
        self._MaxVida = Max
        self.VidaAtual = Max
        self.Dono = Dono
        self.string_imagem = string_imagem
        
    def setDono(self, dono):
        """
            Definir o objeto de qual a Vida vai representar a sua barra de vida.
        """
        self.Dono = dono
    def getPV(self):
       """
           Pegar a quantidade de vida atual.
       """
       return self.VidaAtual
    
    def reduzPV(self, Dano):
        """
            Diminuir a quantidade de vida atual.
            Dano: Quantidade de dano sofrido
            fracao_vida: é uma fração calculado a partir de quantas
                         imagens há na lista de string de imagens.
            bloco_vida: é uma parte da vida maxima calculado a partir de quantas
                        imagens há na lista de string de imagens.
        """
        self.VidaAtual -=Dano
        if self.VidaAtual <0:
            self.VidaAtual = 0
        for i in range(1,len(self.string_imagem)):
            fracao_vida = (len(self.string_imagem)-i)/len(self.string_imagem)
            bloco_vida = self._MaxVida*fracao_vida
            if self.VidaAtual <= bloco_vida:
                self.setString(self.string_imagem[i])
      
            
    def atualiza(self,dt):
        
        if isinstance(self.Dono, IA):
            posX = self.Dono.pos.getX()
            posY = self.Dono.pos.getY()-40
            self.pos.setXY(posX,posY)
        elif isinstance(self.Dono, Jogador):
            posX = self.Dono.pos.getX() + 150
            posY = self.Dono.pos.getY() - 350
            self.pos.setXY(posX,posY)

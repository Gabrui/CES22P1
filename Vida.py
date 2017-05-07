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
            posX = 700
            posY = 0
            self.pos.setXY(posX,posY)

class Velocimetro(Figura):
    
    """
    Representa o HUD Velocimetro.
    """
    def __init__(self, Max,string_imagem = None,Dono = None):
        """
        Max: Quantidade maxima de velocidade
        pos: é um ponto com a posicao inicial do Velocimetor
        string_imagem: é uma lista de string com o caminho para a imagem do 
                        Velocimetro.
        Dono: é o objeto de qual o Velocimetro vai representar a sua barra de 
              velocidade.
        VelAtual: é a velocidade que o dono possui atualmente
        """
        Figura.__init__(self,string_imagem[0])
        self._MaxVida = Max
        self.VelAtual = Max
        self.Dono = Dono
        self.string_imagem = string_imagem
        
    def setDono(self, dono):
        """
            Definir o objeto de qual o Velocimetro vai representar a sua 
            velocidade.
        """
        self.Dono = dono
    def getVel(self):
       """
           Pegar a quantidade de velocidade atual.
       """
       return self.VelAtual
    
    def atualizaVel(self, Dano):
        """
            Atualiza a imagem do velocimetro
            fracao_vel: é uma fração calculado a partir de quantas
                         imagens há na lista de string de imagens.
            bloco_vel: é uma parte da velocidade maxima calculado 
                        a partir de quantas imagens há na lista de string de 
                        imagens.
        """
        self.VelAtual = self.Dono.velo
        for i in range(1,len(self.string_imagem)):
            fracao_vel = (len(self.string_imagem)-i)/len(self.string_imagem)
            bloco_vel = self._MaxVida*fracao_vel
            if self.VelAtual <= bloco_vel:
                self.setString(self.string_imagem[i])
      
            
    def atualiza(self,dt):
        
        if isinstance(self.Dono, Jogador):
            posX = self.Dono.pos.getX() - 150 
            posY = self.Dono.pos.getY() + 350
            self.pos.setXY(posX,posY)

class Altimetro(Figura):
    
    """
    Representa o HUD Velocimetro.
    """
    def __init__(self, Max,string_imagem = None,Dono = None):
        """
        Max: Quantidade maxima de altitude
        pos: é um ponto com a posicao inicial do altimetro
        string_imagem: é uma lista de string com o caminho para a imagem do 
                        altimetro.
        Dono: é o objeto de qual o Velocimetro vai representar a sua barra de 
              altitude.
        altitudeAtual: é a altitude que o dono possui atualmente
        """
        Figura.__init__(self,string_imagem[0])
        self._MaxVida = Max
        self.altitudeAtual = Max
        self.Dono = Dono
        self.string_imagem = string_imagem
        
    def setDono(self, dono):
        """
            Definir o objeto de qual altimetro vai representar a sua altitude.
        """
        self.Dono = dono
        
    def getAltitude(self):
        
       """
           Pegar a altitude Atual.
       """
       return self.altitudeAtual
    
    def atualizaAltitude(self, Dano):
        """
            Atualiza a imagem da altitude
            Dano: Quantidade de dano sofrido
            fracao_altitude: é uma fração calculado a partir de quantas
                         imagens há na lista de string de imagens.
            bloco_altitude: é uma parte da vida maxima calculado a partir de quantas
                            imagens há na lista de string de imagens.
        """
        self.altitudeAtual = self.Dono.pos.getY()
        for i in range(1,len(self.string_imagem)):
            fracao_altitude = (len(self.string_imagem)-i)/len(self.string_imagem)
            bloco_altitude = self._MaxVida*fracao_altitude
            if self.altitudeAtual <= bloco_altitude:
                self.setString(self.string_imagem[i])
      
            
    def atualiza(self,dt):
        
        if isinstance(self.Dono, Jogador):
            posX = 100 
            posY = 350
            self.pos.setXY(posX,posY)
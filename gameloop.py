# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 19:29:56 2017

@author: Dylan N. Sugimoto
"""

from motor import Audio, Renderizador, Entrada, Evento, Figura, Cena, Retangulo, Ponto
import time
from cenario import FundoParalaxeInfinito
from aviao import Jogador

t20 = 50/1000
FPS = 60
td = 1/FPS

class Jogo():
    """Controla o loop principal do jogo, faz as transições de cena"""
    
    def __init__(self):
        """Ainda é só um esboço"""
        self.audio = Audio()
        self.renderizador = Renderizador(800,600)
        self.entrada = Entrada()
        self.even = Evento()
        self.even.escutar("sair", self.irParaCena)
        self.continuarLoop = True
        self.cenaAtual = None
        self.gameplay()
        self.gameloop()
    
    """Ainda estou pensando, podemos discutir esses métodos"""
    def gameplay(self):
        fundos = FundoParalaxeInfinito(800, 600, "imgTeste/estFundo.png", 
                    Retangulo(Ponto(0,0), Ponto(800, 132)), Ponto(0,0), Ponto(0,0))
        #fundo2 = Figura("imgTeste/movFundo.png")
        #fundo3 = Figura("imgTeste/nuvem.png")
        avi = Jogador("imgTeste/hellcat2.png", Ponto(100, 0), 
                 [8000, 90000, 172],  [8000, 4000, 8000, 100, 0.3, 5400, 1],  
                 [5, 50000, 5000/3, 100], [5000, 150])
        
        self.cenaAtual = Cena(self.audio,self.entrada,self.renderizador)
        self.cenaAtual.adicionaFilho(fundos)
        #self.cenaAtual.adicionaFilho(fundo2)
        #self.cenaAtual.adicionaFilho(fundo3)
        self.cenaAtual.adicionaFilho(avi)
        
        #self.even.escutar('MenuPause',self.menuPause)
        #self.even.escutar('Hangar',self.hangar)
    
    
    def gameloop(self):
        tnovo = time.clock()
        while self.continuarLoop:
            tantigo = tnovo
            tnovo = time.clock()
            dt = tnovo - tantigo
            print(dt)
            if dt < td:
                time.sleep(td - dt)
            if dt > t20:
                dt = t20
            self.cenaAtual.atualiza(dt)

            
 
            
    def carregaCenas(self, listaCenas):
        pass
    
    
    def rodarCena(self, cena):
        pass
    
    
    def irParaCena(self, cena):
        if cena is None:
            self.continuarLoop = False
    
    
    def atualizar(self):
        #Relógio
        dt = 15 #Time1 - time0
        if self.continuarLoop:
            self.CenaAtual.atualiza(dt)
            self.cenaAtual.even.propagaLancamento(self.even)
    
Jogo()
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 19:29:56 2017

@author: Dylan N. Sugimoto
"""

from motor import Audio, Renderizador, Entrada, Evento, Figura, Cena, Retangulo, Ponto
import time

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
        fundo1 = Figura("imgTeste/estFundo.png")
        fundo2 = Figura("imgTeste/movFundo.png")
        fundo3 = Figura("imgTeste/nuvem.png")
        aviao = Figura("imgTeste/hellcat2.png")
        
        self.cenaAtual = Cena(self.audio,self.entrada,self.renderizador)
        self.cenaAtual.adicionaFilho(fundo1)
        self.cenaAtual.adicionaFilho(fundo2)
        self.cenaAtual.adicionaFilho(fundo3)
        self.cenaAtual.adicionaFilho(aviao)
        
        #self.even.escutar('MenuPause',self.menuPause)
        #self.even.escutar('Hangar',self.hangar)
    
    
    def gameloop(self):
        tnovo = time.clock()
        while self.continuarLoop:
            tantigo = tnovo
            tnovo = time.clock()
            dt = tnovo - tantigo
            if dt < td:
                time.sleep(td - dt)
            if dt > t20:
                dt = t20
            self.cenaAtual.atualiza(dt)
            self.even.recebeEscuta(self.cenaAtual.even)
            
 
            
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
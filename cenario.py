#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 21:23:16 2017

@author: gabrui
"""

from motor import Camada, Ponto, Figura


class Camera(Camada):
    
    def __init__(self):
        super().__init__()
    
    
    def setPos(self, ponto):
        self.pos = ponto.escalar(-1)
    
    def setAngulo(self, angulo):
        self.rot = angulo.escalar(-1)
    


class Cenario(Camada):
    
    def __init__(self):
        super().__init__()
    

class FundoParalaxeInfinito(Camada):
    
    def __init__(self, larguraTela, alturaTela, textura, corte, pos0, rel):
        """
        Camada que instancia e gerencia um fundo de paralaxe infinito
        @param: textura string
        @param: corte Retangulo
        @param: pos0 Ponto
        @param: rel Ponto De 0 a 1, 1 fundo é estático
        """
        super().__init__()
        self.larguraTela = larguraTela
        self.alturaTela = alturaTela
        self.altura = alturaTela - corte.getAltura() - pos0.getY()
        self.largura = corte.getLargura()
        self.quant = self.larguraTela/self.largura
        self.rel = rel
        
        if rel.getX() > 0:
            self.quant += 1
        
        for i in range(self.quant):
            figura = Figura(textura, corte, 
                    Ponto(i*self.largura+pos0.getX(), self.altura+pos0.getY()))
            self.adicionaFilho(figura)
    
    
    def atualizaFundo(self, dx, dy):
        for filho in self.filhos:
            delta = Ponto(self.rel.getX()*dx, self.rel.getY()*dy)
            filho.pos.soma(delta)
            if filho.retang.getEsquerda() + delta.getX() < - self.largura:
                filho.pos.soma(Ponto(self.largura + self.larguraTela, 0))
            elif filho.retang.getDireita() + delta.getX() > self.larguraTela:
                filho.pos.soma(Ponto(-self.largura - self.larguraTela, 0))
        
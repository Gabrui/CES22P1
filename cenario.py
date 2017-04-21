#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 21:23:16 2017

@author: gabrui
"""

from motor import Camada


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
        super().__init__()
        self.larguraTela = larguraTela
        self.alturaTela = alturaTela
        self.altura = alturaTela - corte.getAltura() - pos0.getY()
        self.largura = corte.getLargura()
        self.num = self.larguraTela/self.largura
        
        if rel.getX() > 0:
            self.num += 1
        
        for i in range(num):
            figura = Figura(textura, corte, Ponto(i*self.largura, self.altura))
            self.adicionaFilho(figura)
    
    
    def atualizaFundo(self, dx, dy):
        for filho in self.filhos:
            filho.pos.setXY(rel.getX()*dx, rel.getY()*dy)
            if filho
        
    
    function FazerFundos (textura, acrescimoY, razaoVeloX, razaoVeloY) {
    
    var fundos = new Array();
    var i;
    var altura = tamV - textura.height - acrescimoY;
    var largura = textura.width;
    var num = Math.ceil(tamH/largura);
    if (razaoVeloX>0)
        num++;
    for ( i = 0; i < num; i++) {
        fundos[i] = new PIXI.Sprite(textura);
        fundos[i].x = i * largura;
        fundos[i].y = altura;
        fundo.addChild(fundos[i]);
    }
    this.atualiza = function () {
        for ( i=0; i<num; i++) {
            fundos[i].x += (1-razaoVeloX) * movel.veloX;
            fundos[i].y += (1-razaoVeloY) * movel.veloY;
            if (fundos[i].x + movel.x < -largura)
                fundos[i].x += tamH+largura;
            else if (fundos[i].x +movel.x > tamH)
                fundos[i].x -= tamH+largura;
        }
    };
}

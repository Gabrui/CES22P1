# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 21:15:54 2017

@author: Dennys
"""

import unittest
# Devaneios geométricos
class Ponto:
    """Classe que representa um ponto 2d do tipo (x, y)"""
    def __init__ (self, x = 0, y = 0):
        self._x = x
        self._y = y
    
    
    def setXY(self, x, y):
        self._x = x
        self._y = y
    
    
    def setX(self, x):
        self._x = x
    
    
    def setY(self, y):
        self._y = y
    
    
    def getX(self):
        return self._x
    
    
    def getY(self):
        return self._y
    
    
    def getXY(self):
        return (self._x, self._y)
    
    
    def distancia2(self, ponto):
        return ((self._x-ponto._x)*(self._x-ponto._x) + 
                (self._y-ponto._y)*(self._y-ponto._y) )
    
    
    def distancia(self, ponto):
        from math import sqrt
        return sqrt(self.distancia2(ponto))
    
    
    def soma(self, ponto):
        """Soma um outro ponto a si próprio"""
        self._x = self._x + ponto._x
        self._y = self._y + ponto._x
    
    
    def retornaSoma(self, ponto):
        """Retorna um novo ponto resultado da soma de si por outro, sem alterar
        o seu próprio valor"""
        return Ponto((self._x + ponto._x, self._y + ponto._y))     
    
    
    def clonar(self):
        """Retorna uma cópia de si mesmo"""
        return Ponto(self._x, self._y)




class Retangulo:
    """Classe que representa um retângulo horizontal"""


    def __init__(self, ponto1 = Ponto(0, 0), ponto2 = None,
                 largura = 0, altura = 0):
        """Inicializa o retângulo com dois pontos ou com um ponto e uma largura
        e uma altura"""
        self._p1 = ponto1
        if ponto2 is not None:
            self._p2 = ponto2
        else:
            self._p2 = self._p1.retornaSoma(Ponto(largura, altura))
    
    # As funções do tipo get SEMPRE devem retornar um NOVO objeto e não uma
    # referência a objetos que ele já tem
    def getLargura(self):
        """"Retorna o valor da largura do retângulo, um valor SEMPRE positivo,
        independentemente da posição dos pontos"""
        larg = self._p1.getX()-self._p2.getX()
        if larg>0:
            return larg
        else:
            return -larg
    
    
    def getAltura(self):
        """Retorna o valor da altura do retângulo, um valor SEMPRE positivo"""
        alt = self._p1.getY()-self._p2.getY()
        if alt>0:
            return alt
        else:
            return -alt

    
    def getTopoEsquerdo(self):
        """Retorna um ponto que representa o ponto superior esquerdo"""
        if self._p1.getX() < self._p2.getX():
            if self._p1.getY() < self._p2.getY():
                return self._p1.clonar()
            else:
                return Ponto(self._p1.getX(), self._p2.getY())
        else:
            if self._p2.getY() < self._p1.getY():
                return self._p2.clonar()
            else:
                return Ponto(self._p2.getX(), self._p1.getY())
    
    
    def getTopoDireito(self):
        """Retorna um ponto que representa o ponto superior direito"""
        return Ponto(self.getTopoEsquerdo()._x + self.getLargura(), \
                     self.getTopoEsquerdo()._y)
    
    
    def getFundoEsquerdo(self):
        """Retorna um ponto que representa o ponto inferior esquerdo"""
        return Ponto(self.getTopoEsquerdo()._x, self.getTopoEsquerdo()._y + \
                     self.getAltura())
    
    
    def getFundoDireito(self):
        """Retorna um ponto que representa o ponto inferior direito"""
        return Ponto(self.getTopoDireito()._x, self.getTopoDireito()._y + \
                     self.getAltura())
    
    
    def setRetangulo(self, ponto1, ponto2):
        """Modifica o retângulo, definindo-o com relação aos pontos"""
        self._p1 = ponto1
        self._p2 = ponto2
    
    
    def setRetanguloQueContem(self, lista_retangulos):
        """Modifica o retângulo, definindo-o como o menor retângulo que contém
        todos os outros retângulos da lista de retângulos."""
        x_esquerda = lista_retangulos[0].getTopoEsquerdo().getX()
        y_esquerda = lista_retangulos[0].getTopoEsquerdo().getY()
        x_direita = lista_retangulos[0].getFundoDireito().getX()
        y_direita = lista_retangulos[0].getTopoDireito().getY()
        for retangulo in lista_retangulos:
            if x_esquerda > retangulo.getTopoEsquerdo().getX():
                x_esquerda = retangulo.getTopoEsquerdo().getX()
            if y_esquerda > retangulo.getTopoEsquerdo().getY():
                y_esquerda = retangulo.getTopoEsquerdo().getY()
            if x_direita < retangulo.getFundoDireito().getX():
                x_direita = retangulo.getFundoDireito().getX()
            if y_direita < retangulo.getFundoDireito().getY():
                y_direita = retangulo.getFundoDireito().getY()
            
    
    def estaDentro(self, ponto):
        """Dado um objeto do tipo Ponto, retorna verdadeiro se ele está dentro
        do retângulo"""
        if ponto._x > self.getTopoEsquerdo()._x and ponto._y > \
        self.getTopoEsquerdo() and ponto._x < self.getFundoDireito()._x and \
        ponto._y < self.getFundoDireito()._y:
            return True
        else:
            return False

class RetanguloTeste(unittest.TestCase):
    
    def setUp(self):
        self.r1 = Retangulo(Ponto(0,0), Ponto(6,6))
        self.r2 = Retangulo(Ponto(3,2), Ponto(-2, 3))
        self.r3 = Retangulo(Ponto(-14,3), Ponto(231,3))
    
    def testaGetTopoEsquerdo(self):
        self.assertEqual(self.r1.getTopoEsquerdo().getX(), 0)
        self.assertEqual(self.r1.getTopoEsquerdo().getY(), 0)
        self.assertEqual(self.r2.getTopoEsquerdo().getX(), -2)
        self.assertEqual(self.r2.getTopoEsquerdo().getY(), 2)
        self.assertEqual(self.r3.getTopoEsquerdo().getX(), -14)
        self.assertEqual(self.r3.getTopoEsquerdo().getY(), 3)
        
    def testaGetTopoDireito(self):
        self.assertEqual(self.r1.getTopoDireito().getX(), 6)
        self.assertEqual(self.r1.getTopoDireito().getY(), 0)
        self.assertEqual(self.r2.getTopoDireito().getX(), 3)
        self.assertEqual(self.r2.getTopoDireito().getY(), 2)
        self.assertEqual(self.r3.getTopoDireito().getX(), 231)
        self.assertEqual(self.r3.getTopoDireito().getY(), 3)
        
    def testaGetFundoEsquerdo(self):
        self.assertEqual(self.r1.getFundoEsquerdo().getX(), 0)
        self.assertEqual(self.r1.getFundoEsquerdo().getY(), 6)
        self.assertEqual(self.r2.getFundoEsquerdo().getX(), -2)
        self.assertEqual(self.r2.getFundoEsquerdo().getY(), 3)
        self.assertEqual(self.r3.getFundoEsquerdo().getX(), -14)
        self.assertEqual(self.r3.getFundoEsquerdo().getY(), 3)
        
    def testaGetFundoDireito(self):
        self.assertEqual(self.r1.getFundoDireito().getX(), 6)
        self.assertEqual(self.r1.getFundoDireito().getY(), 6)
        self.assertEqual(self.r2.getFundoDireito().getX(), 3)
        self.assertEqual(self.r2.getFundoDireito().getY(), 3)
        self.assertEqual(self.r3.getFundoDireito().getX(), 231)
        self.assertEqual(self.r3.getFundoDireito().getY(), 3)
        
        
if __name__ == '__main__':
    unittest.main()
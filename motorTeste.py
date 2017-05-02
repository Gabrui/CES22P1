#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 13:49:41 2017

@author: gabrui
"""

import unittest


from motor import Aux, Angulo, Ponto, Retangulo, Evento

class AuxTeste(unittest.TestCase):
    
    #Esse setUp é do unittest, e é executado antes de cada novo teste
    def setUp(self):
        self.tuplas1 = [(423,43), (32,45), (43,234)]
        self.tuplas2 = [(342,34,445), (884,1,4)]
        self.tuplas3 = [(1, 34), (3, 23), (1, 32)]
    
    
    def testaRemoveTuplas1Elem(self):
        Aux.removeTuplas1Elem(self.tuplas1, 43)
        self.assertEqual(self.tuplas1, [(423,43), (32, 45)])
        Aux.removeTuplas1Elem(self.tuplas2, 34)
        self.assertEqual(self.tuplas2, self.tuplas2)
        Aux.removeTuplas1Elem(self.tuplas3, 1)
        self.assertEqual(self.tuplas3, [(3,23)])
    
    
    def testaExisteTupla1Elem(self):
        self.assertTrue(Aux.existeTupla1Elem(self.tuplas1, 43))
        self.assertFalse(Aux.existeTupla1Elem(self.tuplas2, 1))
        self.assertTrue(Aux.existeTupla1Elem(self.tuplas3, 1))
    
    
    def testaCoordsInscrito(self):
        self.assertAlmostEqual(Aux.coordsInscrito(Angulo(0), 5, 5, 9, 9)[0], 5)
        self.assertAlmostEqual(Aux.coordsInscrito(Angulo(0), 5, 5, 9, 9)[1], 5)
        self.assertAlmostEqual(Aux.coordsInscrito(Angulo(45), 1, 1, 2,2)[0], 
                               2**0.5)
        self.assertAlmostEqual(Aux.coordsInscrito(Angulo(45), 1, 1, 2,2)[1], 
                               2**0.5)
        self.assertAlmostEqual(Aux.coordsInscrito(Angulo(135), 1, 1, 2,2)[0], 
                               2**0.5)
        self.assertAlmostEqual(Aux.coordsInscrito(Angulo(135), 1, 1, 2,2)[1], 
                               2**0.5)
        self.assertAlmostEqual(Aux.coordsInscrito(Angulo(225), 1, 1, 2,2)[0], 
                               2**0.5)
        self.assertAlmostEqual(Aux.coordsInscrito(Angulo(225), 1, 1, 2,2)[1], 
                               2**0.5)
        self.assertAlmostEqual(Aux.coordsInscrito(Angulo(315), 1, 1, 2,2)[0], 
                               2**0.5)
        self.assertAlmostEqual(Aux.coordsInscrito(Angulo(315), 1, 1, 2,2)[1], 
                               2**0.5)
        self.assertAlmostEqual(Aux.coordsInscrito(Angulo(-45), 1, 1, 2,2)[0], 
                               2**0.5)
        self.assertAlmostEqual(Aux.coordsInscrito(Angulo(-45), 1, 1, 2,2)[1], 
                               2**0.5)
        



#Gabriel: Sugou escrever os testes do que eu já programei, vou fazer dos outros
class EventoTeste(unittest.TestCase):
    
    def setUp(self):
        self.even1 = Evento()
        self.even2 = Evento()
        self.even3 = Evento()
    
    def testaSingleton(self):
        self.assertEqual(self.even1, self.even2)
        self.assertEqual(self.even3, self.even2)
    
    
    def testaEscutas(self):
        t = []
        callback1 = lambda lista: lista.append(1)
        callback2 = lambda lista: lista.append(2)
        callback3 = lambda lista: lista.append(3)
        self.even1.escutar('ola', callback1)
        self.even2.escutar('ok', callback2)
        self.even3.escutar('blz', callback3)
        self.even1.lancar('ok', t)
        self.assertEqual(t, [2])
        self.even2.lancar('blz', t)
        self.assertEqual(t, [2, 3])
        self.even3.lancar('ola', t)
        self.assertEqual(t, [2, 3, 1])
    


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
        
        



    
#Executa os testes, se estivermos executando este arquivo
if __name__ == '__main__':
    unittest.main()
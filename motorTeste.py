#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 13:49:41 2017

@author: gabrui
"""

import unittest


from motor import Aux, Angulo, Ponto, Retangulo, Evento, Camada, Figura, \
    Renderizador, Audio, Entrada, Cena, Cor, Texto
from math import sin, cos, atan2, sqrt, pi


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
        self.assertAlmostEqual(Aux.coordsInscrito(Angulo(45), 0, 0, 2,2)[0], 
                               0)
        self.assertAlmostEqual(Aux.coordsInscrito(Angulo(45), 0, 0, 2,2)[1], 
                               2**0.5)
        self.assertAlmostEqual(Aux.coordsInscrito(Angulo(135), 0, 0, 2,2)[0], 
                               2**0.5)
        self.assertAlmostEqual(Aux.coordsInscrito(Angulo(135), 0, 0, 2,2)[1], 
                               2*(2**0.5))
        self.assertAlmostEqual(Aux.coordsInscrito(Angulo(-45), 0, 0, 2,2)[0], 
                               2**0.5)
        self.assertAlmostEqual(Aux.coordsInscrito(Angulo(-45), 0, 0, 2,2)[1], 
                               0)
        self.assertAlmostEqual(Aux.coordsInscrito(Angulo(-135), 0, 0, 2,2)[0], 
                               2*(2**0.5))
        self.assertAlmostEqual(Aux.coordsInscrito(Angulo(-135), 0, 0, 2,2)[1], 
                               2**0.5)
        



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
        self.even1.escutar('ola', callback2)
        self.even3.lancar('ola', t)
        self.assertEqual(t, [2, 3, 1, 1, 2])
        self.even1.escutar('ola', callback3)
        self.even3.lancar('ola', t)
        self.assertEqual(t, [2, 3, 1, 1, 2, 1, 2, 3])
        self.even3.lancar('olasssss', t)
        self.even1.pararDeEscutarTudo()
        self.even1.lancar('ok', t)
        self.even1.lancar('ola', t)
        self.even1.lancar('blz', t)
        self.assertEqual(t, [2, 3, 1, 1, 2, 1, 2, 3])
    
    
    def testaPararDeEscutar(self):
        t = []
        callback1 = lambda lista: lista.append(1)
        callback2 = lambda lista: lista.append(2)
        self.even1.escutar('ola', callback1)
        self.even1.escutar('ola', callback2)
        self.even1.escutar('ola', callback1)
        self.even1.pararDeEscutar('ola', callback1)
        self.even1.lancar('ola', t)
        self.assertEqual(t, [2])
        self.even1.pararDeEscutarTudo()
        self.even1.lancar('ola', t)
        self.assertEqual(t, [2])
        self.even1.escutar('ola', callback1)
        self.even1.escutar('ola', callback2)
        self.even1.lancar('ola', t)
        self.assertEqual(t, [2, 1, 2])
    



class PontoTeste(unittest.TestCase):
    
    def setUp(self):
        self.p1 = Ponto(0, 0)
        self.p2 = Ponto(44, 32)
        self.p3 = Ponto(400, 200)
    
    
    def testeSomaSi(self):
        self.p2 += self.p3
        self.assertEqual(self.p2.getXY(), (444, 232))
    
    
    def testeSoma(self):
        self.assertEqual(444, (self.p2 + self.p3).getX())
        self.assertEqual(232, (self.p2 + self.p3).getY())
    
    
    def testeMultiplicacao(self):
        self.assertEqual((self.p1 * self.p2).getX(), 0)
        self.assertEqual((self.p1 * self.p2).getY(), 0)
        self.assertEqual((self.p1 * self.p3).getX(), 0)
        self.assertEqual((self.p1 * self.p3).getY(), 0)




class RetanguloTeste(unittest.TestCase):
    
    def setUp(self):
        self.r1 = Retangulo(Ponto(0,0), Ponto(6,6))
        self.r2 = Retangulo(Ponto(3,2), Ponto(-2, 3))
        self.r3 = Retangulo(Ponto(-14,3), Ponto(231,3))
    
    
    def testeGetEsquerda(self):
        self.assertEqual(self.r1.getEsquerda(), 0)
        self.assertEqual(self.r2.getEsquerda(), -2)
        self.assertEqual(self.r3.getEsquerda(), -14)
    
    
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
        



class AnguloTeste(unittest.TestCase):
    
    def setUp(self):
        self.a1 = Angulo(100)
        self.a2 = Angulo(200)
        self.a3 = Angulo(730)
        self.a4 = Angulo(pi, False)
        self.a5 = Angulo(4*pi, False)
        self.a6 = Angulo(-2*pi, False)
    
    
    def testeInicial(self):
        self.assertEqual(self.a1.getAngulo(), 100)
        self.assertEqual(self.a2.getAngulo(), -160)
        self.assertEqual(self.a3.getAngulo(), 10)
        self.assertEqual(self.a1.getAngulo(False), pi*100/180)
        self.assertEqual(self.a4.getAngulo(), 180)
        self.assertEqual(self.a5.getAngulo(), 0)
        self.assertEqual(self.a6.getAngulo(), 0)
    
    
    def testeIncremento(self):
        self.a1.incrementa(100)
        self.assertEqual(self.a1.getAngulo(), -160)
        self.a3.incrementa(200)
        self.assertEqual(self.a3.getAngulo(), -150)




class CamadaTeste(unittest.TestCase):
    
    def setUp(self):
        self.f1 = Figura(imagem, Retangulo(Ponto(0,0), Ponto(100, 100)))
        self.f2 = Figura(imagem, Retangulo(Ponto(0,0), Ponto(100, 100)), 
                         Ponto(21, 94))
        self.c0 = Camada()
        self.c1 = Camada(Ponto(43, 27))
        self.c2 = Camada(Ponto(1002, 3842))
        self.c3 = Camada(rot = Angulo(54))
    
    
    def testeTranslacao(self):
        self.c1.adicionaFilho(self.f1)
        self.c1.adicionaFilho(self.f2)
        self.c2.adicionaFilho(self.c1)
        figs, texs = self.c2._observaFilhos()
        self.assertEqual(figs[0][2], 43)
        self.assertEqual(figs[0][3], 27)
        self.assertEqual(figs[1][2], 43+21)
        self.assertEqual(figs[1][3], 27+94)
    
    
    def testeRotacaoPura(self):
        self.c3.adicionaFilho(self.f1)
        self.c3.adicionaFilho(self.f2)
        self.c2.adicionaFilho(self.c3)
        figs, text = self.c2._observaFilhos()
        a = self.c3.rot.getAngulo(False)
        self.assertAlmostEqual(figs[0][2], 0)
        self.assertAlmostEqual(figs[0][3], 0)
        self.assertAlmostEqual(figs[1][2], 21*cos(a) + 94*sin(a))
        self.assertAlmostEqual(figs[1][3], 94*cos(a) - 21*sin(a))
        

rend = Renderizador("Teste", 800, 600)
audi = Audio()
entr = Entrada()
imagem = "imgTeste/sky.png"

class CenaTeste(unittest.TestCase):
    
    def setUp(self):
        self.cena = Cena(audi, entr, rend)
    
    
    def testarFiguras(self):
        pos = Ponto(200, 200)
        centro = Ponto(0, 0)
        f1 = Figura(imagem, Retangulo(Ponto(0,0), Ponto(100, 100)), pos, 
                    rot = Angulo(130), centro = centro)
        f2 = Figura(imagem, Retangulo(Ponto(0,0), Ponto(100, 100)), pos, 
                    centro = Ponto(100,100))
        texto = Texto("Teste", ("Sans", 20, False, False), 
                      cor = Cor(1, 255, 255, 255, 1))
        self.cena.adicionaFilho(f1)
        self.cena.adicionaFilho(f2)
        self.cena.adicionaFilho(texto)
        self.cena.atualiza(1)
        
        
    


    
#Executa os testes, se estivermos executando este arquivo
if __name__ == '__main__':
    unittest.main()
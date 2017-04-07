#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 13:49:41 2017

@author: gabrui
"""

import unittest


from motor import Aux, Angulo
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
    pass
    
    
#Executa os testes, se estivermos executando este arquivo
if __name__ == '__main__':
    unittest.main()
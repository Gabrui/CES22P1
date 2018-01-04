# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 18:22:13 2017

@author: Dylan N. Sugimoto
"""

""" UNUSED """


class Missao:

    def __init__(self, PlayBack, BackScene, Inimigo, Objetivo, EstadoMissao=False,
                 Disponivel=False):
        """
        PlayBack:     referencia da musica de fundo
        BackScene:    referencia da cena de fundo
        EstadoMissao: Completou (True) ou nao (False) a missao
        Disponivel:   Missao jogavel (True) ou nao jogavel (False)
        Inimigo:      lista com numero de inimigos de 
                      cada tipo da missao [(NomeDoInimigo,quantidade)]
        Objetivo:     Objetivo da missao.Lista [NomeDoInimigo,quantidade]
        """
        self._PlayBack = PlayBack
        self._BackScene = BackScene
        self._Inimigo = Inimigo
        self.EstadoMissao = EstadoMissao
        self._Disponivel = Disponivel
        self._Objetivo = Objetivo

    def completouMissao(self):
        return self.EstadoMissao

    def missaoJogavel(self, EstadoMissaoAnterior):
        if EstadoMissaoAnterior == True:
            self._Disponivel = True

    def getPlayback(self):
        return self._PlayBack

    def getBackScene(self):
        return self._BackScene

    def getInimigo(self):
        return self._Inimigo

    def getObjetivo(self):
        return self._Objetivo

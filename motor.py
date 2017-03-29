#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 08:25:06 2017

@author: gabrui
"""

import pygame

pygame.init()


class Aux:
    """Classes com funções auxiliares para mexer com listas etc..."""
    @staticmethod
    def removeTuplas1Elem(lista, elem):
        i = 0
        while i < len(lista):
            if lista[i][0] == elem:
                del lista[i]
            i += 1
    
    @staticmethod
    def existeTupla1Elem(lista, elem):
        for tupla in lista:
            if tupla[0] == elem:
                return True




class Evento:
    """É uma classe que todo objeto que registra eventos deve ter uma instância"""
    _escutaveis = [] #É uma lista de tuplas (stringEvento, funcao_de_chamada) APARADOS
    _disparados = []  #É uma lista de tuplas (stringsEventos, objeto_do_evento) LANÇADOS
    
    
    def adicionaEscutavel(this, string_evento, callback):
        this._escutaveis.append((string_evento, callback))
    
    
    def removeEscutavel(this, string_evento, callback = None):
        if callback is None:
            Aux.removeTuplas1Elem(this._escutaveis, string_evento)
        else:
            this._escutaveis.remove((string_evento, callback))
    
    
    def adicionaDisparo(this, string_evento, objeto_do_evento):
        if Aux.existeTupla1Elem(this._escutaveis, string_evento):
            this._disparados.append((string_evento, objeto_do_evento))
    
    
    def removeDisparo(this, string_evento, objeto_do_evento = None):
        if objeto_do_evento is None:
            Aux.removeTuplas1Elem(this._disparados, string_evento)
        else:
            this._disparados.remove((string_evento, objeto_do_evento))
    
    
    def removeTodosDisparos(this):
        del this._disparados[:]
    
    
    def escuta(this, evento):
        """Executa as funções de escuta dado os disparos de outro evento"""
        for escutavel, callback in this._escutaveis:
            for disparo, objeto_do_evento in evento._disparados: 
                if escutavel == disparo:
                    callback(objeto_do_evento)
    
    def fala(this, evento):
        """Fala para outro evento o que você disparou, e se ele não souber responder,
        ele pega para ele o que você falou"""
        for disparo, objeto_do_evento in this._disparados:
            escutou = False
            for escutavel, callback in evento._escutaveis:
                if escutavel == disparo:
                    callback(objeto_do_evento)
                    escutou = True
            if not escutou:
                evento.adicionaDisparo(disparo, objeto_do_evento)
            this.removeDisparo((disparo, objeto_do_evento))



# Devaneios geométricos
class Ponto:
    """Classe que representa um ponto 2d do tipo (x, y)"""
    def __init__ (this, x, y):
        this._x = x
        this._y = y
    
    
    def setXY(this, x, y):
        this._x = x
        this._y = y
    
    
    def setX(this, x):
        this._x = x
    
    
    def setY(this, y):
        this._y = y
    
    
    def getX(this):
        return this._x
    
    
    def getY(this):
        return this._y
    
    
    def getXY(this):
        return (this._x, this._y)
    
    
    def distancia2(this, ponto):
        return (this._x-ponto._x)*(this._x-ponto._x) + (this._y-ponto._y)*(this._y-ponto._y)
    
    
    def distancia(this, ponto):
        from math import sqrt
        return sqrt(this.distancia2(ponto))
    


class Retangulo:
    def __init__(this, x, y, largura, altura):
        this._p1 = Ponto(x, y)
        this._p2 = Ponto(x + largura, y + altura)



class Angulo:
    """Classe que cuida dos ângulos, que devem estar entre pi e -pi"""
    def __init__ (this, angulo, estaEmRadianos = True):
        if estaEmRadianos:
            this._angulo =  angulo
        else: #Suponho que esteja em graus
            this._angulo = Angulo.grausParaRadianos(angulo)
        this._validaAngulo()
    
    
    @staticmethod
    def grausParaRadianos(angulo):
        from math import radians
        return radians(angulo)
    
    
    @staticmethod
    def RadianosParaGraus(angulo):
        from math import degrees
        return degrees(angulo)
    
    
    def _validaAngulo(this):
        from math import pi
        while this._angulo <= -pi:
            this._angulo += 2*pi
        while this._angulo > pi:
            this.angulo -= 2*pi
    
    
    def getAngulo(this):
        return this._angulo
    
    
    def setAngulo(this, angulo):
        this._angulo = angulo
        this._validaAngulo()




class Renderizavel:
    even = Evento()
    pos = Ponto(0, 0)
    centro = Ponto(0, 0)
    escala = Ponto(1, 1)
    retang = Retangulo(0, 0, 0, 0)
    rot = Angulo(0)
    opacidade = 1
    cor = (255, 255, 255)
    
    def atualiza(this, dt):
        pass




class Figura(Renderizavel):
    
    def __init__(this, string_imagem):
        this.string_imagem = string_imagem




class Texto(Renderizavel):
    
    def __init__(this, string_texto, tupla_fonte):
        this.string_texto = string_texto
        this.tupla_fonte = tupla_fonte




class Camada(Renderizavel):
    filhos = []
    
    
    def adicionaFilho(this, filho):
        this.filhos.append(filho)
    
    
    def removeFilho(this, filho):
        this.filhos.remove(filho)
    
    
    def atualiza(this, dt):
        for filho in this.filhos:
            filho.atualiza(dt)


    def _propagaEventoDeCimaParaBaixo(this, evento):
        this.even.escuta(evento)
        for filho in this.filhos:
            if type(filho) is Camada:
                filho._propagaEventoDeCimaParaBaixo(evento)
            else:
                filho.even.escuta(evento)
    
    
    def _propagaEventoDeBaixoParaCima(this):
        for filho in this.filhos:
            if type(filho) is Camada:
                filho._propagaEventoDeBaixoParaCima()
            filho.even.fala(this.even)
    
    
    def _observaFilhos(this, estado, callbacks):
        for filho in this.filhos:
            if type(filho) is Camada:
                filho._observaFilhos(filho._transforma(estado), callbacks)
            elif type(filho) is Figura:
                pass
            elif type(filho) is Texto:
                pass
    
    
    def _transforma(this, estado):
        """Converte as coordenadas e transformações de um Renderizável para o seu"""
        pass




class Cena(Camada):
    """Classe que representa a cena do jogo, no qual existem as camadas e objetos
    renderizáveis. Ela é responsável pela propagação de eventos. Se comunica com
    a Entrada, com o Audio e com o Renderizador. """
    
    def __init__ (this, audio, entrada, renderizador):
        """Precisa-se da referência aos objetos de Audio, Entrada e Renderizador"""
        this.audio = audio
        this.entrada = entrada
        this.renderizador = renderizador
    
    
    def atualiza(this, dt):
        """Propaga o loop do jogo, sabendo o intervalo de tempo dt transcorrido"""
        this.entrada.atualiza()
        this.even.removeTodosDisparos()
        this.entrada.even.fala(this.even)
        this._propagaEventoDeCimaParaBaixo(this.even)
        this.even.removeTodosDisparos()
        this._propagaEventoDeBaixoParaCima()
        this._propagaEventoDeCimaParaBaixo(this.even)

        this.renderizador.iniciaQuadro()
        
        this.renderizador.finalizaQuadro()




class Entrada:
    """Classe que faz interface com o pygames e registra todos os eventos de entrada"""
    even = Evento()
    
    def __init__(this):
        pass
    
    
    def atualiza(this):
        """Atualiza os seus eventos"""
        this.verTeclado()
        this.verMouse()
    
    
    def verTeclado(this):
        """Observa quais teclas estão pressionadas e se está focado"""
        vazio = True
        for ide, val in enumerate(pygame.key.get_pressed()):
            if val == True:
                vazio = False
                this.even.adicionaRegistro("K_"+pygame.key.name(ide), None)
        if vazio:
            this.even.adicionaRegistro("K_vazio", None)
        if not pygame.key.get_focused():
            this.even.adicionaRegistro("K_desfocado", None)
    
    
    def verMouse(this):
        """Observa a posição do ponteiro e se clica"""
        pass



class Renderizador:
    _listaImagens = []
    
    def __init__(this, largura, altura, corFundo = (0, 0, 0)):
        this.tela = pygame.display.set_mode((largura, altura))
        this.corFundo = corFundo
    
    
    def iniciaQuadro(this):
        this.tela.fill(this.corFundo)
    
    
    def finalizaQuadro(this):
        pygame.display.flip()
    
    
    def desenhaImagem(this, string_imagem, posXY):
        this.tela.blit(this._bancoImagens(string_imagem), posXY)
        
    
    def desenhaTexto(this, string_texto, posXY, tuplaFonte = (None, 12)):
        texto = pygame.font.Font(tuplaFonte[0], tuplaFonte[12])
        this.tela.blit(texto, posXY)
    
    
    def _bancoImagens(this, string_imagem):
        imagem = this._listaImagens.get(string_imagem)
        if imagem == None:
            import os
            caminho = string_imagem.replace('/', os.sep).replace('\\', os.sep)
            imagem = pygame.image.load(caminho)
            this._listaImagens[string_imagem] = imagem
        return imagem
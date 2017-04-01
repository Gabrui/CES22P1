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
    
    
    @staticmethod
    def coordsInscrito(angulo, Cx, Cy, largura, altura):
        """Retorna as coordenadas de um ponto (Cx, Cy) dentro de um retângulo 
        rotacionado em relação a um retangulo horizontal que o circunscreve"""
        return (0, 0)




class Evento:
    """É uma classe que todo objeto que registra eventos deve ter uma instância"""
    _escutaveis = [] #É uma lista de tuplas (stringEvento, funcao_de_chamada) APARADOS
    _disparados = []  #É uma lista de tuplas (stringsEventos, objeto_do_evento) LANÇADOS
    
    #__init__
    
    
    def adicionaEscutavel(self, string_evento, callback):
        self._escutaveis.append((string_evento, callback))
    
    
    def removeEscutavel(self, string_evento, callback = None):
        if callback is None:
            Aux.removeTuplas1Elem(self._escutaveis, string_evento)
        else:
            self._escutaveis.remove((string_evento, callback))
    
    
    def adicionaDisparo(self, string_evento, objeto_do_evento):
        if Aux.existeTupla1Elem(self._escutaveis, string_evento):
            self._disparados.append((string_evento, objeto_do_evento))
    
    
    def removeDisparo(self, string_evento, objeto_do_evento = None):
        if objeto_do_evento is None:
            Aux.removeTuplas1Elem(self._disparados, string_evento)
        else:
            self._disparados.remove((string_evento, objeto_do_evento))
    
    
    def removeTodosDisparos(self):
        del self._disparados[:]
    
    
    def escuta(self, evento):
        """Executa as funções de escuta dado os disparos de outro evento"""
        for escutavel, callback in self._escutaveis:
            for disparo, objeto_do_evento in evento._disparados: 
                if escutavel == disparo:
                    callback(objeto_do_evento)
    
    def fala(self, evento):
        """Fala para outro evento o que você disparou, e se ele não souber responder,
        ele pega para ele o que você falou"""
        for disparo, objeto_do_evento in self._disparados:
            escutou = False
            for escutavel, callback in evento._escutaveis:
                if escutavel == disparo:
                    callback(objeto_do_evento)
                    escutou = True
            if not escutou:
                evento.adicionaDisparo(disparo, objeto_do_evento)
            self.removeDisparo((disparo, objeto_do_evento))




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
        return (self._x-ponto._x)*(self._x-ponto._x) + (self._y-ponto._y)*(self._y-ponto._y)
    
    
    def distancia(self, ponto):
        from math import sqrt
        return sqrt(self.distancia2(ponto))




class Retangulo:
    """Classe que representa um retângulo horizontal"""
    def __init__(self, x, y, largura, altura):
        self._p1 = Ponto(x, y)
        self._p2 = Ponto(x + largura, y + altura)
    """"Precisa implementar mais métodos"""




class Angulo:
    """Classe que cuida dos ângulos, que devem estar entre 180 (inclusive) e -180"""
    
    @staticmethod
    def grausParaRadianos(angulo):
        from math import radians
        return radians(angulo)
    
    
    @staticmethod
    def RadianosParaGraus(angulo):
        from math import degrees
        return degrees(angulo)
    
    
    def _validaAngulo(self):
        while self._angulo <= -180:
            self._angulo += 360
        while self._angulo > 180:
            self.angulo -= 360
    
    
    def __init__ (self, angulo, estaEmGraus = True):
        if estaEmGraus:
            self._angulo =  angulo
        else: #Suponho que esteja em radianos
            self._angulo = Angulo.RadianosParaGraus
        self._validaAngulo()
    
    
    def getAngulo(self):
        return self._angulo
    
    
    def setAngulo(self, angulo):
        self._angulo = angulo
        self._validaAngulo()
    
    
    def getQuadrante(self):
        return 1




class Cor:
    """Classe que representa a opacidade e a tintura aplicada a um renderizável"""
    
    def _validaAlpha(self, alpha):
        if alpha > 1:
            alpha = 1
        elif alpha < 0:
            alpha = 0
        return alpha
    
            
    def _validaRGB(self, RGB):
        RGB = int(RGB)
        if RGB > 255:
            RGB = 255
        elif RGB < 0:
            RGB = 0
        return RGB
    
    
    def __init__(self, opacidade, R, G, B, A):
        self.opacidade = self._validaAlpha(opacidade)
        self.R = self._validaRGB(R)
        self.G = self._validaRGB(G)
        self.B = self._validaRGB(B)
        self.A = self._validaAlpha(A)
    
    
    def setRGBA(self, R, G, B, A):
        self.R = self._validaRGB(R)
        self.G = self._validaRGB(G)
        self.B = self._validaRGB(B)
        self.A = self._validaAlpha(A)
    
    
    def setOpacidade(self, opacidade):
        self.opacidade = self._validaAlpha(opacidade)




class Renderizador:
    _listaImagens = []
    
    def __init__(self, largura, altura, corFundo = (0, 0, 0)):
        self.tela = pygame.display.set_mode((largura, altura))
        self.corFundo = corFundo
    
    
    def iniciaQuadro(self):
        self.tela.fill(self.corFundo)
    
    
    def finalizaQuadro(self):
        pygame.display.flip() #atualiza a tela toda. Talvez seja bom usar .update() para atualizar apenas uma parte da tela
    
    
    def desenhaImagem(self, string_imagem, posXY):
        self.tela.blit(self._bancoImagens(string_imagem), posXY)
        
    
    def desenhaTexto(self, string_texto, posXY, tuplaFonte = (None, 12)):
        texto = pygame.font.Font(tuplaFonte[0], tuplaFonte[12])
        self.tela.blit(texto, posXY)
    
    
    def _bancoImagens(self, string_imagem):
        imagem = self._listaImagens.get(string_imagem)
        if imagem == None:
            import os
            caminho = string_imagem.replace('/', os.sep).replace('\\', os.sep)
            imagem = pygame.image.load(caminho)
            self._listaImagens[string_imagem] = imagem
        return imagem





class Entrada:
    """Classe que faz interface com o pygames e registra todos os eventos de entrada"""
    even = Evento()
    
    def __init__(self):
        pass
    
    
    def atualiza(self):
        """Atualiza os seus eventos"""
        self.verTeclado()
        self.verMouse()
    
    
    def verTeclado(self):
        """Observa quais teclas estão pressionadas e se está focado"""
        vazio = True
        for ide, val in enumerate(pygame.key.get_pressed()):
            if val == True:
                vazio = False
                self.even.adicionaRegistro("K_"+pygame.key.name(ide), None)
        if vazio:
            self.even.adicionaRegistro("K_vazio", None)
        if not pygame.key.get_focused():
            self.even.adicionaRegistro("K_desfocado", None)
    
    
    def verMouse(self):
        """Observa a posição do ponteiro e se clica:
            pygame module to work with the mouse
            
            pygame.mouse.get_pressed	—	get the state of the mouse buttons
                                            return (statebutton1,statebutton2,statebutton3)
            pygame.mouse.get_pos	—	get the mouse cursor position
                                        return (MousePosX,MousePosY) relative to screen top-left corner 
        """
      # apertado = False
      #while not apertado:
          
      #   for event in pygame.event.get():
      #     (button1,button2,button3) = pygame.mouse.get_pressed()
      #     apertado = button1 or button3
      #     
      #     if apertado:
      #        MousePos = pygame.mouse.get_pos
      #        return MousePos MousePos is a tuple
        
        pass




class Audio:
    """Faz a interface com o audio do pygames
    pygame module for controlling streamed audio:
        
    pygame.mixer.music.load	—	Load a music file for playback
    pygame.mixer.music.play	—	Start the playback of the music stream
    pygame.mixer.music.rewind	—	restart music
    pygame.mixer.music.stop	—	stop the music playback
    pygame.mixer.music.pause	—	temporarily stop music playback
    pygame.mixer.music.unpause	—	resume paused music
    pygame.mixer.music.fadeout	—	stop music playback after fading out
    pygame.mixer.music.set_volume	—	set the music volume
    pygame.mixer.music.get_volume	—	get the music volume
    pygame.mixer.music.get_busy	—	check if the music stream is playing
    pygame.mixer.music.set_pos	—	set position to play from
    pygame.mixer.music.get_pos	—	get the music play time
    pygame.mixer.music.queue	—	queue a music file to follow the current
    pygame.mixer.music.set_endevent	—	have the music send an event when playback stops
    pygame.mixer.music.get_endevent	—	get the event a channel sends when playback stops
    """
    
    pass




class Renderizavel:
    """Classe abstrata que contém os atributos básicos de um objeto renderizável"""
    
    def __init__(self, pos = Ponto(), centro = Ponto(), escala = Ponto(1, 1),
                 retang = Retangulo(0, 0, 0, 0), rot = Angulo(0), cor = (1, 0, 0, 0, 0)):
        self.even = Evento()
        self.pos = pos
        self.centro = centro
        self.escala = escala
        self.retang = retang
        self.rot = rot
        self.cor = cor
    
    
    def atualiza(self, dt):
        pass




class Figura(Renderizavel):
    """Representa uma imagem na árvore de renderização"""
    
    def __init__(self, string_imagem, pos = Ponto(0, 0), centro = Ponto(0, 0), escala = Ponto(1, 1),
                 retang = Retangulo(0, 0, 0, 0), rot = Angulo(0), cor = (1, 0, 0, 0, 0)):
        super().__init__(pos, centro, escala, retang, rot, cor)
        self.string_imagem = string_imagem




class Texto(Renderizavel):
    
    """Representa um texto na aŕvore de renderização"""
    
    def __init__(self, string_texto, tupla_fonte, pos = Ponto(0, 0), centro = Ponto(0, 0), escala = Ponto(1, 1),
                 retang = Retangulo(0, 0, 0, 0), rot = Angulo(0), cor = (1, 0, 0, 0, 0)):
        super().__init__(pos, centro, escala, retang, rot, cor)
        self.string_texto = string_texto
        self.tupla_fonte = tupla_fonte
        
        
    """ 
    smallfont = 30
    mediumfont = 50
    largefont = 120
    def text_objects(text,color,size):
       
        if size == "small":
            textSurface = smallfont.render(text, True, color)
        elif size == "medium":
            textSurface = mediumfont.render(text, True, color)
        elif size == "large":
            textSurface = largefont.render(text, True, color)
        return textSurface, textSurface.get_rect()

       def message_to_screen(msg,color, y_displace = 0, size = "small"): funcao para ficar mais facil colocar texto na tela
         textSurf , textRect = text_objects(msg,color,size)
         #gameDisplay.blit(screen_text, [display_width/2, display_height/3]) #colocando msg na tela, (mensagem,posicao)
         textRect.center = (display_width / 2), (display_height/2) + y_displace
         gameDisplay.blit(textSurf,textRect)
    """



class Camada(Renderizavel):
    """Representa uma camada na árvore renderização"""
    
    def __init__(self, pos = Ponto(0, 0), centro = Ponto(0, 0), escala = Ponto(1, 1),
                 retang = Retangulo(0, 0, 0, 0), rot = Angulo(0), cor = (1, 0, 0, 0, 0)):
        super().__init__(pos, centro, escala, retang, rot, cor)
        self.filhos = []
    
    
    def adicionaFilho(self, filho):
        self.filhos.append(filho)
    
    
    def removeFilho(self, filho):
        self.filhos.remove(filho)
    
    
    def atualiza(self, dt):
        for filho in self.filhos:
            filho.atualiza(dt)


    def _propagaEventoDeCimaParaBaixo(self, evento):
        self.even.escuta(evento)
        for filho in self.filhos:
            if type(filho) is Camada:
                filho._propagaEventoDeCimaParaBaixo(evento)
            else:
                filho.even.escuta(evento)
    
    
    def _propagaEventoDeBaixoParaCima(self):
        for filho in self.filhos:
            if type(filho) is Camada:
                filho._propagaEventoDeBaixoParaCima()
            filho.even.fala(self.even)
    
    
    def _observaFilhos(self, estado, callbacks):
        """Retorna os filhos ordenados que tem, separando imagem de texto.
        É uma tupla com uma lista de imagem e uma lista de texto, essas listas
        contém tuplas que definem o estado da figura e texto:
            (string, posX, posY, rotação, opacidade, R, G, B, A"""
        figuras = []
        textos = []
        for filho in self.filhos:
            if type(filho) is Camada:
                filho._observaFilhos(filho._transforma(estado), callbacks)
            elif type(filho) is Figura:
                figuras.append((filho.string_imagem, filho.pos.getX()-7, filho.pos.getY()))
            elif type(filho) is Texto:
                pass
        return (figuras, textos)
    
    
    def _transforma(self, estado):
        """Converte as coordenadas e transformações de um Renderizável para o seu"""
        pass




class Cena(Camada):
    """Classe que representa a cena do jogo, no qual existem as camadas e objetos
    renderizáveis. Ela é responsável pela propagação de eventos. Se comunica com
    a Entrada, com o Audio e com o Renderizador. """
    
    def __init__ (self, audio, entrada, renderizador):
        """Precisa-se da referência aos objetos de Audio, Entrada e Renderizador"""
        self.audio = audio
        self.entrada = entrada
        self.renderizador = renderizador
    
    
    def atualiza(self, dt):
        """Propaga o loop do jogo, sabendo o intervalo de tempo dt transcorrido"""
        self.entrada.atualiza()
        self.even.removeTodosDisparos()
        self.entrada.even.fala(self.even)
        self._propagaEventoDeCimaParaBaixo(self.even)
        self.even.removeTodosDisparos()
        self._propagaEventoDeBaixoParaCima()
        self._propagaEventoDeCimaParaBaixo(self.even)

        self.renderizador.iniciaQuadro()
        
        self.renderizador.finalizaQuadro()


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 08:25:06 2017

@author: gabrui
"""

import pygame
import math

pygame.init()

""" Gabriel:
#OBS: NÃO EXEDER O TAMANHO DA LINHA DE 80 CARACTERES, BEM AQUI --------------->
#OBS: NÃO EXEDER O TAMANHO DA LINHA DE 80 CARACTERES, BEM AQUI --------------->
#POIS EU ESTOU USANDO VÁRIAS JANELAS ABERTAS COM ESSE TAMANHO BEM AQUI ------->
"""


class Aux:
    """Classes com funções auxiliares para mexer com listas etc..."""
    @staticmethod
    def removeTuplas1Elem(lista, elem):
        """Remove as tuplas de uma lista cujo primeiro elemento é o 'elem'"""
        i = 0
        while i < len(lista):
            if lista[i][0] == elem:
                del lista[i]
            i += 1
    
    @staticmethod
    def existeTupla1Elem(lista, elem):
        """Verifica se existe uma tupla em uma lista cujo primeiro elemento é o
        'elem' """
        for tupla in lista:
            if tupla[0] == elem:
                return True
        return False
    
    @staticmethod
    def coordsInscrito(angulo, Cx, Cy, largura, altura):
        """Retorna as coordenadas de um ponto (Cx, Cy) dentro de um retângulo 
        rotacionado em relação a um retangulo horizontal que o circunscreve
        OBS: ver a fórmula que eu já deduzi, conforme a imagem rotacoes.svg"""
        #raise NotImplementedError("Você deveria ter programado aqui!")
        if angulo.getQuadrante() == 1:
            return (Cx*math.cos(angulo.getAngulo(False))
                    + Cy*math.sin(angulo.getAngulo(False)),
                    Cy*math.cos(angulo.getAngulo(False)) 
                    + (largura - Cx)*math.sin(angulo.getAngulo(False)))
        elif angulo.getQuadrante() == 2:
            return (-(largura - Cx)*math.cos(angulo.getAngulo(False))
                    + Cy*math.sin(angulo.getAngulo(False)),
                    -(altura - Cy)*math.cos(angulo.getAngulo(False))
                    + (largura - Cx)*math.sin(angulo.getAngulo(False)))
        elif angulo.getQuadrante() == 3:
            return(-Cx*math.cos(angulo.getAngulo(False))
                   - (altura - Cy)*math.sin(angulo.getAngulo(False)),
                   -Cy*math.cos(angulo.getAngulo(False)) 
                   - Cx*math.sin(angulo.getAngulo(False)))
        elif angulo.getQuadrante() == 4:
            return (Cx*math.cos(angulo.getAngulo(False)) 
                    - (altura - Cy)*math.sin(angulo.getAngulo(False)),
                      Cy*math.cos(angulo.getAngulo(False)) 
                      - Cx*math.sin(angulo.getAngulo(False)))
        

class Singleton:
    """
    Decorador para criação de Slingletons
    """
    def __init__(self, classe):
        self.classe = classe
        self.objeto = None
    
    
    def __call__(self,*args, **kwargs):
        if self.objeto == None:
            self.objeto = self.classe(*args,**kwargs)
        return self.objeto




@Singleton
class Evento:
    """
    É uma classe Singleton como de costume. 
    A performance foi muito prejudicada por várias instâncias de evento e o
    modelo de propagação arquitetado anteriormente
    """
    
    
    def __init__(self):
        """Variáveis de instância _escutaveis"""
        self._escutaveis = {} # Podem ser vistos como aparáveis
    
    
    def escutar(self, string_evento, callback):
        """Começar a escutar determinado evento, isto é, a função de callback
        será executada quando acontecer o evento em questão. 
        Será passado um objeto para a função de callback como parâmetro, 
        contendo informações sobre esse evento."""
        if self._escutaveis.get(string_evento) is None:
            self._escutaveis[string_evento] = [callback]
        else:
            self._escutaveis[string_evento].append(callback)
    
    
    def pararDeEscutar(self, string_evento, callback = None):
        """Para de escutar determinado evento"""
        if callback is None or len(self._escutaveis[string_evento]) == 1:
            del self._escutaveis[string_evento]
        else:
            self._escutaveis[string_evento].remove(callback)
    
    
    def lancar(self, string_evento, objeto_do_evento):
        """Lançar um determinado evento, isto é, gera um evento no qual outros
        objetos podem escutar.
        Para tal, é necessário o indentificador do evento e o objeto
        relacionado ao evento, que será passado como parâmetro para a função de
        callback"""
        if self._escutaveis.get(string_evento) is not None:
            for callback in self._escutaveis[string_evento]:
                callback(objeto_do_evento)




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
        self._y = self._y + ponto._y
    
    
    def retornaSoma(self, ponto):
        """Retorna um novo ponto resultado da soma de si por outro, sem alterar
        o seu próprio valor"""
        return Ponto(self._x + ponto._x, self._y + ponto._y)     
    
    
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
    
    
    def getTopo(self):
        """Retorna o valor de y do ponto no topo do retângulo (menor y)"""
        if self._p1.getY() < self._p2.getY():
            return self._p1.getY()
        return self._p2.getY()
    
    
    def getFundo(self):
        """Retorna o valor de y do ponto no fundo do retângulo (maior y)"""
        if self._p1.getY() > self._p2.getY():
            return self._p1.getY()
        return self._p2.getY()
    
    
    def getEsquerda(self):
        """Retorna o valor de x do ponto na esquerda do retângulo (menor x)"""
        if self._p1.getX() < self._p2.getX():
            return self._p1.getX()
        return self._p2.getX()
    
    
    def getDireita(self):
        """Retorna o valor de x do ponto na direita do retângulo (maior x)"""
        if self._p1.getX() > self._p2.getX():
            return self._p1.getX()
        return self._p2.getX()

    
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
    
    
    def setDimensoes(self, posX, posY, largura, altura):
        """Parecido com o setRetangulo, mas utiliza largura e altura"""
        self._p1.setXY(posX, posY)
        self._p2 = self._p1.retornaSoma(Ponto(largura, altura))




class Angulo:
    """Classe que cuida dos ângulos, armazenados em graus, que devem estar 
    entre 180 (inclusive) e -180"""
    
    @staticmethod
    def grausParaRadianos(angulo):
        from math import radians
        return radians(angulo)
    
    
    @staticmethod
    def radianosParaGraus(angulo):
        from math import degrees
        return degrees(angulo)
    
    
    def _validaAngulo(self):
        """Faz com que o ângulo fique entre 180 (inclusive) e -180 graus"""
        while self._angulo <= -180:
            self._angulo += 360
        while self._angulo > 180:
            self._angulo -= 360
    
    
    def __init__ (self, angulo, emGraus = True):
        """Se não estiver em graus suponho radianos"""
        if emGraus:
            self._angulo =  angulo
        else: #Suponho que esteja em radianos
            self._angulo = Angulo.RadianosParaGraus
        self._validaAngulo()
    
    
    def getAngulo(self, emGraus = True):
        """Retorna o ângulo em graus"""
        if emGraus:
            return self._angulo
        return Angulo.grausParaRadianos(self._angulo)
    
    
    def setAngulo(self, angulo, emGraus = True):
        """Modifica o valor do angulo, mantendo a sua consistência"""
        if emGraus:
            self._angulo =  angulo
        else: #Suponho que caso contrário esteja em radianos
            self._angulo = Angulo.RadianosParaGraus
        self._validaAngulo()
        
    
    def incrementa(self, angulo, emGraus = True):
        """Incrementa um valor de angulo ao atual"""
        if emGraus:
            self.setAngulo(self._angulo + angulo)
        else:
            self.setAngulo(self._angulo + Angulo.radianosParaGraus(angulo))
    
    
    def getQuadrante(self):
        """Retorna o quadrante do ângulo"""
        #raise NotImplementedError("Você deveria ter programado aqui!")
        if 0 <= self._angulo < 90:
            return 1
        elif 90 <= self._angulo< 180:
            return 2
        elif -180 <= self._angulo < -90:
            return 3
        elif -90 <= self._angulo < 0:
            return 4




class Cor:
    """Classe que representa a opacidade e a tintura aplicada a um 
    renderizável"""
    
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
    #Variável de Classe que contém todas as imagem já carregadas pelo pygames
    _listaImagens = {}
    _listaFontes = {}
    
    def __init__(self, largura, altura, corFundo = (0, 0, 0)):
        self.tela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption('As da Aviacao')
        self.corFundo = corFundo
    
    
    def _bancoImagens(self, string_imagem):
        """Retorna um objeto imagem do pygame dado a string"""
        return self._listaImagens.get(string_imagem)
    
    
    def carregaImagem(self, string_imagem):
        """Carrega a imagem na memória e retorna o tamanho dela"""
        import os
        # Dependendo do sistema operacional o separador pode ser / ou \\
        caminho = string_imagem.replace('/', os.sep)
        imagem = pygame.image.load(caminho)
        self._listaImagens[string_imagem] = imagem
        return imagem.get_size()
    
    
    def _carregaFonte(self, tupla_fonte):
        """Carrega a fonte na memória
            tupla_fonte = (string_fonte,int tamanho
                           ,bold = True or False,italic = True or False)
            return int tamanho
        """
        
        # Dependendo do sistema operacional o separador pode ser / ou \\
        name = tupla_fonte[0]
        size = tupla_fonte[1]
        bold = tupla_fonte[2]
        italic = tupla_fonte[3]
        fonte = pygame.font.SysFont(name,size,bold,italic)
        self._listaFontes[tupla_fonte] = fonte
        
    def getSizeText(self,string_texto,tupla_fonte):
        fonte = self._bancoFontes(tupla_fonte)
        return fonte.size(string_texto)
    
    def _bancoFontes(self, tupla_fonte):
        fonte = self._listaFontes.get(tupla_fonte)
        if fonte is None:
            self._carregaFonte(tupla_fonte)
            fonte = self._listaFontes.get(tupla_fonte)
        return fonte
    
    
    def renderiza(self, imagens, textos):
        """Renderiza tudo, a partir da lista de imagens e de texto: 
            (string_imagem, tupla_corte, posX, posY, rotação, opacidade, 
             R, G, B, A, self)
            (string_texto, tupla_fonte, posX, posY, rotação, opacidade, 
             R, G, B, A, self)
            tupla_corte = (posX, posY, largura, altura) referentes ao retangulo
                                                          de corte
        Nessa renderização ele desenha todo o quadro de uma só vez, com base na
        lista de imagens e textos recebidos
        Gabriel: Essas tuplas podem ser melhoradas de acordo com o que vocês 
        acharem conveniente
        Ele retorna uma lista de retangulos com as dimensões reais
        """
        self.tela.fill(self.corFundo)
        retangs = []
        for i in imagens:
            imagem = self._bancoImagens(i[0])
            # nao foi implementado o corte
            recorte = imagem.subsurface(i[1])
            imagemRotate = pygame.transform.rotate(recorte,i[4])
            imagemRotate.set_alpha(i[5])
            self.tela.blit(imagemRotate,(i[2], i[3]))
            larg, alt = imagemRotate.get_size()
            retangs.append((i[10], i[2], i[3], larg, alt))
            
        for i in textos:
            font = self._bancoFontes(i[1])
            textSurface = font.render(i[0], True, (i[6],i[7],i[8]))
            textSurface.set_alpha(i[5])
            textSurfaceRotate = pygame.transform.rotate(textSurface,i[4])
            self.tela.blit(textSurfaceRotate, ([i[2],i[3]]))
            larg, alt = textSurfaceRotate.get_size()
            retangs.append((i[10], i[2], i[3], larg, alt))
            
        pygame.display.flip()
        return retangs



class Entrada:
    """Classe que faz interface com o pygames e registra todos os eventos de 
    entrada, seja de mouse ou teclado"""
    
    def __init__(self):
        self.even = Evento()
    
    
    def _verTeclado(self):
        """Observa quais teclas estão pressionadas e se está focado"""
        vazio = True
        for ide, val in enumerate(pygame.key.get_pressed()):
            if val == True:
                vazio = False
                self.even.lancar("K_"+pygame.key.name(ide), 
                                 "K_"+pygame.key.name(ide))
        if vazio:
            self.even.lancar("K_vazio", "K_vazio")
        if not pygame.key.get_focused():
            self.even.lancar("K_desfocado", "K_desfocado")
    
    
    def _verMouse(self):
        """Observa a posição do ponteiro e se clica, lancando os eventos"""
        
        click = pygame.mouse.get_pressed() 
        mouse = pygame.mouse.get_pos()
        if click[0]:
            self.even.lancar("M_click", Ponto(mouse[0],mouse[1]))
        if click[2]:
            self.even.lancar("M_clickD", Ponto(mouse[0],mouse[1]))
        self.even.lancar("M_pos", Ponto(mouse[0],mouse[1]))
            
    
    def atualiza(self):
        """Atualiza os seus eventos"""
        self._verTeclado()
        self._verMouse()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                quit()



class Audio:
    """Faz a interface com o audio do pygames"""
    
    #Variável de classe dos arquivos carregados pelo pygames
    _arquivos = {}
    
    def __init__ (self):
        self.musicaFundo = None
        
    
    def _carregarAudio(self, string_musica):
        import os
        # Dependendo do sistema operacional o separador pode ser / ou \\
        caminho = string_musica.replace('/', os.sep)
        musica = pygame.mixer.Sound(caminho)
        self._arquivos[string_musica] = musica
        return musica
    
    
    def _bancoAudio(self, string_musica):
        """Retorna o objeto de música a partir da string, e se não tiver
        carregado a música, carrega"""
        musica = self._arquivos[string_musica]
        if musica is None:
            musica = self._carregarAudio(string_musica)
        return musica
    
    
    def setMusicaFundo(self, string_musica, volume = 0.5):
        """A música de fundo a ser tocada"""
        
        self.musicaFundo = self._bancoAudio(string_musica)
        self.musicaFundo.set_volume(volume)
        self.musicaFundo.play(-1)
    
    def setVolumeMusicaFundo(self, volume):
        """Modifica apenas o volume da música de fundo, sem interferir nela"""
       
        self.musicaFundo.set_volume(volume)
    
    def tocarEfeito(self, string_efeito):
        """Toca um efeito sonoro apenas uma vez"""
     
        self.efeito = self._bancoAudio(string_efeito)
        self.efeito.play()
    
    def pararMusicaFundo(self):  
        self.musicaFundo.stop()
        
    def verificarMusicaFundo(self):
        """Retorna verdadeiro se esta tocando."""
        return self.musicaFundo.get_busy()


class Renderizavel:
    """Classe abstrata que contém os atributos básicos de um objeto 
    renderizável"""
    
    def __init__(self, pos = Ponto(), centro = Ponto(), escala = Ponto(1, 1),
                 rot = Angulo(0), cor = Cor(1, 0, 0, 0, 0)):
        """Possui a posição 'pos' que é uma coordenada relativa ao seu pai, o 
        seu centro de rotação 'centro', relativo a si próprio, sua escala de 
        tamanho, seu ângulo de rotação e sua coloração"""
        self.even = Evento()
        self.pos = pos
        self.centro = centro
        self.escala = escala
        self.retang = Retangulo(Ponto(0, 0), Ponto(0, 0))
        self.rot = rot
        self.cor = cor
    
    
    def atualiza(self, dt):
        """Método a ser sobreposto pelos herdeiros, dt representa o tempo 
        não precisa escrever nada aqui"""
        pass




class Figura(Renderizavel):
    """Representa uma imagem na árvore de renderização"""
    
    def setString(self, string_imagem, corte = None):
        """Redefine a string imagem dessa figura"""
        self._string_imagem = string_imagem
        self.corte = corte
        self.even.lancar("imagem_nova", self)
    
    
    def __init__(self, string_imagem, corte = None, pos = Ponto(0, 0), 
                 centro = Ponto(0, 0), escala = Ponto(1, 1), rot = Angulo(0), 
                 cor = Cor(1, 0, 0, 0, 0)):
        """A string_imagem representa o caminho da imagem e é seu 
        indentificador único. O corte representa um retângulo que corta a
        imagem original, no caso dela ser um conjunto de imagens."""
        super().__init__(pos, centro, escala, rot, cor)
        self.setString(string_imagem, corte)
    
    
    def getString(self):
        """Retorna a string_imagem dessa figura"""
        return self._string_imagem
    




class Texto(Renderizavel):
    
    """Representa um texto na aŕvore de renderização"""
    
    def __init__(self, string_texto, tupla_fonte, pos = Ponto(0, 0), 
                 centro = Ponto(0, 0), escala = Ponto(1, 1), rot = Angulo(0), 
                 cor = Cor(1, 0, 0, 0, 0)):
        super().__init__(pos, centro, escala, rot, cor)
        self.tupla_fonte = tupla_fonte
        self.setString(string_texto)
        self.size = 0
    def setString(self, string_texto):
        """Redefine a string do texto dessa texto"""
        self._string_texto = string_texto
        self.even.lancar("texto_novo", self) 
    def getString(self):
        """Retorna a string_texto dessa texto"""
        return self._string_texto



class Camada(Renderizavel):
    """Representa uma camada na árvore renderização"""
    
    def __init__(self, pos = Ponto(), centro = Ponto(), escala = Ponto(1, 1),
                 rot = Angulo(0), cor = Cor(1, 0, 0, 0, 0)):
        super().__init__(pos, centro, escala, rot, cor)
        self.filhos = []
    
    
    def adicionaFilho(self, filho):
        self.filhos.append(filho)
    
    
    def removeFilho(self, filho):
        self.filhos.remove(filho)
    
    
    def atualiza(self, dt):
        for filho in self.filhos:
            filho.atualiza(dt)
    
    
    def _transformaFigura(self, camadaFilha, estado):
        """Converte as coordenadas e transformações de uma figura representada
        pela sua tupla (string_imagem, posX ....) que está no referencial da
        camadaFilha para o seu próprio referencial, retornando a nova tupla"""
        #raise NotImplementedError("Você deveria ter programado aqui!")
        Cx = camadaFilha.centro.getX()
        Cy = camadaFilha.centro.getY()
        alfa = math.atan2(Cy - estado[3],Cx - estado[2])
        hipo = math.sqrt((Cy - estado[3])*(Cy - estado[3]) + 
                         (Cx - estado[2])*(Cx - estado[2]) )
        teta = Angulo.grausParaRadianos(estado[4])
        posX = camadaFilha.pos.getX() + hipo*math.cos(alfa + teta)
        posY = camadaFilha.pos.getY() - hipo*math.sin(alfa + teta)
        return (estado[0],estado[1], posX, posY, estado[4], estado[5],
                estado[6], estado[7],estado[8],estado[9],estado[10])
        
    
    
    def _transformaTexto(self, camadaFilha, estado):
        """Converte as coordenadas e transformações de um texti representado
        pela sua tupla (string_texto, posX ....) que está no referencial da
        camadaFilha para o seu próprio referencial, retornando a nova tupla"""
        #raise NotImplementedError("Você deveria ter programado aqui!")
        Cx = camadaFilha.centro.getX()
        Cy = camadaFilha.centro.getY()
        alfa = math.atan2(Cy - estado[3],Cx - estado[2])
        hipo = math.sqrt((Cy - estado[3])^2 + (Cx - estado[2])^2 )
        teta = Angulo.GrausParaRadianos(estado[4])
        posX = camadaFilha.pos.getX() + hipo*math.cos(alfa + teta)
        posY = camadaFilha.pos.getY() - hipo*math.sin(alfa + teta)
        return (estado[0],estado[1], posX, posY, estado[4], estado[5],
                estado[6], estado[7],estado[8],estado[9],estado[10])
        
    
    
    def _observaFilhos(self):
        """Retorna os filhos que tem, na ordem, separando imagem de texto.
        É uma tupla com uma lista de imagem e uma lista de texto, essas listas
        contém tuplas que definem o estado da figura e texto, no estado mais
        reduzido: atentar que a posX e posY se refere ao ponto superior
        esquerdo do retângulo exterior.
            (string_imagem, tupla_corte, posX, posY, rotação, opacidade, 
             R, G, B, A, self)
            (string_texto, tupla_fonte, posX, posY, rotação, opacidade, 
             R, G, B, A, self)
        Gabriel: Essas tuplas podem ser melhoradas de acordo com o que vocês 
        acharem conveniente"""
        figuras = []
        textos = []
        for filho in self.filhos:
            if isinstance(filho, Camada):
                imgs, txts = filho._observaFilhos()
                for figura in imgs:
                    figuras.append(self._transformaFigura(filho, figura))
                for texto in txts:
                    textos.append(self._transformaTexto(filho, texto))
            elif isinstance(filho, Figura):
                """(string_imagem, tupla_corte, posX, posY, rotação, opacidade, 
                   R, G, B, A, self)
                o self é a referência à própria imagem que gerou a tupla"""
                x, y = Aux.coordsInscrito(filho.rot, filho.centro.getX(), 
                        filho.centro.getY(), filho.corte.getLargura(), 
                                         filho.corte.getAltura())
                x = filho.pos.getX() - x
                y = filho.pos.getY() - y
                figuras.append((filho.getString(), 
                 (filho.corte.getTopoEsquerdo().getX(), filho.corte.getTopoEsquerdo().getY(),
                  filho.corte.getFundoDireito().getX(), filho.corte.getFundoDireito().getY()),
                  x, y, filho.rot.getAngulo(), filho.cor.opacidade, 
                  filho.cor.R, filho.cor.G, filho.cor.B, filho.cor.A, filho))
            elif isinstance(filho, Texto):
                """tupla do texto: 
                (string_texto, tupla_fonte, posX, posY, rotação, opacidade, 
                 R, G, B, A, self)
                o self é a referência à própria imagem que gerou a tupla"""
                x, y = Aux.coordsInscrito(filho.rot, filho.centro.getX(),
                                                     filho.centro.getY(),
                                          filho.size[0], filho.size[1])
                x = filho.pos.getX() - x
                y = filho.pos.getY() - y
                
                textos.append((filho.getString(), filho.tupla_fonte,
                              x, y, filho.rot.getAngulo(), filho.cor.opacidade, 
                              filho.cor.R, filho.cor.G, 
                              filho.cor.B, filho.cor.A, filho))
        #raise NotImplementedError("Você deveria ter programado aqui!")
        return (figuras, textos)
    
    
    def _atualizaRetangs(self):
        """Atualiza os retangs das camadas filhas e depois da sua"""
        for filho in self.filhos:
            if isinstance(filho, Camada):
                filho._atualizaRetangs()
                
        retangs = [filho.retang for filho in self.filhos]
        self.retang.setRetanguloQueContem(retangs)
            




class Botao(Camada):
    """Representa um botão clicável que contém uma imagem de fundo e texto"""
    
    def __init__(self,nome_evento, tupla_string_imagem, tupla_texto, pos = Ponto(), 
                 centro = Ponto(), escala = Ponto(1, 1), rot = Angulo(0), 
                 cor = Cor(1, 0, 0, 0, 0)):
        """
        Cria.
        nome_evento: é uma string com o nome do evento que o botao deve gerar
                     ao ser clicado.
        """
        super().__init__(pos, centro, escala, rot, cor)
        self.even.escutar("M_pos", self._verEmCima)
        self.even.escutar("M_click", self._verClique)
        # Implementar o esboço de imagem abaixo
        self.imagemFundo = Figura(tupla_string_imagem[0]) # Mudar, esboço
        #esboço, mudar
        self.texto = Texto(tupla_texto[0], (tupla_texto[1], tupla_texto[2]))
        self.adicionaFilho(self.imagemFundo)
        self.adicionaFilho(self.texto)
        self._nome_evento = nome_evento
        raise NotImplementedError("Você deveria ter programado aqui!")
    
    
    def _verEmCima(self, mousePos):
        """Recebe um objeto mousePos do tipo ponto e verifica se o mousePos 
        está dentro do seu retângulo de renderização, tomando as ações
        necessárias, como mudar a cor ou imagem de fundo"""
        #raise NotImplementedError("Você deveria ter programado aqui!")
        if self.imagemFundo.retang.estaDentro(mousePos):
            """
            Se está dentro, o botao brilha
            """
            R = self.imagemFundo.cor.R
            G = self.imagemFundo.cor.G
            B = self.imagemFundo.cor.B
            alfa = self.imagemFundo.cor.validaalpha(1)
            self.imagemFundo.cor.setRGBA(R,G,B,alfa)
        else:
            """
            Se não tiver dentro, o botao nao brilha
            """
            R = self.imagemFundo.cor.R
            G = self.imagemFundo.cor.G
            B = self.imagemFundo.cor.B
            alfa = self.imagemFundo.cor.validaalpha(0.5)
            self.imagemFundo.cor.setRGBA(R,G,B,alfa)
    
    def _verClique(self, mousePos):
        """Análogo ao _verEmCima, só que é com o clique agora, o bizu é lançar
        eventos relacionado ao clique, como 'pausar', 'irParaMenuTal' """
        #raise NotImplementedError("Você deveria ter programado aqui!")
        if self.imagemFundo.retang.estaDentro(mousePos):
            """
            Se está dentro, o botao lança o nome do seu evento. 
            """
            self.even.lancar(self._nome_evento,True)
            
    
    """Precisa de outros métodos que ainda não pensei"""
    




class Cena(Camada):
    """Classe que representa a cena do jogo, no qual existem as camadas e 
    objetos renderizáveis. Ela é responsável pela propagação de eventos. Se 
    comunica com a Entrada, com o Audio e com o Renderizador. """
    def inicializaImagem(self, figura):
        lar, alt = self.renderizador.carregaImagem(figura.getString())
        if figura.corte is None:
            figura.corte = Retangulo(Ponto(0, 0), largura = lar, altura = alt)
    def inicializaTexto(self, texto):
        largura,altura = self.renderizador.getSizeTexto(texto.getString(),
                                                        texto.tupla_fonte)
        texto.size = (largura,altura)
    
    
    def __init__ (self, audio, entrada, renderizador, str_musica_fundo = None):
        """Precisa-se da referência aos objetos de Audio, Entrada e 
        Renderizador"""
        super().__init__()
        self.audio = audio
        if str_musica_fundo is not None:
            self.audio.setMusicaFundo(str_musica_fundo)
        self.entrada = entrada
        self.renderizador = renderizador
        
        self.even.escutar("imagem_nova", self.inicializaImagem)
        self.even.escutar("texto_novo", self.inicializaTexto)
        self.even.escutar("tocar_efeito", self.audio.tocarEfeito)
    
    
    def atualiza(self, dt):
        """Propaga o loop do jogo, sabendo o intervalo de tempo dt 
        transcorrido"""
        self.entrada.atualiza()
        
        
        imgs, txts = self._observaFilhos()
        retangs = self.renderizador.renderiza(imgs, txts)
        for ret in retangs:
            ret[0].retang.setDimensoes(ret[1], ret[2], ret[3], ret[4])
        self._atualizaRetangs()
        super().atualiza(dt)
    


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@package motor
Biblioteca arquitetada para servir como base para o jogo em si.

Created on Mon Mar 27 08:25:06 2017

@author: gabrui Gabriel Adriano de Melo
"""

import pygame
import math
from database import banco_dados


class Aux:
    """
    @class Aux
    Classes com funções auxiliares para mexer com listas etc...
    """
    @staticmethod
    def removeTuplas1Elem(lista, elem):
        """
        @function removeTuplas1Elem
        Remove as tuplas de uma lista cujo primeiro elemento é o 'elem'
        @param {list} lista Uma lista de tuplas
        @param {type} elem O primeiro elemento da tupla a ser comparado
        """
        i = 0
        while i < len(lista):
            if lista[i][0] == elem:
                del lista[i]
            i += 1
    
    
    @staticmethod
    def existeTupla1Elem(lista, elem):
        """
        @function existeTupla1Elem
        Verifica se existe uma tupla em uma lista cujo primeiro elemento é o \
            'elem'
        @param {list} lista Uma lista de tuplas
        @param {type} elem O primeiro elemento da tupla a ser comparado
        @returns {bool} Se existe ou não essa tupla na lista
        """
        for tupla in lista:
            if tupla[0] == elem:
                return True
        return False
    
    
    @staticmethod
    def coordsInscrito(angulo, Cx, Cy, largura, altura):
        """
        @function coordsInscrito
        Retorna as coordenadas de um ponto (Cx, Cy) dentro de um retângulo \
            rotacionado em relação a um retangulo horizontal que o \
            circunscreve \
            OBS: ver a fórmula que eu já deduzi, conforme a imagem rotacoes.svg
        @param {Angulo} angulo Um objeto do tipo Angulo que informa o ângulo \
            de rotação
        @param {float} Cx A posição x do ponto a ser transformado
        @param {float} Cy A posição y do ponto a ser transformado
        @param {float} largura A largura do retângulo original
        @param {float} altura A Altura do retângulo original
        @returns {tuple} (x, y) Posição do ponto transformado com relação ao \
            ponto superior esquerdo do retângulo que o circunscreve
        """
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
            return(-(largura - Cx)*math.cos(angulo.getAngulo(False))
                   - (altura - Cy)*math.sin(angulo.getAngulo(False)),
                   - (altura - Cy)*math.cos(angulo.getAngulo(False)) 
                   - Cx*math.sin(angulo.getAngulo(False)))
        elif angulo.getQuadrante() == 4:
            return (Cx*math.cos(angulo.getAngulo(False)) 
                    - (altura - Cy)*math.sin(angulo.getAngulo(False)),
                      Cy*math.cos(angulo.getAngulo(False)) 
                      - Cx*math.sin(angulo.getAngulo(False)))
        




class Singleton:
    """
    @class Singleton
    Decorador para criação de Slingletons
    """
    def __init__(self, classe):
        """
        @function __init__
        Decorador de Slingletons, tem como argumento a classe a ser decorada
        @param {class} classe Classe a ser decorada
        """
        self.classe = classe
        self.objeto = None
    
    
    def __call__(self,*args, **kwargs):
        """
        @function __call__
        Função mágica, chamada quando qualquer método é chamada, em  \
            particular, o __init__
        @param {list} *args Lista de argumentos recebidos
        @param {list} **kwargs Dicionário de argumentos recebidos
        @returns {object} Instância da classe
        """
        if self.objeto == None:
            self.objeto = self.classe(*args,**kwargs)
        return self.objeto





@Singleton
class Evento:
    """
    @class Evento
    É uma classe Singleton como de costume. 
    A performance foi muito prejudicada por várias instâncias de evento e o
    modelo de propagação arquitetado anteriormente
    """
    def __init__(self):
        """
        @fuction __init__
        Inicialização do gerenciador de eventos
        """
        self._escutaveis = {} # Podem ser vistos como aparáveis
    
    
    def escutar(self, string_evento, callback):
        """
        @function escutar
        Começar a escutar determinado evento, isto é, a função de callback \
            será executada quando acontecer o evento em questão. \
            Será passado um objeto para a função de callback como parâmetro, \
            contendo informações sobre esse evento.
        @param {string} string_evento Identificador do evento em questão
        @param {function} callback Função a ser chamada quando o evento for \
            disparado, ela recebe um objeto como parâmetro quando chamada
        """
        if self._escutaveis.get(string_evento) is None:
            self._escutaveis[string_evento] = [callback]
        elif callback not in self._escutaveis[string_evento]:
            self._escutaveis[string_evento].append(callback)
    
    
    def pararDeEscutar(self, string_evento, callback = None):
        """
        @function pararDeEscutar
        Para de escutar determinado evento
        @param {string} string_evento Identificador do evento em questão
        @param {function} callback Se não for passada a função de chamada, \
            todos as escutas com a mesma string_evento serão removidas
        """
        if callback is None or len(self._escutaveis[string_evento]) == 1:
            del self._escutaveis[string_evento]
        else:
            self._escutaveis[string_evento].remove(callback)
    
    
    def pararDeEscutarTudo(self):
        """
        @function pararDeEscutarTudo
        Apaga todas as escutas, de forma a zerar o gerenciador de eventos
        """
        self._escutaveis.clear()
    
    
    def lancar(self, string_evento, objeto_do_evento):
        """
        @function lancar
        Lançar um determinado evento, isto é, gera um evento no qual outros \
            objetos podem escutar.
            Para tal, é necessário o indentificador do evento e o objeto \
            relacionado ao evento, que será passado como parâmetro para a \
            função de callback
        @param {string} string_evento Identificador do evento em questão
        @param {object} objeto_do_evento Objeto a ser passado como parâmetro \
            para  a função de callback associado ao evento em questao
        """
        if self._escutaveis.get(string_evento) is not None:
            for callback in self._escutaveis[string_evento]:
                callback(objeto_do_evento)





class Ponto:
    """
    @class Ponto
    Classe que representa um ponto 2d do tipo (x, y)
    """
    def __init__ (self, x = 0, y = 0):
        """
        @function __init__
        Inicializa o ponto
        @param {float} x Posição x do ponto
        @param {float} y Posição y do ponto
        """
        self._x = x
        self._y = y
    
    
    def setXY(self, x, y):
        """
        @function setXY
        Reinicializa o ponto com nova posição x e y
        @param {float} x Posição x do ponto
        @param {float} y Posição y do ponto
        """
        self._x = x
        self._y = y
    
    
    def setX(self, x):
        """
        @function setX
        Atualiza o ponto com nova posição x
        @param {float} x Posição x do ponto
        """
        self._x = x
    
    
    def setY(self, y):
        """
        @function setY
        Atualiza o ponto com nova posição y
        @param {float} y Posição y do ponto
        """
        self._y = y
    
    
    def getX(self):
        """
        @function getX
        Retorna a posição x do ponto
        @returns {float} Posição x do ponto
        """
        return self._x
    
    
    def getY(self):
        """
        @function getY
        Retorna a posição y do ponto
        @returns {float} Posição y do ponto
        """
        return self._y
    
    
    def getXY(self):
        """
        @function getXY
        Retorna a posição x e y do ponto
        @returns {tuple} Tupla com as posições x e y do ponto
        """
        return (self._x, self._y)
    
    
    def distancia2(self, ponto):
        """
        @function distancia2
        Retorna a distância entre este ponto e outro, ao quadrado
        @returns {float} Distância dos dois pontos ao quadrado
        """
        return ((self._x-ponto._x)*(self._x-ponto._x) + 
                (self._y-ponto._y)*(self._y-ponto._y) )
    
    
    def distancia(self, ponto):
        """
        @function distancia
        Retorna a distância entre este ponto e outro
        @returns {float} Distância dos dois pontos
        """
        return math.sqrt(self.distancia2(ponto))
    
    
    def __mul__(self, escalar):
        """
        @function __mul__
        Retorna um novo Ponto resultado da multiplicação deste ponto por um \
            outro ponto.
        @param {Ponto} Ponto a ser multiplicado
        @returns {Ponto} Novo ponto resultado da operação
        """
        return Ponto(self._x * escalar._x, self._y * escalar._y)
    
    
    def retornaMultEscalar(self, escalar):
        """
        @function retornaMultEscalar
        Retorna um novo Ponto resultado da multiplicação deste ponto por um \
            outro ponto.
        @param {Ponto} Ponto a ser multiplicado
        @returns {Ponto} Novo ponto resultado da operação
        """
        return Ponto(self._x * escalar._x, self._y * escalar._y)
    
    
    def __iadd__(self, ponto):
        """
        @function __iadd__
        Soma um outro ponto a si próprio
        @param {Ponto} Ponto a ser somado
        @returns {Ponto} Si próprio
        """
        self._x = self._x + ponto._x
        self._y = self._y + ponto._y
        return self
    
    
    def soma(self, ponto):
        """
        @function soma
        Soma um outro ponto a si próprio
        @param {Ponto} Ponto a ser somado
        """
        self._x = self._x + ponto._x
        self._y = self._y + ponto._y
    
    
    def __add__(self, ponto):
        """
        @function __add__
        Retorna um novo ponto resultado da soma de si por outro, sem alterar \
            o seu próprio valor
        @param {Ponto} Ponto a ser somado
        @returns {Ponto} Novo ponto resultado da operação
        """
        return Ponto(self._x + ponto._x, self._y + ponto._y)
    
    
    def retornaSoma(self, ponto):
        """
        @function retornaSoma
        Retorna um novo ponto resultado da soma de si por outro, sem alterar \
            o seu próprio valor
        @param {Ponto} Ponto a ser somado
        @returns {Ponto} Novo ponto resultado da operação
        """
        return Ponto(self._x + ponto._x, self._y + ponto._y)     
    
    
    def clonar(self):
        """
        @function clonar
        Retorna um novo ponto que é uma cópia de si próprio
        @returns {Ponto} Novo ponto clonado
        """
        return Ponto(self._x, self._y)





class Retangulo:
    """
    Classe que representa um retângulo horizontal
    """
    def __init__(self, ponto1 = None, ponto2 = None, largura = 0, altura = 0):
        """
        @function __init__
        Inicializa o retângulo com dois pontos ou com um ponto e uma largura \
            e uma altura. O retângulo é horizontal e não pode ser rotacionado.\
            O retângulo utiliza as coordenadas cartesianas com x positivo \ 
            para direita e y positivo para baixo.
        @param {Ponto} ponto1 Representa um vértice do retângulo. Ele é usado \
            como ponto superior esquerdo se não houver
        @param {Ponto} ponto2 Representa o outro vértice diametralmente oposto
        @param {float} largura É ignorado se houver ponto2
        @param {float} altura É ignorado se houver ponto2
        """
        if ponto1 is not None:
            self._p1 = ponto1
        else:
            self._p1 = Ponto(0, 0)
        if ponto2 is not None:
            self._p2 = ponto2
        else:
            self._p2 = self._p1.retornaSoma(Ponto(largura, altura))
    

    def getLargura(self):
        """
        @function getLargura
        Retorna o valor da largura do retângulo, um valor SEMPRE positivo,\
            independentemente da posição dos pontos
        @returns {float} Largura do retângulo
        """
        larg = self._p1.getX()-self._p2.getX()
        if larg>0:
            return larg
        else:
            return -larg
    
    
    def getAltura(self):
        """
        @function getAltura
        Retorna o valor da altura do retângulo, um valor SEMPRE positivo
        @returns {float} Altura do retângulo
        """
        alt = self._p1.getY()-self._p2.getY()
        if alt>0:
            return alt
        else:
            return -alt
    
    
    def getTopo(self):
        """
        @function getTopo
        Retorna o valor de y do ponto no topo do retângulo (menor y)
        @returns {float} Valor de y da aresta do topo
        """
        if self._p1.getY() < self._p2.getY():
            return self._p1.getY()
        return self._p2.getY()
    
    
    def getFundo(self):
        """
        @function getFundo
        Retorna o valor de y do ponto no fundo do retângulo (maior y)
        @returns {float} Valor de y da aresta do fundo
        """
        if self._p1.getY() > self._p2.getY():
            return self._p1.getY()
        return self._p2.getY()
    
    
    def getEsquerda(self):
        """
        @function getEsquerda
        Retorna o valor de x do ponto na esquerda do retângulo (menor x)
        @returns {float} Valor de x da aresta da esquerda
        """
        if self._p1.getX() < self._p2.getX():
            return self._p1.getX()
        return self._p2.getX()
    
    
    def getDireita(self):
        """
        @function getDireita
        Retorna o valor de x do ponto na direita do retângulo (maior x)
        @returns {float} Valor de x da aresta da direita
        """
        if self._p1.getX() > self._p2.getX():
            return self._p1.getX()
        return self._p2.getX()

    
    def getTopoEsquerdo(self):
        """
        @function getTopoEsquerdo
        Retorna um ponto que representa o ponto superior esquerdo
        @returns {Ponto} Novo ponto do topo esquerdo do retângulo
        """
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
        """
        @function getTopoDireito
        Retorna um ponto que representa o ponto superior direito
        @returns {Ponto} Novo ponto que representa o ponto superior direito
        """
        return Ponto(self.getTopoEsquerdo()._x + self.getLargura(), \
                     self.getTopoEsquerdo()._y)
    
    
    def getFundoEsquerdo(self):
        """
        @function getFundoEsquerdo
        Retorna um ponto que representa o ponto inferior esquerdo
        @returns {Ponto} Novo ponto que representa o ponto inferior esquerdo
        """
        return Ponto(self.getTopoEsquerdo()._x, self.getTopoEsquerdo()._y + \
                     self.getAltura())
    
    
    def getFundoDireito(self):
        """
        @function getFundoDireito
        Retorna um ponto que representa o ponto inferior direito
        @returns {Ponto} Novo ponto que representa o ponto inferior direito
        """
        return Ponto(self.getTopoDireito()._x, self.getTopoDireito()._y + \
                     self.getAltura())
    
    
    def setRetangulo(self, ponto1, ponto2):
        """
        @function setRetangulo
        Modifica o retângulo, definindo-o com relação aos pontos
        @param {Ponto} ponto1 Objeto do tipo ponto que define um vértice
        @param {Ponto} ponto2 Outro objeto do tipo ponto do vértice \
            diametralmente oposto
        """
        self._p1 = ponto1
        self._p2 = ponto2
    
    
    def setRetanguloQueContem(self, lista_retangulos):
        """
        @function setRetanguloQueContem
        Modifica o retângulo, definindo-o como o menor retângulo que contém \
            todos os outros retângulos da lista de retângulos.
        @param {list} lista_retangulos Lista de retângulos
        """
        x_esquerda = lista_retangulos[0].getTopoEsquerdo().getX()
        y_topo = lista_retangulos[0].getTopoEsquerdo().getY()
        x_direita = lista_retangulos[0].getFundoDireito().getX()
        y_fundo = lista_retangulos[0].getTopoDireito().getY()
        for retangulo in lista_retangulos:
            if x_esquerda > retangulo.getTopoEsquerdo().getX():
                x_esquerda = retangulo.getTopoEsquerdo().getX()
            if y_topo > retangulo.getTopoEsquerdo().getY():
                y_topo = retangulo.getTopoEsquerdo().getY()
            if x_direita < retangulo.getFundoDireito().getX():
                x_direita = retangulo.getFundoDireito().getX()
            if y_fundo < retangulo.getFundoDireito().getY():
                y_fundo = retangulo.getFundoDireito().getY()
        self.setRetangulo(Ponto(x_esquerda, y_topo), Ponto(x_direita, y_fundo))
            
    
    def estaDentro(self, ponto):
        """
        @function estaDentro
        Dado um objeto do tipo Ponto, retorna verdadeiro se ele está dentro \
            do retângulo
        @param {Ponto} ponto Ponto a ser analisado
        @returns {bool} Se o ponto está dentro ou não
        """
        if ponto.getX() > self.getTopoEsquerdo().getX() and ponto.getY() > \
        self.getTopoEsquerdo().getY() and \
        ponto.getY() < self.getFundoDireito().getY() and\
        ponto.getX()< self.getFundoDireito().getX():
            return True
        else:
            return False
    
    
    def setDimensoes(self, posX, posY, largura, altura):
        """
        @function setDimensoes
        Parecido com o setRetangulo, mas utiliza largura e altura
        @param {float} posX Posição x da aresta esquerda
        @param {float} posY Posição y da aresta superior
        @param {float} largura Largura do retângulo
        @param {float} altura Altura do retângulo
        """
        self._p1.setXY(posX, posY)
        self._p2 = self._p1.retornaSoma(Ponto(largura, altura))





class Angulo:
    """
    Classe que cuida dos ângulos, armazenados em graus, que devem estar 
    entre 180 (inclusive) e -180
    """
    @staticmethod
    def grausParaRadianos(angulo):
        """
        @function grausParaRadianos
        Converte um ângulo em graus para radianos
        @param {float} angulo O ângulo em graus
        @returns {float} O ângulo em radianos
        """
        return math.radians(angulo)
    
    
    @staticmethod
    def radianosParaGraus(angulo):
        """
        @function radianosParaGraus
        Converte um ângulo de radianos para graus
        @param {float} angulo O ângulo em radianos
        @returns {float} O ângulo em graus
        """
        return math.degrees(angulo)
    
    
    def _validaAngulo(self):
        """
        @function _validaAngulo
        Faz com que o ângulo fique entre 180 (inclusive) e -180 graus
        """
        while self._angulo <= -180:
            self._angulo += 360
        while self._angulo > 180:
            self._angulo -= 360
    
    
    def __init__ (self, angulo, emGraus = True):
        """
        @function __init__
        Inicializa o ângulo, se não estiver em graus suponho radianos
        @param {float} angulo
        @param {bool} emGraus Se está em graus
        """
        if emGraus:
            self._angulo =  angulo
        else: #Suponho que esteja em radianos
            self._angulo = Angulo.radianosParaGraus(angulo)
        self._validaAngulo()
    
    
    def getAngulo(self, emGraus = True):
        """
        @function getAngulo
        Retorna o ângulo em graus ou radianos
        @param {bool} emGraus Se o ângulo a ser retornado é em graus, opcional
        @returns {float} Ângulo
        """
        if emGraus:
            return self._angulo
        return Angulo.grausParaRadianos(self._angulo)
    
    
    def setAngulo(self, angulo, emGraus = True):
        """
        @function setAngulo
        Modifica o valor do angulo
        @param {bool} emGraus Se o ângulo a ser retornado é em graus, é \
            opcional, o padrão é verdadeiro
        """
        if emGraus:
            self._angulo =  angulo
        else: #Suponho que caso contrário esteja em radianos
            self._angulo = Angulo.radianosParaGraus(angulo)
        self._validaAngulo()
        
    
    def incrementa(self, angulo, emGraus = True):
        """
        @function incrementa
        Incrementa um valor de angulo ao atual, isto é, a si próprio
        @param {float} angulo Ângulo a ser somado
        @param {bool} emGraus Se o ângulo está em graus, opcional
        """
        if emGraus:
            self.setAngulo(self._angulo + angulo)
        else:
            self.setAngulo(self._angulo + Angulo.radianosParaGraus(angulo))
    
    
    def __add__(self, outro):
        """
        @function __add__
        Retorna um novo Ãngulo resultado da soma deste com outro
        @param {Angulo} angulo Ângulo a ser somado
        @returns {Angulo} Resultado da soma
        """
        return Angulo(self._angulo + outro._angulo)
    
    
    def getQuadrante(self):
        """
        @function getQuadrante
        Retorna o quadrante do ângulo
        @returns {int} Quadrante do ângulo
        """
        #raise NotImplementedError("Você deveria ter programado aqui!")
        if 0 <= self._angulo < 90:
            return 1
        elif 90 <= self._angulo< 180:
            return 2
        elif -180 <= self._angulo < -90:
            return 3
        elif -90 <= self._angulo < 0:
            return 4
    
    
    def getDiferenca(self, outro):
        """
        @function getDiferenca
        Retorna um angulo que é a diferença entre o outro ângulo, isto é, \
            o que é necessário somar a este ângulo para atingir o outro
        @param {Angulo} outro Um objeto do tipo ângulo
        @returns {Angulo} Um novo ângulo resultado da operação
        """
        return Angulo(outro.getAngulo() - self.getAngulo())





class Cor:
    """
    Classe que representa a opacidade e a tintura aplicada a um 
    renderizável
    """
    def _validaAlpha(self, alpha):
        """
        @function _validaAlpha
        Verifica se um valor de alpha (ou opacidade) está dentro do padrão, \
            retornando o seu valor validado
        @param {float} alpha
        @returns {float} O valor de alpha validado
        """
        if alpha > 1:
            alpha = 1
        elif alpha < 0:
            alpha = 0
        return alpha
    
            
    def _validaRGB(self, RGB):
        """
        @function _validaRGB
        Verifica se o valor de uma variável está dentro do padrão RGB, \
            retornando o seu valor validado
        @param {int}
        @returns {int} Valor validado
        """
        RGB = int(RGB)
        if RGB > 255:
            RGB = 255
        elif RGB < 0:
            RGB = 0
        return RGB
    
    
    def __init__(self, opacidade, R, G, B, A):
        """
        @function __init__
        Inicializa uma cor
        @param {float} opacidade É a opacidade (ou alpha) da textura original
        @param {int} R Valor de R da tintura a ser aplicada
        @param {int} G Valor de G da tintura a ser aplicada
        @param {int} B Valor de B da tintura a ser aplicada
        @param {float} alpha É a opacidade (ou alpha) da tintura a ser aplicada
        """
        self.opacidade = self._validaAlpha(opacidade)
        self.R = self._validaRGB(R)
        self.G = self._validaRGB(G)
        self.B = self._validaRGB(B)
        self.A = self._validaAlpha(A)
    
    
    def setRGBA(self, R, G, B, A):
        """
        @function setRGBA
        Modifica a tintura da cor
        @param {int} R Valor de R da tintura a ser aplicada
        @param {int} G Valor de G da tintura a ser aplicada
        @param {int} B Valor de B da tintura a ser aplicada
        @param {float} alpha É a opacidade (ou alpha) da tintura a ser aplicada
        """
        self.R = self._validaRGB(R)
        self.G = self._validaRGB(G)
        self.B = self._validaRGB(B)
        self.A = self._validaAlpha(A)
    
    
    def setOpacidade(self, opacidade):
        """
        @function setOpacidade
        Modifica a opacidade (ou alpha) da textura original
        @param {float} opacidade É a opacidade (ou alpha) da textura original
        """
        self.opacidade = self._validaAlpha(opacidade)





class Renderizador:
    """
    @class Renderizador
    Classe que faz a interface com a pygames de funções relacionadas à \
    renderização
    """
    #Variável de Classe que contém todas as imagem já carregadas pelo pygames
    _listaImagens = {}
    _listaFontes = {}
    
    def __init__(self, nome_tela, largura, altura, corFundo = (0, 0, 0), 
                 icone_tela = ""):
        """
        @function __init__
        Só deve existir apenas um renderizador
        @param {string} nome_tela O nome da janela
        @param {int} largura A largura da janela
        @param {int} altura A altura da janela
        @param {tuple} corFundo Uma tupla de 3 inteiros que define a cor de \
            fundo da renderização
        @param {string} icone_tela A string com o caminho para a imagem a ser \
            utilizado como ícone da tela
        """
        pygame.init()
        self.tela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption(nome_tela)
        self.corFundo = corFundo
        self.even = Evento()
        self.escutas()
    
    
    def escutas(self):
        """
        @function escutas
        Inicializa as escutas que essa classe faz
        """
        self.even.escutar("imagem_nova", self.inicializaImagem)
        self.even.escutar("texto_novo", self.inicializaTexto)
    
    
    def inicializaImagem(self, figura):
        """
        @function inicializaImagem
        Função que manda carregar a imagem no banco de imagens e inicializar \
            o corte da Figura, caso ela não tenha um já definido.
        @param {Figura} figura O objeto Figura a ser inicializado
        """
        img = self._bancoImagens(figura.getString())
        if img is None:
            lar, alt = self._carregaImagem(figura.getString())
        else:
            lar, alt = img.get_size()
        if figura.corte is None:
            figura.corte = Retangulo(Ponto(0, 0), largura = lar, altura = alt)
            
    
    def inicializaTexto(self, texto):
        """
        @function inicializaTexto
        Função responsável por atribuir os valores para o tamanho do texto
        @param {Texto} texto Um objeto do tipo Texto a ser inicializado
        """
        largura,altura = self.getSizeTexto(texto.getString(),
                                                        texto.tupla_fonte)
        texto.size = (largura,altura)
    
    
    def _bancoImagens(self, string_imagem):
        """
        @function _bancoImagens
        Retorna um objeto imagem do pygame dado a string
        @param {string} string_imagem Localiza a imagem
        @returns {pygame.Surface} Um objeto de superfície do pygames
        """
        return self._listaImagens.get(string_imagem)
    
    
    def _carregaImagem(self, string_imagem):
        """
        @function _carregaImagem
        Carrega a imagem na memória e retorna o tamanho dela
        @param {string} Localiza a imagem
        @returns {tuple} Tupla com a largura e a altura da imagem
        """
        from os import sep
        # Dependendo do sistema operacional o separador pode ser / ou \\
        caminho = string_imagem.replace('/', sep)
        imagem = pygame.image.load(caminho)
        self._listaImagens[string_imagem] = imagem
        return imagem.get_size()
    
    
    def _carregaFonte(self, tupla_fonte):
        """
        @function _carregaFonte
        Armazena a fonte na memória
        @param {tuple} tupla_fonte Define o estado da fonte, é organizada da \
            seguinte forma: \
            tupla_fonte = (string_fonte,int tamanho \
                           ,bold = True or False,italic = True or False)
        """
        # Dependendo do sistema operacional o separador pode ser / ou \\
        name = tupla_fonte[0]
        size = tupla_fonte[1]
        bold = tupla_fonte[2]
        italic = tupla_fonte[3]
        fonte = pygame.font.SysFont(name, size, bold, italic)
        self._listaFontes[tupla_fonte] = fonte
        
        
    def getSizeTexto(self, string_texto, tupla_fonte):
        """
        @function getSizeTexto
        Função que retorna a largura e altura da fonte
        @param {string} string_texto É o texto a ser renderizado
        @param {tuple} tupla_fonte Define o estado da fonte
        @returns {tuple} Tupla com a largura e a altura da fonte
        """
        fonte = self._bancoFontes(tupla_fonte)
        return fonte.size(string_texto)


    def _bancoFontes(self, tupla_fonte):
        """
        @function _bancoFontes
        Carrega a fonte na memória
        @param {tuple} tupla_fonte Define o estado 
        @returns {pygame.font} Objeto de fonte do pygame
        """
        fonte = self._listaFontes.get(tupla_fonte)
        if fonte is None:
            self._carregaFonte(tupla_fonte)
            fonte = self._listaFontes.get(tupla_fonte)
        return fonte
    
    
    def renderiza(self, imagens, textos):
        """
        @function renderiza
        Renderiza tudo, a partir da lista de tuplas de imagens e de texto. \
            Nessa renderização ele desenha todo o quadro de uma só vez, com \
            base na lista de imagens e textos recebidos. Retorna uma lista de \
            retangulos com as dimensões reais e posição na tela.
        @param {list} imagens Lista de tuplas de imagens, definidas da \
            seguinte forma:
            (string_imagem, tupla_corte, posX, posY, rotação, opacidade, 
             R, G, B, A, self)
            Onde a tupla_corte é (posX, posY, largura, altura) referentes ao \
            retangulo de corte da imagem
        @param {list} textos Lista de tuplas de textos, definidas da seguinte \
            forma:
            (string_texto, tupla_fonte, posX, posY, rotação, opacidade, 
             R, G, B, A, self)
            Onde a tupla_fonte é definida da seguinte forma:
                tupla_fonte = (string_fonte,int tamanho \
                           ,bold = True or False,italic = True or False)
        @returns {list} Lista com tuplas definidas da seguinte forma:
            (objeto, posX, posY, larg, alt) que são os retângulos que \
            definem o objeto renderizável em questão
        """
        self.tela.fill(self.corFundo)
        retangs = []
        for i in imagens:
            imagem = self._bancoImagens(i[0])
            tam = imagem.get_size()
            # Verifica se o corte é a própria imagem
            if i[1] == (0, 0, tam[0], tam[1]):
                recorte = imagem
            else: # Se não for, realiza o corte
                recorte = imagem.subsurface(i[1])
            # Verifica se a rotação da imagem é nula
            if i[4] == 0:
                imagemRotate = recorte
            else: # Se houver rotação, realiza a transformação
                imagemRotate = pygame.transform.rotate(recorte,i[4])
            # Verifica a opacidade, se for diferente de 1, calcula
            if i[5] != 1 :
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
    """
    @class Entrada
    Classe que faz interface com o pygames e registra todos os eventos de 
    entrada, seja de mouse ou teclado
    """
    def __init__(self):
        """
        @function __init__
        Inicializa a entrada, só deve haver apenas um objeto de entrada.
        """
        self.even = Evento()
        self.clickAntigo = False
    
    
    def _verTeclado(self):
        """
        @function _verTeclado
        Observa quais teclas estão pressionadas e se está focado
        """
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
        """
        @function _verMouse
        Observa a posição do ponteiro e se clica, lancando os eventos
        """
        click = pygame.mouse.get_pressed() 
        mouse = pygame.mouse.get_pos()
        if click[0]:
            if self.clickAntigo == False:
                self.even.lancar("M_fclick", Ponto(mouse[0], mouse[1]))
            self.even.lancar("M_click", Ponto(mouse[0], mouse[1]))
        if click[2]:
            self.even.lancar("M_clickD", Ponto(mouse[0], mouse[1]))
        self.even.lancar("M_pos", Ponto(mouse[0], mouse[1]))
        self.clickAntigo = click[0]
            
    
    def atualiza(self):
        """
        @function atualiza
        Atualiza os seus eventos
        """
        self._verTeclado()
        self._verMouse()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.sair()
                
    
    def sair(self):
        """
        @function sair
        Fecha o jogo
        """
        pygame.quit()
        quit()





class Audio:
    """
    @class Audio
    Faz a interface com o audio do pygames
    """
    #Variável de classe dos arquivos carregados pelo pygames
    _arquivos = {}
    
    def __init__ (self):
        """
        @function __init__
        Inicializa o Audio, só deve haver uma instância do audio
        """
        self.musicaFundo = None
        self.even = Evento()
        self.escutas()
    
    
    def escutas(self):
        """
        @function escutas
        Inicializa as escutas do audio
        """
        self.even.escutar("tocarEfeito", self.tocarEfeito)
        
    
    def _carregarAudio(self, string_musica):
        """
        @function _carregarAudio
        Carrega o arquivo de audio na memória, retornando-o
        @param {string} string_musica Caminho do arquivo de música
        @returns {pygame.Sound} Objeto de música do pygame
        """
        from os import sep
        # Dependendo do sistema operacional o separador pode ser / ou \\
        caminho = string_musica.replace('/', sep)
        musica = pygame.mixer.Sound(caminho)
        self._arquivos[string_musica] = musica
        return musica
    
    
    def _bancoAudio(self, string_musica):
        """
        @function _bancoAudio
        Retorna o objeto de música a partir da string, e se não tiver \
            carregado a música, carrega
        @param {string} string_musica Caminho do arquivo de música
        @returns {pygame.Sound} O objeto de música carregado
        """
        musica = self._arquivos.get(string_musica)
        if musica is None:
            musica = self._carregarAudio(string_musica)
        return musica
    
    
    def setMusicaFundo(self, string_musica, volume = 0.5):
        """
        @function setMusicaFundo
        Determina a música de fundo a ser tocada
        @param {string} string_musica Caminho do arquivo de música
        @param {float} volume O volume da música a ser tocada
        """
        self.musicaFundo = self._bancoAudio(string_musica)
        self.musicaFundo.set_volume(volume)
        self.musicaFundo.play(-1)
    
    
    def setVolumeMusicaFundo(self, volume):
        """
        @function setVolumeMusicaFundo
        Modifica apenas o volume da música de fundo, sem interferir nela
        @param {float} volume O volume da música a ser tocada
        """
        self.musicaFundo.set_volume(volume)
    
    
    def tocarEfeito(self, string_efeito):
        """
        @function tocarEfeito
        Toca um efeito sonoro apenas uma vez
        @param {string} string_efeito O caminho do efeito sonoro a ser tocado
        """
        self.efeito = self._bancoAudio(string_efeito)
        self.efeito.play()
    
    
    def pararMusicaFundo(self):
        """
        @function pararMusicaFundo
        Para a música de fundo
        """
        self.musicaFundo.stop()
        
        
    def verificarMusicaFundo(self):
        """
        @function verificarMusicaFundo
        Verifica o estado da música de fundo
        @returns {bool} Retorna verdadeiro se esta tocando
        """
        return self.musicaFundo.get_busy()





class Renderizavel:
    """
    @class Renderizavel
    Classe abstrata que contém os atributos básicos de um objeto 
    renderizável
    """
    def __init__(self, pos = None, centro = None, escala = None,
                 rot = None, cor = None):
        """
        @function __init__
        Possui a posição 'pos' que é uma coordenada relativa ao seu pai, o \
            seu centro de rotação 'centro', relativo a si próprio, sua escala \ 
            de tamanho, seu ângulo de rotação e sua coloração
        @param {Ponto} pos Posição do renderizável com relação ao seu pai
        @param {Ponto} centro Posição do seu centro de rotação com relação a \
            si próprio, isto é, com relação ao pos
        @param {Ponto} escala Escala x e y, seu tamanho relativo
        @param {Angulo} rot Angulo de rotação com relação ao seu pai
        @param {Cor} cor Tintura e opacidade
        """
        if pos is not None:
            self.pos = pos
        else:
            self.pos = Ponto()
        if centro is not None:
            self.centro = centro
        else:
            self.centro = Ponto()
        if escala is not None:
            self.escala = escala
        else:
            self.escala = Ponto(1, 1)
        if rot is not None:
            self.rot = rot
        else:
            self.rot = Angulo(0)
        if cor is not None:
            self.cor = cor
        else:
            self.cor = Cor(1, 0, 0, 0, 0)
        self.even = Evento()
        """É um Retangulo que contém (circunscreve) todo o seu conteúdo, e só \
        é atualizado na renderização"""
        self.retang = Retangulo(Ponto(0, 0), Ponto(0, 0))
        
    
    def atualiza(self, dt):
        """
        @function atualiza
        Método a ser sobreposto pelos herdeiros, dt representa o tempo
        @param {float} dt O tempo desde a última execução
        """
        pass





class Figura(Renderizavel):
    """
    @class Figura
    Representa uma imagem na árvore de renderização
    """
    def setString(self, string_imagem, corte = None):
        """
        @function setString
        Redefine a string imagem dessa figura, lançando um evento
        @param {string} string_imagem Caminho do arquivo de imagem
        @param {Retangulo} corte Opcional, é o corte da imagem, isto é, um \
            retângulo que define a área renderizável da imagem
        """
        self._string_imagem = string_imagem
        self.corte = corte
        self.even.lancar("imagem_nova", self)
    
    
    def __init__(self, string_imagem, corte = None, pos = None, centro = None, 
                 escala = None, rot = None, cor = None):
        """
        @function __init__
        A string_imagem representa o caminho da imagem e é seu \
            indentificador único. O corte representa um retângulo que corta a \
            imagem original, no caso dela ser um conjunto de imagens.
        @param {string} string_imagem Caminho do arquivo de imagem
        @param {Retangulo} corte Opcional, é o corte da imagem, isto é, um \
            retângulo que define a área renderizável da imagem
        @param {Ponto} pos Posição do renderizável com relação ao seu pai
        @param {Ponto} centro Posição do seu centro de rotação com relação a \
            si próprio, isto é, com relação ao pos
        @param {Ponto} escala Escala x e y, seu tamanho relativo
        @param {Angulo} rot Angulo de rotação com relação ao seu pai
        @param {Cor} cor Tintura e opacidade
        """
        super().__init__(pos, centro, escala, rot, cor)
        Figura.setString(self, string_imagem, corte)
    
    
    def getString(self):
        """
        @function getString
        Retorna a string_imagem dessa figura
        @returns {string} O caminho do arquivo que essa Figura utiliza
        """
        return self._string_imagem

    def ativarEscuta(self):
        pass



class Animacao(Figura):
    """
    @class Animacao
    Classe base para uma animação de spritesheet (folha de animações)
    """
    def setString(self, string_imagem, largu = 0, altu = 0, corte = None):
        """
        @function setString
        Redefine a string imagem dessa figura, isto é, redefinindo a sua \
            folha de animações, e reinicializando-a
        @param {string} string_imagem Caminho do arquivo de imagem
        @param {int} largu Largura da imagem a ser extraída da folha de \
            animações.
        @param {int} altu Altura da imagem a ser extraída da folha de \
            animações.
        @param {Retangulo} corte Opcional, é o corte da imagem, isto é, um \
            retângulo que define a área renderizável da imagem
        """
        super().setString(string_imagem, corte)
        self._ponto0 = self.corte.getTopoEsquerdo()
        self._larguraSS = self.corte.getLargura()
        self._alturaSS = self.corte.getAltura()
        if largu == 0:
            largu = self._larguraSS
        if altu == 0:
            altu = self._alturaSS
        self._largu = largu
        self._altu = altu
        self._colunas = self._larguraSS//self._largu
        self._linhas = self._alturaSS//self._altu
        self._numTotal = self._colunas * self._linhas
        self._numCorte = 0
        self._vezes = 0
        self._dtAnim = 0
        self._T = 1
        self.setNumCorte(0)
    
    
    def __init__(self, string_imagem, largu = 0, altu = 0, corte = None, 
                 pos = None, centro = None, escala = None, rot = None, 
                 cor = None):
        """
        @function __init__
        Suponho cortes regulares, igualmentes distribuidos
        @param {string} string_imagem Caminho do arquivo de imagem
        @param {int} largu Largura da imagem a ser extraída da folha de \
            animações.
        @param {int} altu Altura da imagem a ser extraída da folha de \
            animações.
        @param {Retangulo} corte Opcional, é o corte da imagem, isto é, um \
            retângulo que define a área renderizável da imagem
        @param {Ponto} pos Posição do renderizável com relação ao seu pai
        @param {Ponto} centro Posição do seu centro de rotação com relação a \
            si próprio, isto é, com relação ao pos
        @param {Ponto} escala Escala x e y, seu tamanho relativo
        @param {Angulo} rot Angulo de rotação com relação ao seu pai
        @param {Cor} cor Tintura e opacidade
        """
        super().__init__(string_imagem, corte, pos, centro, escala, rot, cor)
        # Declaração de variáveis
        self._ponto0 = None
        self._larguraSS = 0
        self._alturaSS = 0
        self._largu = 0
        self._altu = 0
        self._colunas = 0
        self._linhas = 0
        self._numTotal = 0
        self._numCorte = 0
        self._vezes = 0
        self._dtAnim = 0
        self._T = 0
        self.setString(string_imagem, largu, altu, corte)
    
    
    def setNumCorte(self, num):
        """
        @function setNumCorte
        Determina o número de corte a ser utilizar, esse número começa do zero
        @param {int} num É o número da figura a ser extraída da spritesheet
        """
        if num < 0 or num >= self._numTotal:
            raise IndexError("Número de corte inválido")
        self._numCorte = num
        linha = num // self._colunas
        coluna = num % self._colunas
        ponto = (self._ponto0 + Ponto(coluna*self._largu, linha*self._altu))
        self.corte.setRetangulo(ponto, ponto + Ponto(self._largu, self._altu))
        
    
    def getNumCorte(self):
        """
        @function getNumCorte
        Retorna o número de corte atual
        @returns {int} Número de corte atual
        """
        return self._numCorte
    
    
    def rodarAnimacao(self, tempo_de_cada_vez, vezes = 1):
        """
        @function rodarAnimacao
        Função responsável por fazer a animação rodar, começando do 0 até o \
            último, repetindo se necessário
        @param {float} tempo_de_cada_vez É o tempo para rodar a animação uma \
            única vez
        @param {int} É o número de vezes que a animação deve ser repetida
        """
        self._dtAnim = 0
        self._numCorte = 0
        self._vezes = vezes
        self._T = tempo_de_cada_vez
        
    
    def atualiza(self, dt):
        """
        @function atualiza
        É quem de fato realiza a animação, deve ser chamada para que a \
            animação ocorra, e não deve ser sobreposto, isto é, deve ser \
            chamdo pela classe que a sobrepõe
        @param {float} dt Tempo desde a última execução
        """
        if self._vezes > 0:
            self.setNumCorte(int(self._dtAnim*self._numTotal/self._T))
            self._dtAnim += dt
            while self._dtAnim >= self._T:
                self._vezes -= 1
                self._dtAnim -= self._T




class Texto(Renderizavel):
    """
    @class Texto
    Representa um texto na aŕvore de renderização
    """
    def __init__(self, string_texto, tupla_fonte, pos = None, centro = None, 
                 escala = None, rot = None, cor = None):
        """
        @function __init__
        É um texto, com significado e estilo
        @param {string} string_texto É o texto a ser renderizado
        @param {tuple} tupla_fonte Contém o estado do texto, é definido por:
            tupla_fonte = ({string} string_fonte, {int} tamanho \
                           , {bool} bold , {bool} italic)
            A string_fonte é o tipo de fonte (arial, helvetica, sans ...)
        @param {Ponto} pos Posição do renderizável com relação ao seu pai
        @param {Ponto} centro Posição do seu centro de rotação com relação a \
            si próprio, isto é, com relação ao pos
        @param {Ponto} escala Escala x e y, seu tamanho relativo
        @param {Angulo} rot Angulo de rotação com relação ao seu pai
        @param {Cor} cor Tintura e opacidade
        """
        super().__init__(pos, centro, escala, rot, cor)
        self.tupla_fonte = tupla_fonte
        self.setString(string_texto)
        self.size = (0, 0)
        
        
    def setString(self, string_texto):
        """
        @function setString
        Redefine a string do texto dessa texto
        @param {string} string_texto Novo texto a ser renderizado
        """
        self._string_texto = string_texto
        self.even.lancar("texto_novo", self) 
        
        
    def getString(self):
        """
        @function getString
        Retorna a string_texto dessa texto
        @returns {string} O texto que está sendo renderizado
        """
        return self._string_texto





class Camada(Renderizavel):
    """
    @class Camada
    Representa uma camada na árvore renderização
    """
    def __init__(self, pos = None, centro = None, escala = None, rot = None, 
                 cor = None):
        """
        @function __init__
        Possui a posição 'pos' que é uma coordenada relativa ao seu pai, o \
            seu centro de rotação 'centro', relativo a si próprio, sua escala \ 
            de tamanho, seu ângulo de rotação e sua coloração
        @param {Ponto} pos Posição do renderizável com relação ao seu pai
        @param {Ponto} centro Posição do seu centro de rotação com relação a \
            si próprio, isto é, com relação ao pos
        @param {Ponto} escala Escala x e y, seu tamanho relativo
        @param {Angulo} rot Angulo de rotação com relação ao seu pai
        @param {Cor} cor Tintura e opacidade
        """
        super().__init__(pos, centro, escala, rot, cor)
        self.filhos = []
    
    
    def adicionaFilho(self, filho):
        """
        @function adicionaFilho
        Adiciona um filho (Renderizável) à camada, para que ele possa \
            integrar a árvore de renderização. Os filhos adicionados \
            primeiros ficam mais ao fundo.
        @param {Renderizavel} filho Objeto do tipo Renderizavel, pode ser uma
            outra Camada, uma Figura, um Texto por exemplo
        """
        self.filhos.append(filho)
    
    
    def removeFilho(self, filho):
        """
        @function removeFilho
        Remove o filho da camada, caso ele esteja presente
        @param {Renderizavel} filho Objeto Renderizavel a ser removido
        """
        if filho in self.filhos:
            self.filhos.remove(filho)
        
        
    def isFilho(self, filho):
        """
        @function isFilho
        Verifica se um dado objeto é filho da camada
        @returns {bool} Retorna verdadeiro se for filho
        """
        return (filho in self.filhos)
    
    
    def atualiza(self, dt):
        """
        @function atualiza
        Atualiza os seus filhos. Atenção, deve ser chamada caso ela seja \
            sobreposta.
        @param {float} dt O tempo em segundos desde a última execução
        """
        for filho in self.filhos:
            filho.atualiza(dt)
    
    
    def _transformaFigura(self, camadaFilha, estado):
        """
        @function _transformaFigura
        Converte as coordenadas e transformações de uma figura representada \
            pela sua tupla (string_imagem, posX ....), que está no referencial\
            da camadaFilha, para o seu próprio referencial, retornando a nova \
            tupla, que é definida da mesma forma: \
            (string_imagem, tupla_corte, posX, posY, rotação, opacidade, \
             R, G, B, A, self) \
            Onde a tupla_corte é (posX, posY, largura, altura) referentes ao \
            retangulo de corte da imagem
        @param {Camada} camadaFilha A camada que contém o estado
        @param {tuple} estado A tupla que define o estado da Figura
        @returns {tuple} O novo estado nas coordenadas desta camada
        """
        ang = camadaFilha.rot.getAngulo()
        if ang != 0:
            Cx = camadaFilha.centro.getX()
            Cy = camadaFilha.centro.getY()
            alfa = math.atan2(Cy - estado[3],Cx - estado[2])
            hipo = math.sqrt((Cy - estado[3])*(Cy - estado[3]) + 
                             (Cx - estado[2])*(Cx - estado[2]) )
            teta = Angulo.grausParaRadianos(ang)
            posX = camadaFilha.pos.getX() - hipo*math.cos(alfa + teta) + Cx
            posY = camadaFilha.pos.getY() - hipo*math.sin(alfa + teta) + Cy
        else:
            posX = camadaFilha.pos.getX() + estado[2]
            posY = camadaFilha.pos.getY() + estado[3]
        return (estado[0],estado[1], posX, posY, estado[4] + ang, estado[5],
                estado[6], estado[7],estado[8],estado[9],estado[10])
        
    
    
    def _transformaTexto(self, camadaFilha, estado):
        """
        @function _transformaTexto
        Converte as coordenadas e transformações de um texto representado \
            pela sua tupla que define o seu estado, que está no referencial \
            da camadaFilha, para o seu próprio referencial, retornando a nova \
            tupla, que é definida da mesma forma: \
            (string_texto, tupla_fonte, posX, posY, rotação, opacidade, \
             R, G, B, A, self) \
            Onde a tupla_fonte é ({string} string_fonte, {int} tamanho, \
                                  {bool} bold , {bool} italic)
        @param {Camada} camadaFilha A camada que contém o estado
        @param {tuple} estado A tupla que define o estado do Texto
        @returns {tuple} O novo estado nas coordenadas desta camada
        """
        return self._transformaFigura(camadaFilha, estado)
    
    
    def _observaFilhos(self):
        """
        @function _observaFilhos
        Retorna os filhos que tem, na ordem, separando imagem de texto. \
            É uma tupla com uma lista de imagem e uma lista de texto, essas \
            listas contém tuplas que definem o estado da figura e texto, no \
            estado mais reduzido, assim definidas para Imagem e Texto: \
            Para Imagem: \
                (string_imagem, tupla_corte, posX, posY, rotação, opacidade, 
                 R, G, B, A, self)
                Onde a tupla_corte é (posX, posY, largura, altura) referentes \
                ao retangulo de corte da imagem. \
            Para Texto: \
                (string_texto, tupla_fonte, posX, posY, rotação, opacidade, \
                R, G, B, A, self) \
                Onde a tupla_fonte é definida da seguinte forma:
                    tupla_fonte = ({string} string_fonte, {int} tamanho, \
                                  {bool} bold , {bool} italic)
        @returns {tuple} Uma tupla que contém uma lista de tuplas para os \
            estados: (figuras, textos), onde figuras é uma lista de tuplas de \
            estado de figuras e textos de textos.
        """
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
                x = filho.pos.getX()
                y = filho.pos.getY()
                figuras.append((filho.getString(), 
                 (filho.corte.getEsquerda(), filho.corte.getTopo(),
                  filho.corte.getLargura(), filho.corte.getAltura()),
                  x, y, filho.rot.getAngulo(), filho.cor.opacidade, 
                  filho.cor.R, filho.cor.G, filho.cor.B, filho.cor.A, filho))
            elif isinstance(filho, Texto):
                """tupla do texto: 
                (string_texto, tupla_fonte, posX, posY, rotação, opacidade, 
                 R, G, B, A, self)
                o self é a referência à própria imagem que gerou a tupla"""
                x = filho.pos.getX()
                y = filho.pos.getY()
                textos.append((filho.getString(), filho.tupla_fonte,
                              x, y, filho.rot.getAngulo(), filho.cor.opacidade, 
                              filho.cor.R, filho.cor.G, 
                              filho.cor.B, filho.cor.A, filho))
        #raise NotImplementedError("Você deveria ter programado aqui!")
        return (figuras, textos)
    
    
    def _transformaFinal(self, figtex):
        """
        @function _transformaFinal
        Realiza a transformação final de coordenadas para as coordenadas de \
            renderização do Pygames, isto é, em relação ao canto superior \
            direito do retângulo que o contém.
        @param {tuple} Uma tupla do tipo (figuras, textos) que contém lista \
            de estados (tuplas de estado) de figuras e textos.
        @returns {tuple} O mesmo tipo de tupla com as coordenadas transformadas
        """
        figs, texs = figtex
        for i in range(len(figs)):
            estado = figs[i]
            filho = estado[10]
            ang = Angulo(estado[4])
            if ang.getAngulo() != 0:
                x, y = Aux.coordsInscrito( ang, filho.centro.getX(), 
                            filho.centro.getY(), filho.corte.getLargura(), 
                                             filho.corte.getAltura())
            else:
                x = filho.centro.getX()
                y = filho.centro.getY()
            x = estado[2] - x
            y = estado[3] - y
            figs[i] = (estado[0], estado[1], x, y, ang.getAngulo(), 
                estado[5], estado[6], estado[7], estado[8], estado[9],
                estado[10])
        for i in range(len(texs)):
            estado = texs[i]
            filho = estado[10]
            ang = Angulo(estado[4])
            if ang.getAngulo() != 0:
                x, y = Aux.coordsInscrito( ang, filho.centro.getX(), 
                            filho.centro.getY(), filho.size[0], filho.size[1])
            else:
                x = filho.centro.getX()
                y = filho.centro.getY()
            x = estado[2] - x
            y = estado[3] - y
            texs[i] = (estado[0], estado[1], x, y, ang.getAngulo(), 
                estado[5], estado[6], estado[7], estado[8], estado[9],
                estado[10])
        return figtex
    
    
    def _atualizaRetangs(self):
        """
        @function _atualizaRetangs
        Atualiza os retangs das camadas filhas e depois o seu próprio retang. \
        É importante notar que o retang é um retângulo horizontal (Retangulo) \
        que circunscreve todo o seu conteúdo e que ele só é atualizado na \
        renderização.
        """
        for filho in self.filhos:
            if isinstance(filho, Camada):
                filho._atualizaRetangs()
                
        retangs = [filho.retang for filho in self.filhos]
        self.retang.setRetanguloQueContem(retangs)





class Botao(Camada):
    """
    @class Botao
    Representa um botão clicável que contém uma imagem de fundo e texto \
    A imagem do Botao já possui fundo e texto.
    """
    def __init__(self,nome_evento,string_chamada, string_imagem1, string_imagem2, som_click,
                 pos = None, centro = None, escala = None, rot = None, 
                 cor = None):
        """
        Cria.
        nome_evento: é uma string com o nome do evento que o botao deve gerar
                     ao ser clicado.
        string_imagem1: é o nome do arquivo imagem do botao em estado normal.
        string_imagem2: é o nome do arquivo imagem do botao com mouse em cima.
        string_chamada: é o nome da cena que fez uma chamada para outra cena.
        som_click:      é o nome do arquivo som do botao quando clicado.
        """
        super().__init__(pos, centro, escala, rot, cor)
        self.even.escutar("M_pos", self._verEmCima)
        self.even.escutar("M_click", self._verClique)
        self.string_imagem1 = string_imagem1
        self.string_imagem2 = string_imagem2
        self.imagem = Figura(string_imagem1)
        self.adicionaFilho(self.imagem)
        self._nome_evento = nome_evento
        self.string_chamada = string_chamada
        self.som_click = som_click
    
    
    def _verEmCima(self, mousePos):
        """Recebe um objeto mousePos do tipo ponto e verifica se o mousePos 
        está dentro do seu retângulo de renderização, tomando as ações
        necessárias, como mudar a cor ou imagem de fundo"""
        
        if self.imagem.retang.estaDentro(mousePos):
            """
            Se está dentro, o botao brilha
            """
            self.imagem.setString(self.string_imagem2)
            self.imagem.cor.setOpacidade(1)
        else:
            """
            Se não tiver dentro, o botao nao brilha
            """
            self.imagem.setString(self.string_imagem1)
            self.imagem.cor.setOpacidade(0.8)
            
    
    def _verClique(self, mousePos):
        """Análogo ao _verEmCima, só que é com o clique agora, o bizu é lançar
        eventos relacionado ao clique, como 'pausar', 'irParaMenuTal' """
        
        if self.imagem.retang.estaDentro(mousePos):
            """
            Se está dentro, o botao lança o nome do seu evento. 
            """
            self.even.lancar("tocarEfeito", self.som_click)
            self.even.lancar(self._nome_evento, self.string_chamada)
    
class item (Botao):
    """
        Representa os itens da loja.
    """
    def __init__(self,nome_evento_compra,string_chamada, string_imagem1,
                 string_imagem2, som_click,valor = None,XP = None,pos = None,
                 centro = None, escala = None, rot = None, 
                 cor = None):
        """
            inicializacao.
            nome_evento_compra: é o nome do item
            _valor: é o preco do item.
            _cadeado: True está com cadeado. False nao está com cadeado
            _img_cadeado: imagem do cadeado
            _XP: é preco do item em pontos de experiencia.
        """
        super().__init__(nome_evento_compra,string_chamada, string_imagem1, 
                         string_imagem2, som_click, pos,centro,escala,rot,cor)
        if valor == None:
            valor = 100
        if XP == None:
            XP = 200
        self._XP = XP
        self._valor = valor
        self._cadeado = True
        #escutar evento de compra. 
        self.even.escutar(nome_evento_compra,self.compra)
        #Criar imagem do cadeado
        self._img_cadeado = Figura("imgTeste/c02_Locker.png",
                                   pos = Ponto(self.retang.getLargura()/2+20,-30))
        #colocar para ser renderizado na Tela
        self.adicionaFilho(self._img_cadeado)
        
    def verificarDisponibilidade(self):
        """
            verifica se este item esta disponivel para compra ou nao.
        """
        #pega o saldo da carteira do Jogador.
        reputacao = banco_dados.getXP()
        #verifica condicao de disponibilidade da compra
        if reputacao >= self._valor:
            return True
        else:
            return False
    def compra(self,chamada):
        """
            realiza a compra do item.
        """
        saldo = banco_dados.getCarteira()
        if saldo >= self._valor:
            banco_dados.acrescimoSaldo(-self._valor)
            return True
        else:
            return False
        
    def atualiza(self,dt):
        
        super().atualiza(dt)
        
        if self.verificarDisponibilidade() and self._cadeado:
            self.removeFilho(self._img_cadeado)
        elif not self.verificarDisponibilidade() and not self._cadeado:
            self.adicionaFilho(self._img_cadeado)

class item_aviao(item):
    """
        representa uma skin de aviao que pode ser vendido na loja (Hangar).
    """
    def __init__(self,string_imagem_aviao,string_imagem_aviao_invertido,
                 nome_evento_compra,string_chamada,string_imagem2,
                 som_click,valor = None,pos = None,
                 centro = None, escala = None, rot = None, 
                 cor = None):
        item.__init__(self,nome_evento_compra,string_chamada,string_imagem_aviao,
                         string_imagem2, som_click,valor,pos,
                         centro, escala, rot, 
                         cor)
        #string da imagem da skin
        self._string_imagem_aviao = string_imagem_aviao
        self._string_imagem_aviao_invertido = string_imagem_aviao_invertido
        #indica se ja foi comprado ou nao
        self._foiComprado = False
        
    def compra(self,chamada):
        #metodo que realiza a compra deste item
        #verifica pagamento
        caixa_aprovado = super().compra(chamada)
        #pega lista de skins do Jogador
        tupla_lista = banco_dados.getStringAviao()
        self._foiComprado = False
        #verifica se este item ja foi comprado
        for string in tupla_lista[0]:
            if string == self._string_imagem_aviao:
                self._foiComprado = True
        if caixa_aprovado and not self._foiComprado:
            #pagamento concluido e nao foi comprado
            #adicionar este item na lista de skin do Jogador
            banco_dados.addStringAviao((self._string_imagem_aviao,
                                        self._string_imagem_aviao_invertido))
        
class Cena(Camada):
    """Classe que representa a cena do jogo, no qual existem as camadas e 
    objetos renderizáveis. Ela é responsável pela propagação de eventos. Se 
    comunica com a Entrada, com o Audio e com o Renderizador. """
    
    def __init__ (self, audio, entrada, renderizador, str_musica_fundo = None):
        """Precisa-se da referência aos objetos de Audio, Entrada e 
        Renderizador"""
        super().__init__()
        self.audio = audio
        if str_musica_fundo is not None:
            self.audio.setMusicaFundo(str_musica_fundo)
        self.entrada = entrada
        self.renderizador = renderizador
    
    
    def atualiza(self, dt):
        """Propaga o loop do jogo, sabendo o intervalo de tempo dt 
        transcorrido"""
        super().atualiza(dt)
        self.entrada.atualiza()
        imgs, txts = self._transformaFinal(self._observaFilhos())
        retangs = self.renderizador.renderiza(imgs, txts)
        for ret in retangs:
            ret[0].retang.setDimensoes(ret[1], ret[2], ret[3], ret[4])
        self._atualizaRetangs()


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 08:25:06 2017

@author: gabrui
"""

import pygame

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
    
    
    @staticmethod
    def coordsInscrito(angulo, Cx, Cy, largura, altura):
        """Retorna as coordenadas de um ponto (Cx, Cy) dentro de um retângulo 
        rotacionado em relação a um retangulo horizontal que o circunscreve
        OBS: ver a fórmula que eu já deduzi, conforme a imagem rotacoes.svg"""
        raise NotImplementedError("Você deveria ter programado aqui!")
        return (0, 0)




class Evento:
    """É uma classe que todo objeto que registra eventos deve ter uma instância
    isto é, ele não é um Singleton como de costume."""
    
    def __init__(self):
        """Variáveis de instância _escutaveis e lancados"""
        #É uma lista de tuplas (stringEvento, funcao_de_chamada)
        self._escutaveis = [] # Podem ser vistos como aparáveis
        #É uma lista de tuplas (stringsEventos, objeto_do_evento) LANÇADOS
        self._lancados = []
    
    
    def escutar(self, string_evento, callback):
        """Começar a escutar determinado evento, isto é, a função de callback
        será executada quando acontecer o evento em questão. 
        Será passado um objeto para a função de callback como parâmetro, 
        contendo informações sobre esse evento."""
        self._escutaveis.append((string_evento, callback))
    
    
    def pararDeEscutar(self, string_evento, callback = None):
        """Para de escutar determinado evento"""
        if callback is None:
            Aux.removeTuplas1Elem(self._escutaveis, string_evento)
        else:
            self._escutaveis.remove((string_evento, callback))
    
    
    def lancar(self, string_evento, objeto_do_evento):
        """Lançar um determinado evento, isto é, gera um evento no qual outros
        objetos podem escutar.
        Para tal, é necessário o indentificador do evento e o objeto
        relacionado ao evento, que será passado como parâmetro para a função de
        callback"""
        if Aux.existeTupla1Elem(self._escutaveis, string_evento):
            self._disparados.append((string_evento, objeto_do_evento))
    
    
    def pararLancamento(self, string_evento, objeto_do_evento = None):
        """Remove um evento da lista de eventos lançados"""
        if objeto_do_evento is None:
            Aux.removeTuplas1Elem(self._disparados, string_evento)
        else:
            self._disparados.remove((string_evento, objeto_do_evento))
    
    
    def pararTodosLancamentos(self):
        """Limpa a lista de eventos lançados"""
        del self._disparados[:]
    
    
    def recebeEscuta(self, evento):
        """Executa as funções de escuta (callback) dado os lançamentos 
        presentes em um outro evento"""
        for escutavel, callback in self._escutaveis:
            for disparo, objeto_do_evento in evento._disparados: 
                if escutavel == disparo:
                    callback(objeto_do_evento)
    
    
    def propagaLancamento(self, evento):
        """Fala para outro evento o que você disparou, e se ele não souber 
        responder, ele pega para ele o que você falou, isto é, parando o seu 
        lançamento e escutando o seu evento ou lançando-o adiante. """
        for disparo, objeto_do_evento in self._disparados:
            escutou = False
            for escutavel, callback in evento._escutaveis:
                if escutavel == disparo:
                    callback(objeto_do_evento)
                    escutou = True
            if not escutou:
                evento.lancar(disparo, objeto_do_evento)
            self.pararLancamento((disparo, objeto_do_evento))




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
        raise NotImplementedError("Você deveria ter programado aqui!")
    
    
    def retornaSoma(self, ponto):
        """Retorna um novo ponto resultado da soma de si por outro, sem alterar
        o seu próprio valor"""
        raise NotImplementedError("Você deveria ter programado aqui!")
        return Ponto()
    
    
    def clonar(self):
        """Retorna uma cópia de si mesmo"""
        raise NotImplementedError("Você deveria ter programado aqui!")
        return Ponto()




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
        raise NotImplementedError("Você deveria ter programado aqui!")
        return 1
    
    
    def getAltura(self):
        """Retorna o valor da altura do retângulo, um valor SEMPRE positivo"""
        raise NotImplementedError("Você deveria ter programado aqui!")
        return 1
    
    
    def getTopoEsquerdo(self):
        """Retorna um ponto que representa o ponto superior esquerdo"""
        raise NotImplementedError("Você deveria ter programado aqui!")
        return Ponto()
    
    
    def getTopoDireito(self):
        """Retorna um ponto que representa o ponto superior direito"""
        raise NotImplementedError("Você deveria ter programado aqui!")
        return Ponto()
    
    
    def getFundoEsquerdo(self):
        """Retorna um ponto que representa o ponto inferior esquerdo"""
        raise NotImplementedError("Você deveria ter programado aqui!")
        return Ponto()
    
    
    def getFundoDireito(self):
        """Retorna um ponto que representa o ponto inferior direito"""
        raise NotImplementedError("Você deveria ter programado aqui!")
        return Ponto()
    
    
    def setRetangulo(self, ponto1, ponto2):
        """Modifica o retângulo, definindo-o com relação aos pontos"""
        raise NotImplementedError("Você deveria ter programado aqui!")
    
    
    def setRetanguloQueContem(self, lista_retangulos):
        """Modifica o retângulo, definindo-o como o menor retângulo que contém
        todos os outros retângulos da lista de retângulos."""
        raise NotImplementedError("Você deveria ter programado aqui!")
    
    
    def estaDentro(self, ponto):
        """Dado um objeto do tipo Ponto, retorna verdadeiro se ele está dentro
        do retângulo"""
        raise NotImplementedError("Você deveria ter programado aqui!")
        return True




class Angulo:
    """Classe que cuida dos ângulos, armazenados em graus, que devem estar 
    entre 180 (inclusive) e -180"""
    
    @staticmethod
    def grausParaRadianos(angulo):
        from math import radians
        return radians(angulo)
    
    
    @staticmethod
    def RadianosParaGraus(angulo):
        from math import degrees
        return degrees(angulo)
    
    
    def _validaAngulo(self):
        """Faz com que o ângulo fique entre 180 (inclusive) e -180 graus"""
        while self._angulo <= -180:
            self._angulo += 360
        while self._angulo > 180:
            self.angulo -= 360
    
    
    def __init__ (self, angulo, emGraus = True):
        """Se não estiver em graus suponho radianos"""
        if emGraus:
            self._angulo =  angulo
        else: #Suponho que esteja em radianos
            self._angulo = Angulo.RadianosParaGraus
        self._validaAngulo()
    
    
    def getAngulo(self):
        """Retorna o ângulo em graus"""
        return self._angulo
    
    
    def setAngulo(self, angulo, emGraus = True):
        if emGraus:
            self._angulo =  angulo
        else: #Suponho que caso contrário esteja em radianos
            self._angulo = Angulo.RadianosParaGraus
        self._validaAngulo()
    
    
    def getQuadrante(self):
        """Retorna o quadrante do ângulo"""
        raise NotImplementedError("Você deveria ter programado aqui!")
        return 1




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
    _listaImagens = []
    _listaFontes = []
    
    def __init__(self, largura, altura, corFundo = (0, 0, 0)):
        self.tela = pygame.display.set_mode((largura, altura))
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
    
    
    def _carregaFonte(self, nome_fonte):
        """Carrega a fonte na memória"""
        raise NotImplementedError("Você deveria ter programado aqui!")
    
    
    def _bancoFontes(self, nome_fonte):
        fonte = self._listaFontes.get(nome_fonte)
        if fonte is None:
            self._carregaFonte(nome_fonte)
            fonte = self._listaFontes.get(nome_fonte)
        return fonte
    
    
    def renderiza(self, imagens, textos):
        """Renderiza tudo, a partir da lista de imagens e de texto: 
            (string_imagem, tupla_corte, posX, posY, rotação, opacidade, 
             R, G, B, A)
            (string_texto, tupla_fonte, posX, posY, rotação, opacidade, 
             R, G, B, A)
        Nessa renderização ele desenha todo o quadro de uma só vez, com base na
        lista de imagens e textos recebidos
        Gabriel: Essas tuplas podem ser melhoradas de acordo com o que vocês 
        acharem conveniente"""
        self.tela.fill(self.corFundo)
        #CÓDIGO AQUI
        raise NotImplementedError("Você deveria ter programado aqui!")
        pygame.display.flip()
        



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
                self.even.lancar("K_"+pygame.key.name(ide), None)
        if vazio:
            self.even.lancar("K_vazio", None)
        if not pygame.key.get_focused():
            self.even.lancar("K_desfocado", None)
    
    
    def _verMouse(self):
        """Observa a posição do ponteiro e se clica, lancando os eventos"""
        raise NotImplementedError("Você deveria ter programado aqui!")
    
    
    def atualiza(self):
        """Atualiza os seus eventos"""
        self._verTeclado()
        self._verMouse()




class Audio:
    """Faz a interface com o audio do pygames"""
    
    #Variável de classe dos arquivos carregados pelo pygames
    arquivos = []
    
    def _bancoAudio(self, string_musica):
        """Retorna o objeto de música a partir da string, e se não tiver
        carregado a música, carrega"""
        raise NotImplementedError("Você deveria ter programado aqui!")
        self.musica = pygame.mixer.Sound(string_musica)
        return self.musica
    
    
    def setMusicaFundo(self, string_musica, volume = 1):
        """A música de fundo a ser tocada"""
        raise NotImplementedError("Você deveria ter programado aqui!")
    
    
    def setVolumeMusicaFundo(self, volume):
        """Modifica apenas o volume da música de fundo, sem interferir nela"""
        raise NotImplementedError("Você deveria ter programado aqui!")
        self.musica.set_volume(volume)
    
    def tocarEfeito(self, string_efeito):
        """Toca um efeito sonoro apenas uma vez"""
        raise NotImplementedError("Você deveria ter programado aqui!")
        self.efeito = pygame.mixer.Sound(string_efeito)
        self.efeito.play()
        
            



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
        self.retang = Retangulo(0, 0, 0, 0)
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
        self.string_texto = string_texto
        self.tupla_fonte = tupla_fonte
        
    



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


    def _propagaEventoDeCimaParaBaixo(self, evento):
        self.even.recebeEscuta(evento)
        for filho in self.filhos:
            if isinstance(filho, Camada):
                filho._propagaEventoDeCimaParaBaixo(evento)
            else:
                filho.even.recebeEscuta(evento)
    
    
    def _propagaEventoDeBaixoParaCima(self):
        for filho in self.filhos:
            if isinstance(filho, Camada):
                filho._propagaEventoDeBaixoParaCima()
            filho.even.propagaLancamento(self.even)
    
    
    def _transformaFigura(self, camadaFilha, estado):
        """Converte as coordenadas e transformações de uma figura representada
        pela sua tupla (string_imagem, posX ....) que está no referencial da
        camadaFilha para o seu próprio referencial, retornando a nova tupla"""
        raise NotImplementedError("Você deveria ter programado aqui!")
        return (estado[0], 0, 0, 0, 0)
    
    
    def _transformaTexto(self, camadaFilha, estado):
        """Converte as coordenadas e transformações de um texti representado
        pela sua tupla (string_texto, posX ....) que está no referencial da
        camadaFilha para o seu próprio referencial, retornando a nova tupla"""
        raise NotImplementedError("Você deveria ter programado aqui!")
        return (estado[0], 0, 0, 0, 0)
    
    
    def _observaFilhos(self):
        """Retorna os filhos que tem, na ordem, separando imagem de texto.
        É uma tupla com uma lista de imagem e uma lista de texto, essas listas
        contém tuplas que definem o estado da figura e texto, no estado mais
        reduzido: atentar que a posX e posY se refere ao ponto superior
        esquerdo do retângulo exterior.
            (string_imagem, tupla_corte, posX, posY, rotação, opacidade, 
             R, G, B, A)
            (string_texto, tupla_fonte, posX, posY, rotação, opacidade, 
             R, G, B, A)
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
                pass #IMPLEMENTAR AQUI
            elif isinstance(filho, Texto):
                pass #IMPLEMENTAR AQUI
        raise NotImplementedError("Você deveria ter programado aqui!")
        return (figuras, textos)




class Botao(Camada):
    """Representa um botão clicável que contém uma imagem de fundo e texto"""
    
    def __init__(self, tupla_string_imagem, tupla_texto, pos = Ponto(), 
                 centro = Ponto(), escala = Ponto(1, 1), rot = Angulo(0), 
                 cor = Cor(1, 0, 0, 0, 0)):
        """Cria"""
        super().__init__(pos, centro, escala, rot, cor)
        raise NotImplementedError("Você deveria ter programado aqui!")
    
    """Precisa de outros métodos que ainda não pensei"""





class Cena(Camada):
    """Classe que representa a cena do jogo, no qual existem as camadas e 
    objetos renderizáveis. Ela é responsável pela propagação de eventos. Se 
    comunica com a Entrada, com o Audio e com o Renderizador. """
    def inicializaImagem(self, figura):
        lar, alt = self.renderizador.carregaImagem(figura.getString())
        if figura.corte is None:
            figura.corte = Retangulo(Ponto(0, 0), largura = lar, altura = alt)
    
    
    def __init__ (self, audio, entrada, renderizador, str_musica_fundo = None):
        """Precisa-se da referência aos objetos de Audio, Entrada e Renderizador"""
        super().__init__()
        self.audio = audio
        if str_musica_fundo is not None:
            self.audio.setMusicaFundo(str_musica_fundo)
        self.entrada = entrada
        self.renderizador = renderizador
        
        self.even.escutar("imagem_nova", self.inicializaImagem)
        self.even.escutar("tocar_efeito", self.audio.tocarEfeito)
    
    
    def atualiza(self, dt):
        """Propaga o loop do jogo, sabendo o intervalo de tempo dt transcorrido"""
        self.entrada.atualiza()
        self.even.pararTodosLancamentos()
        self.entrada.even.propagaLancamento(self.even)
        self._propagaEventoDeCimaParaBaixo(self.even)
        self.even.pararTodosLancamentos()
        self._propagaEventoDeBaixoParaCima()
        self._propagaEventoDeCimaParaBaixo(self.even)
        
        imgs, txts = self._observaFilhos()
        self.renderizador.renderiza(imgs, txts)
    




class Jogo():
    """Controla o loop principal do jogo, faz as transições de cena"""
    
    
    
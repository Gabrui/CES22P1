# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 19:29:56 2017

@author: Dylan N. Sugimoto
"""

from motor import Audio, Renderizador, Entrada, Evento, Figura, Cena, Retangulo, Ponto, Botao
import time
from cenario import FundoParalaxeInfinito
from aviao import Jogador

t20 = 50/1000
FPS = 60
td = 1/FPS

class PainelMenuPrincipal(Cena):
    
    def __init__(self, audio, entrada, renderizador, string_musica_fundo = None):
        Cena.__init__(self, audio, entrada, renderizador, string_musica_fundo)
        #Constantes do Menu Principal
        self._PosXBotaoMenuPrincipal = 329
        self._PosYBotaoJogoNovo      = 175
        self._PosYBotaoJogoSalvo     = 255
        self._PosYBotaoOpcoes        = 335
        self._PosYBotaoCreditos      = 415
        self._PosYBotaoSair          = 495
        self._PosXAviaoDireita1 = 679
        self._PosYAivaoDireita1 = 115
        self._PosXAviaoDireita2 = 654
        self._PosYAviaoDireita2 = 389
        self._PosXAviaoEsquerda = 12
        self._PosYAviaoEsquerda = 49
        self._PosXTituloMenuPrincipal = 179
        self._PosYTituloMenuPrincipal = 12
        self._string_imagem1_botaoNovoJogo = "c04_Text_NovoJogo.png"
        self._string_imagem2_botaoNovoJogo = "c03_Text_NovoJogo.png"
        self._string_imagem1_botaoJogoSalvo = "c04_Text_JogosSalvos.png"
        self._string_imagem2_botaoJogoSalvo = "c03_Text_JogosSalvos.png"
        self._string_imagem1_botaoOpcoes = "c04_Text_Opcoes.png"
        self._string_imagem2_botaoOpcoes = "c03_Text_Opcoes.png"
        self._string_imagem1_botaoCreditos = "c04_Text_Creditos.png"
        self._string_imagem2_botaoCreditos = "c03_Text_Creditos.png"
        self._string_imagem1_botaoSair = "c04_Text_Sair.png"
        self._string_imagem2_botaoSair = "c03_Text_Sair.png"
        self._string_imagem_AviaoDireita1 = "c02_AviaoDireita1.png"
        self._string_imagem_AviaoDireita2 = "c02_AviaoDireita2.png"
        self._string_imagem_AviaoEsquerda = "c02_AviaoEsquerda.png" 
        self._string_imagem_TituloMenuPrincipal = "c03_Text_AsDaAviacao.png"
        #self._string_imagem_Fundo = ""
        #----------------Fim das Constantes do Meneu Principal----------------
        
        #Criando Botoes do Menu
        botaoNovoJogo = Botao("Tutorial",
                              self._string_imagem1_botaoNovoJogo,
                              self._string_imagem2_botaoNovoJogo,
                              Ponto(self._PosXBotaoMenuPrincipal,
                                    self._PosYBotaoJogoNovo))
        botaoJogoSalvo = Botao("MenuJogoSalvo",
                              self._string_imagem1_botaoJogoSalvo,
                              self._string_imagem2_botaoJogoSalvo,
                              Ponto(self._PosXBotaoMenuPrincipal,
                                    self._PosYBotaoJogoSalvo))
        botaoOpcoes = Botao("MenuOpcoes",
                              self._string_imagem1_botaoOpcoes,
                              self._string_imagem2_botaoOpcoes,
                              Ponto(self._PosXBotaoMenuPrincipal,
                                    self._PosYBotaoOpcoes))
        botaoCreditos = Botao("Creditos",
                              self._string_imagem1_botaoCreditos,
                              self._string_imagem2_botaoCreditos,
                              Ponto(self._PosXBotaoMenuPrincipal,
                                    self._PosYBotaoCreditos))
        botaoSair = Botao("Quit",
                          self._string_imagem1_botaoSair,
                          self._string_imagem2_botaoSair,
                          Ponto(self._PosXBotaoMenuPrincipal,
                                self._PosYBotaoSair))
        #Criando imagens e posicionando
        imgAviaoDireita1 = Figura(self._string_imagem_AviaoDireita1,None,
                                  Ponto(self._PosXAviaoDireita1,
                                        self._PosYAviaoDireita1))
        imgAviaoDireita2 = Figura(self._string_imagem_AviaoDireita2,None,
                                  Ponto(self._PosXAviaoDireita2,
                                        self._PosYAviaoDireita2))
        imgAviaoEsquerda = Figura(self._string_imagem_AviaoEsquerda,None,
                                  Ponto(self._PosXAviaoEsquerda,
                                        self._PosYAviaoEsquerda))
        imgTituloMenuPrincipal = Figura(self._string_imagem_TituloMenuPrincipal,
                                        None,
                                        Ponto(self._PosXTituloMenuPrincipal,
                                              self._PosYTituloMenuPrincipal))
        #fundo = Figura(self._string_imagem_Fundo)
        #montando a cena do menu principal
        #self.adicionaFilho(fundo)
        self.adicionaFilho(botaoNovoJogo)
        self.adicionaFilho(botaoJogoSalvo)
        self.adicionaFilho(botaoOpcoes)
        self.adicionaFilho(botaoCreditos)
        self.adicionaFilho(botaoSair)
        self.adicionaFilho(imgAviaoDireita1)
        self.adicionaFilho(imgAviaoDireita2)
        self.adicionaFilho(imgAviaoEsquerda)
        self.adicionaFilho(imgTituloMenuPrincipal)

class PainelTutorial(Cena):
    
    def __init__(self, audio, entrada, renderizador, string_musica_fundo = None):
        Cena.__init__(self, audio, entrada, renderizador, string_musica_fundo)
        
        self._PosXPonteiroFuel = 56
        self._PosYPonteiroFuel = 24
        self._PosXCoin         = 124
        self._PosYCoin         = 15
        self._PosXFuel         = 17
        self._PosYFuel         = 7
        self._PosXHealthPoints = 228
        self._PosYHealthPoint  = 15
        self._PosXHP1          = 494
        self._PosYHP1          = 15
        self._PosXTextCoin     = 170
        self._PosYTextCoin     = 22
        self._PosXTextHealthPoints = 275
        self._PosYTextHealthPoint  = 22
        self._PosXTextMissao3      = 333
        self._PosYTextMissao3      = 22
        
        self._string_imagem_PonteiroFuel = "c(X)_PonteiroFuel.png"
        self._string_imagem_Coin = "c(X)_Coin.png"
        self._string_imagem_Fuel = "c(X+1)_Fuel.png"
        self._string_imagem_HealthPoint = "c(X)_HealthPoints.png"
        self._string_imagem_HP = "c(X+5)_HP1.png"
        self._string_imagem_TextCoin = "c(X)_Text_Coin.png"
        self._string_imagem_TextHealth = "c(X)_Text_Missao3.png"
        self._string_imagem_TextMissao3 ="c(X)_Text_Missao3.png" 
        
        

class Jogo():
    """Controla o loop principal do jogo, faz as transições de cena"""
    
    def __init__(self):
        """Ainda é só um esboço"""
        self.audio = Audio()
        self.renderizador = Renderizador('Ás da Aviação', 800, 600)
        self.entrada = Entrada()
        self.even = Evento()
        self.even.escutar("sair", self.irParaCena)
        self.continuarLoop = True
        self.cenaAtual = None
        self.gameplay()
        self.gameloop()
         
    
    """Ainda estou pensando, podemos discutir esses métodos"""
    def gameplay(self):
        fundos = FundoParalaxeInfinito(800, 600, "imgTeste/estFundo.png", 
                    Retangulo(Ponto(0,0), Ponto(800, 132)), Ponto(0,0), Ponto(0,0))
        #fundo2 = Figura("imgTeste/movFundo.png")
        #fundo3 = Figura("imgTeste/nuvem.png")
        avi = Jogador("imgTeste/hellcat2.png", Ponto(100, 0), Ponto(28, 10),
                 [8000, 90000, 172],  [8000, 4000, 8000, 100, 0.3, 5400, 1],  
                 [5, 50000, 5000/3, 100], [5000, 150])
        
        self.cenaAtual = Cena(self.audio,self.entrada,self.renderizador)
        self.cenaAtual.adicionaFilho(fundos)
        #self.cenaAtual.adicionaFilho(fundo2)
        #self.cenaAtual.adicionaFilho(fundo3)
        self.cenaAtual.adicionaFilho(avi)
        
        #self.even.escutar('MenuPause',self.menuPause)
        #self.even.escutar('Hangar',self.hangar)
    
    def MenuPrincipal(self):
        
        
        
        #trocando de transparencias
        self.cenaAtual = PainelMenuPrincipal(self.audio,self.entrada,
                                             self.renderizador)
        
    
    def gameloop(self):
        tnovo = time.clock()
        while self.continuarLoop:
            tantigo = tnovo
            tnovo = time.clock()
            dt = tnovo - tantigo
            if dt < td:
                time.sleep(td - dt)
            if dt > t20:
                dt = t20
            self.cenaAtual.atualiza(dt)

            
 
            
    def carregaCenas(self, listaCenas):
        pass
    
    
    def rodarCena(self, cena):
        pass
    
    
    def irParaCena(self, cena):
        if cena is None:
            self.continuarLoop = False
    
    
    def atualizar(self):
        #Relógio
        dt = 15 #Time1 - time0
        if self.continuarLoop:
            self.CenaAtual.atualiza(dt)
            self.cenaAtual.even.propagaLancamento(self.even)
    
Jogo()
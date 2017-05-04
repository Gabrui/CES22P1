# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 19:29:56 2017

@author: Dylan N. Sugimoto
"""

from motor import Audio, Renderizador, Entrada, Evento, Figura, Cena, Retangulo, Ponto, Botao
import time
from cenario import FundoParalaxeInfinito
from aviao import Jogador
from Simulador import Simulador
from IA import AviaoInimigo
from Arma import Arma
from Projetil import Projetil
t20 = 50/1000
FPS = 60
td = 1/FPS

class PainelMenuPrincipal(Cena):
    """
        É a classe que monta a cena do menu principal.
    """
    def __init__(self, audio, entrada, renderizador, string_musica_fundo = None):
        Cena.__init__(self, audio, entrada, renderizador, string_musica_fundo)
        #--------------Constantes do Menu Principal---------------------------
        self._PosXBotaoMenuPrincipal = 329
        self._PosYBotaoJogoNovo      = 175
        self._PosYBotaoJogoSalvo     = 255
        self._PosYBotaoOpcoes        = 335
        self._PosYBotaoCreditos      = 415
        self._PosYBotaoSair          = 495
        self._PosXAviaoDireita1 = 679
        self._PosYAviaoDireita1 = 115
        self._PosXAviaoDireita2 = 654
        self._PosYAviaoDireita2 = 389
        self._PosXAviaoEsquerda = 12
        self._PosYAviaoEsquerda = 49
        self._PosXTituloMenuPrincipal = 179
        self._PosYTituloMenuPrincipal = 12
        self._string_imagem1_botaoNovoJogo = "imgTeste/c04_Text_NovoJogo.png"
        self._string_imagem2_botaoNovoJogo = "imgTeste/c03_Text_NovoJogo.png"
        self._string_imagem1_botaoJogoSalvo = "imgTeste/c04_Text_JogosSalvos.png"
        self._string_imagem2_botaoJogoSalvo = "imgTeste/c03_Text_JogosSalvos.png"
        self._string_imagem1_botaoOpcoes = "imgTeste/c04_Text_Opcoes.png"
        self._string_imagem2_botaoOpcoes = "imgTeste/c03_Text_Opcoes.png"
        self._string_imagem1_botaoCreditos = "imgTeste/c04_Text_Creditos.png"
        self._string_imagem2_botaoCreditos = "imgTeste/c03_Text_Creditos.png"
        self._string_imagem1_botaoSair = "imgTeste/c04_Text_Sair.png"
        self._string_imagem2_botaoSair = "imgTeste/c03_Text_Sair.png"
        self._string_imagem_AviaoDireita1 = "imgTeste/c02_AviaoDireita1.png"
        self._string_imagem_AviaoDireita2 = "imgTeste/c02_AviaoDireita2.png"
        self._string_imagem_AviaoEsquerda = "imgTeste/c02_AviaoEsquerda.png" 
        self._string_imagem_TituloMenuPrincipal = "imgTeste/c03_Text_AsDaAviacao.png"
        self._string_imagem_Fundo = "imgTeste/sky.png"
        
        self._string_som_buttonClick = "imgTeste/button_click.ogg"
        #----------------Fim das Constantes do Meneu Principal----------------
        
        #Criando Botoes do Menu
        botaoNovoJogo = Botao("Tutorial",
                              self._string_imagem1_botaoNovoJogo,
                              self._string_imagem2_botaoNovoJogo,
                              self._string_som_buttonClick,
                              Ponto(self._PosXBotaoMenuPrincipal,
                                    self._PosYBotaoJogoNovo))
        botaoJogoSalvo = Botao("MenuJogoSalvo",
                              self._string_imagem1_botaoJogoSalvo,
                              self._string_imagem2_botaoJogoSalvo,
                              self._string_som_buttonClick,
                              Ponto(self._PosXBotaoMenuPrincipal,
                                    self._PosYBotaoJogoSalvo))
        botaoOpcoes = Botao("MenuOpcoes",
                              self._string_imagem1_botaoOpcoes,
                              self._string_imagem2_botaoOpcoes,
                              self._string_som_buttonClick,
                              Ponto(self._PosXBotaoMenuPrincipal,
                                    self._PosYBotaoOpcoes))
        botaoCreditos = Botao("Creditos",
                              self._string_imagem1_botaoCreditos,
                              self._string_imagem2_botaoCreditos,
                              self._string_som_buttonClick,
                              Ponto(self._PosXBotaoMenuPrincipal,
                                    self._PosYBotaoCreditos))
        botaoSair = Botao("Quit",
                          self._string_imagem1_botaoSair,
                          self._string_imagem2_botaoSair,
                          self._string_som_buttonClick,
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
        img_fundo = Figura(self._string_imagem_Fundo)
        #montando a cena do menu principal
        self.adicionaFilho(img_fundo)
        self.adicionaFilho(botaoNovoJogo)
        self.adicionaFilho(botaoJogoSalvo)
        self.adicionaFilho(botaoOpcoes)
        self.adicionaFilho(botaoCreditos)
        self.adicionaFilho(botaoSair)
        self.adicionaFilho(imgAviaoDireita1)
        self.adicionaFilho(imgAviaoDireita2)
        self.adicionaFilho(imgAviaoEsquerda)
        self.adicionaFilho(imgTituloMenuPrincipal)
#---------------------------------Fim da Classe Menu Principal-----------------

class PainelTutorial(Cena):
    """
        É a classe que monta a cena do tutorial.
    """    
    def __init__(self, audio, entrada, renderizador, string_musica_fundo = None):
        Cena.__init__(self, audio, entrada, renderizador, string_musica_fundo)
       
        #----------------------Constantes--------------------------------------
        self._PosXPonteiroFuel = 56
        self._PosYPonteiroFuel = 24
        self._PosXCoin         = 124
        self._PosYCoin         = 15
        self._PosXFuel         = 17
        self._PosYFuel         = 7
        self._PosXHealthPoints = 228
        self._PosYHealthPoints = 15
        self._PosXHP1          = 494
        self._PosYHP1          = 15
        self._PosXTextCoin     = 170
        self._PosYTextCoin     = 22
        self._PosXTextHealthPoints = 275
        self._PosYTextHealthPoints = 22
        self._PosXTextMissao3      = 333
        self._PosYTextMissao3      = 22
        
        self._string_imagem_PonteiroFuel = "imgTeste/c(X)_PonteiroFuel.png"
        self._string_imagem_Coin = "imgTeste/c(X)_Coin.png"
        self._string_imagem_Fuel = "imgTeste/c(X+1)_Fuel.png"
        self._string_imagem_HealthPoint = "imgTeste/c(X)_HealthPoints.png"
        self._string_imagem_HP = "imgTeste/c(X+5)_HP1.png"
        self._string_imagem_TextCoin = "imgTeste/c(X)_Text_Coin.png"
        self._string_imagem_TextHealth = "imgTeste/c(X)_Text_Missao3.png"
        self._string_imagem_TextMissao3 ="imgTeste/c(X)_Text_Missao3.png" 
        self._string_imagem_Fundo = "imgTeste/sky.png"
        #--------------------------Fim das COnstates-------------------------
       
        #Criando as imagens do tutorial
        img_PonteiroFuel = Figura(self._string_imagem_PonteiroFuel,None,
                                  Ponto(self._PosXPonteiroFuel,
                                        self._PosYPonteiroFuel))
        img_Coin = Figura(self._string_imagem_Coin, None, 
                          Ponto(self._PosXCoin,self._PosYCoin))
        img_Fuel = Figura(self._string_imagem_Fuel,None,Ponto(self._PosXFuel,
                                                              self._PosYFuel))
        img_HealthPoints = Figura(self._string_imagem_HealthPoint,None, 
                         Ponto(self._PosXHealthPoints,self._PosYHealthPoints))
        img_HP1 = Figura(self._string_imagem_HP, None,
                         Ponto(self._PosXHP1,self._PosYHP1))
        img_TextCoin = Figura(self._string_imagem_TextCoin,None, 
                              Ponto(self._PosXTextCoin,self._PosYTextCoin))
        img_TextHealthPoint = Figura(self._string_imagem_TextHealth,None,
                                     Ponto(self._PosXTextHealthPoints,
                                           self._PosYTextHealthPoints))
        img_TextMissao3 = Figura(self._string_imagem_TextMissao3,None,
                                 Ponto(self._PosXTextMissao3,
                                       self._PosYTextMissao3))
        img_Fundo = Figura(self._string_imagem_Fundo)
        #montando o tutorial
        self.adicionaFilho(img_Fundo)
        self.adicionaFilho(img_PonteiroFuel)
        self.adicionaFilho(img_Coin)
        self.adicionaFilho(img_Fuel)
        self.adicionaFilho(img_HealthPoints)
        self.adicionaFilho(img_HP1)
        self.adicionaFilho(img_TextCoin)
        self.adicionaFilho(img_TextHealthPoint)
        self.adicionaFilho(img_TextMissao3)
        
        self.even.escutar("M_click",self.Proximo)
        
    def Proximo(self, chamada):
        self.even.lancar("MenuOperacoes", True)
#------------------------------------Fim da Classe PainelTutorial--------------

class PainelMenuOperacoes(Cena):
    """
        É a classe que monta a cena do menu de operacoes.
    """
    def __init__(self, audio, entrada, renderizador, string_musica_fundo = None):
        Cena.__init__(self, audio, entrada, renderizador, string_musica_fundo)
        
        #-----------------Constantes do Menu Principal------------------------
        
        self._PosBackGround = Ponto(0,33)
        self._PosOperacao1 = Ponto(125,145)
        self._PosOperacao2 = Ponto(355,145)
        self._PosTextOperacao1 = Ponto(130,250)
        self._PosTextOperacao2 = Ponto(365,250)
        self._PosTextOperacao3 = Ponto(597,250)
        self._PosBotaoPlay1 = Ponto(125,500)
        self._PosText_GueraGraBret = Ponto(180,300)
        self._PosTextRetornar = Ponto(660,485)
        
        self._string_imagem_fundo = "imgTeste/sky.png"
        self._string_imagem_Background = "imgTeste/c01_Background.png"
        self._string_imagem_Operacao1 = "imgTeste/c02_Operacao1.png"
        self._string_imagem_Operacao2 = "imgTeste/c02_Operacao2.png"
        self._string_imagem_TextOperacao1 = "imgTeste/c02_Text_Operacao1.png"
        self._string_imagem_TextOperacao2 = "imgTeste/c02_Text_Operacao2.png"
        self._string_imagem_TextOpercao3 = "imgTeste/c02_Text_Operacao3.png"
        self._string_imagem_BotaoPlay = "imgTeste/c02_BotaoPlay.png"
        self._string_imagem_TextGuerraGraBret = "imgTeste/c02_Text_GuerraGraBret.png"
        self._string_imagem_TextRetornar = "imgTeste/c02_Text_Retornar.png"
        
        self._string_som_buttonClick = "imgTeste/button_click.ogg"
        #--------------------Fim das constantes------------------------------
        
        #Criando imagens
        img_fundo = Figura(self._string_imagem_fundo)
        img_background = Figura(self._string_imagem_Background,None,
                                self._PosBackGround)
        img_Operacao1 = Figura(self._string_imagem_Operacao1,None,
                               self._PosOperacao1)
        img_Operacao2 = Figura(self._string_imagem_Operacao2,None,
                               self._PosOperacao2)
        img_TextOperacao1 = Figura(self._string_imagem_TextOperacao1,None,
                                   self._PosTextOperacao1)
        img_TextOperacao2 = Figura(self._string_imagem_TextOperacao2,None,
                                   self._PosTextOperacao2)
        img_TextOperacao3 = Figura(self._string_imagem_TextOpercao3,None,
                                   self._PosTextOperacao3)
        img_TextGuerraGraBret = Figura(self._string_imagem_TextGuerraGraBret,None,
                                       self._PosText_GueraGraBret)
        
        botao_TextRetornar = Botao("MenuPrincipal",
                                   self._string_imagem_TextRetornar,
                                   self._string_imagem_TextRetornar,
                                   self._string_som_buttonClick,
                                   self._PosTextRetornar)
        
        botao_PlayOperacao1 = Botao("MenuMissao1",
                                    self._string_imagem_BotaoPlay,
                                    self._string_imagem_BotaoPlay,
                                    self._string_som_buttonClick,
                                    self._PosBotaoPlay1)
        #montando a cena
        self.adicionaFilho(img_fundo)
        self.adicionaFilho(img_background)
        self.adicionaFilho(img_Operacao1)
        self.adicionaFilho(img_Operacao2)
        self.adicionaFilho(img_TextOperacao1)
        self.adicionaFilho(img_TextOperacao2)
        self.adicionaFilho(img_TextOperacao3)
        self.adicionaFilho(img_TextGuerraGraBret)
        self.adicionaFilho(botao_TextRetornar)
        self.adicionaFilho(botao_PlayOperacao1)
#----------------------------------Fim da Classe PainelMenuOperacoes-----------       
        
class PainelMissoes1(Cena):
    """
        É a classe que monta a cena do primeiro Menu de Missoes.
    """
    def __init__(self, audio, entrada, renderizador, string_musica_fundo = None):
        Cena.__init__(self, audio, entrada, renderizador, string_musica_fundo)
       
        #--------------------Constantes----------------------------------------
        self._Posbackground = Ponto(4,41)
        self._PosBotaoMissao1 = Ponto(120,160)
        self._PosBotaoMissao2 = Ponto(300,160)
        self._PosBotaoMissao3 = Ponto(480,160)
        self._PosBotaoMissao4 = Ponto(660,160)
        self._PosBotaoMissao5 = Ponto(120,320)
        self._PosBotaoMissao6 = Ponto(300,320)
        self._PosBotaoMissao7 = Ponto(480,320)
        self._PosBotaoMissao8 = Ponto(660,320)
        self._PosBotaoRetornar = Ponto(660,490)
        
        self._string_imagem_fundo = "imgTeste/sky.png"
        self._string_imagem_background = "imgTeste/c01_Background._missao.png"
        self._string_imagem_BotaoMissao1 = "imgTeste/c02_Missao1.png"
        self._string_imagem_BotaoMissao2 = "imgTeste/c02_Missao2.png"
        self._string_imagem_BotaoMissao3 = "imgTeste/c02_Missao3.png"
        self._string_imagem_BotaoMissao4 = "imgTeste/c02_Missao4.png"
        self._string_imagem_BotaoMissao5 = "imgTeste/c02_Missao5.png"
        self._string_imagem_BotaoMissao6 = "imgTeste/c02_Missao6.png"
        self._string_imagem_BotaoMissao7 = "imgTeste/c02_Missao7.png"
        self._string_imagem_BotaoMissao8 = "imgTeste/c02_Missao8.png"
        self._string_imagem_BotaoRetornar = "imgTeste/c02_BotaoRetornar.png"
        
        self._string_som_buttonClick = "imgTeste/button_click.ogg"
        #---------------Fim das Constantes---------------------------------
        
        #criando imagens
        img_background = Figura(self._string_imagem_background,None,
                                self._Posbackground)
        img_fundo = Figura(self._string_imagem_fundo)
        #criando botoes
        botao_Missao1 = Botao("Play",self._string_imagem_BotaoMissao1,
                              self._string_imagem_BotaoMissao1,
                              self._string_som_buttonClick,
                              self._PosBotaoMissao1)
        botao_Missao2 = Botao("Play", self._string_imagem_BotaoMissao2,
                              self._string_imagem_BotaoMissao2,
                              self._string_som_buttonClick,
                              self._PosBotaoMissao2)
        botao_Missao3 = Botao("Play",self._string_imagem_BotaoMissao3,
                              self._string_imagem_BotaoMissao3,
                              self._string_som_buttonClick,
                              self._PosBotaoMissao3)
        botao_Missao4 = Botao("Play", self._string_imagem_BotaoMissao4,
                              self._string_imagem_BotaoMissao4,
                              self._string_som_buttonClick,
                              self._PosBotaoMissao4)
        botao_Missao5 = Botao("Play",self._string_imagem_BotaoMissao5,
                              self._string_imagem_BotaoMissao5,
                              self._string_som_buttonClick,
                              self._PosBotaoMissao5)
        botao_Missao6 = Botao("Play", self._string_imagem_BotaoMissao6,
                              self._string_imagem_BotaoMissao6,
                              self._string_som_buttonClick,
                              self._PosBotaoMissao6)
        botao_Missao7 = Botao("Play",self._string_imagem_BotaoMissao7,
                              self._string_imagem_BotaoMissao7,
                              self._string_som_buttonClick,
                              self._PosBotaoMissao7)
        botao_Missao8 = Botao("Play", self._string_imagem_BotaoMissao8,
                              self._string_imagem_BotaoMissao8,
                              self._string_som_buttonClick,
                              self._PosBotaoMissao8)
        #montando a cena
        self.adicionaFilho(img_fundo)
        self.adicionaFilho(img_background)
        self.adicionaFilho(botao_Missao1)
        self.adicionaFilho(botao_Missao2)
        self.adicionaFilho(botao_Missao3)
        self.adicionaFilho(botao_Missao4)
        self.adicionaFilho(botao_Missao5)
        self.adicionaFilho(botao_Missao6)
        self.adicionaFilho(botao_Missao7)
        self.adicionaFilho(botao_Missao8)
#-----------------------------Fim da classe PainelMenuMissoes1-----------------
       
class PainelHangar(Cena):
    """
        É a classe que monta a cena do Hangar.
    """
    def __init__(self,audio,entrada,renderizador,string_musica = None):
        Cena.__init__(self,audio,entrada,renderizador,string_musica)
        
        #-----------Constanstes------------------------------------------------
        
        self._Posbackground = Ponto(0,17)
        self._PosTextVidaExtra = Ponto(220,129)
        self._PosHealthPoint   = Ponto(184,181)
        self._PosTextBomba     = Ponto(220,226)
        self._PosMissile       = Ponto(145,245)
        self._PosTextAviaoAmigo = Ponto(263,321)
        self._PosJunkerFriend   = Ponto(132,345)
        self._PosTextAviaoMesserschmidt = Ponto(462,136)
        self._PosAviaoMesserschmidt = Ponto(616,165)
        self._PosLocker1            = Ponto(647,255)
        self._PosLocker2            = Ponto(647,375)
        self._PosTextRetornar       = Ponto(749,553)
        self._PosCoin1              = Ponto(220,160)
        self._PosCoin2              = Ponto(220,257)
        self._PosCoin3              = Ponto(262,372)
        self._PosCoin4              = Ponto(323,473)
        
        self._string_imagem_background = "c01_HangarBackground.png"
        self._string_imagem_TextVidaExtra = "c02_Text_VidaExtra.png"
        self._string_imagem_HealthPoint = "c02_HealthPoint.png"
        self._string_imagem_TextBomba = "c02_Text_Bomba.png"
        self._string_imagem_Missile = "c02_Missile.png"
        self._string_imagem_TextAviaoAmigo = "c02_Text_AviaoAmigo.png"
        self._string_imagem_JunkerFriend = "c02_JunkerFriend.png"
        self._string_imagem_TextAviaoMesserschmidt = "c02_Text_AviaoMesserschmidt.png"
        self._string_imagem_AviaoMesserschmidt = "c02_AviaoMesserschmidt.png"
        self._string_imagem_Locker1 = "c02_Locker.png"
        self._string_imagem_Locker2 = "c02_Locker.png"
        self._string_imagem_TextRetornar = "c02_Text_Retornar.png"
        self._string_imagem_Coin1 ="c02_Coin.png"
        self._string_imagem_Coin2 ="c02_Coin.png"
        self._string_imagem_Coin3 ="c02_Coin.png"
        self._string_imagem_Coin4 ="c02_Coin.png"
        #---------------------------Fim das COnstantes-------------------------
        
        #criando imagens
        img_background    = Figura(self._string_imagem_background,None,
                                self._Posbackground)
        img_TextVidaExtra = Figura(self._string_imagem_TextVidaExtra,None,
                                   self._PosTextVidaExtra)
        img_HealthPoint   = Figura(self._string_imagem_HealthPoint,None,
                                 self._PosHealthPoint)
        img_TextBomba     = Figura(self._string_imagem_TextBomba,None,
                                   self._PosTextBomba)
        img_Missile       = Figura(self._string_imagem_Missile,None,
                                   self._PosMissile)
        img_TextAviaoAmigo = Figura(self._string_imagem_TextAviaoAmigo,None,
                                    self._PosTextAviaoAmigo)
        img_JunkerFriend   = Figura(self._string_imagem_JunkerFriend,None,
                                    self._PosJunkerFriend)
        img_TextAviaoMesserschmidt = Figura(self._string_imagem_TextAviaoMesserschmidt,
                                            None,self._PosTextAviaoMesserschmidt)
        img_AviaoMesserschmidt = Figura(self._string_imagem_AviaoMesserschmidt,
                                        None,self._PosAviaoMesserschmidt)
        img_Locker1            = Figura(self._string_imagem_Locker1,None,
                                        self._PosLocker1)
        img_Locker2            = Figura(self._string_imagem_Locker2,None,
                                        self._string_imagem_Locker2)
        img_TextRetornar       = Figura(self._string_imagem_TextRetornar, None,
                                        self._PosTextRetornar)
        img_Coin1              = Figura(self._string_imagem_Coin1,None,
                                        self._string_imagem_Coin1)
        img_Coin2              = Figura(self._string_imagem_Coin2,None,
                                        self._string_imagem_Coin2)
        img_Coin3              = Figura(self._string_imagem_Coin3,None,
                                        self._string_imagem_Coin3)
        img_Coin4              = Figura(self._string_imagem_Coin4,None,
                                        self._string_imagem_Coin4)
        #montando a cena
        self.adicionaFilho(img_background)
        self.adicionaFilho(img_TextVidaExtra)
        self.adicionaFilho(img_HealthPoint)
        self.adicionaFilho(img_TextBomba)
        self.adicionaFilho(img_Missile)
        self.adicionaFilho(img_TextAviaoAmigo)
        self.adicionaFilho(img_JunkerFriend)
        self.adicionaFilho(img_TextAviaoMesserschmidt)
        self.adicionaFilho(img_AviaoMesserschmidt)
        self.adicionaFilho(img_Locker1)
        self.adicionaFilho(img_Locker2)
        self.adicionaFilho(img_TextRetornar)
        self.adicionaFilho(img_Coin1)
        self.adicionaFilho(img_Coin2)
        self.adicionaFilho(img_Coin3)
        self.adicionaFilho(img_Coin4)
#----------------------Fim da Classe PainelHangar------------------------------

class PainelJogosSalvos(Cena):
    """
        É a classe que monta a cena do Menu de Jogos Salvos.
    """
    def __init__(self,audio,entrada,renderizador,string_musica = None):
        Cena.__init__(self,audio,entrada,renderizador,string_musica)
        
        #--------------------------Constantes----------------------------------
        
        self._Posbackground = Ponto(4,43)
        self._PosTextJogo1  = Ponto(7,50)
        self._PosTextJogo2  = Ponto(7,55)
        self._PosTextJogo3  = Ponto(7,60)
        self._PosTextJogoSalvo = Ponto(7,43)
        self._PosTextRetornar  = Ponto(7,65)
        
        self._string_imagem_background = "c01_Background.png"
        self._string_imagem_TextJogo1  = "c02_Text_Jogo1.png"
        self._string_imagem_TextJogo2  = "c02_Text_Jogo2.png"
        self._string_imagem_TextJogo3  = "c02_Text_Jogo3.png"
        self._string_imagem_TextJogosSalvos = "c02_Text_JogosSalvos.png"
        self._string_imagem_TextRetornar = "c02_Text_Retornar.png"
        
        self._string_som_buttonClick = "imgTeste/button_click.ogg"
        #---------------------------Fim das constantes-------------------------
        
        img_background = Figura(self._string_imagem_background,None,
                                self._Posbackground)
        img_TextJogo1  = Figura(self._string_imagem_TextJogo1,None,
                                self._PosTextJogo1)
        img_TextJogo2  = Figura(self._string_imagem_TextJogo2,None,
                                self._PosTextJogo2)
        img_TextJogo3  = Figura(self._string_imagem_TextJogo3,None,
                                self._PosTextJogo3)
        img_TextJogosSalvo = Figura(self._string_imagem_TextJogosSalvos,None,
                                       self._PosTextJogoSalvo)
        Botao_TextRetornar = Botao("MenuPrincipal",
                                   self._string_imagem_TextRetornar,
                                   self._string_imagem_TextRetornar,
                                   self._string_som_buttonClick,
                                   self._PosTextRetornar)
        #montando a cena
        self.adicionaFilho(img_background)
        self.adicionaFIlho(img_TextJogo1)
        self.adicionaFIlho(img_TextJogo2)
        self.adicionaFIlho(img_TextJogo3)
        self.adicionaFilho(img_TextJogosSalvo)
        self.adicionaFilho(Botao_TextRetornar)
#------------------------------Fim da Classe Jogos Salvo-----------------------


class Jogo():
    """Controla o loop principal do jogo, faz as transições de cena"""
    
    def __init__(self):
        """Ainda é só um esboço"""
        self.larguraTela = 1000
        self.alturaTela  = 800
        self.CorBlit     = (200,200,255)
        
        self.audio = Audio()
        self.renderizador = Renderizador('As da Aviacao',self.larguraTela,
                                         self.alturaTela,self.CorBlit)
        self.entrada = Entrada()
        self.even = Evento()
        self.continuarLoop = True
        self.cenaAtual = None
        
        self.even.escutar("sair", self.irParaCena)
        self.even.escutar("MenuPrincipal",self.MenuPrincipal)
        self.even.escutar("Tutorial",self.Tutorial)
        self.even.escutar("MenuOperacoes",self.MenuOperacoes)
        self.even.escutar("Play", self.gameplay)
        self.even.escutar("MenuMissao1", self.MenuMissao1)
        
        self.MenuPrincipal(True)
        self.gameloop()
         
    
    """Ainda estou pensando, podemos discutir esses métodos"""
    def gameplay(self,chamada):
        fundos = FundoParalaxeInfinito(self.larguraTela, self.alturaTela, "imgTeste/estFundo.png", 
                    Retangulo(Ponto(0,0), Ponto(800, 132)), Ponto(0,0), Ponto(0,0))
        #fundo2 = Figura("imgTeste/movFundo.png")
        #fundo3 = Figura("imgTeste/nuvem.png")
        avi = Jogador("imgTeste/hellcat2.png", Ponto(100, 100), Ponto(28, 10),
                 [8000, 90000, 172],  [8000, 4000, 8000, 100, 0.3, 5400, 1],  
                 [5, 50000, 5000/3, 100], [5000, 150])
        
        self.cenaAtual = Cena(self.audio,self.entrada,self.renderizador)
        self.cenaAtual.adicionaFilho(fundos)
        
        projetilArmaAviaoInimigo = Projetil("imgTeste/BulletEnemies.png",
                                            "imgTeste/MetalHit 1.wav",10,None)
        armaAviaoInimigo = Arma("imgTeste/gun1Light.ogg",
                                projetilArmaAviaoInimigo)
        aviaoInimigo = AviaoInimigo("imgTeste/aviaoInimigo em -x.png",
                                    "imgTeste/aviaoInimigo em x.png",
                                    "imgTeste/airplane.ogg",
                                    armaAviaoInimigo,Ponto(300,100),100,None,None,
                                    None,None,None,None)
        armaAviaoInimigo.setDono = aviaoInimigo
        
        simulador = Simulador(200)
        simulador.adicionaFilho(avi)
        simulador.adicionaFilho(aviaoInimigo)
        self.cenaAtual.adicionaFilho(simulador)
        #self.cenaAtual.adicionaFilho(fundo2)
        #self.cenaAtual.adicionaFilho(fundo3)
        #self.cenaAtual.adicionaFilho(avi)
        
        #self.even.escutar('MenuPause',self.menuPause)
        #self.even.escutar('Hangar',self.hangar)
    
    def MenuPrincipal(self,chamada):
        
        #trocando de transparencias
        self.cenaAtual = PainelMenuPrincipal(self.audio,self.entrada,
                                             self.renderizador)
    def Tutorial(self,chamada):
        
        #trocando de transparencias
        self.cenaAtual = PainelTutorial(self.audio,self.entrada,
                                        self.renderizador)
    def MenuOperacoes(self,chamada):
        
        #trocando de transparencias
        self.cenaAtual = PainelMenuOperacoes(self.audio,self.entrada,
                                         self.renderizador)
    def MenuMissao1(self,chamada):
        
        #trocando de transparencias
        self.cenaAtual = PainelMissoes1(self.audio,self.entrada,
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
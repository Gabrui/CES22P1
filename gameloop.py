# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 19:29:56 2017

@author: Dylan N. Sugimoto
"""

from motor import Audio, Renderizador, Entrada, Evento, Figura, Cena, \
                  Retangulo, Ponto, Botao, Animacao
import time
from cenario import FundoParalaxeInfinito, Camera
from aviao import Jogador
from Simulador import Simulador
from IA import AviaoInimigo,TorreInimiga
from Arma import Arma
from Projetil import Projetil
from Vida import Vida
from database import banco_dados, arquivo

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
        self._string_imagem_Fundo = "imgTeste/sky1_menor.png"
        
        self._string_som_buttonClick = "imgTeste/button_click.ogg"
        #----------------Fim das Constantes do Meneu Principal----------------
        
        #Criando Botoes do Menu
        botaoNovoJogo = Botao("Tutorial","MenuPrincipal",
                              self._string_imagem1_botaoNovoJogo,
                              self._string_imagem2_botaoNovoJogo,
                              self._string_som_buttonClick,
                              Ponto(self._PosXBotaoMenuPrincipal,
                                    self._PosYBotaoJogoNovo))
        botaoJogoSalvo = Botao("MenuJogoSalvo","MenuPrincipal",
                              self._string_imagem1_botaoJogoSalvo,
                              self._string_imagem2_botaoJogoSalvo,
                              self._string_som_buttonClick,
                              Ponto(self._PosXBotaoMenuPrincipal,
                                    self._PosYBotaoJogoSalvo))
        botaoOpcoes = Botao("MenuOpcoes","MenuPrincipal",
                              self._string_imagem1_botaoOpcoes,
                              self._string_imagem2_botaoOpcoes,
                              self._string_som_buttonClick,
                              Ponto(self._PosXBotaoMenuPrincipal,
                                    self._PosYBotaoOpcoes))
        botaoCreditos = Botao("Creditos","MenuPrincipal",
                              self._string_imagem1_botaoCreditos,
                              self._string_imagem2_botaoCreditos,
                              self._string_som_buttonClick,
                              Ponto(self._PosXBotaoMenuPrincipal,
                                    self._PosYBotaoCreditos))
        botaoSair = Botao("sair","MenuPrincipal",
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
        self._string_imagem_Fundo = "imgTeste/sky1_menor.png"
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
        #self.adicionaFilho(img_TextMissao3)
        
        self.even.escutar("M_fclick",self.Proximo)
        
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
        self._PosOperacao1 = Ponto(125,160)
        self._PosOperacao2 = Ponto(355,160)
        self._PosTextOperacao1 = Ponto(130,260)
        self._PosTextOperacao2 = Ponto(365,260)
        self._PosTextOperacao3 = Ponto(597,260)
        self._PosBotaoPlay1 = Ponto(180,310)
        self._PosText_GueraGraBret = Ponto(400,100)
        self._PosTextRetornar = Ponto(660,485)
        
        self._string_imagem_fundo = "imgTeste/sky1_menor.png"
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
        
        botao_TextRetornar = Botao("MenuPrincipal","MenuOperacoes",
                                   self._string_imagem_TextRetornar,
                                   self._string_imagem_TextRetornar,
                                   self._string_som_buttonClick,
                                   self._PosTextRetornar)
        
        botao_PlayOperacao1 = Botao("MenuMissao1","MenuOperacoes",
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
        
        self._string_imagem_fundo = "imgTeste/sky1_menor.png"
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
        botao_Missao1 = Botao("Play","MenuMissoes",
                              self._string_imagem_BotaoMissao1,
                              self._string_imagem_BotaoMissao1,
                              self._string_som_buttonClick,
                              self._PosBotaoMissao1)
        botao_Missao2 = Botao("Play","MenuMissoes",
                              self._string_imagem_BotaoMissao2,
                              self._string_imagem_BotaoMissao2,
                              self._string_som_buttonClick,
                              self._PosBotaoMissao2)
        botao_Missao3 = Botao("Play","MenuMissoes",
                              self._string_imagem_BotaoMissao3,
                              self._string_imagem_BotaoMissao3,
                              self._string_som_buttonClick,
                              self._PosBotaoMissao3)
        botao_Missao4 = Botao("Play","MenuMissoes" ,
                              self._string_imagem_BotaoMissao4,
                              self._string_imagem_BotaoMissao4,
                              self._string_som_buttonClick,
                              self._PosBotaoMissao4)
        botao_Missao5 = Botao("Play","MenuMissoes",
                              self._string_imagem_BotaoMissao5,
                              self._string_imagem_BotaoMissao5,
                              self._string_som_buttonClick,
                              self._PosBotaoMissao5)
        botao_Missao6 = Botao("Play", "MenuMissoes",
                              self._string_imagem_BotaoMissao6,
                              self._string_imagem_BotaoMissao6,
                              self._string_som_buttonClick,
                              self._PosBotaoMissao6)
        botao_Missao7 = Botao("Play","MenuMissoes",
                              self._string_imagem_BotaoMissao7,
                              self._string_imagem_BotaoMissao7,
                              self._string_som_buttonClick,
                              self._PosBotaoMissao7)
        botao_Missao8 = Botao("Play", "MenuMissoes",
                              self._string_imagem_BotaoMissao8,
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
        self._PosHealthPoint   = Ponto(150,151)
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
        
        self._string_imagem_background = "imgTeste/c01_HangarBackground.png"
        self._string_imagem_TextVidaExtra = "imgTeste/c02_Text_VidaExtra.png"
        self._string_imagem_HealthPoint = "imgTeste/c02_HealthPoint.png"
        self._string_imagem_TextBomba = "imgTeste/c02_Text_Bomba.png"
        self._string_imagem_Missile = "imgTeste/c02_Missile.png"
        self._string_imagem_TextAviaoAmigo = "imgTeste/c02_Text_AviaoAmigo.png"
        self._string_imagem_JunkerFriend = "imgTeste/c02_JunkerFriend.png"
        self._string_imagem_TextAviaoMesserschmidt = "imgTeste/c02_Text_AviaoMesserschmidt.png"
        self._string_imagem_AviaoMesserschmidt = "imgTeste/c02_AviaoMesserschmidt.png"
        self._string_imagem_Locker1 = "imgTeste/c02_Locker.png"
        self._string_imagem_Locker2 = "imgTeste/c02_Locker.png"
        self._string_imagem_TextRetornar = "imgTeste/c02_Text_Retornar.png"
        self._string_imagem_Coin1 ="imgTeste/c02_Coin.png"
        self._string_imagem_Coin2 ="imgTeste/c02_Coin.png"
        self._string_imagem_Coin3 ="imgTeste/c02_Coin.png"
        self._string_imagem_Coin4 ="imgTeste/c02_Coin.png"
        
        self._string_som_buttonClick = "imgTeste/button_click.ogg"
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
                                        self._PosLocker2)
        img_Coin1              = Figura(self._string_imagem_Coin1,None,
                                        self._PosCoin1)
        img_Coin2              = Figura(self._string_imagem_Coin2,None,
                                        self._PosCoin2)
        img_Coin3              = Figura(self._string_imagem_Coin3,None,
                                        self._PosCoin3)
        img_Coin4              = Figura(self._string_imagem_Coin4,None,
                                        self._PosCoin4)
        botao_TextRetornar       = Botao("MenuOperacoes","MenuHangar",
                                       self._string_imagem_TextRetornar,
                                       self._string_imagem_TextRetornar,
                                       self._string_som_buttonClick,
                                        self._PosTextRetornar)
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
        self.adicionaFilho(botao_TextRetornar)
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
        self._PosTextJogo1  = Ponto(10,50)
        self._PosTextJogo2  = Ponto(10,55)
        self._PosTextJogo3  = Ponto(10,60)
        self._PosTextJogoSalvo = Ponto(10,80)
        self._PosTextRetornar  = Ponto(10,90)
        
        self._string_imagem_background = "imgTeste/c01_Background.png"
        self._string_imagem_TextJogo1  = "imgTeste/c02_Text_Jogo1.png"
        self._string_imagem_TextJogo2  = "imgTeste/c02_Text_Jogo2.png"
        self._string_imagem_TextJogo3  = "imgTeste/c02_Text_Jogo3.png"
        self._string_imagem_TextJogosSalvos = "imgTeste/c02_Text_JogosSalvos2.png"
        self._string_imagem_TextRetornar = "imgTeste/c02_Text_Retornar.png"
        
        self._string_som_buttonClick = "imgTeste/button_click.ogg"
        #---------------------------Fim das constantes-------------------------
        
        img_background = Figura(self._string_imagem_background,None,
                                self._Posbackground)
        img_TextJogo1  = Botao("ler","teste",self._string_imagem_TextJogo1,
                               self._string_imagem_TextJogo1,
                               self._string_som_buttonClick,
                               self._PosTextJogo1)
        img_TextJogo2  = Figura(self._string_imagem_TextJogo2,None,
                                self._PosTextJogo2)
        img_TextJogo3  = Figura(self._string_imagem_TextJogo3,None,
                                self._PosTextJogo3)
        img_TextJogosSalvo = Figura(self._string_imagem_TextJogosSalvos,None,
                                       self._PosTextJogoSalvo)
        Botao_TextRetornar = Botao("MenuPrincipal","MenuJogoSalvo",
                                   self._string_imagem_TextRetornar,
                                   self._string_imagem_TextRetornar,
                                   self._string_som_buttonClick,
                                   self._PosTextRetornar)
        #montando a cena
        self.adicionaFilho(img_background)
        self.adicionaFilho(img_TextJogo1)
        self.adicionaFilho(img_TextJogo2)
        self.adicionaFilho(img_TextJogo3)
        self.adicionaFilho(img_TextJogosSalvo)
        self.adicionaFilho(Botao_TextRetornar)
    
        self.even.escutar("ler",self.lerArquivo)
    
    def lerArquivo(self, nome):
        """
            Ler arquivo.
        """
        ler_arquivo = arquivo()
        dadosSalvos = ler_arquivo.ler(nome)
        banco_dados.setCarteira(dadosSalvos[1])
        banco_dados.setProgresso(dadosSalvos[0])
        self.even.lancar("MenuPrincipal","MenuJogoSalvo")
        
#------------------------------Fim da Classe Jogos Salvo-----------------------

class PainelMenuPause(Cena):
    
    def __init__(self,audio,entrada,renderizador,string_musica_fundo=None):
        Cena.__init__(self,audio,entrada,renderizador,string_musica_fundo)
        
        #-------------Constantes-----------------------------------------------
        
        self._PosbackGround = Ponto(190,41)
        self._PosTextResumir = Ponto(400,200)
        self._PosTextJogosSalvos = Ponto(380,300)
        self._PosTextAbortar = Ponto(400,400)
        
        self._string_imagem_background = "imgTeste/c01_Background_pause.png"
        self._string_imagem_textResumir = "imgTeste/c02_Text_Resumir.png"
        self._string_imagem_textJogosSalvos = "imgTeste/c02_Text_JogosSalvos.png"
        self._string_imagem_textAbortar = "imgTeste/c02_Text_Abortar.png"
        self._string_som_buttonClick = "imgTeste/button_click.ogg"
        #--------------Fim das constantes--------------------------------------
        
        #CRIAR imagens
        img_background = Figura(self._string_imagem_background,None,
                                self._PosbackGround)
        #Criar botoes
        Botao_resumir = Botao("Play","MenuPause",self._string_imagem_textResumir,
                              self._string_imagem_textResumir,
                              self._string_som_buttonClick,
                              self._PosTextResumir)
        Botao_JogosSalvos = Botao("MenuJogoSalvo","MenuPause",
                                  self._string_imagem_textJogosSalvos,
                                  self._string_imagem_textJogosSalvos,
                                  self._string_som_buttonClick,
                                  self._PosTextJogosSalvos)
        Botao_Abortar = Botao("sair","MenuPause",self._string_imagem_textAbortar,
                              self._string_imagem_textAbortar,
                              self._string_som_buttonClick,
                              self._PosTextAbortar)
        #montar cena
        self.adicionaFilho(img_background)
        self.adicionaFilho(Botao_resumir)
        self.adicionaFilho(Botao_JogosSalvos)
        self.adicionaFilho(Botao_Abortar)
    
#----------------Fim da classe PainelMenuPause---------------------------------    

class PainelGameOver(Cena):
    
    def __init__(self,audio,entrada,renderizador,string_musica_fundo=None):
        Cena.__init__(self,audio,entrada,renderizador,string_musica_fundo)
        
        #-------------Constantes-----------------------------------------------
        #posicoes
        self._PosbackGround = Ponto(190,41)
        self._PosTextResumir = Ponto(330,200)
        self._PosTextGameOver = Ponto(360,60)
        self._PosTextSair = Ponto(330,400)
        #imagens
        self._string_imagem_background = "imgTeste/c01_Background_vazio.png"
        self._string_imagem_continuar = "imgTeste/c01_botao_continuar.png"
        self._string_imagem_continuar2 = "imgTeste/c01_botao_continuar2.png"
        self._string_imagem_textSair = "imgTeste/c04_Text_Sair.png"
        self._string_imagem_textSair2 = "imgTeste/c03_Text_Sair.png"
        self._string_imagem_textGameOVer = "imgTeste/text_Game_over.png"
        #sons
        self._string_som_buttonClick = "imgTeste/button_click.ogg"
        #--------------Fim das constantes--------------------------------------
        
        #CRIAR imagens
        img_background = Figura(self._string_imagem_background,
                                pos = self._PosbackGround)
        img_Text_gameOver = Figura(self._string_imagem_textGameOVer,
                                   pos = self._PosTextGameOver)
        #Criar botoes
        Botao_continuar = Botao("Play","MenuGameOver",self._string_imagem_continuar,
                              self._string_imagem_continuar2,
                              self._string_som_buttonClick,
                              self._PosTextResumir)
        Botao_sair = Botao("sair","MenuGameOver",self._string_imagem_textSair,
                              self._string_imagem_textSair2,
                              self._string_som_buttonClick,
                              self._PosTextSair)
        #montar cena
        self.adicionaFilho(img_background)
        self.adicionaFilho(img_Text_gameOver)
        self.adicionaFilho(Botao_continuar)
        self.adicionaFilho(Botao_sair)
#----------------Fim da Classe PainelGameOver----------------------------------------



class Painelgameplay(Cena):
    
    def __init__(self,audio,entrada,renderizador,larguraTela,alturaTela,
                 string_musica_fundo=None):
        Cena.__init__(self,audio,entrada,renderizador,string_musica_fundo)
        
        fundo0 = FundoParalaxeInfinito(larguraTela,alturaTela, 
                         "imgTeste/estFundo.png",Ponto(-1, -0.4), Ponto(0, 80))
        fundo1 = FundoParalaxeInfinito(larguraTela, alturaTela, 
                         "imgTeste/movFundo.png", Ponto(0,0), Ponto(0,0))
        fundo3 = Figura("imgTeste/nuvem.png")
        
        #criando jogador
        Barra_Vida_Jogador = Vida(1000, Ponto(larguraTela-340,0),Ponto(10,10),
                                  "imgTeste/barra_vida_interna.png",
                                  "imgTeste/barra_vida_externa.png")
        projetilJogador = Projetil("imgTeste/BulletEnemies.png","imgTeste/MetalHit1.ogg",
                                   1,Ponto(0,0))
        armaJogador = Arma("imgTeste/M4A1_Single.ogg",projetilJogador)
        avi = Jogador("imgTeste/hellcat2.png", "imgTeste/hellcat-2.png", 
                     Ponto(100, 100), Ponto(28, 10),
                     [[8000, 90000, 172],  [8000, 4000, 8000, 100, 0.3, 5400, 1],  
                     [5, 37000, 5000/3, 100], [5000, 150]], arma = armaJogador,
                     string_som_fallShell="imgTeste/Shells_falls.ogg",
                     PV = Barra_Vida_Jogador)
        armaJogador.setDono(avi)
        #Criando aviao inimigo
        Barra_Vida_AviaoInimigo = Vida(100,Ponto(300,100),Ponto(2,2),
                                       "imgTeste/barra_vida_interna_IA.png",
                                       "imgTeste/barra_vida_externa_IA.png")
        projetilArmaAviaoInimigo = Projetil("imgTeste/BulletEnemies.png",
                                                "imgTeste/MetalHit1.ogg",100,
                                                Ponto(0,0))
        armaAviaoInimigo = Arma("imgTeste/MP5_SMG_auto.ogg",
                                    projetilArmaAviaoInimigo)
        aviaoInimigo = AviaoInimigo("imgTeste/aviaoInimigo em x.png",
                                        "imgTeste/aviaoInimigo em -y.png",
                                        "imgTeste/airplane_b25-1.ogg",
                                        armaAviaoInimigo,
                                        Ponto(300,100),
                                        Barra_Vida_AviaoInimigo,
                                        "imgTeste/Explosion_6.ogg",
                                        "imgTeste/Shells_falls.ogg",
                                        None,None,
                                        None,None)
        armaAviaoInimigo.setDono(aviaoInimigo)
        #Criando outro aviao inimigo
        Barra_Vida_AviaoInimigo2 = Vida(100,Ponto(300,50),Ponto(2,2),
                                        "imgTeste/barra_vida_interna_IA.png",
                                        "imgTeste/barra_vida_externa_IA.png")
        projetilArmaAviaoInimigo2 = Projetil("imgTeste/BulletEnemies.png",
                                                "imgTeste/MetalHit1.ogg",100,
                                                Ponto(0,0))
        armaAviaoInimigo2 = Arma("imgTeste/MP5_SMG_auto.ogg",
                                    projetilArmaAviaoInimigo2)
        aviaoInimigo2 = AviaoInimigo("imgTeste/aviaoInimigo em x.png",
                                        "imgTeste/aviaoInimigo em -y.png",
                                        "imgTeste/airplane_b25-1.ogg",
                                        armaAviaoInimigo2,
                                        Ponto(300,50),
                                        Barra_Vida_AviaoInimigo2,
                                        "imgTeste/Explosion_6.ogg",
                                        "imgTeste/Shells_falls.ogg",
                                        None,None,
                                        None,None)
        armaAviaoInimigo2.setDono(aviaoInimigo2)
        #Criando Torre Inimiga
        Barra_Vida_TorreInimiga = Vida(1000,Ponto(800,580),Ponto(2,2),
                                       "imgTeste/barra_vida_interna_IA.png",
                                       "imgTeste/barra_vida_externa_IA.png")
        projetilTorreInimiga = Projetil("imgTeste/Bullet_3.png",
                                        "imgTeste/MetalHit1.ogg",
                                        10,Ponto(0,0))
        armaTorreInimiga = Arma("imgTeste/Anti_Aircraft_Gun.ogg",
                                projetilTorreInimiga)
        torreInimiga = TorreInimiga("imgTeste/Cano_Turret_simetrica.png",
                                    "imgTeste/Shells_falls.ogg",
                                    armaTorreInimiga,
                                    Barra_Vida_TorreInimiga,Ponto(800,580),
                                    None,None,
                                    None,None)
        armaTorreInimiga.setDono(torreInimiga)
        baseTorreInimiga = Figura("imgTeste/Base_Turret.png", 
                                  pos = Ponto(800, 580), 
                                  centro = Ponto(34, 5))
        
        #criar Hangar
        hangar = Figura("imgTeste/airport.png", pos = Ponto(1800,580))
        
        simulador = Simulador(alturaTela-50,larguraTela)
        simulador.adicionaFilho(avi)
        camera = Camera(larguraTela, alturaTela, avi, 0)
        camera.adicionaFilho(fundo0)
        camera.adicionaFilho(fundo1)
        camera.adicionaFilho(fundo3)
        camera.adicionaFilho(baseTorreInimiga)
        camera.adicionaFilho(simulador)
        simulador.adicionaFilho(aviaoInimigo)
        simulador.adicionaFilho(torreInimiga)
        simulador.adicionaFilho(aviaoInimigo2)
        simulador.adicionaFilho(Barra_Vida_AviaoInimigo)
        simulador.adicionaFilho(Barra_Vida_AviaoInimigo2)
        simulador.adicionaFilho(Barra_Vida_TorreInimiga)
        simulador.adicionaHangar(hangar)
        self.adicionaFilho(Barra_Vida_Jogador)
        self.adicionaFilho(camera)
        
        banco_dados.setObjetivo("AviaoInimigo",1)
        
        self.even.escutar("K_p",self.pausar)
        
    def atualiza(self,dt):
        """
            atualiza. E verifica se o objetivo foi completado
        """
        super().atualiza(dt)
        if banco_dados.verificarObjetivo():
            
            texto_dialogo = Figura("imgTeste/caixa_dialogo_objetivo_concluido.png")
            self.adicionaFilho(texto_dialogo)
            
        
        
    def pausar(self,chamada):
        self.even.lancar("MenuPause","gameplay")
        
        
    def ativarEscuta(self):
        self.even.escutar("K_p",self.pausar)
        for filho in self.filhos:
            filho.ativarEscuta()
#---------------------------------Fim da classe Painelgameplay-----------------
class Jogo():
    """Controla o loop principal do jogo, faz as transições de cena"""
    
    def __init__(self):
        """
            larguraTela:   é a largura da Tela.
            alturaTela:    é a altura da Tela.
            CorBlit:       é a cor do fundo da Tela
            audio:         objeto audio da cena
            renderizador:  objeto renderizador da cena
            entrada:       objeto entrada que verifica entradas
            continuarloop: variavel booleana que mantém o loop do jogo
            cenaAtual:     é a cena que está sendo exibida na Tela.
            cenaAnterior:  é a cena anterior do gameplay.
        """
        self.larguraTela = 1000
        self.alturaTela  = 700
        self.CorBlit     = (200,200,255)
        
        self.renderizador = Renderizador('As da Aviacao',self.larguraTela,
                                         self.alturaTela,self.CorBlit)
        self.audio = Audio()
        self.entrada = Entrada()
        self.even = Evento()
        self.continuarLoop = True
        self.cenaAtual = None
        self.cenaAnterior = None
        
        self.limparEventos()
        
        self.MenuPrincipal(True)
        self.gameloop()
         
    
    """Ainda estou pensando, podemos discutir esses métodos"""
    def gameplay(self,chamada):
        self.audio.pararMusicaFundo()
        self.limparEventos()
   
        if chamada == "MenuPause":
           self.cenaAtual = self.cenaAnterior
           self.cenaAtual.ativarEscuta()
           
        else:
            
            self.cenaAtual = Painelgameplay(self.audio,self.entrada,
                                            self.renderizador,self.larguraTela,
                                            self.alturaTela,
                                            "imgTeste/NowOrNever.ogg")
            self.cenaAnterior = self.cenaAtual
    
    
    def MenuPrincipal(self,chamada):
        self.limparEventos()
        #trocando de transparencias
        self.cenaAtual = PainelMenuPrincipal(self.audio,self.entrada,
                                             self.renderizador,
                                             "imgTeste/World_War_II_Soundtrack.ogg")
    
    
    def Tutorial(self,chamada):
        self.limparEventos()
        #trocando de transparencias
        self.cenaAtual = PainelTutorial(self.audio,self.entrada,
                                        self.renderizador)
    
    
    def MenuOperacoes(self,chamada):
        self.limparEventos()
        #trocando de transparencias
        self.cenaAtual = PainelMenuOperacoes(self.audio,self.entrada,
                                         self.renderizador)
    
    
    def MenuMissao1(self,chamada):
        self.limparEventos()
        #trocando de transparencias
        self.cenaAtual = PainelMissoes1(self.audio,self.entrada,
                                        self.renderizador)
    def MenuPause(self,chamada):
        #limpando eventos
        self.limparEventos()
        #trocando de  transparencias
        self.cenaAtual = PainelMenuPause(self.audio,self.entrada,
                                         self.renderizador)
    def MenuJogosSalvos(self,chamada):
        
        #limpando eventos
        self.limparEventos()
        #trocando de  transparencias
        self.cenaAtual = PainelJogosSalvos(self.audio,self.entrada,
                                         self.renderizador)
    def MenuHangar(self, chamada):
        
        #limpando eventos
        self.limparEventos()
        #trocando de  transparencias
        self.cenaAtual = PainelHangar(self.audio,self.entrada,
                                         self.renderizador)
    def MenuGameOver(self, chamada):
        
        #limpando eventos
        self.limparEventos()
        #trocando de  transparencias
        self.cenaAtual = PainelGameOver(self.audio,self.entrada,
                                         self.renderizador)
    
    def limparEventos(self):
        self.even.pararDeEscutarTudo()
        self.even.escutar("sair", self.sair)
        self.even.escutar("MenuPrincipal",self.MenuPrincipal)
        self.even.escutar("Tutorial",self.Tutorial)
        self.even.escutar("MenuOperacoes",self.MenuOperacoes)
        self.even.escutar("Play", self.gameplay)
        self.even.escutar("MenuMissao1", self.MenuMissao1)
        self.even.escutar("MenuPause",self.MenuPause)
        self.even.escutar("MenuJogoSalvo",self.MenuJogosSalvos)
        self.even.escutar("Hangar",self.MenuHangar)
        self.even.escutar("GameOver",self.MenuGameOver)
        self.audio.escutas()
        self.renderizador.escutas()
    
    
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
           # dt /= 3
            self.cenaAtual.atualiza(dt)

            
 
            
    def carregaCenas(self, listaCenas):
        pass
    
    
    def rodarCena(self, cena):
        pass
    
    
    def sair(self, cena):
        
        salva_dados = arquivo()
        salva_dados.salvar("teste",banco_dados)
        self.entrada.sair()
    
    
    
Jogo()
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 19:29:56 2017

@author: Dylan N. Sugimoto
"""

from motor import Audio, Renderizador, Entrada, Evento, Figura, Cena, \
                  Retangulo, Ponto, Botao, Animacao,item_aviao
import time
from cenario import FundoParalaxeInfinito, Camera
from aviao import Jogador
from Simulador import Simulador
from IA import AviaoInimigo,TorreInimiga
from Arma import Arma
from Projetil import Projetil
from Vida import Vida,Velocimetro
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
        botaoNovoJogo = Botao("MenuNovoJogo","MenuPrincipal",
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
        botaoCreditos = Botao("MenuCreditos","MenuPrincipal",
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
        self._PosXPonteiroFuel        = 56
        self._PosYPonteiroFuel        = 24
        self._PosXCoin                = 124
        self._PosYCoin                = 15
        self._PosXFuel                = 17
        self._PosYFuel                = 7
        self._PosXHealthPoints        = 228
        self._PosYHealthPoints        = 15
        self._PosXHP1                 = 494
        self._PosYHP1                 = 15
        self._PosXTextCoin            = 170
        self._PosYTextCoin            = 22
        self._PosXTextHealthPoints    = 275
        self._PosYTextHealthPoints    = 22
        self._PosXTextMissao3         = 328
        self._PosYTextMissao3         = 22
        self._PosXBotaoPause          = 789
        self._PosYBotaoPause          = 8
        self._PosXBotaoSom            = 838
        self._PosYBotaoSom            = 6
        self._PosXBotaoConfirmar      = 763
        self._PosYBotaoConfirmar      = 469
        self._PosXBalao               = 252
        self._PosYBalao               = 312
        self._PosXAviao1              = 255
        self._PosYAviao1              = 278
        self._PosXBala1               = 343
        self._PosYBala1               = 298
        self._PosXAviao2              = 451
        self._PosYAviao2              = 103
        self._PosXBala2               = 383
        self._PosYBala2               = 152
        self._PosXAviao3              = 680
        self._PosYAviao3              = 209
        self._PosXBala3               = 622
        self._PosYBala3               = 242
        self._PosXAviao4              = 755
        self._PosYAviao4              = 364
        self._PosXBala4               = 716
        self._PosYBala4               = 385
        
        
        
        self._string_imagem_PonteiroFuel = "imgTeste/c02_PonteiroFuel.png"
        self._string_imagem_Coin = "imgTeste/c02_Coin.png"
        self._string_imagem_Fuel = "imgTeste/c02_Fuel.png"
        self._string_imagem_HealthPoint = "imgTeste/c02_HealthPoints.png"
        self._string_imagem_HP = "imgTeste/c02_HP5.png"
        self._string_imagem_TextCoin = "imgTeste/c02_Text_Coin.png"
        self._string_imagem_TextHealth = "imgTeste/c02_Text_HealthPoints.png"
        self._string_imagem_TextMissao3 ="imgTeste/c02_Text_Missao3.png" 
        self._string_imagem_Fundo = "imgTeste/sky1_menor.png"
        self._string_imagem_BotaoSom = "imgTeste/c02_BotaoSom.png"
        self._string_imagem_BotaoPause = "imgTeste/c02_BotaoPause.png"
        self._string_imagem_BotaoConfirmar = "imgTeste/c02_BotaoConfirmar.png"
        self._string_imagem_Balao = "imgTeste/c02_Balao1.png"
        self._string_imagem_Aviao1 = "imgTeste/c02_Aviao1.png"
        self._string_imagem_Bala1 = "imgTeste/c02_Bala1.png"
        self._string_imagem_Aviao2 = "imgTeste/c02_Aviao2.png"
        self._string_imagem_Bala2 = "imgTeste/c02_Bala2.png"
        self._string_imagem_Aviao3 = "imgTeste/c02_Aviao3.png"
        self._string_imagem_Bala3 = "imgTeste/c02_Bala3.png"
        self._string_imagem_Aviao4 = "imgTeste/c02_Aviao4.png"
        self._string_imagem_Bala4 = "imgTeste/c02_Bala4.png"
        self._string_som_buttonClick = "imgTeste/button_click.ogg"
        
        #--------------------------Fim das Constates---------------------------
       
        #------------------Criando as imagens do tutorial----------------------
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
        img_BotaoSom = Figura(self._string_imagem_BotaoSom,None,
                              Ponto(self._PosXBotaoSom,
                                    self._PosYBotaoSom))
        img_BotaoPause = Figura(self._string_imagem_BotaoPause,None,
                              Ponto(self._PosXBotaoPause,
                                    self._PosYBotaoPause))
        img_Aviao1 = Figura(self._string_imagem_Aviao1,None,
                            Ponto(self._PosXAviao1,
                                  self._PosYAviao1))
        img_Bala1 = Figura(self._string_imagem_Bala1,None,
                            Ponto(self._PosXBala1,
                                  self._PosYBala1))
        img_Aviao2 = Figura(self._string_imagem_Aviao2,None,
                            Ponto(self._PosXAviao2,
                                  self._PosYAviao2))
        img_Bala2 = Figura(self._string_imagem_Bala2,None,
                            Ponto(self._PosXBala2,
                                  self._PosYBala2))
        img_Aviao3 = Figura(self._string_imagem_Aviao3,None,
                            Ponto(self._PosXAviao3,
                                  self._PosYAviao3))
        img_Bala3 = Figura(self._string_imagem_Bala3,None,
                            Ponto(self._PosXBala3,
                                  self._PosYBala3))
        img_Aviao4 = Figura(self._string_imagem_Aviao4,None,
                            Ponto(self._PosXAviao4,
                                  self._PosYAviao4))
        img_Bala4 = Figura(self._string_imagem_Bala4,None,
                            Ponto(self._PosXBala4,
                                  self._PosYBala4))
        self.img_Balao = Figura(self._string_imagem_Balao,None,
                           Ponto(self._PosXBalao,
                           self._PosYBalao))
        
        img_Fundo = Figura(self._string_imagem_Fundo)
        
        #----------------Criando os botoes do Menu Tutorial--------------------
        botao_Confirmar = Botao("MenuOperacoes","Tutorial",
                                   self._string_imagem_BotaoConfirmar,
                                   self._string_imagem_BotaoConfirmar,
                                   self._string_som_buttonClick,
                                   Ponto(self._PosXBotaoConfirmar,
                                         self._PosYBotaoConfirmar))
        
        #montando o tutorial
        self.adicionaFilho(img_Fundo)
        self.adicionaFilho(img_PonteiroFuel)
        self.adicionaFilho(img_Coin)
        self.adicionaFilho(img_Fuel)
        self.adicionaFilho(img_HealthPoints)
        self.adicionaFilho(img_HP1)
        self.adicionaFilho(img_TextCoin)
        self.adicionaFilho(img_TextHealthPoint)
        self.adicionaFilho(img_BotaoSom)
        self.adicionaFilho(img_BotaoPause)
        self.adicionaFilho(img_TextMissao3)
        self.adicionaFilho(img_Aviao1)
        self.adicionaFilho(img_Bala1)
        self.adicionaFilho(img_Aviao2)
        self.adicionaFilho(img_Bala2)
        self.adicionaFilho(img_Aviao3)
        self.adicionaFilho(img_Bala3)
        self.adicionaFilho(img_Aviao4)
        self.adicionaFilho(img_Bala4)
        self.adicionaFilho(self.img_Balao)
        self.adicionaFilho(botao_Confirmar)
        
        self.even.escutar("M_fclick",self.Proximo)
        self.tuplasBaloes = [("imgTeste/c02_Balao2.png",421,168),
                    ("imgTeste/c02_Balao3.png",1,83),
                    ("imgTeste/c02_Balao4.png",140,61),
                    ("imgTeste/c02_Balao5.png",549,65),
                    ("imgTeste/c02_Balao6.png",670,72)]
        self.balao = 0
        
    #criar os baloes que se alternam na tela
        
    '''for (diretorio,posX,posY) in tuplasBaloes:
            self._string_imagem_Balao = diretorio
            self._PosXBalao = posX
            self._PosYBalao = posY'''
    def Proximo(self, chamada): 
        if self.balao < 5:
            self.img_Balao.setString(self.tuplasBaloes[self.balao][0])
            self.img_Balao.pos.setXY(self.tuplasBaloes[self.balao][1],
                                     self.tuplasBaloes[self.balao][2]
                                     )
            self.balao += 1
    

#------------------------------------Fim da Classe PainelTutorial--------------

class PainelMenuOperacoes(Cena):
    """
        É a classe que monta a cena do menu de operacoes.
    """
    def __init__(self, audio, entrada, renderizador, string_musica_fundo = None):
        Cena.__init__(self, audio, entrada, renderizador, string_musica_fundo)
        
        #-----------------Constantes do Menu Principal------------------------
        
        self._PosBackgroundOperacoes = Ponto(0,33)
        self._PosOperacao1 = Ponto(122,148)
        self._PosOperacao2 = Ponto(354,148)
        self._PosOperacao3 = Ponto(586,148)
        self._PosCadeadoOperacao2 = Ponto(417,152)
        self._PosCadeadoOperacao3 = Ponto(648,152)
        self._PosTextOperacao1 = Ponto(130,260)
        self._PosTextOperacao2 = Ponto(365,260)
        self._PosTextOperacao3 = Ponto(584,260)
        self._PosBotaoPlay1 = Ponto(125,302)
        self._PosText_GueraGraBret = Ponto(179,306)
        self._PosTextRetornar = Ponto(660,485)
        self._PosTextHangar = Ponto(101,486)
        
        self._string_imagem_fundo = "imgTeste/sky1_menor.png"
        self._string_imagem_BackgroundOperacoes = "imgTeste/c01_Background.png"
        self._string_imagem_Operacao1 = "imgTeste/c02_Operacao1.png"
        self._string_imagem_Operacao2 = "imgTeste/c02_Operacao2.png"
        self._string_imagem_CadeadoOperacao2 = "imgTeste/Cadeado.png"
        self._string_imagem_CadeadoOperacao3 = "imgTeste/Cadeado.png"
        self._string_imagem_TextOperacao1 = "imgTeste/c02_Text_Operacao1.png"
        self._string_imagem_TextOperacao2 = "imgTeste/c02_Text_Operacao2.png"
        self._string_imagem_TextOperacao3 = "imgTeste/c02_Text_Operacao3.png"
        self._string_imagem_BotaoPlay = "imgTeste/c02_BotaoPlay.png"
        self._string_imagem_TextGuerraGraBret = "imgTeste/c02_Text_GuerraGraBret.png"
        self._string_imagem_TextRetornar = "imgTeste/c02_BotaoRetornar.png"
        self._string_imagem_TextHangar = "imgTeste/c02_Text_Hangar.png"
        
        self._string_som_buttonClick = "imgTeste/button_click.ogg"
        #--------------------Fim das constantes------------------------------
        
        #Criando imagens
        img_fundo = Figura(self._string_imagem_fundo)
        img_BackgroundOperacoes = Figura(self._string_imagem_BackgroundOperacoes,None,
                                self._PosBackgroundOperacoes)
        img_Operacao1 = Figura(self._string_imagem_Operacao1,None,
                               self._PosOperacao1)
        img_Operacao2 = Figura(self._string_imagem_Operacao2,None,
                               self._PosOperacao2)
        img_Operacao3 = Figura(self._string_imagem_Operacao2,None,
                               self._PosOperacao3)
        img_CadeadoOperacao2 = Figura(self._string_imagem_CadeadoOperacao2,
                                      None, self._PosCadeadoOperacao2)
        img_CadeadoOperacao3 = Figura(self._string_imagem_CadeadoOperacao3,
                                      None, self._PosCadeadoOperacao3)
        img_TextOperacao1 = Figura(self._string_imagem_TextOperacao1,None,
                                   self._PosTextOperacao1)
        img_TextOperacao2 = Figura(self._string_imagem_TextOperacao2,None,
                                   self._PosTextOperacao2)
        img_TextOperacao3 = Figura(self._string_imagem_TextOperacao3,None,
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
        botao_TextHangar = Botao("Hangar","MenuOperacoes",
                                 self._string_imagem_TextHangar,
                                 self._string_imagem_TextHangar,
                                 self._string_som_buttonClick,
                                 self._PosTextHangar)
        #montando a cena
        self.adicionaFilho(img_fundo)
        self.adicionaFilho(img_BackgroundOperacoes)
        self.adicionaFilho(img_Operacao1)
        self.adicionaFilho(img_Operacao2)
        self.adicionaFilho(img_Operacao3)
        self.adicionaFilho(img_TextOperacao1)
        self.adicionaFilho(img_TextOperacao2)
        self.adicionaFilho(img_TextOperacao3)
        self.adicionaFilho(img_TextGuerraGraBret)
        self.adicionaFilho(img_CadeadoOperacao2)
        self.adicionaFilho(img_CadeadoOperacao3)
        self.adicionaFilho(botao_TextRetornar)
        self.adicionaFilho(botao_PlayOperacao1)
        self.adicionaFilho(botao_TextHangar)
        
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
        self._PosTextRetornar = Ponto(660,498)
        
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
        self._string_imagem_TextRetornar = "imgTeste/c02_BotaoRetornar.png"
        
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
        botao_TextRetornar = Botao("MenuOperacoes","Hangar",
                                   self._string_imagem_TextRetornar,
                                   self._string_imagem_TextRetornar,
                                   self._string_som_buttonClick,
                                   self._PosTextRetornar) 
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
        self.adicionaFilho(botao_TextRetornar)
        
#-----------------------------Fim da classe PainelMenuMissoes1-----------------
       
class PainelHangar(Cena):
    """
        É a classe que monta a cena do Hangar.
    """
    def __init__(self,audio,entrada,renderizador,string_musica = None):
        Cena.__init__(self,audio,entrada,renderizador,string_musica)
        
        #-----------Constanstes------------------------------------------------
        
        self._PosBackgroundHangar           = Ponto(0,7)
        self._PosTextVidaExtra              = Ponto(220,129)
        self._PosHealthPoint                = Ponto(148,148)
        self._PosTextBomba                  = Ponto(220,226)
        self._PosMissile                    = Ponto(145,245)
        self._PosTextAviaoAmigo             = Ponto(263,321)
        self._PosJunkerFriend               = Ponto(132,345)
        self._PosTextAviaoMesserschmidt     = Ponto(462,136)
        self._PosAviaoMesserschmidt         = Ponto(616,165)
        self._PosLocker1                    = Ponto(647,255)
        self._PosLocker2                    = Ponto(647,375)
        self._PosTextRetornar               = Ponto(664,500)
        self._PosCoin1                      = Ponto(220,160)
        self._PosCoin2                      = Ponto(220,257)
        self._PosCoin3                      = Ponto(262,372)
        self._PosCoin4                      = Ponto(323,473)
        self._PosPatente                    = Ponto(737,56)
        self._PosText0XP                    = Ponto(167,479)
        self._PosText0GP                    = Ponto(366,479)
        self._PosText20VidaExtra            = Ponto(263,166)
        self._PosText20Bomba                = Ponto(263,263)
        self._PosText210JunkerFriend        = Ponto(303,378)           
        
        self._string_imagem_BackgroundHangar = "imgTeste/c01_BackgroundHangar.png"
        self._string_imagem_TextVidaExtra = "imgTeste/c02_Text_VidaExtra.png"
        self._string_imagem_HealthPoint = "imgTeste/c02_HealthPoint.png"
        self._string_imagem_TextBomba = "imgTeste/c02_Text_Bomba.png"
        self._string_imagem_Missile = "imgTeste/c02_Missile.png"
        self._string_imagem_TextAviaoAmigo = "imgTeste/c02_Text_AviaoAmigo.png"
        self._string_imagem_JunkerFriend = "imgTeste/c02_JunkerFriend.png"
        self._string_imagem_TextAviaoMesserschmidt = "imgTeste/c02_Text_AviaoMesserschmidt.png"
        self._string_imagem_Locker1 = "imgTeste/c02_Locker.png"
        self._string_imagem_Locker2 = "imgTeste/c02_Locker.png"
        self._string_imagem_TextRetornar = "imgTeste/c02_BotaoRetornar.png"
        self._string_imagem_Coin1 ="imgTeste/c02_Coin.png"
        self._string_imagem_Coin2 ="imgTeste/c02_Coin.png"
        self._string_imagem_Coin3 ="imgTeste/c02_Coin.png"
        self._string_imagem_Coin4 ="imgTeste/c02_Coin.png"
        self._string_imagem_Patente = "imgTeste/c02_Text_Soldado.png"
        self._string_imagem_fundo = "imgTeste/sky1_menor.png"
        self._string_imagem_Text0 = "imgTeste/c02_Text_0.png"
        self._string_imagem_Text20 = "imgTeste/c02_Text_20.png"
        self._string_imagem_Text210 = "imgTeste/c02_Text_210.png"
        self._string_imagem_AviaoMesserschmidt = "imgTeste/aviaoPiloto em x.png"
        self._string_imagem_AviaoMesserschmidt_invertido =\
                                      "imgTeste/aviaoPiloto em x_invertido.png"
        #---------------------------Fim das COnstantes-------------------------
        
        #----------------Criando as imagens do Menu Hangar e posicionando------
        img_BackgroundHangar    = Figura(self._string_imagem_BackgroundHangar,None,
                                self._PosBackgroundHangar)
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
        img_Patente            = Figura(self._string_imagem_Patente,None,
                                        self._PosPatente)
        img_Text0GP            = Figura(self._string_imagem_Text0,None,
                                        self._PosText0GP)
        img_Text0XP            = Figura(self._string_imagem_Text0,None,
                                        self._PosText0XP)
        img_Text20VidaExtra    = Figura(self._string_imagem_Text20,None,
                                        self._PosText20VidaExtra)
        img_Text20Bomba        = Figura(self._string_imagem_Text20,None,
                                        self._PosText20Bomba)
        img_Text210JunkerFriend = Figura(self._string_imagem_Text210,None,
                                          self._PosText210JunkerFriend)
        #imagem de fundo
        img_fundo = Figura(self._string_imagem_fundo)
        #barulho do click
        self._string_som_buttonClick = "imgTeste/button_click.ogg"
        
        #-------------------------Criando botoes do Menu Hangar-------------
        botao_TextRetornar = Botao("MenuOperacoes","Hangar",
                                   self._string_imagem_TextRetornar,
                                   self._string_imagem_TextRetornar,
                                   self._string_som_buttonClick,
                                   self._PosTextRetornar)    
        #--------------------------------criando itens-------------------------
        item_AviaoMesserschmidt = \
                             item_aviao(self._string_imagem_AviaoMesserschmidt,
                              self._string_imagem_AviaoMesserschmidt_invertido,
                               "AviaoMesserschmidt","Hangar",
                               self._string_imagem_AviaoMesserschmidt,
                               self._string_som_buttonClick,
                               100,100,self._PosAviaoMesserschmidt)
        
        #montando a cena
        self.adicionaFilho(img_fundo)
        self.adicionaFilho(img_BackgroundHangar)
        self.adicionaFilho(img_TextVidaExtra)
        self.adicionaFilho(img_HealthPoint)
        self.adicionaFilho(img_TextBomba)
        self.adicionaFilho(img_Missile)
        self.adicionaFilho(img_TextAviaoAmigo)
        self.adicionaFilho(img_JunkerFriend)
        self.adicionaFilho(img_TextAviaoMesserschmidt)
        self.adicionaFilho(img_Locker1)
        self.adicionaFilho(img_Locker2)
        self.adicionaFilho(img_Coin1)
        self.adicionaFilho(img_Coin2)
        self.adicionaFilho(img_Coin3)
        self.adicionaFilho(img_Coin4)
        self.adicionaFilho(img_Patente)
        self.adicionaFilho(img_Text0GP)
        self.adicionaFilho(img_Text0XP)
        self.adicionaFilho(img_Text20VidaExtra)
        self.adicionaFilho(img_Text20Bomba)
        self.adicionaFilho(img_Text210JunkerFriend)
        self.adicionaFilho(botao_TextRetornar)
        self.adicionaFilho(item_AviaoMesserschmidt)
        
        self._dtMudar = 0
        self._dtMin = 2
        
        self.even.escutar("K_m", self.mudarSkin)
        
    def mudarSkin(self,chamada):
        
        self._dtMudar +=1
        tam = banco_dados.getTamListaSkinAviao()
        
        if tam > 1 and self._dtMudar > self._dtMin:
            print("mudou skin")
            self._dtMudar = 0
            banco_dados.MudarSkinAtual()
        elif tam <= 1:
            print("Voce nao possui outros avioes!")
            
#----------------------Fim da Classe PainelHangar------------------------------

class PainelJogoSalvo(Cena):
    """
        É a classe que monta a cena do Menu Opcoes.
    """    
    def __init__(self, audio, entrada, renderizador, string_musica_fundo = None):
        Cena.__init__(self, audio, entrada, renderizador, string_musica_fundo)
       
        #---------------Constantes do Menu Jogos Salvos------------------------
        self._PosXBackgroundJogoSalvo          = 190
        self._PosYBackgroundJogoSalvo          = 41
        self._PosXJogoSalvo                    = 361
        self._PosYJogoSalvo                    = 59
        self._PosXBotaoJogo1                   = 400
        self._PosYBotaoJogo1                   = 175
        self._PosXBotaoJogo2                   = 400
        self._PosYBotaoJogo2                   = 225
        self._PosXBotaoJogo3                   = 400
        self._PosYBotaoJogo3                   = 275
        self._PosXTextRetornar                 = 496
        self._PosYTextRetornar                 = 497
        
        self._string_imagem_BackgroundJogoSalvo = "imgTeste/c01_BackgroundJogosSalvos.png"
        self._string_imagem_JogoSalvo = "imgTeste/c02_Text_JogosSalvos.png"
        self._string_imagem1_botaoJogo1 = "imgTeste/c02_Text_Jogo1.png"
        self._string_imagem2_botaoJogo1 = "imgTeste/c03_Text_Jogo1.png"
        self._string_imagem1_botaoJogo2 = "imgTeste/c02_Text_Jogo2.png"
        self._string_imagem2_botaoJogo2 = "imgTeste/c03_Text_Jogo2.png"
        self._string_imagem1_botaoJogo3 = "imgTeste/c02_Text_Jogo3.png"
        self._string_imagem2_botaoJogo3 = "imgTeste/c03_Text_Jogo3.png"
        self._string_imagem_TextRetornar = "imgTeste/c02_BotaoRetornar.png"
        #fundo do Menu Jogos Salvos
        self._string_imagem_Fundo = "imgTeste/sky1_menor.png"
        #barulho do click
        self._string_som_buttonClick = "imgTeste/button_click.ogg"
        #----------------Fim das Constates do Menu Jogos Salvos----------------
       
        #--------Criando as imagens do Menu Jogos Salvos e posicionando--------
        img_BackgroundJogoSalvo = Figura(self._string_imagem_BackgroundJogoSalvo,None,
                                  Ponto(self._PosXBackgroundJogoSalvo,
                                        self._PosYBackgroundJogoSalvo))
        img_JogoSalvo = Figura(self._string_imagem_JogoSalvo, None, 
                        Ponto(self._PosXJogoSalvo,self._PosYJogoSalvo))
        
        img_fundo = Figura(self._string_imagem_Fundo)
        
        #-----------------------Criando Botoes do Menu-------------------------
        botaoJogo1 = Botao("ler", "teste",
                              self._string_imagem1_botaoJogo1,
                              self._string_imagem2_botaoJogo1,
                              self._string_som_buttonClick,
                              Ponto(self._PosXBotaoJogo1,
                                    self._PosYBotaoJogo1))
        botaoJogo2 = Botao("ler", "teste",
                              self._string_imagem1_botaoJogo2,
                              self._string_imagem2_botaoJogo2,
                              self._string_som_buttonClick,
                              Ponto(self._PosXBotaoJogo2,
                                    self._PosYBotaoJogo2))
        botaoJogo3 = Botao("ler", "teste",
                              self._string_imagem1_botaoJogo3,
                              self._string_imagem2_botaoJogo3,
                              self._string_som_buttonClick,
                              Ponto(self._PosXBotaoJogo3,
                                    self._PosYBotaoJogo3))
        botao_TextRetornar = Botao("MenuPrincipal","MenuJogoSalvo",
                                   self._string_imagem_TextRetornar,
                                   self._string_imagem_TextRetornar,
                                   self._string_som_buttonClick,
                                   Ponto(self._PosXTextRetornar,
                                         self._PosYTextRetornar))
        #--------------Montando a cena do Menu Jogos Salvos--------------------
        self.adicionaFilho(img_fundo)
        self.adicionaFilho(img_BackgroundJogoSalvo)
        self.adicionaFilho(img_JogoSalvo)
        self.adicionaFilho(botaoJogo1)
        self.adicionaFilho(botaoJogo2)
        self.adicionaFilho(botaoJogo3)
        self.adicionaFilho(botao_TextRetornar)
        
        self.even.escutar("ler",self.lerArquivo)
    
    def lerArquivo(self, nome):
        """
            Ler arquivo.
        """
        ler_arquivo = arquivo()
        dadosSalvos = ler_arquivo.ler(nome)
        banco_dados.setCarteira(dadosSalvos[1])
        banco_dados.setProgresso(dadosSalvos[0])
        banco_dados.setStringAviao((dadosSalvos[2],dadosSalvos[3]))
        banco_dados.setExperiencia(dadosSalvos[4])
        self.even.lancar("MenuPrincipal","MenuJogoSalvo")
        
        
#------------------------------Fim da Classe Jogo Salvo-----------------------

class PainelOpcoes(Cena):
    """
        É a classe que monta a cena do Menu Opcoes.
    """    
    def __init__(self, audio, entrada, renderizador, string_musica_fundo = None):
        Cena.__init__(self, audio, entrada, renderizador, string_musica_fundo)
       
        #------------------Constantes do Menu Opcoes---------------------------
        self._PosXBackgroundOpcoes             = 190
        self._PosYBackgroundOpcoes             = 41
        self._PosXQualidadeGrafica             = 354
        self._PosYQualidadeGrafica             = 349
        self._PosXVolumeMusica                 = 354
        self._PosYVolumeMusica                 = 261
        self._PosXVolumeSons                   = 354
        self._PosYVolumeSons                   = 173
        self._PosXBotaoVolumeSonsDesligado     = 318
        self._PosYBotaoVolumeSonsDesligado     = 209
        self._PosXBotaoVolumeSonsNormal        = 440
        self._PosYBotaoVolumeSonsNormal        = 209
        self._PosXBotaoVolumeSonsAlto          = 548
        self._PosYBotaoVolumeSonsAlto          = 209
        self._PosXBotaoVolumeMusicaDesligado   = 318
        self._PosYBotaoVolumeMusicaDesligado   = 297
        self._PosXBotaoVolumeMusicaNormal      = 440
        self._PosYBotaoVolumeMusicaNormal      = 297
        self._PosXBotaoVolumeMusicaAlto        = 548
        self._PosYBotaoVolumeMusicaAlto        = 297
        self._PosXBotaoQualidadeGraficaNormal  = 368
        self._PosYBotaoQualidadeGraficaNormal  = 385
        self._PosXBotaoQualidadeGraficaAlta    = 501
        self._PosYBotaoQualidadeGraficaAlta    = 385
        self._PosXTextRetornar                 = 496
        self._PosYTextRetornar                 = 497
        
        self._string_imagem_BackgroundOpcoes = "imgTeste/c01_BackgroundOpcoes.png"
        self._string_imagem_QualidadeGrafica = "imgTeste/c02_Text_QualidadeGrafica.png"
        self._string_imagem_VolumeMusica = "imgTeste/c02_Text_VolumeMusica.png"
        self._string_imagem_VolumeSons = "imgTeste/c02_Text_VolumeSons.png"
        self._string_imagem1_botaoVolumeSonsDesligado = "imgTeste/c02_Text_Desligado.png"
        self._string_imagem2_botaoVolumeSonsDesligado = "imgTeste/c03_Text_Desligado.png"
        self._string_imagem1_botaoVolumeSonsNormal = "imgTeste/c02_Text_Normal.png"
        self._string_imagem2_botaoVolumeSonsNormal = "imgTeste/c03_Text_Normal.png"
        self._string_imagem1_botaoVolumeSonsAlto = "imgTeste/c02_Text_Alto.png"
        self._string_imagem2_botaoVolumeSonsAlto = "imgTeste/c03_Text_Alto.png"
        self._string_imagem1_botaoVolumeMusicaDesligado ="imgTeste/c02_Text_Desligado.png"
        self._string_imagem2_botaoVolumeMusicaDesligado ="imgTeste/c03_Text_Desligado.png"
        self._string_imagem1_botaoVolumeMusicaNormal = "imgTeste/c02_Text_Normal.png"
        self._string_imagem2_botaoVolumeMusicaNormal = "imgTeste/c03_Text_Normal.png"
        self._string_imagem1_botaoVolumeMusicaAlto = "imgTeste/c02_Text_Alto.png"
        self._string_imagem2_botaoVolumeMusicaAlto = "imgTeste/c03_Text_Alto.png"
        self._string_imagem1_botaoQualidadeGraficaNormal = "imgTeste/c02_Text_Normal.png"
        self._string_imagem2_botaoQualidadeGraficaNormal = "imgTeste/c03_Text_Normal.png"
        self._string_imagem1_botaoQualidadeGraficaAlta = "imgTeste/c02_Text_Alta.png"
        self._string_imagem2_botaoQualidadeGraficaAlta = "imgTeste/c03_Text_Alta.png"
        self._string_imagem_TextRetornar = "imgTeste/c02_BotaoRetornar.png"
        #fundo do Menu Opcoes
        self._string_imagem_Fundo = "imgTeste/sky1_menor.png"
        #barulho do click
        self._string_som_buttonClick = "imgTeste/button_click.ogg"
        #-------------------Fim das Constates do Menu Opcoes-------------------
       
        #----------Criando as imagens do Menu Opcoes e posicionando------------
        img_BackgroundOpcoes = Figura(self._string_imagem_BackgroundOpcoes,None,
                                  Ponto(self._PosXBackgroundOpcoes,
                                        self._PosYBackgroundOpcoes))
        img_QualidadeGrafica = Figura(self._string_imagem_QualidadeGrafica, None, 
                          Ponto(self._PosXQualidadeGrafica,self._PosYQualidadeGrafica))
        img_VolumeMusica = Figura(self._string_imagem_VolumeMusica,None,Ponto(self._PosXVolumeMusica,
                                                              self._PosYVolumeMusica))
        img_VolumeSons = Figura(self._string_imagem_VolumeSons,None, 
                         Ponto(self._PosXVolumeSons,self._PosYVolumeSons))
        
        img_fundo = Figura(self._string_imagem_Fundo)
        
        #-----------------------Criando Botoes do Menu-------------------------
        botaoVolumeSonsDesligado = Botao("A DEFINIR", "MenuOpcoes",
                              self._string_imagem1_botaoVolumeSonsDesligado,
                              self._string_imagem2_botaoVolumeSonsDesligado,
                              self._string_som_buttonClick,
                              Ponto(self._PosXBotaoVolumeSonsDesligado,
                                    self._PosYBotaoVolumeSonsDesligado))
        botaoVolumeSonsNormal = Botao("A DEFINIR", "MenuOpcoes",
                              self._string_imagem1_botaoVolumeSonsNormal,
                              self._string_imagem2_botaoVolumeSonsNormal,
                              self._string_som_buttonClick,
                              Ponto(self._PosXBotaoVolumeSonsNormal,
                                    self._PosYBotaoVolumeSonsNormal))
        botaoVolumeSonsAlto = Botao("A DEFINIR", "MenuOpcoes",
                              self._string_imagem1_botaoVolumeSonsAlto,
                              self._string_imagem2_botaoVolumeSonsAlto,
                              self._string_som_buttonClick,
                              Ponto(self._PosXBotaoVolumeSonsAlto,
                                    self._PosYBotaoVolumeSonsAlto))
        botaoVolumeMusicaDesligado = Botao("A DEFINIR", "MenuOpcoes",
                              self._string_imagem1_botaoVolumeMusicaDesligado,
                              self._string_imagem2_botaoVolumeMusicaDesligado,
                              self._string_som_buttonClick,
                              Ponto(self._PosXBotaoVolumeMusicaDesligado,
                                    self._PosYBotaoVolumeMusicaDesligado))
        botaoVolumeMusicaNormal = Botao("A DEFINIR", "MenuOpcoes",
                              self._string_imagem1_botaoVolumeMusicaNormal,
                              self._string_imagem2_botaoVolumeMusicaNormal,
                              self._string_som_buttonClick,
                              Ponto(self._PosXBotaoVolumeMusicaNormal,
                                    self._PosYBotaoVolumeMusicaNormal))
        botaoVolumeMusicaAlto = Botao("A DEFINIR", "MenuOpcoes",
                              self._string_imagem1_botaoVolumeMusicaAlto,
                              self._string_imagem2_botaoVolumeMusicaAlto,
                              self._string_som_buttonClick,
                              Ponto(self._PosXBotaoVolumeMusicaAlto,
                                    self._PosYBotaoVolumeMusicaAlto))
        botaoQualidadeGraficaNormal = Botao("A DEFINIR", "MenuOpcoes",
                              self._string_imagem1_botaoQualidadeGraficaNormal,
                              self._string_imagem2_botaoQualidadeGraficaNormal,
                              self._string_som_buttonClick,
                              Ponto(self._PosXBotaoQualidadeGraficaNormal,
                                    self._PosYBotaoQualidadeGraficaNormal))
        botaoQualidadeGraficaAlta = Botao("A DEFINIR", "MenuOpcoes",
                              self._string_imagem1_botaoQualidadeGraficaAlta,
                              self._string_imagem2_botaoQualidadeGraficaAlta,
                              self._string_som_buttonClick,
                              Ponto(self._PosXBotaoQualidadeGraficaAlta,
                                    self._PosYBotaoQualidadeGraficaAlta))
        botao_TextRetornar = Botao("MenuPrincipal","MenuOpcoes",
                                   self._string_imagem_TextRetornar,
                                   self._string_imagem_TextRetornar,
                                   self._string_som_buttonClick,
                                   Ponto(self._PosXTextRetornar,
                                         self._PosYTextRetornar))
        #------------------Montando a cena do Menu Opcoes----------------------
        self.adicionaFilho(img_fundo)
        self.adicionaFilho(img_BackgroundOpcoes)
        self.adicionaFilho(img_VolumeSons)
        self.adicionaFilho(img_VolumeMusica)
        self.adicionaFilho(img_QualidadeGrafica)
        self.adicionaFilho(botaoVolumeSonsDesligado)
        self.adicionaFilho(botaoVolumeSonsNormal)
        self.adicionaFilho(botaoVolumeSonsAlto)
        self.adicionaFilho(botaoVolumeMusicaDesligado)
        self.adicionaFilho(botaoVolumeMusicaNormal)
        self.adicionaFilho(botaoVolumeMusicaAlto)
        self.adicionaFilho(botaoQualidadeGraficaNormal)
        self.adicionaFilho(botaoQualidadeGraficaAlta)
        self.adicionaFilho(botao_TextRetornar)
        
#------------------------------------Fim da Classe Menu Opcoes-----------------


class PainelCreditos(Cena):
    """
        É a classe que monta a cena do Menu Creditos.
    """    
    def __init__(self, audio, entrada, renderizador, string_musica_fundo = None):
        Cena.__init__(self, audio, entrada, renderizador, string_musica_fundo)
       
        #------------------Constantes do Menu Creditos---------------------------
        self._PosXBackgroundCreditos             = 190
        self._PosYBackgroundCreditos             = 41
        self._PosXBotaoDennys1                   = 370
        self._PosYBotaoDennys1                   = 261
        self._PosXBotaoGabriel1                  = 314
        self._PosYBotaoGabriel1                  = 181
        self._PosXBotaoDylan1                    = 346
        self._PosYBotaoDylan1                    = 221
        self._PosXTextRetornar                   = 496
        self._PosYTextRetornar                   = 497
        
        self._string_imagem_BackgroundCreditos = "imgTeste/c01_BackgroundCreditos.png"
        self._string_imagem1_botaoDennys = "imgTeste/c02_Text_Dennys.png"
        self._string_imagem2_botaoDennys = "imgTeste/c03_Text_Dennys.png"
        self._string_imagem1_botaoDylan = "imgTeste/c02_Text_Dylan.png"
        self._string_imagem2_botaoDylan = "imgTeste/c03_Text_Dylan.png"
        self._string_imagem1_botaoGabriel = "imgTeste/c02_Text_Gabriel.png"
        self._string_imagem2_botaoGabriel = "imgTeste/c03_Text_Gabriel.png"
        self._string_imagem_TextRetornar = "imgTeste/c02_BotaoRetornar.png"
        #fundo do Menu Opcoes
        self._string_imagem_Fundo = "imgTeste/sky1_menor.png"
        #barulho do click
        self._string_som_buttonClick = "imgTeste/button_click.ogg"
        #-------------------Fim das Constantes do Menu Creditos-------------------
       
        #----------Criando as imagens do Menu Creditos e posicionando------------
        img_BackgroundCreditos = Figura(self._string_imagem_BackgroundCreditos,None,
                                  Ponto(self._PosXBackgroundCreditos,
                                        self._PosYBackgroundCreditos))
        
        img_fundo = Figura(self._string_imagem_Fundo)
        
        #-----------------------Criando Botoes do Menu-------------------------
        botaoDennys = Botao("A DEFINIR", "MenuCreditos",
                              self._string_imagem1_botaoDennys,
                              self._string_imagem2_botaoDennys,
                              self._string_som_buttonClick,
                              Ponto(self._PosXBotaoDennys1,
                                    self._PosYBotaoDennys1))
        botaoDylan = Botao("A DEFINIR", "MenuCreditos",
                              self._string_imagem1_botaoDylan,
                              self._string_imagem2_botaoDylan,
                              self._string_som_buttonClick,
                              Ponto(self._PosXBotaoDylan1,
                                    self._PosYBotaoDylan1))
        botaoGabriel = Botao("A DEFINIR", "MenuCreditos",
                              self._string_imagem1_botaoGabriel,
                              self._string_imagem2_botaoGabriel,
                              self._string_som_buttonClick,
                              Ponto(self._PosXBotaoGabriel1,
                                    self._PosYBotaoGabriel1))
        botao_TextRetornar = Botao("MenuPrincipal","MenuCreditos",
                                   self._string_imagem_TextRetornar,
                                   self._string_imagem_TextRetornar,
                                   self._string_som_buttonClick,
                                   Ponto(self._PosXTextRetornar,
                                         self._PosYTextRetornar))
        #------------------Montando a cena do Menu Creditos----------------------
        self.adicionaFilho(img_fundo)
        self.adicionaFilho(img_BackgroundCreditos)
        self.adicionaFilho(botaoDennys)
        self.adicionaFilho(botaoDylan)
        self.adicionaFilho(botaoGabriel)
        self.adicionaFilho(botao_TextRetornar)
        
#----------------------------Fim da Classe Menu Creditos-----------------------


class PainelNovoJogo(Cena):
    """
        É a classe que monta a cena do Menu Novo Jogo.
    """    
    def __init__(self, audio, entrada, renderizador, string_musica_fundo = None):
        Cena.__init__(self, audio, entrada, renderizador, string_musica_fundo)
       
        #------------------Constantes do Menu Novo Jogo------------------------
        self._PosXBackgroundNovoJogo             = 190
        self._PosYBackgroundNovoJogo             = 41
        self._PosXBotaoIniciar                   = 411
        self._PosYBotaoIniciar                   = 174
        self._PosXBotaoTutorial                  = 394
        self._PosYBotaoTutorial                  = 221
        self._PosXTextRetornar                   = 496
        self._PosYTextRetornar                   = 497
        
        self._string_imagem_BackgroundNovoJogo = "imgTeste/c01_BackgroundNovoJogo.png"
        self._string_imagem1_botaoIniciar = "imgTeste/c02_Text_Iniciar.png"
        self._string_imagem2_botaoIniciar = "imgTeste/c03_Text_Iniciar.png"
        self._string_imagem1_botaoTutorial = "imgTeste/c02_Text_Tutorial.png"
        self._string_imagem2_botaoTutorial = "imgTeste/c03_Text_Tutorial.png"
        self._string_imagem_TextRetornar = "imgTeste/c02_BotaoRetornar.png"
        #fundo do Menu Novo Jogo
        self._string_imagem_Fundo = "imgTeste/sky1_menor.png"
        #barulho do click
        self._string_som_buttonClick = "imgTeste/button_click.ogg"
        #-------------------Fim das Constantes do Menu Novo Jogo---------------
       
        #--------Criando as imagens do Menu Novo Jogo e posicionando-----------
        img_BackgroundNovoJogo = Figura(self._string_imagem_BackgroundNovoJogo,
                                        None,Ponto(self._PosXBackgroundNovoJogo,
                                        self._PosYBackgroundNovoJogo))
        
        img_fundo = Figura(self._string_imagem_Fundo)
        
        #-----------------------Criando Botoes do Menu-------------------------
        botaoIniciar = Botao("MenuOperacoes", "MenuNovoJogo",
                              self._string_imagem1_botaoIniciar,
                              self._string_imagem2_botaoIniciar,
                              self._string_som_buttonClick,
                              Ponto(self._PosXBotaoIniciar,
                                    self._PosYBotaoIniciar))
        botaoTutorial = Botao("Tutorial", "MenuNovoJogo",
                              self._string_imagem1_botaoTutorial,
                              self._string_imagem2_botaoTutorial,
                              self._string_som_buttonClick,
                              Ponto(self._PosXBotaoTutorial,
                                    self._PosYBotaoTutorial))
        botao_TextRetornar = Botao("MenuPrincipal","MenuNovoJogo",
                                   self._string_imagem_TextRetornar,
                                   self._string_imagem_TextRetornar,
                                   self._string_som_buttonClick,
                                   Ponto(self._PosXTextRetornar,
                                         self._PosYTextRetornar))
        #------------------Montando a cena do Menu Novo Jogo-------------------
        self.adicionaFilho(img_fundo)
        self.adicionaFilho(img_BackgroundNovoJogo)
        self.adicionaFilho(botaoIniciar)
        self.adicionaFilho(botaoTutorial)
        self.adicionaFilho(botao_TextRetornar)
        
#----------------------------Fim da Classe Menu Novo Jogo----------------------

class PainelMenuPause(Cena):
    
    def __init__(self,audio,entrada,renderizador,string_musica_fundo=None):
        Cena.__init__(self,audio,entrada,renderizador,string_musica_fundo)
        
        #-------------Constantes-----------------------------------------------
        
        self._PosBackgroundPause = Ponto(190,41)
        self._PosTextResumir = Ponto(403,174)
        self._PosTextMenuPrincipal = Ponto(367,221)
        self._PosTextAbortar = Ponto(401,271)
        
        self._string_imagem_BackgroundPause = "imgTeste/c01_BackgroundPause.png"
        self._string_imagem1_textResumir = "imgTeste/c02_Text_Resumir.png"
        self._string_imagem2_textResumir = "imgTeste/c03_Text_Resumir.png"
        self._string_imagem1_textMenuPrincipal = "imgTeste/c02_Text_MenuPrincipal.png"
        self._string_imagem2_textMenuPrincipal = "imgTeste/c03_Text_MenuPrincipal.png"
        self._string_imagem1_textAbortar = "imgTeste/c02_Text_Abortar.png"
        self._string_imagem2_textAbortar = "imgTeste/c03_Text_Abortar.png"
        self._string_som_buttonClick = "imgTeste/button_click.ogg"
        #fundo do Menu Novo Jogo
        self._string_imagem_Fundo = "imgTeste/sky1_menor.png"
        #barulho do click
        self._string_som_buttonClick = "imgTeste/button_click.ogg"
        #--------------Fim das constantes--------------------------------------
        
        #CRIAR imagens
        img_BackgroundPause = Figura(self._string_imagem_BackgroundPause,None,
                                self._PosBackgroundPause)
        img_fundo = Figura(self._string_imagem_Fundo)
        #Criar botoes
        botao_Resumir = Botao("Play","MenuPause",
                              self._string_imagem1_textResumir,
                              self._string_imagem2_textResumir,
                              self._string_som_buttonClick,
                              self._PosTextResumir)
        botao_MenuPrincipal = Botao("MenuPrincipal","MenuPause",
                                  self._string_imagem1_textMenuPrincipal,
                                  self._string_imagem2_textMenuPrincipal,
                                  self._string_som_buttonClick,
                                  self._PosTextMenuPrincipal)
        botao_Abortar = Botao("sair","MenuPause",
                              self._string_imagem1_textAbortar,
                              self._string_imagem2_textAbortar,
                              self._string_som_buttonClick,
                              self._PosTextAbortar)
        #montar cena
        self.adicionaFilho(img_fundo)
        self.adicionaFilho(img_BackgroundPause)
        self.adicionaFilho(botao_Resumir)
        self.adicionaFilho(botao_MenuPrincipal)
        self.adicionaFilho(botao_Abortar)
    
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
        Botao_continuar = Botao("Play","MenuGameOver",
                                self._string_imagem_continuar,
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
#----------------Fim da Classe PainelGameOver----------------------------------



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
        Velocimetro_Jogador = Velocimetro(200,Ponto(0,alturaTela-50),
                                          Ponto(40,50),
                                          "imgTeste/c(X)_PonteiroFuel.png",
                                          "imgTeste/c(X+1)_Fuel.png")
        projetilJogador = Projetil("imgTeste/BulletEnemies.png",
                                   "imgTeste/MetalHit1.ogg",
                                   1,Ponto(0,0))
        armaJogador = Arma("imgTeste/M4A1_Single.ogg",projetilJogador)
        img_aviao_jogador = banco_dados.getSkinAtual()[0]
        img_aviao_jogador2 =  banco_dados.getSkinAtual()[1]
        avi = Jogador(img_aviao_jogador, img_aviao_jogador2, 
                     Ponto(100, 100), Ponto(28, 10),
                     [[8000, 90000, 172],  [8000, 4000, 8000, 100, 0.3, 5400, 1],  
                     [5, 37000, 5000/3, 100], [5000, 150]], arma = armaJogador,
                     string_som_fallShell="imgTeste/Shells_falls.ogg",
                     PV = Barra_Vida_Jogador)
        Velocimetro_Jogador.setDono(avi)
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
                                    Barra_Vida_TorreInimiga, 
                                    pos = Ponto(800,580),
                                    centro = Ponto(0, 46),
                                    posTiro = Ponto(95, 46)
                                    )
        armaTorreInimiga.setDono(torreInimiga)
        baseTorreInimiga = Figura("imgTeste/Base_Turret.png", 
                                  pos = Ponto(800, 580), 
                                  centro = Ponto(33, 9)
                                  )
        
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
        self.adicionaFilho(camera)
        self.adicionaFilho(Velocimetro_Jogador)
        self.adicionaFilho(Barra_Vida_Jogador)
        
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
        
        self.limparEventos()
   
        if chamada == "MenuPause":
           self.cenaAtual = self.cenaAnterior
           self.cenaAtual.ativarEscuta()
           
        else:
            self.audio.pararMusicaFundo()
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
    def MenuJogoSalvo(self,chamada):
        self.limparEventos()
        #trocando de transparencias
        self.cenaAtual = PainelJogoSalvo(self.audio,self.entrada,
                                           self.renderizador,
                                           "imgTeste/World_War_II_Soundtrack.ogg")
    def MenuOpcoes(self,chamada):
        self.limparEventos()
        #trocando de transparencias
        self.cenaAtual = PainelOpcoes(self.audio,self.entrada,self.renderizador,
                                      "imgTeste/World_War_II_Soundtrack.ogg")
    
    def MenuNovoJogo(self,chamada):
        self.limparEventos()
        #trocando de transparencias
        self.cenaAtual = PainelNovoJogo(self.audio,self.entrada,self.renderizador,
                                      "imgTeste/World_War_II_Soundtrack.ogg")
    
    def MenuCreditos(self,chamada):
        self.limparEventos()
        #trocando de transparencias
        self.cenaAtual = PainelCreditos(self.audio,self.entrada,self.renderizador,
                                        "imgTeste/World_War_II_Soundtrack.ogg")
    
    def MenuOperacoes(self,chamada):
        self.limparEventos()
        #trocando de transparencias
        if chamada == "MenuHangar":
            self.audio.pararMusicaFundo()
            musica_fundo = "imgTeste/01_-_Sketchy_Logic_-_Ride_Onward.ogg"
        else:
            musica_fundo = None
        self.cenaAtual = PainelMenuOperacoes(self.audio,self.entrada,
                                         self.renderizador, musica_fundo)
    
    
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

    def MenuHangar(self, chamada):
        self.audio.pararMusicaFundo()
        #limpando eventos
        self.limparEventos()
        #trocando de  transparencias
        musica_fundo = "imgTeste/05_-_Sketchy_Logic_-_Victory_and_Respite.ogg"
        self.cenaAtual = PainelHangar(self.audio,self.entrada,
                                         self.renderizador,musica_fundo)
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
        self.even.escutar("Hangar", self.MenuHangar)
        self.even.escutar("MenuPause",self.MenuPause)
        self.even.escutar("MenuNovoJogo", self.MenuNovoJogo)
        self.even.escutar("MenuOpcoes", self.MenuOpcoes)
        self.even.escutar("MenuCreditos", self.MenuCreditos)
        self.even.escutar("MenuJogoSalvo",self.MenuJogoSalvo)
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
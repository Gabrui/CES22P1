# -*- coding: utf-8 -*-
"""
Created on Mon May  1 13:14:34 2017

@author: Dylan N. Sugimoto
"""

import aviao
import motor
import Projetil
import IA


class Simulador(motor.Camada):
    """
        Realiza operacoes de fundo do gameplay, como verificar colisoes.
    """
    def __init__(self, posChao, larguraTela):
        motor.Camada.__init__(self)
        """
            posChao: é a posicao do chao (int).
            meialarguraTela: é a metade da largura da tela.
        """
        self.PosXCentroTela = larguraTela/2
        self.meialarguraTela = larguraTela/2
        self.posChao = posChao
        #Ativa a escuta de eventos
        self.ativarEscuta()
               
        
    def ativarEscuta(self):
        #escuta o evento do disparo e adiciona o filho que é um projetil
        self.even.escutar("Atirar",self.adicionaFilho)
        for filho in self.filhos:
            if isinstance(filho,aviao.Jogador) or isinstance(filho,IA.IA):
                filho.ativarEscuta()
        
    def atualiza(self, dt):
        #verificando colisoes 
        self.verificarColisao(dt)
        #lancando a posicao do Jogador
        for filho in self.filhos:
            if isinstance(filho, aviao.Jogador):
                self.PosXCentroTela = filho.pos.getX()
                self.even.lancar("PlayerLocation",(filho.pos.getX(),
                                                   filho.pos.getY(),
                                                   filho.xVel,filho.yVel))
        super().atualiza(dt)
        
    
    def verificarColisao(self,dt):
        
        """
            Verifica colisoes.
        """
        self._atualizaRetangs()
        #Coletando objetos existentes no gameplay
        figuras = self.filhos
        for filhos in figuras:
            for irmao in figuras:
                #comparar objetos diferentes
                if filhos != irmao:
                    #criando retangulo de referencia
                    referencia = filhos.retang
                    #canto superior esquerdo
                    canto1Irmao = irmao.retang.getTopoEsquerdo()
                    #canto inferior direito
                    canto4Irmao = irmao.retang.getFundoEsquerdo()
                    #canto superior direito
                    canto2Irmao = irmao.retang.getTopoDireito()
                    #canto inferior esquerdo
                    canto3Irmao = irmao.retang.getFundoDireito()
                    #cantos: lista dos cantos da Figura
                    cantos = [canto1Irmao,canto2Irmao,canto3Irmao,canto4Irmao]
                    colidiu = False
                    for pontos in cantos:
                        #verifica colisao
                        colisao = referencia.estaDentro(pontos)
                        if colisao:
                            colidiu = True
                    if colidiu:
                        
                        #se houver colisao entre projeteis, remove os dois
                        #projeteis do gameplay
                        if isinstance(filhos,Projetil.Projetil) and \
                        isinstance(irmao,Projetil.Projetil):
                             self.removeFilho(filhos)
                             self.removeFilho(irmao)
                        elif (isinstance(filhos,Projetil.Projetil) and \
                              isinstance(irmao, aviao.Aviao)):
                              #Se houver colisao entre Jogador e projetil,
                              #reduz os pontos de vida do Jogador
                              #irmao[10].reduzPV(filhos[10].getDano())
                              #chama animacao de fisica de impacto do projetil
                              filhos.fisicaDeImpacto()
                               #remove o projetil do gameplay
                              self.removeFilho(filhos)
                              #verifica se o Jogador esta vivo
                              #if irmao[10].getPV() <= 0:
                              #    if isinstance(irmao,aviao.Jogador):
                                  #se nao tiver vivo, chama tela de G.O.
                              #      self.even.lancar("GameOver",True)
                        elif(isinstance(filhos, aviao.Aviao) and \
                             isinstance(irmao,Projetil.Projetil)):
                               #o mesmo que a anterior
                               # filhos[10].reduzPV(filhos[10].getDano())
                              irmao.fisicaDeImpacto()
                              self.removeFilho(irmao)
                                #if filhos[10].getPV() <= 0:
                                #    if isinstance(filhos,aviao.Jogador):
                                  #      self.even.lancar("GameOver",True)
                                       
                        elif (isinstance(filhos,Projetil.Projetil) and\
                              isinstance(irmao,IA.IA)):
                           
                            #Se houver colisao entre projetil e IA
                            #reduz os pontos de vida da IA
                            irmao.reduzPV(filhos.getDano())
                            #Chama animacao de impacto do projetil
                                
                            filhos.fisicaDeImpacto()
                            #remove o projetil do gameplay
                            self.removeFilho(filhos)
                            if irmao.getPV() <= 0:
                                
                                 #     irmao[10].explosao()
                                #Se IA esvier morta, remove do gameplay
                                self.removeFilho(irmao)
                        elif(isinstance(filhos, IA.IA) and \
                             isinstance(irmao,Projetil.Projetil)):
                            
                                #o mesmo que a anterior
                            filhos.reduzPV(irmao.getDano())
                            irmao.fisicaDeImpacto()
                            self.removeFilho(irmao)
                            if filhos.getPV() <= 0:
                                #   filhos[10].explosao()
                                 self.removeFilho(filhos)
                                 
            if isinstance(filhos, Projetil.Projetil):
                if filhos.pos.getX()<self.PosXCentroTela-self.meialarguraTela or\
                   filhos.pos.getX() > self.PosXCentroTela + self.meialarguraTela\
                   or filhos.pos.getY() >= self.posChao:
                   #Se for projetil ou IA, remove do gameplay
                   self.removeFilho(filhos)
            
            if filhos.pos.getY() >= self.posChao:
                
                if isinstance(filhos, aviao.Aviao):
                    #Se for Jogador, chama tela de G.O.
                    #filhos[10].explosao()
                    filhos.yVel *= -1
                    self.even.lancar("GameOver", True)
                elif isinstance(filhos, IA.AviaoInimigo):
                    #Se houver colisao entre aviaoInimigo e chao
                    #Chama o metodo de animacao da explosao
                    filhos.explosao(dt)
                    #retira da lista de filhos
                    self.removeFilho(filhos)
                    
                               
                               
                               
                               
                               
                               
                               
                               
                               
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 12:00:23 2017

@author: Dylan N. Sugimoto
"""
import motor
import math

velPadrao = -100 #constante de valor padrao de velocidade para IA
distanciaManobra = 400 #valor constante para distancia minima para
                       # realizar Manobra180V
erro = 5 #erro angular aceitavel para atirar

class IA(motor.Renderizavel):
    def __init__(self,arma,Barra_Vida, pos, vel, alvoPos,
                 alvoVel,
                 deltaAngTol,string_som_fallShell=None):
        motor.Renderizavel.__init__(self)
        """
        Barra_Vida: é um objeto do tipo Vida
        alvoPos: (posXdoJogador,posYdoJogador)
        alvoVel: (velXdoJogador,velYdoJogador)
        arma:    Objeto do tipo Arma
        pos:     tupla de posicao do IA
        vel:     tupla de velocidade do IA
        velAng:  velocidade angular de IA
        deltaAngTol: angulo de tolerancia para disparo
        string_som_disparo: nome do arquivo do som do disparo
        """
        
        if pos is None:
            pos = motor.Ponto(0,0)
        if vel is None:
            vel=motor.Ponto(velPadrao,0)
        if alvoPos is None:
            alvoPos = motor.Ponto(0,0)
        if alvoVel is None:
            alvoVel = motor.Ponto(0,0)
        if deltaAngTol is None:
            deltaAngTol = motor.Angulo(erro)
            
        self.Barra_Vida = Barra_Vida
        self.Barra_Vida.setDono(self)

        
        self.Pos = pos
        self.Vel = vel
        self.velAng = 0
        self.deltaAngTol = deltaAngTol
        self.arma = arma
        self.distanciaManobra = distanciaManobra
        self._string_som_fallShell = string_som_fallShell
        self.alvoPos = alvoPos
        self.alvoVel = alvoVel
        
        self.dtAtirar = 0
        self.dtAtirarMin = 1
        
        self.distanciaMira = 300 #distancia em que IA ajusta a mira
        
        #ativa a escuta de eventos
        self.ativarEscuta()
        
        self._valor = 10
    
    def getValor(self):
        """
            Retorna quanto que a IA vale em pontos de jogo
        """
        return self._valor
    
    def reduzPV(self,dano):
        """
            reduz a quantidade de pontos de vida da IA
        """
        self.Barra_Vida.reduzPV(dano)
    def getPV(self):
        """
            retorna a quantidade de vida da IA
        """
        return self.Barra_Vida.getPV()
        
    
    def ativarEscuta(self):
        #escuta o evento e chama a funcao
        #PlayerLocation: é o evento da posicao do player
        self.even.escutar("PlayerLocation", self.localizar)
        
    def localizar(self, alvo):
        """
            Receber a posicao e a velocidade do Jogador.
            alvoPos: (poX,posY)
            alvoVel: (velx,vely)
        """
        self.alvoPos.setXY(alvo[0],alvo[1])
        self.alvoVel.setXY(alvo[2],alvo[3])
        
    def mira(self, dt):
        """
            Ajusta a mira para acertar o jogador
        """
        visada = motor.Angulo(math.atan2(self.pos.getY() - self.alvoPos.getY(),
                            self.alvoPos.getX() - self.pos.getX()), False)
        dif = self.rot.getDiferenca(visada).getAngulo()
        self.velMax = 56
        
        # Cálculo da velocidade
        if abs(dif) < self.velMax:
            vel = dif
        elif dif > 0:
            vel = self.velMax
        else:
            vel = -self.velMax
        if abs(dif) < self.deltaAngTol.getAngulo():
            self.dtAtirar +=dt
            if self.dtAtirar> self.dtAtirarMin:
                self.shoot(dt)
            
        # Runge-Kutta de primeira ordem :D
        self.rot.incrementa(vel*dt)    

    def shoot(self,dt):
        """
        lanca evento de disparo.
        """
        #zera o contador
        self.dtAtirar =0
        #copia o projetil
        projetil = self.arma.getProjetil()
        #copia a posicao
        posInicialProjetil = self.pos.clonar()
        #ajusta a posicao inicial do projetil
        posInicialProjetil.setXY(posInicialProjetil.getX()+
                            math.cos(self.rot.getAngulo(False))*50,
                                 posInicialProjetil.getY() - 
                      math.sin(self.rot.getAngulo(False))*50)
        #coloca a posicao inicial no projetil
        projetil.Disparo(posInicialProjetil,self.rot.getAngulo())
        #Pegar nome do arquivo do som do disparo
        self._string_som_disparo = self.arma.getSom()
        #lanca para ser adicionado no simulador
        self.even.lancar("Atirar",projetil)
        #lanca para tocar sons
        self.even.lancar("tocarEfeito",self._string_som_disparo)
        self.even.lancar("tocarEfeito",self._string_som_fallShell)

class AviaoInimigo(IA,motor.Animacao):
    
    
    def __init__(self,img1,img2, audio, arma, pos,PV,string_som_explosao,
                 string_som_fallShell, vel, alvoPos,
                 alvoVel,  
                 deltaAngTol): 
        IA.__init__(self,arma,PV, pos, vel, alvoPos,
                 alvoVel,
                 deltaAngTol,string_som_fallShell)
        motor.Animacao.__init__(self,img1,pos = pos)

        """
        img:     É a string do nome do arquivo imagem do aviao
        audio:   É a string do nome do arquivo audio do aviao
        alvoPos: (posXdoJogador,posYdoJogador)
        alvoVel: (velXdoJogador,velYdoJogador)
        arma:    Objeto do tipo Arma
        pos:     tupla de posicao do aviao inimigo
        vel:     tupla de velocidade do aviao inimigo
        deltaAngTol: angulo de tolerancia para disparo
        imgX:        A imagem 1 é para esquerda, e a 2 para direita.
        velo:     É o módulo da velocidade do aviao
        """
        
        if pos is None:
            pos = motor.Ponto(0,0)
        if vel is None:
            vel=motor.Ponto(velPadrao,0)
        if alvoPos is None:
            alvoPos = motor.Ponto(0,0)
        if alvoVel is None:
            alvoVel = motor.Ponto(0,0)
        if deltaAngTol is None:
            deltaAngTol = motor.Angulo(erro)
            
        self.img1 = img1
        self.img2 = img2
        self.tol = 0.087
        self.Manobra180V = False
        self._string_som_explosao = string_som_explosao
        self._audio = audio
        # self.even.lancar("tocarEfeito",self._audio)
        self.vivo = True
        
        limiteEsquerdo = 600
        limitedireito  = 600
        self._iniciar_perseguicao = False
        self._posX_barrera_esquerda = pos.getX() - limiteEsquerdo
        self._posX_barrera_direita  = pos.getX() + limitedireito
        self._posX_barrera_centro = (self._posX_barrera_esquerda  +\
                                     self._posX_barrera_direita)/2
        self._posY_barrera_centro = pos.getY()
       
        self._valor = 100
        
    def realizarManobra180H(self):
        
        if not self.Manobra180V:
            #Troca a imagem
            self.setString(self.img2)
            #troca o estado na manobra
            #voando para direita
            
        elif self.Manobra180V:
            #Troca a imagem
            self.setString(self.img1)
            #Troca o estado da manobra
            #voando pra esquerda
 
    
    def voarSimples(self, dt):
        # 140 é a velocidade em pixel/s
        self.velo = 140
        self.pos.setX(self.pos.getX() + 
                      math.cos(self.rot.getAngulo(False))*self.velo*dt)
        self.pos.setY(self.pos.getY() - 
                      math.sin(self.rot.getAngulo(False))*self.velo*dt)
        if (180-self.tol <=math.fabs(self.rot.getAngulo())%180<= 180)\
           and self.pos.getX() > self.alvoPos.getX():
               self.Manobra180V = False
               self.realizarManobra180H()
        elif (0 <=math.fabs(self.rot.getAngulo())%360<= self.tol)\
           and self.pos.getX() < self.alvoPos.getX():
               self.Manobra180V = True
               self.realizarManobra180H()
   
    def patrulhar(self,dt):
        """
            Aviao inimigo fica limitado a voar em uma determinada regiao
        """
        visada = motor.Angulo(math.atan2(self.pos.getY() - self._posY_barrera_centro,
                            self._posX_barrera_centro - self.pos.getX()), False)
        dif = self.rot.getDiferenca(visada).getAngulo()
        self.velMax = 56
        
        # Cálculo da velocidade
        if abs(dif) < self.velMax:
            vel = dif
        elif dif > 0:
            vel = self.velMax
        else:
            vel = -self.velMax
            
        # Runge-Kutta de primeira ordem :D
        self.rot.incrementa(vel*dt) 
        
    
    def explosao(self,dt):
        if self.vivo: # Se ficar atualizando, a explosão fica só no primeiro
            self.velo = 0
            self.setString("imgTeste/explosion17.png", 64, 64)
            self.rodarAnimacao(3, 1)
            self.even.lancar("tocarEfeito",self._string_som_explosao)
        self.vivo = False
        return self.Barra_Vida
        
    def atualiza(self,dt):
        
        motor.Animacao.atualiza(self, dt)
        if self.vivo:
            if self._iniciar_perseguicao:
                self.mira(dt)
                self.voarSimples(dt)
            elif not self._iniciar_perseguicao:
                self.patrulhar(dt)
                self.voarSimples(dt)
            if self._posX_barrera_esquerda <= self.alvoPos.getX() <= \
               self._posX_barrera_direita:
                
                self._iniciar_perseguicao = True
            elif self.alvoPos.getX() <= self._posX_barrera_esquerda or \
                 self.alvoPos.getX() >= self._posX_barrera_direita:
               
                self._iniciar_perseguicao = False


class TorreInimiga(IA,motor.Figura):
    
    def __init__(self,img,string_som_fallShell,
                 arma,PV, pos, vel, alvoPos,
                 alvoVel,
                 deltaAngTol): 
        IA.__init__(self,arma, PV, pos, vel, alvoPos,
                 alvoVel,
                 deltaAngTol,string_som_fallShell)
        motor.Figura.__init__(self,img, centro = motor.Ponto(110,100))
        """
        img:     É a string do nome do arquivo imagem da Torre inimiga
        string_som_disparo:   É a string do nome do arquivo audio do disparo
        alvoPos: (posXdoJogador,posYdoJogador)
        alvoVel: (velXdoJogador,velYdoJogador)
        arma:    Objeto do tipo Arma
        pos:     tupla de posicao da Torre Inimiga
        vel:     tupla de velocidade da Torre inimiga. No caso é sempre zero.
        deltaAngTol: angulo de tolerancia para disparo
        """
        
        if pos is None:
            pos = motor.Ponto(0,0)
        if vel is None:
            vel=motor.Ponto(velPadrao,0)
        if alvoPos is None:
            alvoPos = motor.Ponto(0,0)
        if alvoVel is None:
            alvoVel = motor.Ponto(0,0)
        if deltaAngTol is None:
            deltaAngTol = motor.Angulo(10)
        self.pos.setXY(pos.getX(),pos.getY())
        
        self._valor = 1000
        
    def atualiza(self,dt):
        self.mira(dt)
           
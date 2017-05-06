# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 12:00:23 2017

@author: Dylan N. Sugimoto
"""
import motor
import math
from Vida import Vida 
velPadrao = -100 #constante de valor padrao de velocidade para IA
distanciaManobra = 400 #valor constante para distancia minima para
                       # realizar Manobra180V
erro = 5 #erro angular aceitavel para atirar

class IA(motor.Renderizavel, Vida):
    def __init__(self,arma, PV, pos, vel, alvoPos,
                 alvoVel,
                 deltaAngTol,string_som_disparo = None,string_som_fallShell=None):
        motor.Renderizavel.__init__(self)
        Vida.__init__(self,PV)
        """
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
        
        self.PV = PV
        self._string_som_disparo = string_som_disparo 
        
        self.distanciaMira = 300 #distancia em que IA ajusta a mira
        
        #ativa a escuta de eventos
        self.ativarEscuta()
    
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
        tupla_tiro: (PosicaodaIA, direcaoDeDIsparo,ObjetoProjetil)
        """
        self.dtAtirar =0
        projetil = self.arma.getProjetil()
        posInicialProjetil = self.pos.clonar()
        posInicialProjetil.setXY(posInicialProjetil.getX()+
                            math.cos(self.rot.getAngulo(False))*50,
                                 posInicialProjetil.getY() - 
                      math.sin(self.rot.getAngulo(False))*50)
        projetil.Disparo(posInicialProjetil,self.rot.getAngulo())
        self.even.lancar("Atirar",projetil)
        self.even.lancar("tocarEfeito",self._string_som_disparo)
        self.even.lancar("tocarEfeito",self._string_som_fallShell)

class AviaoInimigo(IA,motor.Figura):
    
    
    def __init__(self,img1,img2, audio, arma, pos,PV,string_som_disparo,
                 string_som_explosao,string_som_fallShell, vel, alvoPos,
                 alvoVel,  
                 deltaAngTol): 
        IA.__init__(self,arma,PV, pos, vel, alvoPos,
                 alvoVel,
                 deltaAngTol,string_som_disparo,string_som_fallShell)
        motor.Figura.__init__(self,img1, centro = motor.Ponto(32,20))
        """
        img:     É a string do nome do arquivo imagem do aviao
        audio:   É a string do nome do arquivo audio do aviao
        alvoPos: (posXdoJogador,posYdoJogador)
        alvoVel: (velXdoJogador,velYdoJogador)
        arma:    Objeto do tipo Arma
        pos:     tupla de posicao do aviao inimigo
        vel:     tupla de velocidade do aviao inimigo
        velAng:  velocidade angular do aviao inimigo
        deltaAngTol: angulo de tolerancia para disparo
        imgX:        A imagem 1 é para esquerda, e a 2 para direita.
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
        self.tol = 0.080
        self.Manobra180V = False
        self._string_som_explosao = string_som_explosao
        self._audio = audio
       # self.even.lancar("tocarEfeito",self._audio)
        
        self.distanciaReacao = 30
        
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
    
    def explosao(self):
        self.rot.setAngulo(-self.rot.getAngulo())
        self.even.lancar("tocarEfeito",self._string_som_explosao)
    
        
    def atualiza(self,dt):
    
        self.mira(dt)
        self.voarSimples(dt)
        """if self.Pos.distancia2(self.alvoPos) > self.distanciaReacao:
            self.perseguir()
            self.aim()
            
        self.voar(dt)"""
    
    
    

class TorreInimiga(IA,motor.Figura):
    
    def __init__(self,img,string_som_disparo,string_som_fallShell,
                 arma,PV, pos, vel, alvoPos,
                 alvoVel,
                 deltaAngTol): 
        IA.__init__(self,arma, PV, pos, vel, alvoPos,
                 alvoVel,
                 deltaAngTol, string_som_disparo,string_som_fallShell)
        motor.Figura.__init__(self,img)
        """
        img:     É a string do nome do arquivo imagem da Torre inimiga
        string_som_disparo:   É a string do nome do arquivo audio do disparo
        alvoPos: (posXdoJogador,posYdoJogador)
        alvoVel: (velXdoJogador,velYdoJogador)
        arma:    Objeto do tipo Arma
        pos:     tupla de posicao da Torre Inimiga
        vel:     tupla de velocidade da Torre inimiga. No caso é sempre zero.
        ang:     inclinacao angular da reta definida 
                 pelo vetor velocidade da Torre Inimiga
        velAng:  velocidade angular da Torre inimiga
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
            deltaAngTol = motor.Angulo(erro)

        def atualiza(self,dt):
            self.mira(dt)
           
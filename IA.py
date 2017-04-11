# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 12:00:23 2017

@author: Dylan N. Sugimoto
"""
import motor
import math

velPadrao = 10 #constante de valor padrao de velocidade para IA
distanciaManobra = 300 #valor constante para distancia minima para realizar Manobra180V
distanciaPerseguir = 200#distancia maxima no qual IA comeca diminuir velocidade
aceleracaoAngular = 0.1#velocidade com que IA rotaciona
aceleracao = 1#rapidez com que IA aumenta a sua velocidade em X
desaceleracao = 1#rapidez com que IA diminui a sua velocidade em X

class IA():
    def __init__(self,arma, pos = motor.Ponto(0,0), vel=motor.Ponto(velPadrao,0), alvoPos = motor.Ponto(0,0),
                 alvoVel = motor.Ponto(0,0), ang = motor.Angulo(0), angUni = motor.Angulo(0), 
                 deltaAngTol = motor.Angulo(5)):
        """
        alvoPos: (posXdoJogador,posYdoJogador)
        alvoVel: (velXdoJogador,velYdoJogador)
        arma:    Objeto do tipo Arma
        pos:     tupla de posicao do IA
        vel:     tupla de velocidade do IA
        ang:     inclinacao angular da reta definida 
                 pelo vetor velocidade de IA
        angUni:  inclinacao angular da reta que uni
                 o alvo e a IA
        velAng:  velocidade angular de IA
        distanciaPerseguir: distancia minima para o qual o IA 
                            tenta estabelecer a mesma velocidade que a do Jogador
        deltaAngTol: angulo de tolerancia para disparo
        """
        self.Pos = pos
        self.Vel = vel
        self.ang = ang
        self.ang.setAngulo(math.atan2(vel[1],vel[0]))
        self.velAng = 0
        self.deltaAngTol = deltaAngTol
        self.arma = arma
        self.distanciaPerseguir = distanciaPerseguir
        self.distanciaManobra = distanciaManobra
        
        self.alvoPos = alvoPos
        self.alvoVel = alvoVel
        self.angUni = angUni
        
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
        
        difY = self.Pos.getY() - alvo[1]
        difX = self.Pos.getX() - alvo[0]
        self.angUni.set(math.atan2(difY,difX))
        
    def aim(self):
        """
        Diminui o angulo de visada para zero.
        E se o angulo de visada estiver dentro da tolerancia de disparo
        ,então, atira.
        """
        AngVisada = self.ang.getAngulo() - self.angUni.getAngulo()
        if AngVisada >0:
            self.velAng = -aceleracaoAngular
        elif AngVisada < 0 :
            self.velAng = +aceleracaoAngular
        elif AngVisada == 0:
            self.velAng = 0
        if AngVisada <= self.deltaAngTol:
            self.shoot()
 
    def shoot(self):
        """
        lanca evento de disparo.
        tupla_tiro: (PosicaodaIA, direcaoDeDIsparo,ObjetoArma)
        """
        tupla_tiro = (self.Pos.clonar(),self.ang.getAngulo(),
                     self.arma)
        self.even.lancar("Atirar",tupla_tiro)

class AviaoInimigo(IA,motor.Figura):
    
    
    def __init__(self,img,audio, arma, pos = motor.Ponto(0,0), vel=motor.Ponto(velPadrao,0), alvoPos = motor.Ponto(0,0),
                 alvoVel = motor.Ponto(0,0), ang = motor.Angulo(0), angUni = motor.Angulo(0), 
                 deltaAngTol = motor.Angulo(5)): 
        IA.__init__(self,arma, pos = motor.Ponto(0,0), vel=motor.Ponto(velPadrao,0), alvoPos = motor.Ponto(0,0),
                 alvoVel = motor.Ponto(0,0), ang = motor.Angulo(0), angUni = motor.Angulo(0), 
                 deltaAngTol = motor.Angulo(5))
        motor.Figura.__init__(img)
        """
        img:     É a string do nome do arquivo imagem do aviao
        audio:   É a string do nome do arquivo audio do aviao
        alvoPos: (posXdoJogador,posYdoJogador)
        alvoVel: (velXdoJogador,velYdoJogador)
        arma:    Objeto do tipo Arma
        pos:     tupla de posicao do IA
        vel:     tupla de velocidade do IA
        ang:     inclinacao angular da reta definida 
                 pelo vetor velocidade de IA
        angUni:  inclinacao angular da reta que uni
                 o alvo e a IA
        velAng:  velocidade angular de IA
        distanciaPerseguir: distancia minima para o qual o IA 
                            tenta estabelecer a mesma velocidade que a do Jogador
        deltaAngTol: angulo de tolerancia para disparo
        """
        
        self._audio = audio
        self.even.lancar("tocar_efeito",self._audio)

    def perseguir(self):
        """
        Ajusta a velocidade X da IA, de acordo com a posicao relativa 
        do Jogador com a IA
        """
        if self.Pos.getX() < self.alvoPos.getX() and self.Vel.getX() < 0:
               """
               Inverte a direcao de voo
               """
               if self.Pos.distancia2(self.alvoPos) > self.distanciaManobra:
                   self.Vel.setX(0)
                   self.even.lancar("Manobra180V",(self.Pos.clonar(), self.ang.getAngulo()))
                   self.Vel.setX(velPadrao)
               elif self.Vel.getX() >= self.alvoVel.getX():
                   acelX = self.Vel.getX() - aceleracao
                   self.Vel.setX(acelX)
        elif (self.Pos.getX() > self.alvoPos.getX()) and (self.Vel.getX() > 0):
              """
              Inverte a direcao de voo
              """
              if self.Pos.distancia2(self.alvoPos) > self.distanciaManobra:
                  self.Vel.setX(0)
                  self.even.lancar("Manobra180V",(self.Pos.clonar(), self.ang.getAngulo()))
                  self.Vel.setX(-velPadrao)
              elif self.Vel.getX() <= self.alvoVel.getX():
                  acelX = self.Vel.getX() + aceleracao
                  self.Vel.setX(acelX)   
                   
        elif self.Pos.distancia2(self.alvoPos) <self.distanciaPerseguir:
            """
            se tiver a uma certa distancia, diminui a sua velocidade 
            para igualar à velocidade do jogador.
            """
            if self.Vel.getX() > self.alvoVel.getX() and self.Vel.getX()>0:
                acelX = self.Vel.getX() - desaceleracao
                if acelX >= self.alvoVel.getX() and acelX != 0:
                    self.Vel.setX(acelX)
                elif self.alvoVel.getX() != 0:
                    self.Vel.setX(self.alvoVel.getX())
            elif self.Vel.getX() < self.alvoVel.getX() and self.Vel.getX() < 0:
                acelX = self.Vel.getX() + desaceleracao
                if acelX <= self.alvoVel.getX() and acelX != 0:
                    self.Vel.setX(acelX)
                elif self.alvoVel.getX() != 0:
                    self.Vel.setX(self.alvoVel.getX())
    def voar(self):
       self.Pos.soma(self.Vel.getXY) #atualiza a posicao para o frame seguinte
       if self.Velang != 0: 
           """
           Se a velocidade angular nao for zero, tem que rotacionar a velocidade
           e a figura de um angulo igual ao modulo da velocidade angular.
           Logo, o novo Vx e novo Vy sao as projecoes do modulo de V.
           """
           ang = math.atan2(self.Vel.getY(),self.Vel.getX()) + self.Velang
           self.ang.setAngulo(ang,False) #novo angulo com a horizontal
           projX = self.Vel.distancia((0,0))*math.cos(self.ang.getAngulo(False))
           projY = self.Vel.distancia((0,0))*math.sin(self.ang.getAngulo(False))
           NovoVx = int(projX)#deve ser inteiro para alterar a posicao
           NovoVy = int(projY)#deve ser inteiro para posicao ser inteira (pixel)
           if NovoVx == 0 and projX!= 0:
               #se o truncamento zerar uma velocidade nao nula
               NovoVx = 1
           if  NovoVy == 0 and projY!= 0:
               #se o truncamento zerar uma velocidade nao nula
               NovoVy = 1
           self.Vel.setXY((NovoVx,NovoVy))
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 12:00:23 2017

@author: Dylan N. Sugimoto
"""
import motor
import math
from Vida import Vida 
velPadrao = -100 #constante de valor padrao de velocidade para IA
distanciaManobra = 400 #valor constante para distancia minima para realizar Manobra180V
distanciaPerseguir = 200#distancia maxima no qual IA comeca diminuir velocidade
aceleracaoAngular = 0.01#velocidade com que IA rotaciona
aceleracao = 1#rapidez com que IA aumenta a sua velocidade em X
desaceleracao = 1#rapidez com que IA diminui a sua velocidade em X
erro = 0 #erro angular aceitavel para atirar

class IA(motor.Renderizavel, Vida):
    def __init__(self,arma, PV, pos, vel, alvoPos,
                 alvoVel, ang, angUni, 
                 deltaAngTol):
        motor.Renderizavel.__init__(self)
        Vida.__init__(self,PV)
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
        
        if pos is None:
            pos = motor.Ponto(0,0)
        if vel is None:
            vel=motor.Ponto(velPadrao,0)
        if alvoPos is None:
            alvoPos = motor.Ponto(0,0)
        if alvoVel is None:
            alvoVel = motor.Ponto(0,0)
        if ang is None:
            ang = motor.Angulo(0)
        if angUni is None:
            angUni = motor.Angulo(0)
        if deltaAngTol is None:
            deltaAngTol = motor.Angulo(erro)
            
        self.Pos = pos
        self.Vel = vel
        self.ang = ang
        self.ang.setAngulo(math.atan2(vel.getY(),vel.getX()))
        self.velAng = 0
        self.deltaAngTol = deltaAngTol
        self.arma = arma
        self.distanciaPerseguir = distanciaPerseguir
        self.distanciaManobra = distanciaManobra
        
        self.alvoPos = alvoPos
        self.alvoVel = alvoVel
        self.angUni = angUni
        
        self.PV = PV
        
        self.distanciaMira = 300 #distancia em que IA ajusta a mira
        
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
        self.angUni.setAngulo(math.atan2(difY,difX),False)
        
    def aim(self):
        """
        Diminui o angulo de visada para zero.
        E se o angulo de visada estiver dentro da tolerancia de disparo
        ,então, atira.
        """
        AngVisada = self.ang.getAngulo() - self.angUni.getAngulo()
           
        if self.Vel.getX() > 0 and self.Pos.getX() >= self.alvoPos.getX():
            #Se o jogador estiver nas costas da IA
            if self.ang.getAngulo() == 0:
                #e IA estiver na horizontal,
                #IA mantem a direcao da velocidade
                self.velAng = 0
            elif self.ang.getAngulo() >0:
                #e IA estiver subindo
                #IA tenta voltar para voo horizontal
                self.velAng = -aceleracaoAngular
            elif self.ang.getAngulo() < 0:
                #e IA estiver descendo
                #IA tenta voltar para voo horizontal
                self.velAng = +aceleracaoAngular
                
        elif self.Vel.getX() < 0 and self.Pos.getX() <= self.alvoPos.getX():
            #Se o jogador estiver nas costas da IA
            if self.ang.getAngulo() == 0:
                #e IA estiver na horizontal,
                #IA mantem a direcao da velocidade
                self.velAng = 0
            elif self.ang.getAngulo() >0:
                #e IA estiver subindo
                #IA tenta voltar para voo horizontal
                self.velAng = -aceleracaoAngular
            elif self.ang.getAngulo() < 0:
                #e IA estiver descendo
                #IA tenta voltar para voo horizontal
                self.velAng = +aceleracaoAngular
        else:
            #Ajustando a mira
            if AngVisada >0 and self.alvoPos.getX() - self.Pos.getX()> self.distanciaMira:
                self.velAng = -aceleracaoAngular
            elif AngVisada < 0 and self.Pos.getX() - self.alvoPos.getX()>self.distanciaMira:
                self.velAng = +aceleracaoAngular
            elif AngVisada == 0:
                self.velAng = 0
            if AngVisada <= self.deltaAngTol.getAngulo():
               #Atirar
               self.shoot()
           
                
        
        
        
    def shoot(self):
        """
        lanca evento de disparo.
        tupla_tiro: (PosicaodaIA, direcaoDeDIsparo,ObjetoProjetil)
        """
        projetil = self.arma.getProjetil()
        posInicialProjetil = self.Pos.clonar()
        posInicialProjetil.setXY(posInicialProjetil.getX()+self.Vel.getX(),
                                 posInicialProjetil.getY()+self.Vel.getY())
        projetil.Disparo(posInicialProjetil,self.ang.getAngulo())
        self.even.lancar("Atirar",projetil)

class AviaoInimigo(IA,motor.Figura):
    
    
    def __init__(self,img1,img2, audio, arma, pos,PV, vel, alvoPos,
                 alvoVel, ang, angUni, 
                 deltaAngTol): 
        IA.__init__(self,arma,PV, pos, vel, alvoPos,
                 alvoVel, ang, angUni, 
                 deltaAngTol)
        motor.Figura.__init__(self,img1)
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
        if ang is None:
            ang = motor.Angulo(0)
        if angUni is None:
            angUni = motor.Angulo(0)
        if deltaAngTol is None:
            deltaAngTol = motor.Angulo(erro)
            
        self.img1 = img1
        self.img2 = img2
        
        self.Manobra180V = False
        
        self._audio = audio
        self.even.lancar("tocar_efeito",self._audio)
        
        self.distanciaReacao = 30
        
    def realizarManobra180V(self):
        
        if not self.Manobra180V:
            #Troca a imagem
            self.setString(self.img2)
            #troca o estado na manobra
            #voando para direita
            self.Manobra180V = True
            
        elif self.Manobra180V:
            #Troca a imagem
            self.setString(self.img1)
            #Troca o estado da manobra
            #voando pra esquerda
            self.Manobra180V = False
        #calcula novo angulo da imagem    
        novoRot = - self.ang.getAngulo()
        #atualiza o angulo da imagem
        self.rot.setAngulo(novoRot)
  
    def perseguir(self):
        """
        Ajusta a velocidade X da IA, de acordo com a posicao relativa 
        do Jogador com a IA
        """
        if (self.Pos.getX() < self.alvoPos.getX()) and (self.Vel.getX() < 0):
               """
               Inverte a direcao de voo
               """
               if self.alvoPos.getX() - self.Pos.getX() > self.distanciaManobra:
                   self.Vel.setX(0)
                   self.realizarManobra180V()
                   self.Vel.setX(-velPadrao)
               elif self.Vel.getX() >= self.alvoVel.getX():
                   acelX = self.Vel.getX() - aceleracao
                   self.Vel.setX(acelX)
        elif (self.Pos.getX() > self.alvoPos.getX()) and (self.Vel.getX() > 0):
              """
              Inverte a direcao de voo
              """
              if self.Pos.getX() - self.alvoPos.getX() > self.distanciaManobra:
                  self.Vel.setX(0)
                  self.realizarManobra180V()
                  self.Vel.setX(velPadrao)
              elif self.Vel.getX() <= self.alvoVel.getX():
                  acelX = self.Vel.getX() + aceleracao
                  self.Vel.setX(acelX)   
                   
        elif self.Pos.distancia2(self.alvoPos) <self.distanciaPerseguir:
            """
            se tiver a uma certa distancia, diminui a sua velocidade 
            para igualar à velocidade do jogador.
            """
            if self.Vel.getX() > self.alvoVel.getX() and self.Vel.getX()>0 and\
               self.Pos.getX()< self.alvoPos.getX():
                   
                acelX = self.Vel.getX() - desaceleracao
                if acelX >= self.alvoVel.getX() and acelX > 0:
                    self.Vel.setX(acelX)
                elif self.alvoVel.getX() > 0 and self.Vel.getX()<= self.alvoVel.getX():
                    self.Vel.setX(self.alvoVel.getX())
                
            elif self.Vel.getX() < self.alvoVel.getX() and self.Vel.getX() < 0\
                 and self.Pos.getX() > self.alvoPos.getX():
                acelX = self.Vel.getX() + desaceleracao
                if acelX <= self.alvoVel.getX() and acelX < 0:
                    self.Vel.setX(acelX)
                elif self.alvoVel.getX() < 0 and\
                    self.Vel.getX() > self.alvoVel.getX():
                        
                    self.Vel.setX(self.alvoVel.getX())
            
    def voar(self,dt):
        
       #atualiza a posicao para o frame seguinte
       acrescimoX = int(self.Vel.getX()*dt)
       acrescimoY = int(self.Vel.getY()*dt)
       self.Pos.soma(motor.Ponto(acrescimoX,acrescimoY)) 
       #atualiza a posicao da Figura
       self.pos.setXY(self.Pos.getX(),self.Pos.getY())       
       if self.velAng != 0: 
           """
           Se a velocidade angular nao for zero, tem que rotacionar a velocidade
           e a figura de um angulo igual ao modulo da velocidade angular.
           Logo, o novo Vx e novo Vy sao as projecoes do modulo de V.
           """
           ang = math.atan2(self.Vel.getY(),self.Vel.getX()) + self.velAng
           self.ang.setAngulo(ang,False) #novo angulo com a horizontal
           self.rot.setAngulo(self.ang.getAngulo())#atualiza o angulo da Figura
           projX = self.Vel.distancia(motor.Ponto(0,0))*math.cos(self.ang.getAngulo(False))
           projY = self.Vel.distancia(motor.Ponto(0,0))*math.sin(self.ang.getAngulo(False))
           NovoVx = int(projX)#deve ser inteiro para alterar a posicao
           NovoVy = int(projY)#deve ser inteiro para posicao ser inteira (pixel)
           if NovoVx == 0 and ((-math.pi/2)<self.ang.getAngulo()<(math.pi/2)):
               #se a velocidade horizontal for zerada
               #atribui um valor padrao
               NovoVx = -velPadrao
           elif NovoVx == 0 and ((math.pi/2)<self.ang.getAngulo() or\
                                 self.ang.getAngulo() <(-math.pi/2)):
               #se a velocidade horizontal for zerada
               #atribui um valor padrao
               NovoVx = velPadrao
           if  NovoVy == 0 and projY!= 0:
               #se o truncamento zerar a velocidade vertical nao nula
               NovoVy = 1
           self.Vel.setXY(NovoVx,NovoVy)
    
    def atualiza(self,dt):
        
        if self.Pos.distancia2(self.alvoPos) > self.distanciaReacao:
            self.perseguir()
            self.aim()
            
        self.voar(dt)

class TorreInimiga(IA,motor.Figura):
    
    def __init__(self,img,audio, arma,PV, pos, vel, alvoPos,
                 alvoVel, ang, angUni, 
                 deltaAngTol): 
        IA.__init__(self,arma, PV, pos, vel, alvoPos,
                 alvoVel, ang, angUni, 
                 deltaAngTol)
        motor.Figura.__init__(self,img)
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
        
        if pos is None:
            pos = motor.Ponto(0,0)
        if vel is None:
            vel=motor.Ponto(velPadrao,0)
        if alvoPos is None:
            alvoPos = motor.Ponto(0,0)
        if alvoVel is None:
            alvoVel = motor.Ponto(0,0)
        if ang is None:
            ang = motor.Angulo(0)
        if angUni is None:
            angUni = motor.Angulo(0)
        if deltaAngTol is None:
            deltaAngTol = motor.Angulo(erro)
            
        self._audio = audio
        self.even.lancar("tocar_efeito",self._audio)
       
        def apontar(self):
            #atualiza novo angulo
            novoAng = self.ang.getAngulo(False) + self.velAng
            if novoAng >=0:#para garantir que a turreta nao aponte para baixo
                self.ang.setAngulo(novoAng)#atualiza o angulo
                self.rot.setAngulo(self.ang.getAngulo())#atualiza angulo da FIgura
            
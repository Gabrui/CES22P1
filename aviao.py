#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 12:40:42 2017

@author: gabrui
"""

from motor import Figura, Ponto
import math

class Aviao(Figura):
    
    def __init__(self, string_imagem, pos0, c0,arma,string_som_fallShell):
        super().__init__(string_imagem, pos = pos0, centro = c0)
        
        self.arma = arma
        self._string_som_fallShell = string_som_fallShell
        
    def shoot(self,dt):
        """
        lanca evento de disparo.
        """

        #zera o contador
        self.dtAtirar =0
        self.disparar = False
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

class Jogador(Aviao):
    
    """
    #Funciona com 
    # 1º: Condições aerodinâmicas macro: [arrastoMax, sustMax, veloMax, 
    [gráficoDosCoeficientes] ]
    # 2º: Empuxo: [empuxoMax, forcaMotorMax, arrFrontHMax, atritoMotor, 
    arrFrontHRat, hVeloMax, hMassa]
    # 3º: Sistema Rotacional: [manobrabilidade, tElevadorMax, tEstabilizadorMax
    , tArrastoRotMax]
    # 4º: Inercia Macro: [massa, momentoInercia]
    # ([8000, 90000, 172],  [8000, 4000, 8000, 100, 0.3, 5400, 1],  
    [5, 50000, 5000/3, 100], [5000, 150])
    """
    def __init__(self, string_imagem, string_imagem_invertida, pos0, c0, 
                 aerMacro, empuxoMacro, rotMacro, inerciaMacro,arma,
                 string_som_fallShell):
        super().__init__(string_imagem, pos0, c0,arma,string_som_fallShell)
        self.img1 = string_imagem
        self.img2 = string_imagem_invertida
        
        #Constantes matemáticas
        self.radianosParaGraus      = 180 / math.pi
        self.grausParaRadianos      = math.pi/180
        
        #Informações de vôo
        self.altitude               = 0
        self.densidade              = 1.225
        self.DENSIDADEMAR           = 1.225
        self.pressao                = 10000
        self.temperatura            = 15
        self.velveld                = 0
        self.velmVelmDm             = 0
    
        #Arrasto da fuselagem e velocidade
        self.arrasto                = 0
        self.arrastoMax             = aerMacro[0]  #Requer inicialização.
        self.arrastoEsp             = 0
        self.velo                   = 0
        self.veloMax                = aerMacro[2] #Requer inicialização.
    
        #Empuxo e hélices
        self.hVelD                  = 0
        self.hVelmDm                = 0
        self.hArrastoRotacional     = 0
        #self.hArrastoRotacionalMax        #Requer inicialização.
        self.arrFrontH              = 0
        self.arrFrontHMax           = empuxoMacro[1] #Requer inicialização.
        self.hArrFrontRot           = 0
        self.empuxo                 = 0
        self.empuxoMax              = empuxoMacro[0] #Requer inicialização.
        self.percMotor              = 0
        #self.hArrFrontRotMax              #Requer inicialização
        self.hArrFrontRat           = empuxoMacro[4]   #Requer inicialização
        self.hForcaMotorMax         = empuxoMacro[2]   #Requer inicialização
        self.hAtritoMotor           = empuxoMacro[3]   #Requer inicialização
        self.hVelo                  = 0
        self.hVeloMax               = empuxoMacro[5]   #Requer inicialização.
        self.hMassa                 = empuxoMacro[6]   #Requer inicialização.
        self.empuxoMaxKef           = 0
    
        #Peso
        self.GRAVIDADE   = 9.80665
        self.massa       = inerciaMacro[0]       #Requer inicialização.
        self.peso        = 0
    
        #Sustentação
        self.sustentacao = 0
        self.sustEsp     = 0
        self.sustMax     = aerMacro[1] #Requer inicialização.
        self.angCtpCorr  = 0
        
        #Gráfico
        self.angAtaq     = 0
        self.constRatAer = [0, 0]         #Primeiro arrasto depois sustentação.
        self.graficoAngAtaq = [[-180,0.5,-0.5],[-90,45,-1],[-30,4,-1],
            [-22,2,-1],[-20,1.6,-4],[-17,1.2,-5],[-15,1,-4.5],[-6,0.3,-2], 
            [0,0,0],[6,0.3,3.5],[18,1.2,10],[19,1.5,10],[20,1.8,4],
            [26,2.5,-0.5],[30,4,-0.9],[90,45,-1],[180,1,-0.5]]
        # = aerMacro[3]
        
        #Localização Cartesiana
        self.xForca  = 0
        self.yForca  = 0
        self.xAcel   = 0
        self.yAcel   = 0
        self.xVel    = 150
        self.yVel    = 0
        self.sinA    = 0
        self.sinVelo = 0
        self.cosA    = 1
        self.cosVelo = 1
    
        #Torque
        self.manobrabilidade   = rotMacro[0] #Requer inicialização.
        self.elevador          = 0
        self.tElevador         = 0
        self.tElevadorMax      = rotMacro[1]  #Requer inicialização.
        self.torque            = 0
        self.tEstabilizador    = 0
        self.tEstabilizadorMax = rotMacro[2]  #Requer inicialização.
        self.tArrastoRot       = 0
        self.tArrastoRotMax    = rotMacro[3]  #Requer inicialização.
        self.momentoInercia    = inerciaMacro[1] #Requer inicialização.
        self.angVelo           = 0
        self.angVeloRad        = 0
        self.velocidadeAngular = 0
        self.aceleracaoAngular = 0
    
        #Renderização
        self.lado             = 1
        self.dx               = 0
        self.dy               = 0
        self.rotacao          = 0
        self.rotacaoRad       = 0
            
        #Constantes pós-calculadas
        self.kArr              = 0
        self.kSust             = 0
        
        
        self.velmVelmDm = self.veloMax * self.veloMax * self.DENSIDADEMAR
        self.hVelmDm = self.hVeloMax * self.hVeloMax * self.DENSIDADEMAR
        self.kArr = self.arrastoMax / self.velmVelmDm
        self.kSust = self.sustMax / self.velmVelmDm
        self.empuxoMaxKef = self.empuxoMax + self.arrFrontHMax
        self.hArrFrontRotMax = ((self.hForcaMotorMax - self.hAtritoMotor) * (
                (1 - self.hArrFrontRat) * self.arrFrontHMax /self.empuxoMaxKef)
        /(1 - ((1 - self.hArrFrontRat) * self.arrFrontHMax/self.empuxoMaxKef)))
        self.hArrastoRotacionalMax = (self.hForcaMotorMax +self.hArrFrontRotMax
        - self.hAtritoMotor)
        
        self.ativarEscuta()
        self.cima = False
        self.baixo = False
        self.direita = False
        self.esquerda = False
        self.virar = False
        self.dtVirar = 2
        self.dtVirarMin = 1
        
        self.disparar = False
        self.dtAtirar = 1
        self.dtAtirarMin = 2
        
    def ativarEscuta(self):
        #lancar pedido de escuta
        self.even.escutar("K_up", self._cCima)
        self.even.escutar("K_down", self._cBaixo)
        self.even.escutar("K_right", self._cDireita)
        self.even.escutar("K_left", self._cEsquerda)
        self.even.escutar("K_space", self._cVirar)
        self.even.escutar("K_f",self.disparo)
        
    def disparo(self,dt):
        self.disparar = True
    
    def _cCima(self, eventoTeclado):
        self.cima = True
        
    
    def _cBaixo(self, eventoTeclado):
        self.baixo = True
    
    
    def _cDireita(self, eventoTeclado):
        self.direita = True
    
    
    def _cEsquerda(self, eventoTeclado):
        self.esquerda = True
    
    
    def _cVirar(self, eventoTeclado):
        self.virar = True
    
    
    def inverterFigura(self):
        if self.getString() == self.img1:
            self.setString(self.img2)
        else:
            self.setString(self.img1)
    
    
    def calculus(self, dt):
        
        #CONTROLADOR:
        if self.cima:
            self.elevador = self.lado
        elif self.baixo:
            self.elevador = -self.lado
        else:
            self.elevador = 0
        if self.direita:
            self.percMotor += 0.5 * dt
        elif self.esquerda:
            self.percMotor -= 0.5 * dt
        if self.percMotor > 1:
            self.percMotor = 1 
        elif self.percMotor < 0:
            self.percMotor = 0
        if self.virar and self.dtVirar > self.dtVirarMin:
            self.lado *= -1
            self.inverterFigura()
            self.dtVirar = 0
            
        #DADOS ATMOSFÉRICOS:
        #altitude = 10000
        #temperatura = 15.04 - 0.00649 * altitude
        #pressao = 101.29 * Math.pow(((temperatura + 273.1)/288.08), 5.256)
        #densidade = pressao / (0.2869 * (temperatura + 273.1))

        #PREPROCESSAMENTO DE VELOCIDADE
        self.velo = math.sqrt((self.xVel * self.xVel) + (self.yVel *self.yVel))
        # É um nome para: velo * velo * densidade
        self.velveld = self.velo * self.velo * self.densidade
        self.hVelD = self.hVelo * self.hVelo * self.densidade

        #FORÇAS AERODINÂMICAS E PESO
        self._interpolar(self.angAtaq, self.constRatAer, self.graficoAngAtaq)                
        #https:#www.youtube.com/watch?v=dY3daNK1Tek
        self.arrasto = (self.kArr * self.velveld * (1 + self.constRatAer[0]) * 
                        (1 + self.arrastoEsp))  
        # angAtaqArr deverá ser definido covenientemente através de um gráfico.
        self.sustentacao = (self.kSust * self.velveld * 
                    (1 + self.constRatAer[1]) * (1 + self.sustEsp) * self.lado)
        # angAtaqSust idem
        self.peso = self.GRAVIDADE * self.massa
        self.arrFrontH = (self.arrFrontHMax * self.velveld) / (self.velmVelmDm)
        self.empuxo = ((self.hVelD / self.hVelmDm) * self.empuxoMaxKef
                       - self.arrFrontH)
        
        #ANGULOS DE ROTAÇÃO DE DE ATAQUE
        if self.velo > 0:
            self.angVeloRad = math.atan2(self.yVel, self.xVel)
        self.angVelo = self.angVeloRad * self.radianosParaGraus
        self.angAtaq = (self.angVelo - self.rotacao) * self.lado
        if self.angAtaq < -180:
                self.angAtaq += 360
        elif self.angAtaq > 180:
                self.angAtaq -= 360
        
        self.sinVelo = math.sin(self.angVeloRad)
        self.cosVelo = math.cos(self.angVeloRad)

        #MOTOR(EMPUXO)
        #Estabelece o limite para a velocidade da hélice
        self.hArrastoRotacional = (self.hArrastoRotacionalMax * self.hVelD 
                                   / self.hVelmDm)
        #A componente rotacional que o ar exerce nas hélices
        self.hArrFrontRot = self.velveld/self.velmVelmDm * self.hArrFrontRotMax
        # A velocidade rotacional das hélices
        if self.hVelo > 0:
            self.hVelo+=(((self.hForcaMotorMax*self.percMotor+self.hArrFrontRot 
              - (self.hAtritoMotor+self.hArrastoRotacional))/self.hMassa) * dt)
        else: 
            self.hVelo+=(((self.hForcaMotorMax*self.percMotor+self.hArrFrontRot 
              + (self.hAtritoMotor+self.hArrastoRotacional))/self.hMassa) * dt)
                         

        #ELEVADOR
        #angElevador += eleMotor - (angElevador / angElevadorMax) * 
        #       (velveld / velmVelmDm) * eleMotor * 0.8 #O ângulo do elevador
        #if (angElevador > angElevatorMax) {
        #    angElevator = angElevatorMax
        #}

        #TORQUE E VELOCIDADE ANGULAR
        #Deu SU-35: https:#www.youtube.com/watch?v=eFjO-kWuBBE para 
        #elevador*50000, angAtaq/40*50000, momentoInercia=200 sem tArrastoRot
        #* tElevadorMax * (angElevador / angElevadorMax) # Torque do elevador 
        #varia com a velocidade e a inclinação
        self.tElevador = ((self.velveld / self.velmVelmDm) * self.elevador 
                          * self.tElevadorMax)
        
        # Tende o avião à velocidade, no stall fica impossivel de virar com 
        #elevador
        self.tEstabilizador = ((self.velveld / self.velmVelmDm) * self.angAtaq 
                               * self.tEstabilizadorMax) * self.lado
        #* (angAtaq / angStall) * angElevadorMax 
        # Estabelece uma velocidade angular máxima, primeiro grau para 
        #conservar o sinal
        self.tArrastoRot = - self.velocidadeAngular * self.tArrastoRotMax
        #tElevadorMax * (veloAng * densidade) / (veloAngMax * DENSIDADEMAR) 
        # A força angular
        self.torque = (self.tElevador + self.tEstabilizador + self.tArrastoRot)
        self.aceleracaoAngular = self.torque / self.momentoInercia
        self.rotacao += (self.velocidadeAngular * dt 
                         + self.aceleracaoAngular*dt*dt/2)
        #Velocidade angular
        self.velocidadeAngular += self.aceleracaoAngular *dt
        if self.rotacao > 180:
            self.rotacao -= 360
        elif self.rotacao < -180:
            self.rotacao += 360
        self.rotacaoRad = self.rotacao * self.grausParaRadianos
        self.sinA = math.sin(self.rotacaoRad)
        self.cosA = math.cos(self.rotacaoRad)

        #INTEGRAÇÃO DAS FORÇAS E DA VELOCIDADE
        if self.velo != 0:
            self.angCtpCorr = dt*self.sustentacao/(2*self.massa*self.velo)
        self.xForca = (self.cosA * self.empuxo - self.cosVelo * self.arrasto + 
                math.sin(self.angVeloRad-self.angCtpCorr) * self.sustentacao)
        self.yForca = (self.sinA * self.empuxo + self.peso - 
                       math.cos(self.angVeloRad-self.angCtpCorr) * 
                       self.sustentacao - self.sinVelo * self.arrasto)
        self.xAcel = self.xForca / self.massa
        self.yAcel = self.yForca / self.massa
        self.dx = (self.xVel*dt + self.xAcel*dt*dt/2)
        self.dy = (self.yVel*dt + self.yAcel*dt*dt/2)
        self.xVel += self.xAcel * dt
        self.yVel += self.yAcel * dt
        
        # Reinicia Controle do Elevador e de eventos:
        self.elevador = 0
        self.cima = False
        self.baixo = False
        self.direita = False
        self.esquerda = False
        self.virar = False
        self.dtVirar += dt
        
    
    def _interpolar(self, entrada, saida, pontos):
        #Verificação de segurança
        quantPontPos = len(pontos)
        quantSaida = len(saida)
        if quantSaida < 1 or quantPontPos < 2 or entrada < pontos[0][0] or \
           entrada > pontos[quantPontPos-1][0]:
            return False
        
        #Faz uma busca binária em pontos, ficando a entrada contida entre inf 
        # e sup
        inf=0
        sup=quantPontPos-1
        med = (inf + sup) // 2
        while sup > inf+1:
            med = (inf + sup) // 2
            if pontos[med][0] > entrada:
                sup = med
            else:
                inf = med
        
        #Faz a interpolação linear para cada saida
        for i in range(quantSaida):
            saida[i] = (pontos[inf][i+1] + (pontos[sup][i+1]-pontos[inf][i+1]) 
            * (entrada - pontos[inf][0]) / (pontos[sup][0]-pontos[inf][0]))
        
        
        return True
    
    
    def atualiza(self, dt):
        
        self.dtAtirar +=dt
        if self.disparar and self.dtAtirar >= self.dtAtirarMin:
            self.shoot(dt)
        self.disparar = False
        self.calculus(dt)
        self.pos.soma(Ponto(self.dx, self.dy))
        self.rot.setAngulo(-self.rotacao)
        
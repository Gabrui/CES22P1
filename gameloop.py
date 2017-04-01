# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 19:29:56 2017

@author: Dylan N. Sugimoto
"""

import pygame

pygame.init()

def gameLoop():
    
  
    gameExit = False
    gameOver = False
    

    while not gameExit:
        
        if gameOver == True:
            """
            Apresentar tela de GameOver
            """
            pass
             
        for event in pygame.event.get():
            """
            Pegar as entradas, repassar os eventos
            ,executar os eventos.
            """
        """
        Calcular as novas posicoes das imagens
        Colocar as imagens da memoria
        Preencher o fundo
        Atualizar a tela
        """
  
        #clock.tick(FPS) define o FPS do jogo
        
    """
    Fazer chamada da próxima cena
    ou sair
    """
   
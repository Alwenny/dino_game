import pygame
from sys import exit
import os
from random import choice
from config import * 
from sprites import *     
from interface import *
from bd import BancoDeDados

class Jogo:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption('Dino Game POO')
        self.relogio = pygame.time.Clock()
        self.rodando = True

        self.som_colisao = pygame.mixer.Sound(os.path.join(DIRETORIO_SONS, 'death_sound.wav'))
        self.som_pontuacao = pygame.mixer.Sound(os.path.join(DIRETORIO_SONS, 'score_sound.wav'))
        
        self.caixa_nome = CaixaTexto((LARGURA/2) - 100, (ALTURA/2), 200, 50)

        largura_botao = 150
        altura_botao = 50

        self.botao_jogar = Botao((LARGURA/2) - (largura_botao/2), (ALTURA/2) + 80, largura_botao, altura_botao, "Jogar")
        
        self.banco = BancoDeDados()

        self.exibindo_ranking = False
        self.lista_ranking = []

        self.novo_jogo()

    def novo_jogo(self):
        self.velocidade_jogo = 10
        self.pontos = 0
        self.colidiu = False
        self.escolha_obstaculo = choice([0, 1])

        self.todas_as_sprites = pygame.sprite.Group()
        self.grupo_obstaculos = pygame.sprite.Group()

        self.dino = Dino()
        self.todas_as_sprites.add(self.dino)

        for i in range(4):
            nuvem = Nuvens()
            self.todas_as_sprites.add(nuvem)
        
        for i in range(LARGURA*2//64):
            chao = Chao(i)
            self.todas_as_sprites.add(chao)

        self.cacto = Cacto()
        self.dino_voador = DinoVoador()
        
        self.todas_as_sprites.add(self.cacto)
        self.todas_as_sprites.add(self.dino_voador)
        
        self.grupo_obstaculos.add(self.cacto)
        self.grupo_obstaculos.add(self.dino_voador)

    def run(self):
        while True:
            self.relogio.tick(30)
            self.eventos()
            self.atualizar()
            self.desenhar()

    def eventos(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                if self.exibindo_ranking:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.botao_jogar.foi_clicado(pygame.mouse.get_pos()):
                            self.novo_jogo()
                            self.exibindo_ranking = False 

                elif self.colidiu:
                    self.caixa_nome.tratar_evento(event)
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.botao_jogar.foi_clicado(pygame.mouse.get_pos()):
                            self.salvar_pontuacao()

                            self.lista_ranking = self.banco.consultar_melhores()
                            
                            self.exibindo_ranking = True 
                            
                            self.caixa_nome.texto = ""

                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if self.dino.rect.y == self.dino.pos_y_inicial:
                                self.dino.pular()

    def atualizar(self):
        if not self.colidiu:
            self.todas_as_sprites.update()
            
            self.cacto.velocidade = self.velocidade_jogo
            self.dino_voador.velocidade = self.velocidade_jogo
            for sprite in self.todas_as_sprites:
                if isinstance(sprite, Nuvens):
                    sprite.velocidade = self.velocidade_jogo

            self.pontos += 1

            if self.cacto.rect.topright[0] <= 0 or self.dino_voador.rect.topright[0] <= 0:
                self.escolha_obstaculo = choice([0, 1])
                self.cacto.rect.x = LARGURA
                self.dino_voador.rect.x = LARGURA
                self.cacto.escolha = self.escolha_obstaculo
                self.dino_voador.escolha = self.escolha_obstaculo

            if self.pontos % 100 == 0:
                self.som_pontuacao.play()
                if self.velocidade_jogo < 23:
                    self.velocidade_jogo += 1

            colisoes = pygame.sprite.spritecollide(self.dino, self.grupo_obstaculos, False, pygame.sprite.collide_mask)
            if colisoes:
                self.som_colisao.play()
                self.colidiu = True

    def desenhar_texto(self, texto, tamanho, cor, x, y):
        fonte = Fonte.get(tamanho)
        texto_surf = fonte.render(texto, True, cor)

        rect = texto_surf.get_rect()
        rect.midtop = (x, y)
        self.tela.blit(texto_surf, rect)

    def desenhar(self):
        if not self.colidiu:
            self.tela.fill(BRANCO)
            self.todas_as_sprites.draw(self.tela)
            self.desenhar_texto(str(self.pontos), 40, PRETO, 520, 30)
        
        elif self.exibindo_ranking:
            self.tela.fill(BRANCO)
            
            self.desenhar_texto('TOP 5 JOGADORES', 30, PRETO, LARGURA//2, 50)
            
            pos_y = 100
            for i, jogador in enumerate(self.lista_ranking):
                texto = f"{i+1}º {jogador[0]} ..... {jogador[1]}"
                self.desenhar_texto(texto, 20, PRETO, LARGURA//2, pos_y)
                pos_y += 40 
            
            self.botao_jogar.desenhar(self.tela)

        else:
            self.tela.fill(BRANCO)

            self.desenhar_texto('GAME OVER', 40, PRETO, LARGURA//2, ALTURA//2 - 150)
            self.desenhar_texto(f'Sua Pontuação: {self.pontos}', 20, PRETO, LARGURA//2, ALTURA//2 - 100)
            self.desenhar_texto('Digite seu nome:', 15, PRETO, LARGURA//2, ALTURA//2 - 30)
            
            self.caixa_nome.desenhar(self.tela)

            self.botao_jogar.desenhar(self.tela)

        pygame.display.flip()

    def salvar_pontuacao(self):
        if self.caixa_nome.texto != "" and self.pontos > 0:
            
            self.banco.inserir_recorde(self.caixa_nome.texto, self.pontos)

if __name__ == '__main__':
    jogo = Jogo()
    jogo.run()


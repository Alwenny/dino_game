import pygame
from config import *
import os


class Fonte:
    @staticmethod
    def get(tamanho):
        caminho = os.path.join(DIRETORIO_FONTE, 'PressStart2P-Regular.ttf')
        return pygame.font.Font(caminho, tamanho)

class Botao:
    def __init__(self, x, y, largura, altura, texto):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor = CINZA
        self.texto = texto
        self.font = Fonte.get(20)

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, self.rect)
        img_texto = self.font.render(self.texto, True, PRETO)
        rect_texto = img_texto.get_rect(center=self.rect.center)
        tela.blit(img_texto, rect_texto)

    def foi_clicado(self, pos_mouse):
        if self.rect.collidepoint(pos_mouse):
            return True
        else:
            return False
        
class CaixaTexto:
    def __init__(self, x, y, largura, altura):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor_inativa = CINZA
        self.cor_ativa = CINZA_CLARO
        self.cor_atual = self.cor_inativa
        self.texto = ''
        self.ativo = False
        self.font = Fonte.get(20)

    def tratar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(evento.pos):
                self.ativo = not self.ativo
            else:
                self.ativo = False

            self.cor_atual = self.cor_ativa if self.ativo else self.cor_inativa
        
        if evento.type == pygame.KEYDOWN:
            if self.ativo:
                if evento.key == pygame.K_RETURN:
                    print(self.texto)
                elif evento.key == pygame.K_BACKSPACE:
                    self.texto = self.texto[:-1]
                else:
                    if len(self.texto) < 3:
                        self.texto += evento.unicode
    
    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor_atual, self.rect)
        pygame.draw.rect(tela, PRETO, self.rect, 2)
        img_texto = self.font.render(self.texto, True, PRETO)
        tela.blit(img_texto, (self.rect.x + 5, self.rect.y + 15))

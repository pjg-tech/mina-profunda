"""Efeitos visuais: partículas (pedacinhos de pedra) e textos que sobem ("+30")."""

import random

import pygame

from config import AMARELO, PRETO


class Particula:
    """Pedacinho de pedra que é jogado para cima e cai com gravidade."""

    def __init__(self, x, y, cor):
        self.x = x
        self.y = y
        self.vx = random.uniform(-200, 200)   # velocidade horizontal (pixels por segundo)
        self.vy = random.uniform(-350, -50)   # velocidade vertical (negativa = para cima)
        self.cor = cor
        self.vida = random.uniform(0.4, 0.9)  # segundos até sumir

    def atualizar(self, dt):
        """Move a partícula e aplica a gravidade."""
        self.vy = self.vy + 700 * dt   # gravidade puxa para baixo
        self.x = self.x + self.vx * dt
        self.y = self.y + self.vy * dt
        self.vida = self.vida - dt

    def desenhar(self, tela):
        """Desenha um quadradinho."""
        pygame.draw.rect(tela, self.cor, (int(self.x), int(self.y), 5, 5))


class TextoFlutuante:
    """Texto que sobe e vai ficando transparente até sumir."""

    def __init__(self, x, y, texto, cor, fonte):
        self.x = x
        self.y = y
        self.imagem = fonte.render(texto, True, cor)
        self.sombra = fonte.render(texto, True, PRETO)
        self.vida = 1.0   # segundos até sumir

    def atualizar(self, dt):
        """Sobe 60 pixels por segundo."""
        self.y = self.y - 60 * dt
        self.vida = self.vida - dt

    def desenhar(self, tela):
        """Desenha o texto centralizado, cada vez mais transparente."""
        transparencia = max(0, int(255 * self.vida))   # 255 = opaco, 0 = invisível
        self.imagem.set_alpha(transparencia)
        self.sombra.set_alpha(transparencia)
        x = self.x - self.imagem.get_width() // 2
        tela.blit(self.sombra, (x + 2, self.y + 2))
        tela.blit(self.imagem, (x, self.y))


class Efeitos:
    """Guarda todos os efeitos ativos, atualiza e apaga os que acabaram."""

    def __init__(self, fonte):
        self.fonte = fonte
        self.lista = []   # partículas e textos juntos: todos têm atualizar, desenhar e vida

    def explosao(self, x, y, cor, quantidade=15):
        """Cria várias partículas saindo de um ponto."""
        for i in range(quantidade):
            if len(self.lista) < 400:   # limite para o jogo não ficar lento
                self.lista.append(Particula(x, y, cor))

    def texto(self, x, y, texto, cor=AMARELO):
        """Cria um texto flutuante."""
        self.lista.append(TextoFlutuante(x, y, texto, cor, self.fonte))

    def atualizar(self, dt):
        """Atualiza todos e mantém só os que ainda têm vida."""
        for efeito in self.lista:
            efeito.atualizar(dt)
        vivos = []
        for efeito in self.lista:
            if efeito.vida > 0:
                vivos.append(efeito)
        self.lista = vivos

    def desenhar(self, tela):
        """Desenha todos os efeitos."""
        for efeito in self.lista:
            efeito.desenhar(tela)

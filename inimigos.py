"""Coisas que aparecem na mina: ladrões e pedras que caem (perigos) e minérios raros (bônus)."""

import random

import pygame

from config import ALTURA, CENTRO_ROCHA, LARGURA_MINA


class Ladrao:
    """Atravessa a tela. Precisa de 3 cliques para ser derrotado.

    Se chegar ao outro lado, foge e rouba 10% do minério.
    Nas Cavernas e nos Cristais é um morcego; no Magma, uma bola de fogo.
    """

    def __init__(self, numero_camada):
        if random.random() < 0.5:   # 50% de chance de vir de cada lado
            self.x = -40
            self.velocidade = 110 + 25 * numero_camada
        else:
            self.x = LARGURA_MINA + 40
            self.velocidade = -(110 + 25 * numero_camada)
        self.y = random.randint(130, ALTURA - 160)
        self.vida = 3
        self.eh_fogo = numero_camada == 3
        self.tempo = 0
        self.vivo = True
        self.fugiu = False

    def atualizar(self, dt):
        """Anda em linha reta. Se sair da tela, fugiu."""
        self.tempo = self.tempo + dt
        self.x = self.x + self.velocidade * dt
        if self.x < -60 or self.x > LARGURA_MINA + 60:
            self.vivo = False
            self.fugiu = True

    def contem(self, posicao):
        """True se a posição do clique está em cima do ladrão (dentro de um raio de 30 px)."""
        dx = posicao[0] - self.x
        dy = posicao[1] - self.y
        return dx * dx + dy * dy <= 30 * 30

    def acertar(self):
        """Tira uma vida. Devolve True se o ladrão foi derrotado."""
        self.vida = self.vida - 1
        if self.vida <= 0:
            self.vivo = False
            return True
        return False

    def desenhar(self, tela):
        """Desenha o morcego (ou a bola de fogo) e uma barrinha com as vidas que faltam."""
        x = int(self.x)
        y = int(self.y)
        quadro = int(self.tempo * 10) % 2   # alterna entre 0 e 1, dez vezes por segundo
        if self.eh_fogo:
            raio = 24 if quadro == 0 else 20
            pygame.draw.circle(tela, (255, 90, 20), (x, y), raio)
            pygame.draw.circle(tela, (255, 190, 50), (x, y), raio - 8)
        else:
            asa = -14 if quadro == 0 else 4   # asa para cima ou para baixo
            pygame.draw.polygon(tela, (45, 35, 55), [(x - 8, y), (x - 34, y + asa), (x - 22, y + 6)])
            pygame.draw.polygon(tela, (45, 35, 55), [(x + 8, y), (x + 34, y + asa), (x + 22, y + 6)])
            pygame.draw.ellipse(tela, (45, 35, 55), (x - 11, y - 13, 22, 26))
            pygame.draw.circle(tela, (255, 60, 60), (x - 4, y - 4), 3)
            pygame.draw.circle(tela, (255, 60, 60), (x + 4, y - 4), 3)
        for i in range(self.vida):
            pygame.draw.rect(tela, (230, 70, 60), (x - 15 + i * 11, y - 32, 9, 4))


class PedraCaindo:
    """Pedra que cai do teto na cabeça do minerador. Clique nela para destruir antes que acerte."""

    def __init__(self, x, y_alvo, cor):
        self.x = x
        self.y = -30
        self.y_alvo = y_alvo   # altura da cabeça do minerador
        self.cor = cor
        self.vivo = True
        self.acertou = False

    def atualizar(self, dt):
        """Cai 150 pixels por segundo. Ao chegar na cabeça do minerador, acertou."""
        self.y = self.y + 150 * dt
        if self.y >= self.y_alvo:
            self.vivo = False
            self.acertou = True

    def contem(self, posicao):
        """True se a posição do clique está em cima da pedra."""
        dx = posicao[0] - self.x
        dy = posicao[1] - self.y
        return dx * dx + dy * dy <= 26 * 26

    def desenhar(self, tela):
        """Desenha a pedra e uma sombra na cabeça do minerador, avisando onde ela vai cair."""
        pygame.draw.ellipse(tela, (20, 15, 15), (self.x - 18, self.y_alvo - 4, 36, 8))
        x = int(self.x)
        y = int(self.y)
        pontos = [(x - 16, y - 6), (x - 4, y - 16), (x + 14, y - 10), (x + 16, y + 8), (x, y + 16), (x - 14, y + 10)]
        pygame.draw.polygon(tela, self.cor, pontos)
        pygame.draw.polygon(tela, (30, 25, 25), pontos, 2)


class MinerioRaro:
    """Pedra brilhante que aparece por alguns segundos. Clicar nela dá um bônus grande."""

    def __init__(self, cor, duracao):
        self.cor = cor
        self.duracao = duracao
        self.tempo = 0
        self.vivo = True
        # Sorteia uma posição até achar uma que fique longe da rocha principal
        while True:
            self.x = random.randint(50, LARGURA_MINA - 50)
            self.y = random.randint(130, ALTURA - 60)
            dx = self.x - CENTRO_ROCHA[0]
            dy = self.y - CENTRO_ROCHA[1]
            if dx * dx + dy * dy > 140 * 140:
                break

    def atualizar(self, dt):
        """Some depois de 'duracao' segundos."""
        self.tempo = self.tempo + dt
        if self.tempo >= self.duracao:
            self.vivo = False

    def contem(self, posicao):
        """True se a posição do clique está em cima da pedra brilhante."""
        dx = posicao[0] - self.x
        dy = posicao[1] - self.y
        return dx * dx + dy * dy <= 28 * 28

    def desenhar(self, tela):
        """Desenha um losango brilhante. Pisca quando falta pouco para sumir."""
        falta = self.duracao - self.tempo
        if falta < 1.5 and int(falta * 10) % 2 == 0:
            return   # neste quadro não desenha: assim ela pisca
        x = self.x
        y = self.y
        losango = [(x, y - 20), (x + 14, y), (x, y + 20), (x - 14, y)]
        pygame.draw.circle(tela, (255, 255, 200), (x, y), 28, 2)
        pygame.draw.polygon(tela, self.cor, losango)
        pygame.draw.polygon(tela, (255, 255, 255), losango, 2)

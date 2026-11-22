"""A rocha que o jogador quebra clicando."""

import random

import pygame

from config import BRANCO, CENTRO_ROCHA, RAIO_ROCHA
from ui import clarear, escurecer

# Formato da rocha: pontos em volta do centro (x, y). Formam um polígono irregular.
FORMATO = [(-60, -75), (30, -85), (80, -30), (85, 40), (30, 85), (-50, 80), (-85, 20), (-80, -45)]

# Rachaduras: linhas que aparecem conforme a rocha perde vida
RACHADURAS = [((0, 0), (-40, -35)), ((0, 0), (40, -40)), ((-5, 5), (30, 50)),
              ((0, 0), (-50, 30)), ((5, 0), (60, 10))]


class Rocha:
    """Rocha com vida. Quando a vida acaba, ela quebra e volta com vida cheia."""

    def __init__(self, camada):
        self.cor = camada.cor_rocha
        self.cor_minerio = camada.cor_minerio
        self.vida_max = camada.vida
        self.vida = self.vida_max
        self.tempo_pulo = 0   # maior que 0 enquanto a rocha está "encolhida" depois de um clique
        self.sortear_manchas()

    def sortear_manchas(self):
        """Sorteia onde ficam as manchas de minério (muda a cada rocha nova)."""
        self.manchas = []
        for i in range(7):
            x = random.randint(-50, 50)
            y = random.randint(-50, 50)
            raio = random.randint(7, 14)
            self.manchas.append((x, y, raio))

    def receber_dano(self, dano):
        """Tira vida da rocha. Devolve quantas rochas quebraram.

        Pode quebrar mais de uma de uma vez se o dano for maior que a vida.
        """
        self.vida = self.vida - dano
        quebradas = 0
        while self.vida <= 0:
            quebradas = quebradas + 1
            self.vida = self.vida + self.vida_max   # rocha nova (sobra do dano continua valendo)
        if quebradas > 0:
            self.sortear_manchas()
        return quebradas

    def bater(self):
        """Faz a rocha encolher um pouco (efeito de clique)."""
        self.tempo_pulo = 0.08

    def contem(self, posicao):
        """True se a posição está dentro do círculo da rocha (teorema de Pitágoras)."""
        dx = posicao[0] - CENTRO_ROCHA[0]
        dy = posicao[1] - CENTRO_ROCHA[1]
        return dx * dx + dy * dy <= RAIO_ROCHA * RAIO_ROCHA

    def atualizar(self, dt):
        """Conta o tempo do efeito de clique."""
        self.tempo_pulo = max(0, self.tempo_pulo - dt)

    def desenhar(self, tela):
        """Desenha sombra, rocha, manchas de minério, rachaduras e barra de vida."""
        cx, cy = CENTRO_ROCHA
        escala = 0.9 if self.tempo_pulo > 0 else 1.0   # encolhe 10% depois do clique

        pygame.draw.ellipse(tela, (15, 10, 8), (cx - 80, cy + 62, 160, 30))   # sombra no chão

        pontos = []
        for x, y in FORMATO:
            pontos.append((cx + x * escala, cy + y * escala))
        pygame.draw.polygon(tela, self.cor, pontos)
        pygame.draw.polygon(tela, escurecer(self.cor, 55), pontos, 4)   # contorno

        for x, y, raio in self.manchas:
            centro = (cx + x * escala, cy + y * escala)
            pygame.draw.circle(tela, self.cor_minerio, centro, raio)
            pygame.draw.circle(tela, clarear(self.cor_minerio, 80), (centro[0] - 3, centro[1] - 3), raio // 3)

        # Quanto menos vida, mais rachaduras aparecem
        dano = 1 - self.vida / self.vida_max            # 0 = inteira, 1 = quase quebrando
        quantas = int(dano * (len(RACHADURAS) + 1))
        for inicio, fim in RACHADURAS[:quantas]:
            pygame.draw.line(tela, escurecer(self.cor, 85), (cx + inicio[0], cy + inicio[1]),
                             (cx + fim[0], cy + fim[1]), 3)

        # Barra de vida
        x = cx - 80
        y = cy + RAIO_ROCHA + 25
        pygame.draw.rect(tela, (30, 30, 30), (x, y, 160, 12), border_radius=6)
        pygame.draw.rect(tela, (90, 200, 90), (x, y, int(160 * self.vida / self.vida_max), 12), border_radius=6)
        pygame.draw.rect(tela, BRANCO, (x, y, 160, 12), 1, border_radius=6)

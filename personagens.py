"""Personagens da mina: o minerador do jogador e os ajudantes comprados na loja."""

import pygame

from config import CENTRO_ROCHA, CHAO, MINERADOR_X, RAIO_ROCHA

PELE = (240, 195, 150)
MADEIRA = (120, 80, 40)
FERRO = (175, 180, 190)

# As duas posições do braço com a picareta, como deslocamentos (dx, dy) a partir dos pés.
# Trocar de uma posição para a outra dá a impressão de movimento.
PICARETA_LEVANTADA = {"mao": (-10, -77), "cabo": (-25, -103), "ferro": ((-11, -111), (-39, -95))}
PICARETA_ABAIXADA = {"mao": (25, -48), "cabo": (53, -38), "ferro": ((47, -23), (59, -53))}


class Minerador:
    """Personagem do jogador. Bate a picareta na rocha a cada clique."""

    def __init__(self):
        self.tempo_golpe = 0   # > 0 enquanto a picareta está abaixada
        self.atordoado = 0     # > 0 enquanto está tonto (levou uma pedra na cabeça)

    def golpear(self):
        """Abaixa a picareta por um instante."""
        self.tempo_golpe = 0.1

    def atordoar(self, segundos):
        """Deixa o minerador tonto (sem conseguir minerar) por alguns segundos."""
        self.atordoado = segundos

    def atualizar(self, dt):
        """Diminui os temporizadores."""
        self.tempo_golpe = max(0, self.tempo_golpe - dt)
        self.atordoado = max(0, self.atordoado - dt)

    def ponto(self, deslocamento):
        """Transforma um deslocamento (dx, dy) em posição na tela, a partir dos pés do minerador."""
        return (MINERADOR_X + deslocamento[0], CHAO + deslocamento[1])

    def desenhar(self, tela, picareta_quente=False):
        """Desenha o minerador com retângulos, círculos e linhas."""
        x = MINERADOR_X
        # Pernas, botas, corpo e cinto
        pygame.draw.rect(tela, (60, 60, 95), (x - 12, CHAO - 30, 10, 26))
        pygame.draw.rect(tela, (60, 60, 95), (x + 2, CHAO - 30, 10, 26))
        pygame.draw.rect(tela, (70, 45, 25), (x - 14, CHAO - 6, 28, 6))
        pygame.draw.rect(tela, (200, 80, 40), (x - 15, CHAO - 62, 30, 34), border_radius=6)
        pygame.draw.rect(tela, (80, 50, 30), (x - 15, CHAO - 34, 30, 5))
        # Cabeça, olho, capacete e lanterna do capacete
        pygame.draw.circle(tela, PELE, (x, CHAO - 75), 13)
        pygame.draw.circle(tela, (30, 30, 30), (x + 6, CHAO - 77), 2)
        pygame.draw.rect(tela, (240, 200, 40), (x - 14, CHAO - 94, 28, 14), border_radius=7)
        pygame.draw.rect(tela, (200, 160, 30), (x - 17, CHAO - 82, 34, 4))
        pygame.draw.circle(tela, (255, 255, 210), (x + 9, CHAO - 88), 4)

        # Braço e picareta: escolhe a posição conforme está golpeando ou não
        if self.tempo_golpe > 0:
            pose = PICARETA_ABAIXADA
        else:
            pose = PICARETA_LEVANTADA
        ombro = (x + 2, CHAO - 56)
        mao = self.ponto(pose["mao"])
        cabo = self.ponto(pose["cabo"])
        ferro1 = self.ponto(pose["ferro"][0])
        ferro2 = self.ponto(pose["ferro"][1])
        pygame.draw.line(tela, PELE, ombro, mao, 7)
        pygame.draw.line(tela, MADEIRA, mao, cabo, 5)
        if picareta_quente:
            pygame.draw.line(tela, (255, 80, 40), ferro1, ferro2, 6)   # ferro vermelho de quente
        else:
            pygame.draw.line(tela, FERRO, ferro1, ferro2, 6)

        # Estrelinhas em cima da cabeça quando está tonto
        if self.atordoado > 0:
            for dx in (-15, 0, 15):
                pygame.draw.circle(tela, (255, 230, 80), (x + dx, CHAO - 105 - abs(dx) // 3), 4)


class Ajudantes:
    """Desenha os ajudantes comprados na loja, para o jogador VER o que comprou."""

    def __init__(self):
        self.tempo = 0
        self.carrinho_x = 100
        self.carrinho_velocidade = 80   # pixels por segundo (negativo = para a esquerda)

    def atualizar(self, dt):
        """Conta o tempo e move o carrinho de um lado para o outro."""
        self.tempo = self.tempo + dt
        self.carrinho_x = self.carrinho_x + self.carrinho_velocidade * dt
        if self.carrinho_x > 620 or self.carrinho_x < 60:
            self.carrinho_velocidade = -self.carrinho_velocidade   # bateu na ponta: inverte

    def desenhar_atras(self, tela, loja, cor_minerio):
        """Ajudantes que ficam atrás da rocha: carrinho e laser."""
        if loja.nivel("carrinho") > 0:
            self.desenhar_carrinho(tela, cor_minerio)
        if loja.nivel("laser") > 0:
            self.desenhar_laser(tela)

    def desenhar_frente(self, tela, loja):
        """Ajudantes que ficam na frente da rocha: broca e até 3 anões."""
        if loja.nivel("broca") > 0:
            self.desenhar_broca(tela)
        quantos_anoes = min(3, loja.nivel("anao"))
        for i in range(quantos_anoes):
            # Cada anão bate num ritmo diferente (soma i para não ficarem sincronizados)
            batendo = int(self.tempo * 4 + i) % 2 == 0
            self.desenhar_anao(tela, 445 + i * 45, batendo)

    def desenhar_anao(self, tela, x, batendo):
        """Anão de barba branca e gorro vermelho, com uma picareta virada para a rocha."""
        pygame.draw.rect(tela, (60, 130, 70), (x - 9, CHAO - 28, 18, 22), border_radius=4)
        pygame.draw.rect(tela, (70, 45, 25), (x - 9, CHAO - 6, 18, 6))
        pygame.draw.circle(tela, PELE, (x, CHAO - 34), 8)
        pygame.draw.polygon(tela, (225, 225, 225), [(x - 8, CHAO - 33), (x + 8, CHAO - 33), (x, CHAO - 18)])
        pygame.draw.polygon(tela, (200, 40, 40), [(x - 9, CHAO - 39), (x + 9, CHAO - 39), (x + 2, CHAO - 58)])
        if batendo:
            pygame.draw.line(tela, MADEIRA, (x - 4, CHAO - 24), (x - 26, CHAO - 18), 3)
            pygame.draw.line(tela, FERRO, (x - 28, CHAO - 28), (x - 24, CHAO - 8), 4)
        else:
            pygame.draw.line(tela, MADEIRA, (x - 4, CHAO - 24), (x + 4, CHAO - 46), 3)
            pygame.draw.line(tela, FERRO, (x - 4, CHAO - 48), (x + 12, CHAO - 44), 4)

    def desenhar_broca(self, tela):
        """Máquina com uma broca encostada na rocha. As listras trocam de lugar para parecer que gira."""
        y = 320
        ponta = CENTRO_ROCHA[0] + RAIO_ROCHA - 5
        pygame.draw.rect(tela, (110, 90, 70), (530, y - 22, 75, 44), border_radius=6)
        pygame.draw.polygon(tela, (190, 195, 205), [(530, y - 18), (530, y + 18), (ponta, y)])
        deslocamento = 9 if int(self.tempo * 10) % 2 == 0 else 0
        for listra_x in range(500 - deslocamento, ponta, -18):
            pygame.draw.line(tela, (120, 125, 135), (listra_x, y - 10), (listra_x - 6, y + 10), 2)

    def desenhar_laser(self, tela):
        """Canhão no teto disparando um raio vermelho na rocha."""
        x = CENTRO_ROCHA[0]
        fim = CENTRO_ROCHA[1] - RAIO_ROCHA + 10
        largura = 8 if int(self.tempo * 10) % 2 == 0 else 5   # o raio "treme"
        pygame.draw.line(tela, (255, 60, 60), (x, 120), (x, fim), largura)
        pygame.draw.line(tela, (255, 230, 230), (x, 120), (x, fim), 2)
        pygame.draw.rect(tela, (90, 95, 110), (x - 22, 100, 44, 22), border_radius=4)

    def desenhar_carrinho(self, tela, cor_minerio):
        """Trilho e carrinho cheio de minério andando."""
        trilho_y = 610
        pygame.draw.line(tela, (90, 80, 70), (0, trilho_y), (680, trilho_y), 4)
        x = int(self.carrinho_x)
        for dx in (-12, 0, 12):
            pygame.draw.circle(tela, cor_minerio, (x + dx, trilho_y - 26), 9)
        pygame.draw.polygon(tela, (110, 70, 40), [(x - 32, trilho_y - 28), (x + 32, trilho_y - 28),
                                                  (x + 25, trilho_y - 8), (x - 25, trilho_y - 8)])
        pygame.draw.circle(tela, (40, 40, 40), (x - 15, trilho_y - 6), 7)
        pygame.draw.circle(tela, (40, 40, 40), (x + 15, trilho_y - 6), 7)

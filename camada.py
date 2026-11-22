"""Camadas da mina. Cada camada é uma fase com cenário, rocha, valores e desafios próprios."""

import random

import pygame

from config import ALTURA, LARGURA_MINA

# Para criar uma camada nova, basta acrescentar um dicionário nesta lista.
#   vida: cliques (dano) para quebrar uma rocha | valor: minério que cada rocha dá
#   escuridao: 0 = claro, 255 = totalmente escuro
#   pedras: caem pedras do teto? | calor: a picareta pode superaquecer?
CAMADAS = [
    {"nome": "Superfície", "cor_topo": (125, 90, 58), "cor_baixo": (78, 52, 33),
     "cor_rocha": (135, 135, 140), "cor_minerio": (45, 45, 50),
     "vida": 5, "valor": 3, "custo_descer": 300,
     "ladroes": False, "escuridao": 0, "pedras": False, "calor": False},

    {"nome": "Cavernas", "cor_topo": (48, 42, 52), "cor_baixo": (16, 13, 20),
     "cor_rocha": (100, 88, 82), "cor_minerio": (235, 190, 60),
     "vida": 40, "valor": 30, "custo_descer": 8_000,
     "ladroes": True, "escuridao": 225, "pedras": False, "calor": False},

    {"nome": "Cristais", "cor_topo": (40, 22, 68), "cor_baixo": (10, 6, 30),
     "cor_rocha": (115, 80, 165), "cor_minerio": (120, 240, 255),
     "vida": 150, "valor": 150, "custo_descer": 150_000,
     "ladroes": True, "escuridao": 170, "pedras": True, "calor": False},

    {"nome": "Magma", "cor_topo": (85, 22, 12), "cor_baixo": (30, 6, 2),
     "cor_rocha": (55, 42, 42), "cor_minerio": (255, 115, 20),
     "vida": 500, "valor": 700, "custo_descer": 1_000_000,
     "ladroes": True, "escuridao": 0, "pedras": True, "calor": True},
]


def misturar(cor1, cor2, t):
    """Cor no meio do caminho entre cor1 e cor2. t=0 dá cor1, t=1 dá cor2, t=0.5 dá a do meio."""
    r = int(cor1[0] + (cor2[0] - cor1[0]) * t)
    g = int(cor1[1] + (cor2[1] - cor1[1]) * t)
    b = int(cor1[2] + (cor2[2] - cor1[2]) * t)
    return (r, g, b)


class Camada:
    """Guarda os dados de uma camada e o desenho do cenário dela."""

    def __init__(self, numero, largura=LARGURA_MINA):
        dados = CAMADAS[numero]
        self.numero = numero
        self.largura = largura
        self.nome = dados["nome"]
        self.cor_rocha = dados["cor_rocha"]
        self.cor_minerio = dados["cor_minerio"]
        self.vida = dados["vida"]
        self.valor = dados["valor"]
        self.custo_descer = dados["custo_descer"]
        self.tem_ladroes = dados["ladroes"]
        self.escuridao = dados["escuridao"]
        self.tem_pedras = dados["pedras"]
        self.tem_calor = dados["calor"]

        self.eh_ultima = numero == len(CAMADAS) - 1
        if self.eh_ultima:
            self.nome_proxima = "Núcleo"
        else:
            self.nome_proxima = CAMADAS[numero + 1]["nome"]

        # O cenário é desenhado UMA vez numa imagem; depois é só colar a imagem na tela
        self.fundo = self.criar_fundo(dados["cor_topo"], dados["cor_baixo"])

    def criar_fundo(self, cor_topo, cor_baixo):
        """Cria a imagem do cenário: um degradê de cores mais as decorações da camada."""
        fundo = pygame.Surface((self.largura, ALTURA))
        for y in range(ALTURA):   # uma linha de cada cor, de cima para baixo
            cor = misturar(cor_topo, cor_baixo, y / ALTURA)
            pygame.draw.line(fundo, cor, (0, y), (self.largura, y))

        random.seed(self.numero)   # semente fixa: o sorteio sai sempre igual, então o cenário não muda
        if self.numero == 0:
            self.decorar_superficie(fundo)
        elif self.numero == 1:
            self.decorar_cavernas(fundo)
        elif self.numero == 2:
            self.decorar_cristais(fundo)
        else:
            self.decorar_magma(fundo)
        random.seed()   # volta a sortear normalmente
        return fundo

    def decorar_superficie(self, fundo):
        """Céu, sol, nuvens, grama e pedrinhas na terra."""
        pygame.draw.rect(fundo, (130, 190, 240), (0, 0, self.largura, 170))
        pygame.draw.circle(fundo, (255, 230, 120), (self.largura - 90, 60), 32)
        for x in (80, 330, 560):
            pygame.draw.circle(fundo, (245, 248, 255), (x, 70), 22)
            pygame.draw.circle(fundo, (245, 248, 255), (x + 25, 62), 28)
            pygame.draw.circle(fundo, (245, 248, 255), (x + 52, 70), 20)
        pygame.draw.rect(fundo, (70, 160, 70), (0, 165, self.largura, 18))
        for i in range(35):
            x = random.randint(0, self.largura)
            y = random.randint(200, ALTURA)
            pygame.draw.ellipse(fundo, (100, 72, 48), (x, y, 20, 10))

    def decorar_cavernas(self, fundo):
        """Estalactites (no teto) e estalagmites (no chão)."""
        for x in range(-20, self.largura, 45):
            comprimento = random.randint(30, 110)
            pygame.draw.polygon(fundo, (30, 25, 33), [(x, 0), (x + 40, 0), (x + 20, comprimento)])
            comprimento = random.randint(20, 70)
            pygame.draw.polygon(fundo, (30, 25, 33), [(x, ALTURA), (x + 40, ALTURA), (x + 20, ALTURA - comprimento)])

    def decorar_cristais(self, fundo):
        """Cristais coloridos perto das paredes."""
        cores = [(170, 90, 230), (90, 210, 240), (230, 110, 200)]
        for i in range(22):
            if i % 2 == 0:
                x = random.randint(0, 120)                               # parede da esquerda
            else:
                x = random.randint(self.largura - 120, self.largura)     # parede da direita
            y = random.randint(150, ALTURA)
            altura = random.randint(40, 120)
            cor = random.choice(cores)
            pygame.draw.polygon(fundo, cor, [(x, y), (x + 10, y - altura), (x + 20, y), (x + 10, y + 10)])

    def decorar_magma(self, fundo):
        """Rachaduras de lava nas paredes e um rio de lava embaixo."""
        for i in range(14):
            x = random.randint(0, self.largura)
            y = random.randint(100, ALTURA - 150)
            pontos = [(x, y)]
            for j in range(5):
                x = x + random.randint(-25, 25)
                y = y + random.randint(8, 25)
                pontos.append((x, y))
            pygame.draw.lines(fundo, (200, 70, 15), False, pontos, 3)
        pygame.draw.rect(fundo, (230, 90, 20), (0, ALTURA - 70, self.largura, 70))
        pygame.draw.rect(fundo, (255, 160, 40), (0, ALTURA - 70, self.largura, 10))

    def desenhar(self, tela):
        """Cola a imagem do cenário na tela."""
        tela.blit(self.fundo, (0, 0))

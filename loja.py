"""Loja: duas abas de itens (Mineração e Equipamentos) e o botão de descer de camada."""

import pygame

from config import ALTURA, AMARELO, BRANCO, CINZA, COR_PAINEL, LARGURA_LOJA, LARGURA_MINA, VERDE, VERMELHO
from ui import clarear, desenhar_texto, formatar_numero

# clique: dano a mais em cada clique | dps: dano automático por segundo
ITENS_MINERACAO = [
    {"id": "picareta", "nome": "Picareta melhor", "desc": "+2 de dano por clique",
     "custo": 15, "aumento": 1.6, "clique": 2, "dps": 0, "maximo": None},
    {"id": "anao", "nome": "Anão minerador", "desc": "+1 de dano por segundo",
     "custo": 20, "aumento": 1.15, "clique": 0, "dps": 1, "maximo": None},
    {"id": "carrinho", "nome": "Carrinho de mina", "desc": "+8 de dano por segundo",
     "custo": 250, "aumento": 1.15, "clique": 0, "dps": 8, "maximo": None},
    {"id": "broca", "nome": "Broca a vapor", "desc": "+50 de dano por segundo",
     "custo": 3_500, "aumento": 1.15, "clique": 0, "dps": 50, "maximo": None},
    {"id": "laser", "nome": "Escavadeira laser", "desc": "+300 de dano por segundo",
     "custo": 45_000, "aumento": 1.15, "clique": 0, "dps": 300, "maximo": None},
]

# Equipamentos não dão dano: mudam regras do jogo (o efeito de cada um está em partida.py)
ITENS_EQUIPAMENTOS = [
    {"id": "lanterna", "nome": "Lanterna", "desc": "Ilumina mais o escuro",
     "custo": 150, "aumento": 4, "clique": 0, "dps": 0, "maximo": 3},
    {"id": "ima", "nome": "Ímã de minérios", "desc": "Mais pedras brilhantes",
     "custo": 600, "aumento": 4, "clique": 0, "dps": 0, "maximo": 3},
    {"id": "capacete", "nome": "Capacete reforçado", "desc": "Fica menos tempo tonto",
     "custo": 8_000, "aumento": 4, "clique": 0, "dps": 0, "maximo": 3},
    {"id": "resfriador", "nome": "Resfriador", "desc": "Esquenta mais devagar",
     "custo": 100_000, "aumento": 2, "clique": 0, "dps": 0, "maximo": 3},
]


class Item:
    """Um item da loja. Pode ser comprado várias vezes e fica mais caro a cada compra."""

    def __init__(self, dados):
        self.id = dados["id"]
        self.nome = dados["nome"]
        self.desc = dados["desc"]
        self.custo_inicial = dados["custo"]
        self.aumento = dados["aumento"]
        self.clique = dados["clique"]
        self.dps = dados["dps"]
        self.maximo = dados["maximo"]   # None = pode comprar sem limite
        self.quantidade = 0

    def custo(self):
        """Preço da próxima compra. Ex.: custo 20 e aumento 1.15 -> 20, 23, 26, 30..."""
        return int(self.custo_inicial * self.aumento ** self.quantidade)

    def no_maximo(self):
        """True quando o item já chegou ao nível máximo."""
        return self.maximo is not None and self.quantidade >= self.maximo


class Loja:
    """Painel do lado direito da tela."""

    def __init__(self):
        self.mineracao = []
        for dados in ITENS_MINERACAO:
            self.mineracao.append(Item(dados))
        self.equipamentos = []
        for dados in ITENS_EQUIPAMENTOS:
            self.equipamentos.append(Item(dados))
        self.todos = self.mineracao + self.equipamentos
        self.aba = 0   # 0 = Mineração, 1 = Equipamentos

        # Retângulos clicáveis (posição e tamanho de cada coisa na loja)
        x = LARGURA_MINA + 12
        self.rect_aba_mineracao = pygame.Rect(x, 50, 135, 32)
        self.rect_aba_equipamentos = pygame.Rect(x + 141, 50, 135, 32)
        self.rects_itens = []
        for i in range(5):
            self.rects_itens.append(pygame.Rect(x, 92 + i * 70, 276, 62))
        self.rect_descer = pygame.Rect(x, 450, 276, 66)

    def itens_da_aba(self):
        """Lista de itens da aba que está aberta."""
        if self.aba == 0:
            return self.mineracao
        return self.equipamentos

    def nivel(self, id_item):
        """Quantas vezes o item com esse id foi comprado."""
        for item in self.todos:
            if item.id == id_item:
                return item.quantidade
        return 0

    def dano_clique(self):
        """Dano de cada clique: 1 + o bônus das picaretas."""
        total = 1
        for item in self.todos:
            total = total + item.clique * item.quantidade
        return total

    def dps(self):
        """Dano automático por segundo de todos os ajudantes somados."""
        total = 0
        for item in self.todos:
            total = total + item.dps * item.quantidade
        return total

    def comprar(self, item, partida):
        """Compra o item se tiver minério e se ele não estiver no máximo."""
        if item.no_maximo() or not partida.gastar(item.custo()):
            partida.jogo.sons.tocar("erro")
            return
        item.quantidade = item.quantidade + 1
        partida.jogo.sons.tocar("compra")

    def tratar_clique(self, posicao, partida):
        """Vê onde o clique foi: numa aba, num item ou no botão de descer."""
        if self.rect_aba_mineracao.collidepoint(posicao):
            self.aba = 0
        elif self.rect_aba_equipamentos.collidepoint(posicao):
            self.aba = 1
        elif self.rect_descer.collidepoint(posicao):
            partida.descer()
        else:
            itens = self.itens_da_aba()
            for i in range(len(itens)):
                if self.rects_itens[i].collidepoint(posicao):
                    self.comprar(itens[i], partida)

    # ---------- desenho ----------

    def desenhar(self, tela, fontes, partida):
        """Desenha o painel inteiro: título, abas, itens, botão de descer e estatísticas."""
        pygame.draw.rect(tela, COR_PAINEL, (LARGURA_MINA, 0, LARGURA_LOJA, ALTURA))
        pygame.draw.line(tela, (70, 60, 80), (LARGURA_MINA, 0), (LARGURA_MINA, ALTURA), 3)
        desenhar_texto(tela, fontes["grande"], "LOJA", AMARELO, LARGURA_MINA + LARGURA_LOJA // 2, 24, "centro")

        self.desenhar_aba(tela, fontes, "Mineração", self.rect_aba_mineracao, self.aba == 0)
        self.desenhar_aba(tela, fontes, "Equipamentos", self.rect_aba_equipamentos, self.aba == 1)
        itens = self.itens_da_aba()
        for i in range(len(itens)):
            self.desenhar_item(tela, fontes, itens[i], self.rects_itens[i], partida.minerio)
        self.desenhar_botao_descer(tela, fontes, partida)

        estatisticas = [
            f"Dano por clique: {formatar_numero(self.dano_clique())}",
            f"Dano automático: {formatar_numero(self.dps())}/s",
            f"Rochas quebradas: {formatar_numero(partida.rochas_quebradas)}",
            f"Cliques: {formatar_numero(partida.cliques)}",
        ]
        for i in range(len(estatisticas)):
            desenhar_texto(tela, fontes["pequena"], estatisticas[i], CINZA, LARGURA_MINA + 20, 530 + i * 24)

    def desenhar_aba(self, tela, fontes, nome, rect, selecionada):
        """Desenha uma aba. A aba aberta fica mais clara e com borda branca."""
        if selecionada:
            pygame.draw.rect(tela, (85, 75, 115), rect, border_radius=6)
            pygame.draw.rect(tela, BRANCO, rect, 1, border_radius=6)
            desenhar_texto(tela, fontes["pequena"], nome, BRANCO, rect.centerx, rect.centery, "centro")
        else:
            pygame.draw.rect(tela, (40, 36, 48), rect, border_radius=6)
            desenhar_texto(tela, fontes["pequena"], nome, CINZA, rect.centerx, rect.centery, "centro")

    def desenhar_item(self, tela, fontes, item, rect, minerio):
        """Desenha o cartão de um item: nome, descrição, preço e quantidade comprada."""
        pode_comprar = not item.no_maximo() and minerio >= item.custo()
        cor = (52, 64, 88) if pode_comprar else (44, 40, 50)
        if rect.collidepoint(pygame.mouse.get_pos()):
            cor = clarear(cor, 20)
        pygame.draw.rect(tela, cor, rect, border_radius=8)
        pygame.draw.rect(tela, (90, 85, 110), rect, 1, border_radius=8)

        cor_nome = BRANCO if pode_comprar else CINZA
        desenhar_texto(tela, fontes["media"], item.nome, cor_nome, rect.x + 10, rect.y + 2)
        desenhar_texto(tela, fontes["pequena"], item.desc, CINZA, rect.x + 10, rect.y + 25)
        if item.no_maximo():
            desenhar_texto(tela, fontes["pequena"], "Nível máximo", VERDE, rect.x + 10, rect.y + 42)
        else:
            cor_preco = AMARELO if pode_comprar else VERMELHO
            desenhar_texto(tela, fontes["pequena"], f"Custo: {formatar_numero(item.custo())}",
                           cor_preco, rect.x + 10, rect.y + 42)

        if item.maximo is None:
            quantidade = str(item.quantidade)
        else:
            quantidade = f"{item.quantidade}/{item.maximo}"
        desenhar_texto(tela, fontes["grande"], quantidade, (120, 115, 140), rect.right - 12, rect.y + 10, "direita")

    def desenhar_botao_descer(self, tela, fontes, partida):
        """Botão verde quando dá para descer; cinza quando falta minério."""
        camada = partida.camada
        rect = self.rect_descer
        if partida.minerio >= camada.custo_descer:
            pygame.draw.rect(tela, (50, 120, 70), rect, border_radius=10)
            pygame.draw.rect(tela, BRANCO, rect, 2, border_radius=10)
            cor_texto = BRANCO
            cor_preco = AMARELO
        else:
            pygame.draw.rect(tela, (44, 40, 50), rect, border_radius=10)
            pygame.draw.rect(tela, (90, 85, 110), rect, 2, border_radius=10)
            cor_texto = CINZA
            cor_preco = VERMELHO
        desenhar_texto(tela, fontes["media"], f"Descer para: {camada.nome_proxima}", cor_texto,
                       rect.centerx, rect.y + 20, "centro")
        desenhar_texto(tela, fontes["pequena"], f"Custo: {formatar_numero(camada.custo_descer)}", cor_preco,
                       rect.centerx, rect.y + 46, "centro")

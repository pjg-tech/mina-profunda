"""Telas que não são a partida: Menu, Instruções, Pause e Vitória."""

import pygame

import save
from camada import Camada
from config import ALTURA, AMARELO, BRANCO, CINZA, LARGURA, VERDE
from efeitos import Efeitos
from ui import Botao, Tela, desenhar_texto, formatar_numero

CENTRO_X = LARGURA // 2


def escurecer_tela(tela, quanto):
    """Cobre a tela com preto semitransparente (quanto: 0 = nada, 255 = tudo preto)."""
    sombra = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    sombra.fill((0, 0, 0, quanto))
    tela.blit(sombra, (0, 0))


class Menu(Tela):
    """Tela inicial: Novo jogo, Continuar, Instruções e Sair."""

    def __init__(self, jogo):
        super().__init__(jogo)
        self.fundo = Camada(0, LARGURA)   # usa o cenário da Superfície como fundo
        self.botao_novo = Botao(CENTRO_X - 140, 250, 280, 56, "Novo jogo", (60, 140, 80))
        self.botao_continuar = Botao(CENTRO_X - 140, 322, 280, 56, "Continuar")
        self.botao_instrucoes = Botao(CENTRO_X - 140, 394, 280, 56, "Instruções")
        self.botao_sair = Botao(CENTRO_X - 140, 466, 280, 56, "Sair")
        self.botao_continuar.ativo = save.existe_save()   # só dá para continuar se houver save
        jogo.sons.tocar_musica(0)

    def tratar_evento(self, evento):
        """Vê qual botão foi clicado."""
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.botao_novo.clicado(evento.pos):
                self.jogo.novo_jogo()
            elif self.botao_continuar.clicado(evento.pos):
                self.jogo.continuar_jogo()
            elif self.botao_instrucoes.clicado(evento.pos):
                self.jogo.ir_para_instrucoes()
            elif self.botao_sair.clicado(evento.pos):
                self.jogo.sair()

    def desenhar(self, tela):
        """Fundo escurecido, título e botões."""
        self.fundo.desenhar(tela)
        escurecer_tela(tela, 110)
        desenhar_texto(tela, self.jogo.fontes["titulo"], "MINA PROFUNDA", AMARELO, CENTRO_X, 120, "centro")
        desenhar_texto(tela, self.jogo.fontes["media"], "Cave até o núcleo do planeta!", BRANCO, CENTRO_X, 175, "centro")
        for botao in (self.botao_novo, self.botao_continuar, self.botao_instrucoes, self.botao_sair):
            botao.desenhar(tela, self.jogo.fontes["media"])


class Instrucoes(Tela):
    """Tela que explica as regras do jogo."""

    LINHAS = [
        "Clique na rocha para minerar. Cada rocha quebrada dá minério.",
        "LOJA > Mineração: picaretas e ajudantes que mineram sozinhos.",
        "LOJA > Equipamentos: lanterna, ímã, capacete e resfriador.",
        "Junte minério para DESCER: Superfície > Cavernas > Cristais > Magma > Núcleo.",
        "Pedras brilhantes aparecem às vezes: clique rápido para ganhar bônus!",
        "Ladrões: clique 3 vezes antes que fujam, ou roubam 10% do minério.",
        "Cavernas e Cristais são escuros: a lanterna ilumina em volta do mouse.",
        "Cristais e Magma: pedras caem do teto! Clique nelas antes que acertem você.",
        "Magma: a picareta esquenta. Se superaquecer, espere ela esfriar.",
        "Chegue ao Núcleo do planeta para vencer!",
        "",
        "ESC pausa o jogo. O progresso é salvo automaticamente.",
    ]

    def __init__(self, jogo):
        super().__init__(jogo)
        self.fundo = Camada(1, LARGURA)   # cenário das Cavernas
        self.botao_voltar = Botao(CENTRO_X - 120, ALTURA - 95, 240, 56, "Voltar")

    def tratar_evento(self, evento):
        """Volta ao menu com o botão Voltar ou com ESC."""
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            self.jogo.ir_para_menu()
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.botao_voltar.clicado(evento.pos):
                self.jogo.ir_para_menu()

    def desenhar(self, tela):
        """Título e uma linha de texto embaixo da outra."""
        self.fundo.desenhar(tela)
        escurecer_tela(tela, 150)
        desenhar_texto(tela, self.jogo.fontes["grande"], "COMO JOGAR", AMARELO, CENTRO_X, 55, "centro")
        for i in range(len(self.LINHAS)):
            desenhar_texto(tela, self.jogo.fontes["media"], self.LINHAS[i], BRANCO, 90, 105 + i * 38)
        self.botao_voltar.desenhar(tela, self.jogo.fontes["media"])


class Pause(Tela):
    """Jogo pausado: mostra a partida congelada atrás e dois botões."""

    def __init__(self, jogo, partida):
        super().__init__(jogo)
        self.partida = partida   # guarda a partida para poder voltar para ela
        self.botao_continuar = Botao(CENTRO_X - 170, 280, 340, 56, "Continuar")
        self.botao_menu = Botao(CENTRO_X - 170, 352, 340, 56, "Salvar e sair para o menu")

    def tratar_evento(self, evento):
        """ESC ou Continuar voltam ao jogo. O outro botão salva e vai para o menu."""
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            self.jogo.voltar_para_partida(self.partida)
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.botao_continuar.clicado(evento.pos):
                self.jogo.voltar_para_partida(self.partida)
            elif self.botao_menu.clicado(evento.pos):
                self.partida.salvar()
                self.jogo.ir_para_menu()

    def desenhar(self, tela):
        """Desenha a partida (sem atualizar, por isso ela fica parada) e escurece por cima."""
        self.partida.desenhar(tela)
        escurecer_tela(tela, 160)
        desenhar_texto(tela, self.jogo.fontes["titulo"], "PAUSADO", BRANCO, CENTRO_X, 180, "centro")
        self.botao_continuar.desenhar(tela, self.jogo.fontes["media"])
        self.botao_menu.desenhar(tela, self.jogo.fontes["media"])

    def ao_sair(self):
        """Se fechar a janela durante o pause, salva mesmo assim."""
        self.partida.salvar()


class Vitoria(Tela):
    """Tela final: o núcleo do planeta, fogos de artifício e as estatísticas da partida."""

    def __init__(self, jogo, partida):
        super().__init__(jogo)
        minutos = int(partida.tempo_jogo) // 60
        segundos = int(partida.tempo_jogo) % 60
        self.estatisticas = [
            f"Tempo de jogo: {minutos} min {segundos} s",
            f"Cliques: {formatar_numero(partida.cliques)}",
            f"Rochas quebradas: {formatar_numero(partida.rochas_quebradas)}",
            f"Minério total: {formatar_numero(partida.total_minerado)}",
        ]
        self.efeitos = Efeitos(jogo.fontes["media"])
        self.timer_fogos = 0
        self.botao_menu = Botao(CENTRO_X - 120, ALTURA - 100, 240, 56, "Voltar ao menu", VERDE)

    def tratar_evento(self, evento):
        """Botão de voltar ao menu."""
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.botao_menu.clicado(evento.pos):
                self.jogo.ir_para_menu()

    def atualizar(self, dt):
        """Solta um "fogo de artifício" de partículas a cada 0,6 segundo."""
        self.timer_fogos = self.timer_fogos - dt
        if self.timer_fogos <= 0:
            self.efeitos.explosao(CENTRO_X, 300, (255, 200, 60), 30)
            self.timer_fogos = 0.6
        self.efeitos.atualizar(dt)

    def desenhar(self, tela):
        """Núcleo (círculos de fora para dentro), fogos, título, estatísticas e botão."""
        tela.fill((40, 8, 4))
        pygame.draw.circle(tela, (120, 30, 10), (CENTRO_X, 300), 120)
        pygame.draw.circle(tela, (220, 90, 20), (CENTRO_X, 300), 95)
        pygame.draw.circle(tela, (255, 180, 40), (CENTRO_X, 300), 65)
        pygame.draw.circle(tela, (255, 240, 180), (CENTRO_X, 300), 35)
        self.efeitos.desenhar(tela)
        desenhar_texto(tela, self.jogo.fontes["titulo"], "VOCÊ CHEGOU AO NÚCLEO!", AMARELO, CENTRO_X, 70, "centro")
        for i in range(len(self.estatisticas)):
            desenhar_texto(tela, self.jogo.fontes["media"], self.estatisticas[i], BRANCO, CENTRO_X, 450 + i * 28, "centro")
        self.botao_menu.desenhar(tela, self.jogo.fontes["media"])

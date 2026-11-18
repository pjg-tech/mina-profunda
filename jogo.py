"""Classe Jogo: abre a janela, guarda o que todas as telas usam e roda o loop principal."""

import pygame

import save
from config import ALTURA, FPS, LARGURA, TITULO
from partida import Partida
from sons import Sons
from telas import Instrucoes, Menu, Pause, Vitoria


class Jogo:
    """Controla a janela e qual tela está ativa (menu, partida, pause...)."""

    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption(TITULO)
        self.relogio = pygame.time.Clock()
        self.fontes = {
            "titulo": pygame.font.SysFont("segoeui", 56, bold=True),
            "grande": pygame.font.SysFont("segoeui", 32, bold=True),
            "media": pygame.font.SysFont("segoeui", 19, bold=True),
            "pequena": pygame.font.SysFont("segoeui", 15),
        }
        self.sons = Sons()
        self.rodando = True
        self.tela_atual = Menu(self)

    # ---------- troca de telas (as telas chamam estes métodos) ----------

    def ir_para_menu(self):
        """Mostra o menu inicial."""
        self.tela_atual = Menu(self)

    def ir_para_instrucoes(self):
        """Mostra a tela de instruções."""
        self.tela_atual = Instrucoes(self)

    def novo_jogo(self):
        """Apaga o save antigo e começa uma partida do zero."""
        save.apagar_save()
        self.tela_atual = Partida(self)

    def continuar_jogo(self):
        """Começa uma partida com o progresso lido do save."""
        self.tela_atual = Partida(self, save.carregar())

    def pausar(self, partida):
        """Mostra a tela de pause (guardando a partida para poder voltar)."""
        self.tela_atual = Pause(self, partida)

    def voltar_para_partida(self, partida):
        """Sai do pause e volta para a mesma partida."""
        self.tela_atual = partida

    def vencer(self, partida):
        """Mostra a tela de vitória com as estatísticas da partida."""
        self.tela_atual = Vitoria(self, partida)

    def sair(self):
        """Avisa a tela atual (para ela salvar, se precisar) e encerra o loop."""
        self.tela_atual.ao_sair()
        self.rodando = False

    # ---------- loop principal ----------

    def rodar(self):
        """Repete FPS vezes por segundo: eventos -> atualizar -> desenhar."""
        while self.rodando:
            # dt = segundos desde o último quadro (no máximo 0,1 para não "pular" se travar)
            dt = min(self.relogio.tick(FPS) / 1000, 0.1)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.sair()
                else:
                    self.tela_atual.tratar_evento(evento)

            if self.rodando:
                self.tela_atual.atualizar(dt)
                self.tela_atual.desenhar(self.tela)
                pygame.display.flip()   # mostra na janela o que foi desenhado

        pygame.quit()

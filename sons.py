"""Toca os efeitos sonoros e as músicas (arquivos .wav da pasta sons/)."""

import pygame

EFEITOS = ["clique", "quebra", "acerto", "compra", "bonus", "erro", "descer", "vitoria"]


class Sons:
    """Carrega os sons uma vez e toca quando o jogo pede."""

    def __init__(self):
        self.efeitos = {}
        self.musica_atual = None
        try:
            pygame.mixer.init()
            for nome in EFEITOS:
                self.efeitos[nome] = pygame.mixer.Sound(f"sons/{nome}.wav")
            self.ativo = True
        except pygame.error:
            # Computador sem placa de som (ou arquivo faltando): o jogo roda sem som
            self.ativo = False

    def tocar(self, nome):
        """Toca um efeito sonoro pelo nome. Ex.: tocar('clique')."""
        if self.ativo:
            self.efeitos[nome].play()

    def tocar_musica(self, numero):
        """Toca a música da camada 'numero' repetindo sem parar."""
        if not self.ativo or self.musica_atual == numero:
            return
        pygame.mixer.music.load(f"sons/musica{numero}.wav")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)   # -1 = repetir para sempre
        self.musica_atual = numero

    def parar_musica(self):
        """Para a música que está tocando."""
        if self.ativo:
            pygame.mixer.music.stop()
        self.musica_atual = None

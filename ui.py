"""Ferramentas de interface usadas em várias telas: classe Tela, botão, texto e cores."""

import pygame

from config import BRANCO, COR_BOTAO, COR_DESATIVADO, PRETO


class Tela:
    """Modelo de tela. Menu, Partida, Pause etc. herdam desta classe.

    Toda tela tem os mesmos 4 métodos. O Jogo chama esses métodos
    na tela que estiver ativa, sem precisar saber qual tela é.
    """

    def __init__(self, jogo):
        self.jogo = jogo

    def tratar_evento(self, evento):
        """Recebe um evento do pygame (clique, tecla...)."""

    def atualizar(self, dt):
        """Atualiza a tela. dt = segundos desde o último quadro."""

    def desenhar(self, tela):
        """Desenha a tela."""

    def ao_sair(self):
        """Chamado quando o jogador fecha a janela."""


def formatar_numero(n):
    """Deixa números grandes curtos: 1500 vira '1,5 mil' e 2000000 vira '2,0 mi'."""
    if n >= 1_000_000_000:
        texto = f"{n / 1_000_000_000:.1f} bi"
    elif n >= 1_000_000:
        texto = f"{n / 1_000_000:.1f} mi"
    elif n >= 1_000:
        texto = f"{n / 1_000:.1f} mil"
    else:
        return str(int(n))
    return texto.replace(".", ",")


def clarear(cor, quanto):
    """Deixa uma cor mais clara somando 'quanto' em cada parte (sem passar de 255)."""
    return (min(255, cor[0] + quanto), min(255, cor[1] + quanto), min(255, cor[2] + quanto))


def escurecer(cor, quanto):
    """Deixa uma cor mais escura (sem ficar abaixo de 0)."""
    return (max(0, cor[0] - quanto), max(0, cor[1] - quanto), max(0, cor[2] - quanto))


def desenhar_texto(tela, fonte, texto, cor, x, y, alinhamento="esquerda"):
    """Escreve um texto com sombra preta.

    alinhamento:
      'esquerda' -> (x, y) é o canto de cima à esquerda do texto
      'direita'  -> (x, y) é o canto de cima à direita do texto
      'centro'   -> (x, y) é o centro do texto
    """
    imagem = fonte.render(texto, True, cor)
    if alinhamento == "centro":
        x = x - imagem.get_width() // 2
        y = y - imagem.get_height() // 2
    elif alinhamento == "direita":
        x = x - imagem.get_width()
    sombra = fonte.render(texto, True, PRETO)
    tela.blit(sombra, (x + 2, y + 2))
    tela.blit(imagem, (x, y))


class Botao:
    """Botão retangular com texto. Fica mais claro quando o mouse passa por cima."""

    def __init__(self, x, y, largura, altura, texto, cor=COR_BOTAO):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor = cor
        self.ativo = True   # botão desativado fica cinza e não pode ser clicado

    def clicado(self, posicao):
        """True se o botão está ativo e a posição do clique está dentro dele."""
        return self.ativo and self.rect.collidepoint(posicao)

    def desenhar(self, tela, fonte):
        """Desenha o retângulo, a borda e o texto do botão."""
        if not self.ativo:
            cor = COR_DESATIVADO
        elif self.rect.collidepoint(pygame.mouse.get_pos()):
            cor = clarear(self.cor, 35)
        else:
            cor = self.cor
        pygame.draw.rect(tela, PRETO, self.rect.move(0, 4), border_radius=10)   # sombra
        pygame.draw.rect(tela, cor, self.rect, border_radius=10)
        pygame.draw.rect(tela, BRANCO, self.rect, 2, border_radius=10)          # borda
        desenhar_texto(tela, fonte, self.texto, BRANCO, self.rect.centerx, self.rect.centery, "centro")

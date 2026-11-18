"""Tela principal do jogo. Junta todas as partes: camada, rocha, minerador, perigos e loja."""

import random

import pygame

import save
from camada import Camada
from config import (ALTURA, AMARELO, BRANCO, CENTRO_ROCHA, CHAO, CINZA, DEBUG, LARGURA_MINA,
                    MINERADOR_X, RAIO_ROCHA, SALVAR_A_CADA, VERMELHO)
from efeitos import Efeitos
from inimigos import Ladrao, MinerioRaro, PedraCaindo
from loja import Loja
from personagens import Ajudantes, Minerador
from rocha import Rocha
from ui import Tela, desenhar_texto, formatar_numero

CALOR_POR_CLIQUE = 7         # quanto a picareta esquenta a cada clique (só no Magma)
RESFRIAMENTO = 25            # quanto ela esfria por segundo
TEMPO_SUPERAQUECIDA = 3      # segundos sem poder minerar depois de superaquecer


class Partida(Tela):
    """Guarda tudo de um jogo em andamento: minério, loja, camada atual e o que está na tela."""

    def __init__(self, jogo, dados_save=None):
        super().__init__(jogo)
        # Progresso (é isso que vai para o save)
        self.minerio = 0
        self.total_minerado = 0
        self.cliques = 0
        self.rochas_quebradas = 0
        self.tempo_jogo = 0
        self.loja = Loja()
        numero_camada = 0
        if dados_save is not None:
            numero_camada = self.carregar_save(dados_save)

        # Coisas na tela
        self.minerador = Minerador()
        self.ajudantes = Ajudantes()
        self.efeitos = Efeitos(jogo.fontes["media"])
        self.ladroes = []
        self.raros = []
        self.pedras = []

        # Temporizadores: contam para trás; quando chegam a 0, algo acontece
        self.timer_raro = random.uniform(8, 15)
        self.timer_ladrao = random.uniform(12, 20)
        self.timer_pedra = random.uniform(6, 10)
        self.timer_save = SALVAR_A_CADA

        self.calor = 0                 # de 0 a 100
        self.superaquecida = 0         # > 0 enquanto a picareta está quente demais
        self.entrar_camada(numero_camada)

    # ---------- camadas ----------

    def entrar_camada(self, numero):
        """Prepara uma camada: cenário, rocha nova, música e limpa os perigos da anterior."""
        self.camada = Camada(numero)
        self.rocha = Rocha(self.camada)
        self.ladroes = []
        self.raros = []
        self.pedras = []
        self.calor = 0
        self.superaquecida = 0
        self.aviso_camada = f"Camada {numero + 1}: {self.camada.nome}"
        self.tempo_aviso_camada = 2.5
        self.jogo.sons.tocar_musica(numero)

    def descer(self):
        """Paga o custo e vai para a próxima camada. Na última, o jogador vence."""
        if not self.gastar(self.camada.custo_descer):
            self.jogo.sons.tocar("erro")
            return
        if self.camada.eh_ultima:
            save.apagar_save()
            self.jogo.sons.parar_musica()
            self.jogo.sons.tocar("vitoria")
            self.jogo.vencer(self)
        else:
            self.jogo.sons.tocar("descer")
            self.entrar_camada(self.camada.numero + 1)

    # ---------- minério ----------

    def ganhar(self, quantidade):
        """Soma minério."""
        self.minerio = self.minerio + quantidade
        self.total_minerado = self.total_minerado + quantidade

    def gastar(self, quantidade):
        """Tira minério se tiver o suficiente. Devolve True se conseguiu pagar."""
        if self.minerio < quantidade:
            return False
        self.minerio = self.minerio - quantidade
        return True

    def minerio_por_segundo(self):
        """Quanto os ajudantes mineram sozinhos por segundo: (dano/s ÷ vida da rocha) × valor."""
        return self.loja.dps() / self.camada.vida * self.camada.valor

    def rochas_quebraram(self, quantidade):
        """Dá o minério das rochas quebradas e mostra a explosão."""
        ganho = quantidade * self.camada.valor
        self.ganhar(ganho)
        self.rochas_quebradas = self.rochas_quebradas + quantidade
        cx, cy = CENTRO_ROCHA
        self.efeitos.explosao(cx, cy, self.camada.cor_minerio, 20)
        self.efeitos.texto(cx, cy - 120, f"+{formatar_numero(ganho)}")

    def avisar(self, texto):
        """Mostra um aviso vermelho em cima do minerador."""
        self.efeitos.texto(MINERADOR_X, CHAO - 140, texto, VERMELHO)
        self.jogo.sons.tocar("erro")

    # ---------- eventos (teclado e mouse) ----------

    def tratar_evento(self, evento):
        """ESC pausa, F2 dá minério (só no modo DEBUG) e o clique do mouse vai para clique()."""
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                self.jogo.pausar(self)
            elif evento.key == pygame.K_F2 and DEBUG:
                self.ganhar(max(1000, self.minerio * 2))
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            self.clique(evento.pos)

    def clique(self, posicao):
        """Descobre o que foi clicado. Testa primeiro o que está "na frente" e para no primeiro que achar."""
        for raro in self.raros:
            if raro.contem(posicao):
                bonus = max(self.camada.valor * 10, self.minerio_por_segundo() * 30)
                self.ganhar(bonus)
                raro.vivo = False
                self.efeitos.explosao(raro.x, raro.y, raro.cor, 30)
                self.efeitos.texto(raro.x, raro.y - 30, f"BÔNUS +{formatar_numero(bonus)}")
                self.jogo.sons.tocar("bonus")
                return

        for pedra in self.pedras:
            if pedra.contem(posicao):
                pedra.vivo = False
                self.ganhar(self.camada.valor * 2)
                self.efeitos.explosao(pedra.x, pedra.y, pedra.cor, 15)
                self.jogo.sons.tocar("quebra")
                return

        for ladrao in self.ladroes:
            if ladrao.contem(posicao):
                self.jogo.sons.tocar("acerto")
                if ladrao.acertar():
                    recompensa = self.camada.valor * 3
                    self.ganhar(recompensa)
                    self.efeitos.explosao(ladrao.x, ladrao.y, (200, 200, 200), 20)
                    self.efeitos.texto(ladrao.x, ladrao.y - 30, f"+{formatar_numero(recompensa)}")
                return

        if self.rocha.contem(posicao):
            self.clicar_rocha(posicao)
        else:
            self.loja.tratar_clique(posicao, self)

    def clicar_rocha(self, posicao):
        """Minera, a não ser que o minerador esteja tonto ou a picareta quente demais."""
        if self.minerador.atordoado > 0:
            self.avisar("Atordoado!")
            return
        if self.superaquecida > 0:
            self.avisar("Muito quente!")
            return

        self.cliques = self.cliques + 1
        self.rocha.bater()
        self.minerador.golpear()
        self.jogo.sons.tocar("clique")
        self.efeitos.explosao(posicao[0], posicao[1], self.camada.cor_rocha, 5)
        quebradas = self.rocha.receber_dano(self.loja.dano_clique())
        if quebradas > 0:
            self.rochas_quebraram(quebradas)
            self.jogo.sons.tocar("quebra")

        if self.camada.tem_calor:
            # Cada nível de resfriador faz a picareta esquentar 25% menos
            self.calor = self.calor + CALOR_POR_CLIQUE * (1 - 0.25 * self.loja.nivel("resfriador"))
            if self.calor >= 100:
                self.calor = 100
                self.superaquecida = TEMPO_SUPERAQUECIDA
                self.avisar("Picareta superaqueceu!")

    # ---------- atualização (roda a cada quadro) ----------

    def atualizar(self, dt):
        """Mineração automática, calor, perigos, bônus e salvamento automático."""
        self.tempo_jogo = self.tempo_jogo + dt
        self.tempo_aviso_camada = self.tempo_aviso_camada - dt

        # Os ajudantes mineram sozinhos: dano por segundo × segundos que passaram
        quebradas = self.rocha.receber_dano(self.loja.dps() * dt)
        if quebradas > 0:
            self.rochas_quebraram(quebradas)

        self.atualizar_calor(dt)
        self.rocha.atualizar(dt)
        self.minerador.atualizar(dt)
        self.ajudantes.atualizar(dt)
        self.efeitos.atualizar(dt)
        self.criar_coisas_novas(dt)
        self.mover_coisas(dt)

        self.timer_save = self.timer_save - dt
        if self.timer_save <= 0:
            self.salvar()
            self.timer_save = SALVAR_A_CADA

    def atualizar_calor(self, dt):
        """A picareta esfria com o tempo. Se superaqueceu, fica travada até o tempo acabar."""
        if self.superaquecida > 0:
            self.superaquecida = self.superaquecida - dt
            if self.superaquecida <= 0:
                self.calor = 0
        else:
            self.calor = max(0, self.calor - RESFRIAMENTO * dt)

    def criar_coisas_novas(self, dt):
        """De tempos em tempos aparecem pedras brilhantes, ladrões e pedras caindo."""
        ima = self.loja.nivel("ima")
        self.timer_raro = self.timer_raro - dt
        if self.timer_raro <= 0:
            # Cada nível de ímã: a pedra fica 1,5 s a mais e aparece 20% mais rápido
            self.raros.append(MinerioRaro(self.camada.cor_minerio, 6 + 1.5 * ima))
            self.timer_raro = random.uniform(15, 30) * (1 - 0.2 * ima)

        if self.camada.tem_ladroes:
            self.timer_ladrao = self.timer_ladrao - dt
            if self.timer_ladrao <= 0:
                self.ladroes.append(Ladrao(self.camada.numero))
                self.timer_ladrao = random.uniform(12, 25)

        if self.camada.tem_pedras:
            self.timer_pedra = self.timer_pedra - dt
            if self.timer_pedra <= 0:
                self.pedras.append(PedraCaindo(MINERADOR_X, CHAO - 100, self.camada.cor_rocha))
                self.timer_pedra = random.uniform(8, 16)

    def mover_coisas(self, dt):
        """Move tudo e trata o que fugiu (ladrão) ou acertou o minerador (pedra)."""
        for raro in self.raros:
            raro.atualizar(dt)

        for ladrao in self.ladroes:
            ladrao.atualizar(dt)
            if ladrao.fugiu:
                roubo = int(self.minerio * 0.1)
                self.minerio = self.minerio - roubo
                self.efeitos.texto(LARGURA_MINA // 2, 120, f"Roubaram {formatar_numero(roubo)}!", VERMELHO)
                self.jogo.sons.tocar("erro")

        for pedra in self.pedras:
            pedra.atualizar(dt)
            if pedra.acertou:
                # Sem capacete: 4 s tonto. Cada nível de capacete tira 1 s (mínimo de 1 s)
                self.minerador.atordoar(max(1, 4 - self.loja.nivel("capacete")))
                self.efeitos.explosao(pedra.x, pedra.y, pedra.cor, 15)
                self.avisar("Atordoado!")

        # Mantém nas listas só o que continua vivo
        self.raros = [raro for raro in self.raros if raro.vivo]
        self.ladroes = [ladrao for ladrao in self.ladroes if ladrao.vivo]
        self.pedras = [pedra for pedra in self.pedras if pedra.vivo]

    # ---------- desenho ----------

    def desenhar(self, tela):
        """Desenha em ordem, do fundo para a frente (o que vem depois fica por cima)."""
        self.camada.desenhar(tela)
        self.ajudantes.desenhar_atras(tela, self.loja, self.camada.cor_minerio)
        self.rocha.desenhar(tela)
        self.ajudantes.desenhar_frente(tela, self.loja)
        self.minerador.desenhar(tela, self.superaquecida > 0)
        for raro in self.raros:
            raro.desenhar(tela)
        for ladrao in self.ladroes:
            ladrao.desenhar(tela)
        for pedra in self.pedras:
            pedra.desenhar(tela)
        self.efeitos.desenhar(tela)
        if self.camada.escuridao > 0:
            self.desenhar_escuridao(tela)
        if self.camada.tem_calor:
            self.desenhar_barra_calor(tela)
        self.desenhar_painel(tela)
        self.loja.desenhar(tela, self.jogo.fontes, self)
        if self.tempo_aviso_camada > 0:
            desenhar_texto(tela, self.jogo.fontes["grande"], self.aviso_camada, BRANCO,
                           LARGURA_MINA // 2, 140, "centro")

    def desenhar_escuridao(self, tela):
        """Cobre a mina com uma camada preta e "fura" buracos de luz no minerador e no mouse."""
        sombra = pygame.Surface((LARGURA_MINA, ALTURA), pygame.SRCALPHA)   # SRCALPHA = aceita transparência
        sombra.fill((0, 0, 0, self.camada.escuridao))
        # Um círculo com transparência 0 apaga a sombra naquele lugar
        pygame.draw.circle(sombra, (0, 0, 0, 0), (CENTRO_ROCHA[0] - 40, CENTRO_ROCHA[1] + 20), 190)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x < LARGURA_MINA:
            raio_lanterna = 70 + 50 * self.loja.nivel("lanterna")
            pygame.draw.circle(sombra, (0, 0, 0, 0), (mouse_x, mouse_y), raio_lanterna)
        tela.blit(sombra, (0, 0))

    def desenhar_barra_calor(self, tela):
        """Barra de calor da picareta, embaixo da barra de vida da rocha (só no Magma)."""
        x = CENTRO_ROCHA[0] - 80
        y = CENTRO_ROCHA[1] + RAIO_ROCHA + 45
        desenhar_texto(tela, self.jogo.fontes["pequena"], "Calor", BRANCO, x - 50, y - 3)
        pygame.draw.rect(tela, (30, 30, 30), (x, y, 160, 12), border_radius=6)
        if self.superaquecida > 0:
            cor = BRANCO
        else:
            cor = (255, 140, 40)
        pygame.draw.rect(tela, cor, (x, y, int(160 * self.calor / 100), 12), border_radius=6)
        pygame.draw.rect(tela, BRANCO, (x, y, 160, 12), 1, border_radius=6)

    def desenhar_painel(self, tela):
        """Painel de cima: minério, minério por segundo e camada atual."""
        painel = pygame.Surface((LARGURA_MINA - 20, 82), pygame.SRCALPHA)
        painel.fill((0, 0, 0, 140))   # preto meio transparente
        tela.blit(painel, (10, 10))
        fontes = self.jogo.fontes
        desenhar_texto(tela, fontes["grande"], f"Minério: {formatar_numero(self.minerio)}", AMARELO, 24, 14)
        desenhar_texto(tela, fontes["pequena"], f"+{formatar_numero(self.minerio_por_segundo())} por segundo",
                       BRANCO, 26, 60)
        desenhar_texto(tela, fontes["media"], f"{self.camada.nome} ({self.camada.numero + 1}/4)", BRANCO,
                       LARGURA_MINA - 24, 20, "direita")
        desenhar_texto(tela, fontes["pequena"], "ESC = pausar", CINZA, LARGURA_MINA - 24, 60, "direita")

    # ---------- save ----------

    def salvar(self):
        """Grava o progresso no save.json."""
        quantidades = {}
        for item in self.loja.todos:
            quantidades[item.id] = item.quantidade
        save.salvar({
            "minerio": self.minerio,
            "total_minerado": self.total_minerado,
            "cliques": self.cliques,
            "rochas_quebradas": self.rochas_quebradas,
            "tempo_jogo": self.tempo_jogo,
            "camada": self.camada.numero,
            "itens": quantidades,
        })

    def carregar_save(self, dados):
        """Restaura o progresso salvo. Devolve o número da camada onde o jogador estava."""
        self.minerio = dados["minerio"]
        self.total_minerado = dados["total_minerado"]
        self.cliques = dados["cliques"]
        self.rochas_quebradas = dados["rochas_quebradas"]
        self.tempo_jogo = dados["tempo_jogo"]
        for item in self.loja.todos:
            item.quantidade = dados["itens"].get(item.id, 0)
        return dados["camada"]

    def ao_sair(self):
        """Salva quando o jogador fecha a janela."""
        self.salvar()

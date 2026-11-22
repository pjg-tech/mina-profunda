"""Constantes do jogo: valores que não mudam durante a partida."""

TITULO = "Mina Profunda"
LARGURA = 1000   # largura da janela (pixels)
ALTURA = 650     # altura da janela (pixels)
FPS = 60         # quadros por segundo

# A janela é dividida em duas partes: a mina (esquerda) e a loja (direita)
LARGURA_LOJA = 300
LARGURA_MINA = LARGURA - LARGURA_LOJA   # 700

# Posição da rocha e do minerador
CENTRO_ROCHA = (350, 355)
RAIO_ROCHA = 85
MINERADOR_X = 228
CHAO = 450   # altura dos pés dos personagens

SALVAR_A_CADA = 30   # segundos entre um salvamento automático e outro

# Modo de teste: se for True, a tecla F2 dá minério extra
DEBUG = False

# Cores no formato (vermelho, verde, azul), cada um de 0 a 255
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (150, 150, 150)
AMARELO = (255, 215, 60)
VERMELHO = (230, 70, 60)
VERDE = (80, 200, 110)
COR_BOTAO = (70, 110, 170)
COR_DESATIVADO = (80, 80, 85)
COR_PAINEL = (28, 24, 34)

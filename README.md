# Mina Profunda

Jogo 2D de mineração estilo *clicker*, feito em Python com PyGame para o Projeto Final de Design de Software (Insper).

Comece minerando rochas na superfície e cave cada vez mais fundo: Cavernas → Cristais → Magma → Núcleo do planeta.

## Integrantes
- Pedro Gonçalves
- Bernardo lennenberg

## Como rodar
1. Instale o Python 3 (https://www.python.org/downloads/).
2. Instale o PyGame:
   ```
   pip install pygame
   ```
3. **Dentro da pasta do jogo** (os sons e o save são procurados nela), rode:
   ```
   python main.py
   ```
   No Windows, também dá para clicar duas vezes em `Jogar.bat`.

## Como jogar
- Clique na rocha para minerar: o minerador bate a picareta a cada clique.
- **Loja > Mineração:** picareta melhor (mais dano por clique) e ajudantes que mineram sozinhos (anões, carrinho, broca e laser), que aparecem na tela quando comprados.
- **Loja > Equipamentos:** lanterna, ímã de minérios, capacete e resfriador (nível máximo 3).
- Junte minério para descer: Superfície → Cavernas → Cristais → Magma → Núcleo (vitória).
- Clique nas pedras brilhantes para ganhar bônus.
- A partir das Cavernas aparecem ladrões: clique 3 vezes neles antes que fujam, ou eles roubam 10% do seu minério.

Cada camada tem um desafio próprio:

| Camada | Desafio |
|---|---|
| Superfície | Tutorial: só minerar |
| Cavernas | Escuro: a lanterna ilumina em volta do mouse. Morcegos ladrões |
| Cristais | Escuro (menos) e pedras que caem do teto e atordoam o minerador |
| Magma | A picareta esquenta e pode superaquecer. Bolas de fogo e pedras caindo |

- ESC pausa o jogo. O progresso é salvo automaticamente em `save.json`.
- Modo de teste: com `DEBUG = True` em `config.py`, a tecla F2 dá minério extra.

## Vídeo
(link do vídeo)

## Estrutura do código e divisão do trabalho
O código foi dividido em duas partes, uma para cada integrante.

**Parte 1: estrutura do jogo e telas** (nome 1)
| Arquivo | O que faz |
|---|---|
| `main.py` | Arquivo que deve ser executado |
| `config.py` | Constantes (tamanho da tela, posições, cores) |
| `jogo.py` | Classe `Jogo`: janela, loop principal e troca de telas |
| `ui.py` | Classe base `Tela`, classe `Botao` e funções de texto e cor |
| `telas.py` | Telas `Menu`, `Instrucoes`, `Pause` e `Vitoria` |
| `partida.py` | Classe `Partida`: a tela de jogo, que junta todas as partes |
| `save.py` | Salvar e carregar o progresso em JSON |
| `sons.py` + `sons/` | Efeitos sonoros e músicas |

**Parte 2: o mundo da mina** (nome 2)
| Arquivo | O que faz |
|---|---|
| `camada.py` | Dados e cenário das 4 camadas (fases) |
| `rocha.py` | Classe `Rocha`: a rocha que é quebrada com cliques |
| `personagens.py` | Classes `Minerador` e `Ajudantes` (anões, carrinho, broca, laser) |
| `inimigos.py` | Classes `Ladrao`, `PedraCaindo` e `MinerioRaro` |
| `efeitos.py` | Classes `Particula`, `TextoFlutuante` e `Efeitos` |
| `loja.py` | Classes `Item` e `Loja` (abas Mineração/Equipamentos e botão de descer) |

## Créditos
- Imagens: todas desenhadas com formas do `pygame.draw` (sem arquivos de imagem).
- Sons e músicas (`sons/*.wav`): gerados por um script de síntese de áudio feito com IA (ver abaixo).

## Uso de IA generativa
O código deste jogo foi gerado com o assistente de IA Claude (Anthropic), a partir da ideia e dos requisitos do grupo: primeiro um protótipo, depois melhorias (minerador animado, ajudantes visíveis, aba de equipamentos, escuridão, pedras caindo, calor da picareta, docstrings e balanceamento) e por fim uma versão simplificada para facilitar o entendimento. Os sons `.wav` foram gerados por um script de áudio também feito pela IA. O grupo revisou o código e é responsável por entendê-lo. **Atualizem esta seção** conforme modificarem o código, indicando o que foi feito pelo grupo e o que veio de IA, com o link do histórico da conversa, como pede a página do projeto.

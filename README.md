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

## Vídeo
https://youtu.be/eyaZOTmW2os

## Estrutura do código e divisão do trabalho
O código foi dividido em duas partes, uma para cada integrante.

**Parte 1: estrutura do jogo e telas** (Pedro Gonçalves)
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

**Parte 2: o mundo da mina** (Bernardo lennenberg)
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
Ferramenta: Claude (Anthropic), via Claude Code. Não é a ferramenta institucional do Insper.

- **Gerado por IA (100%):** o código de todos os arquivos `.py`, os sons, este README (exceto edições pontuais do grupo) e o roteiro automático que gravou o vídeo de demonstração.
- **Feito pelo grupo:** a escolha do clicker de mineração e das camadas (rocha, cristais, magma) e os pedidos de melhoria e de simplificação.
- **Divisão em partes:** indica quem ficou responsável por estudar e enviar cada parte, e não autoria do código. Os commits de Pedro foram preparados com ajuda da IA.
- **Estudo:** materiais para entender o código também foram gerados com IA.

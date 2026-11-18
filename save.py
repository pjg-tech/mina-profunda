"""Salva e carrega o progresso do jogo num arquivo JSON."""

import json
import os

ARQUIVO = "save.json"


def existe_save():
    """True se já existe um arquivo de save."""
    return os.path.exists(ARQUIVO)


def salvar(dados):
    """Grava o dicionário 'dados' no arquivo."""
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=2)


def carregar():
    """Lê o arquivo e devolve o dicionário salvo."""
    with open(ARQUIVO, encoding="utf-8") as arquivo:
        return json.load(arquivo)


def apagar_save():
    """Apaga o arquivo de save (usado em 'Novo jogo' e quando o jogador vence)."""
    if existe_save():
        os.remove(ARQUIVO)

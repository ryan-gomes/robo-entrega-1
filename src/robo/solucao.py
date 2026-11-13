"""Soluções da Entrega 1 do Projeto do Robô.

A implementação é deliberadamente recursiva e não usa memoização, conforme o
escopo da primeira entrega.
"""

from __future__ import annotations

from typing import Any, MutableSequence, Sequence

Mapa = Sequence[Sequence[int | None]]


def recursivo(
    mapa: Mapa,
    linha: int = 0,
    coluna: int = 0,
    contador: MutableSequence[int] | None = None,
) -> int | None:
    """Retorna o menor custo da posição atual até a chegada.

    ``None`` representa um caminho impossível. Cada chamada considera apenas
    os movimentos para a direita e para baixo. O parâmetro opcional ``contador``
    existe para medir o trabalho sem alterar a lógica do algoritmo.

    Não há memória de resultados anteriores: uma mesma posição pode ser
    recalculada por ramos diferentes da árvore de recursão.
    """
    if not (0 <= linha < len(mapa) and 0 <= coluna < len(mapa[0])):
        return None

    if contador is not None:
        contador[0] += 1

    valor = mapa[linha][coluna]
    if valor is None:
        return None

    ultima_linha = linha == len(mapa) - 1
    ultima_coluna = coluna == len(mapa[0]) - 1
    if ultima_linha and ultima_coluna:
        return valor

    custo_direita = recursivo(mapa, linha, coluna + 1, contador)
    custo_baixo = recursivo(mapa, linha + 1, coluna, contador)
    custos_possiveis = [custo for custo in (custo_direita, custo_baixo) if custo is not None]

    if not custos_possiveis:
        return None
    return valor + min(custos_possiveis)


def guloso(mapa: Mapa) -> int | None:
    """Aplica a regra gulosa: vizinho livre mais barato, direita no empate.

    A função não pretende encontrar sempre a solução ótima; ela serve como
    comparação experimental com a busca exaustiva recursiva.
    """
    linha = coluna = 0
    custo_total = 0
    altura, largura = len(mapa), len(mapa[0])

    while True:
        valor_atual = mapa[linha][coluna]
        if valor_atual is None:
            return None
        custo_total += valor_atual
        if linha == altura - 1 and coluna == largura - 1:
            return custo_total

        vizinhos = []
        # A ordem garante a preferência pela direita quando os custos empatam.
        if coluna + 1 < largura and mapa[linha][coluna + 1] is not None:
            vizinhos.append((mapa[linha][coluna + 1], linha, coluna + 1))
        if linha + 1 < altura and mapa[linha + 1][coluna] is not None:
            vizinhos.append((mapa[linha + 1][coluna], linha + 1, coluna))
        if not vizinhos:
            return None
        _, linha, coluna = min(vizinhos, key=lambda vizinho: vizinho[0])


def contar_chamadas(mapa: Mapa) -> tuple[int | None, int]:
    """Executa a recursão e devolve ``(custo, quantidade_de_chamadas)``."""
    contador = [0]
    custo = recursivo(mapa, contador=contador)
    return custo, contador[0]


def validar_mapa(mapa: Any) -> str | None:
    """Retorna uma mensagem de erro ou ``None`` quando o mapa é válido."""
    if not isinstance(mapa, list) or not mapa:
        return "'custos' deve ser uma lista não vazia."
    if any(not isinstance(linha, list) or not linha for linha in mapa):
        return "'custos' deve conter linhas não vazias."
    largura = len(mapa[0])
    if any(len(linha) != largura for linha in mapa):
        return "todas as linhas de 'custos' devem ter o mesmo tamanho."
    for linha in mapa:
        for valor in linha:
            # bool é subtipo de int em Python, por isso precisa ser excluído.
            if valor is not None and (isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0):
                return "cada custo deve ser um inteiro positivo ou null."
    return None


def resolver(entrada: str | dict[str, Any]) -> dict[str, Any]:
    """Valida uma entrada JSON e devolve o resultado definido no contrato."""
    import json

    if isinstance(entrada, str):
        try:
            dados = json.loads(entrada)
        except json.JSONDecodeError as erro:
            return {"status": "entrada_invalida", "erro": f"JSON inválido: {erro.msg}."}
    elif isinstance(entrada, dict):
        # Aceitar dict facilita o uso em testes Python; a interface oficial é JSON.
        dados = entrada
    else:
        return {"status": "entrada_invalida", "erro": "a entrada deve ser um texto JSON."}

    if not isinstance(dados, dict) or "custos" not in dados:
        return {"status": "entrada_invalida", "erro": "a entrada deve conter a chave 'custos'."}

    mapa = dados["custos"]
    erro = validar_mapa(mapa)
    if erro is not None:
        return {"status": "entrada_invalida", "erro": erro}

    custo = recursivo(mapa)
    if custo is None:
        return {"status": "sem_caminho", "custo": None}
    return {"status": "ok", "custo": custo}

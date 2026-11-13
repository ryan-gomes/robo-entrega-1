"""Interface de linha de comando para resolver mapas do robô."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .solucao import resolver


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Encontra o menor custo de um robô em uma grade."
    )
    parser.add_argument(
        "arquivo",
        nargs="?",
        type=Path,
        help="arquivo JSON; sem ele, a entrada será lida da entrada padrão",
    )
    args = parser.parse_args()

    try:
        texto = args.arquivo.read_text(encoding="utf-8") if args.arquivo else sys.stdin.read()
    except OSError as erro:
        print(json.dumps({"status": "entrada_invalida", "erro": str(erro)}, ensure_ascii=False))
        return 1

    print(json.dumps(resolver(texto), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

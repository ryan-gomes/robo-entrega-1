# Projeto do Robô — Entrega 1

Implementação individual em Python do problema de encontrar o menor custo de uma rota em uma grade. A solução usa recursão sem memoização, conforme o enunciado, e inclui uma estratégia gulosa para comparação.

## Requisitos

- Python 3.10 ou superior;
- nenhuma dependência externa para executar a solução e os testes.

## Instalação local

Na raiz do projeto, recomenda-se criar um ambiente virtual:

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -e .
```

## Uso

A aplicação recebe um arquivo JSON ou lê JSON pela entrada padrão:

```bash
python -m robo.cli exemplos/mapa_exemplo.json
# ou
cat exemplos/mapa_exemplo.json | python -m robo.cli
```

Saída esperada para o mapa do enunciado:

```json
{"status": "ok", "custo": 11}
```

## Testes

```bash
python -m unittest discover -s tests -v
```

## Organização

- `src/robo/solucao.py`: validação, função `resolver`, busca `recursivo`, `guloso` e medição de chamadas;
- `src/robo/cli.py`: interface de linha de comando;
- `tests/`: testes obrigatórios e casos criados para o trabalho;
- `exemplos/`: entradas JSON de demonstração;
- `docs/relatorio.md` e `docs/relatorio.pdf`: relatório em formato de artigo;
- `CONTRIBUTING.md`: convenções de versionamento e contribuição.

A lista de coordenadas do caminho e a memoização não fazem parte desta entrega, como determinado no enunciado.

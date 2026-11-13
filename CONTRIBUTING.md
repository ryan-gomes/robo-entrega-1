# Convenções de desenvolvimento

Este é um projeto acadêmico individual. As alterações devem ser pequenas, explicáveis e relacionadas a um requisito do enunciado.

## Commits

Use mensagens no imperativo e em português, por exemplo:

- `feat: adiciona busca recursiva sem memoização`
- `test: cobre entradas inválidas`
- `docs: atualiza explicação da estratégia gulosa`

Antes de criar um commit, execute os testes com `python -m unittest discover -s tests -v`. Não versione ambientes virtuais, caches, arquivos compilados ou resultados de execução.

## Comentários no código

Os comentários devem explicar decisões ou regras do problema, e não repetir literalmente o que a linha já faz. As funções públicas possuem docstrings em português para apoiar a leitura educacional.

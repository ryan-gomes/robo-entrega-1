import json
import sys
import unittest
from pathlib import Path

# Permite executar os testes diretamente na raiz, antes de uma instalação local.
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from robo.solucao import contar_chamadas, guloso, recursivo, resolver


class TestResolver(unittest.TestCase):
    def assert_resultado(self, custos, esperado):
        self.assertEqual(resolver(json.dumps({"custos": custos})), esperado)

    def test_casos_obrigatorios(self):
        self.assert_resultado([[7]], {"status": "ok", "custo": 7})
        self.assert_resultado([[1, 2, 3]], {"status": "ok", "custo": 6})
        self.assert_resultado([[1], [2], [3]], {"status": "ok", "custo": 6})
        self.assert_resultado([[1, 1, 1], [1, 1, 1]], {"status": "ok", "custo": 4})
        self.assert_resultado(
            [[2, 1, 9, 9, 9], [3, None, 1, 1, 9], [1, 1, 1, None, 2], [9, 9, 1, 1, 1]],
            {"status": "ok", "custo": 11},
        )
        self.assert_resultado([[1, 1, None], [2, None, 1], [1, 1, 1]], {"status": "ok", "custo": 6})
        for mapa in ([[None]], [[None, 1], [1, 1]], [[1, 1], [1, None]], [[1, None], [None, 1]]):
            self.assert_resultado(mapa, {"status": "sem_caminho", "custo": None})

    def test_casos_invalidos(self):
        for entrada in (
            {"custos": []}, {"custos": [[]]}, {"custos": [[1, 2], [3]]},
            {"custos": [[True, 1]]}, {"custos": [["1", 1]]},
            {"custos": [[1.5, 1]]}, {"custos": [[0, 1]]}, {"custos": [[-1, 1]]},
            {"matriz": [[1]]},
        ):
            self.assertEqual(resolver(json.dumps(entrada))["status"], "entrada_invalida")
        self.assertEqual(resolver('{"custos": [[1, 2]') ["status"], "entrada_invalida")
        self.assertEqual(resolver([[1]])["status"], "entrada_invalida")

    def test_tres_casos_criados_pelo_estudante(self):
        self.assert_resultado([[4, None, 2], [1, 1, 1]], {"status": "ok", "custo": 7})
        self.assert_resultado([[5, 1], [None, 2], [1, 1]], {"status": "ok", "custo": 9})
        self.assert_resultado([[2, 100, 100], [3, 4, 100], [100, 1, 1]], {"status": "ok", "custo": 11})


class TestRecursaoEGuloso(unittest.TestCase):
    def test_recursivo_retorna_none_sem_rota(self):
        self.assertIsNone(recursivo([[1, None], [None, 1]]))

    def test_contagem_de_chamadas(self):
        casos = (
            ([[1] * 3 for _ in range(2)], 9),
            ([[1] * 3 for _ in range(3)], 19),
            ([[1] * 6 for _ in range(6)], 923),
            ([[1] * 10 for _ in range(10)], 184755),
            ([[1] * 10], 10),
        )
        for mapa, chamadas in casos:
            _, quantidade = contar_chamadas(mapa)
            self.assertEqual(quantidade, chamadas)

    def test_guloso_acerta_e_respeita_empate_a_direita(self):
        exemplo = [[2, 1, 9, 9, 9], [3, None, 1, 1, 9], [1, 1, 1, None, 2], [9, 9, 1, 1, 1]]
        self.assertEqual(guloso(exemplo), 26)
        self.assertEqual(guloso([[1, 1], [1, 1]]), 3)

    def test_grade_propria_em_que_guloso_erra(self):
        mapa = [[1, 1, 50], [5, 50, 50], [1, 1, 1]]
        self.assertEqual(recursivo(mapa), 9)
        self.assertEqual(guloso(mapa), 103)


if __name__ == "__main__":
    unittest.main()

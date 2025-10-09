import unittest
from parser import parse_code

class TestParser(unittest.TestCase):

    def test_single_component(self):
        code = 'Botao(texto="Clique", x=10, y=20)'
        result = parse_code(code)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['tipo'], 'botao')
        self.assertEqual(result[0]['propriedades'], {'texto': 'Clique', 'x': 10, 'y': 20})

    def test_multiple_components(self):
        code = '''
        Label(texto='Nome:')
        CaixaDeTexto(x=100, y=0)
        '''
        result = parse_code(code)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['tipo'], 'label')
        self.assertEqual(result[1]['tipo'], 'caixadetexto')
        self.assertEqual(result[1]['propriedades']['x'], 100)

    def test_all_data_types(self):
        code = 'Componente(texto="Teste", inteiro=123, flutuante=45.6, texto_simples=\'abc\')'
        result = parse_code(code)
        props = result[0]['propriedades']
        self.assertEqual(props['texto'], 'Teste')
        self.assertIsInstance(props['texto'], str)
        self.assertEqual(props['inteiro'], 123)
        self.assertIsInstance(props['inteiro'], int)
        self.assertEqual(props['flutuante'], 45.6)
        self.assertIsInstance(props['flutuante'], float)
        self.assertEqual(props['texto_simples'], 'abc')
        self.assertIsInstance(props['texto_simples'], str)

    def test_whitespace_and_empty_lines(self):
        code = '''

        Botao( texto = "OK" , y = 50 )

        Label(texto="Info")

        '''
        result = parse_code(code)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['propriedades']['texto'], 'OK')
        self.assertEqual(result[0]['propriedades']['y'], 50)

    def test_invalid_syntax(self):
        code = 'Isto nao e valido'
        result = parse_code(code)
        self.assertEqual(len(result), 0) # Should not parse anything

    def test_case_insensitivity_of_component(self):
        code = 'LaBeL(texto="Case Test")'
        result = parse_code(code)
        self.assertEqual(result[0]['tipo'], 'label')

    def test_no_properties(self):
        code = 'Botao()'
        result = parse_code(code)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['tipo'], 'botao')
        self.assertEqual(result[0]['propriedades'], {})

if __name__ == '__main__':
    unittest.main()
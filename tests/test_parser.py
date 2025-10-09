import unittest
import sys
import os

# Add the src directory to the Python path to import modules from there
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.parser import parse_dsl
from src.components import UIComponent

class TestDSLParser(unittest.TestCase):

    def test_simple_component(self):
        """Tests parsing a single component without children."""
        code = "Button(text='Click Me', color='blue')"
        result = parse_dsl(code)
        expected = UIComponent(
            type='Button',
            properties={'text': 'Click Me', 'color': 'blue'},
            layout_params={},
            children=[]
        )
        self.assertEqual(result, expected)

    def test_component_with_layout_params(self):
        """Tests parsing a component with layout parameters."""
        code = "Text(value='Hello', width=200, alignment='center')"
        result = parse_dsl(code)
        expected = UIComponent(
            type='Text',
            properties={'value': 'Hello'},
            layout_params={'width': 200, 'alignment': 'center'},
            children=[]
        )
        self.assertEqual(result, expected)

    def test_nested_components(self):
        """Tests parsing a component with nested children."""
        code = """
Container(
    alignment='center',
    children=[
        Text(value='Title'),
        Button(text='Submit', width='fill')
    ]
)
"""
        result = parse_dsl(code)
        expected = UIComponent(
            type='Container',
            properties={},
            layout_params={'alignment': 'center'},
            children=[
                UIComponent(
                    type='Text',
                    properties={'value': 'Title'},
                    layout_params={},
                    children=[]
                ),
                UIComponent(
                    type='Button',
                    properties={'text': 'Submit'},
                    layout_params={'width': 'fill'},
                    children=[]
                )
            ]
        )
        self.assertEqual(result, expected)

    def test_invalid_syntax(self):
        """Tests if the parser handles syntax errors gracefully."""
        code = "Button(text='Missing Quote)"
        result = parse_dsl(code)
        self.assertIsNone(result)

    def test_empty_input(self):
        """Tests if the parser handles empty input."""
        code = ""
        result = parse_dsl(code)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
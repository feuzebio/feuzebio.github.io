import ast
from .components import UIComponent

class DSLParser(ast.NodeVisitor):
    """
    Parses a Python-like DSL string into a tree of UIComponent objects
    using Python's Abstract Syntax Tree (AST).
    """

    def visit_Call(self, node: ast.Call):
        """Processes a function call, like Button(...) or Container(...)."""
        component_type = node.func.id
        properties = {}
        layout_params = {}
        children = []

        for keyword in node.keywords:
            arg_name = keyword.arg
            arg_value = self._get_value(keyword.value)

            if arg_name == 'children':
                if isinstance(keyword.value, ast.List):
                    children = [self.visit(child_node) for child_node in keyword.value.elts]
                else:
                    # Handle single child case if necessary
                    children = [self.visit(keyword.value)]
            elif arg_name in ['width', 'height', 'margin', 'alignment']:
                layout_params[arg_name] = arg_value
            else:
                properties[arg_name] = arg_value

        # We only return the component if it's a valid call, otherwise child nodes will be None
        if component_type:
            return UIComponent(
                type=component_type,
                properties=properties,
                layout_params=layout_params,
                children=children
            )
        return None

    def _get_value(self, node: ast.AST):
        """Extracts the Python value from an AST node."""
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Dict):
            return {self._get_value(k): self._get_value(v) for k, v in zip(node.keys, node.values)}
        elif isinstance(node, ast.List):
            return [self._get_value(e) for e in node.elts]
        # Add more type handlers as needed (e.g., for tuples)
        return None

def parse_dsl(code_string: str) -> UIComponent:
    """
    Parses the DSL code string and returns the root UIComponent.
    """
    try:
        # We expect a single expression, so we get the first body element
        parsed_ast = ast.parse(code_string.strip(), mode='eval')
        parser = DSLParser()
        # The top level node in 'eval' mode is Expression
        return parser.visit(parsed_ast.body)
    except (SyntaxError, AttributeError, TypeError) as e:
        print(f"Error parsing DSL: {e}")
        return None
import ast
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests


class RouteVisitor(ast.NodeVisitor):
    """
    AST visitor to find Flask/FastAPI routes and extract their info.
    """
    def __init__(self):
        self.routes = []

    def visit_FunctionDef(self, node):
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call):
                decorator_name = self._get_decorator_name(decorator)
                if decorator_name in ['app.route', 'app.get', 'app.post', 'app.put', 'app.delete']:
                    route_info = self._extract_route_info(node, decorator, decorator_name)
                    if route_info:
                        self.routes.append(route_info)
        self.generic_visit(node)

    def _get_decorator_name(self, decorator):
        """Recursively get the full decorator name (e.g., 'app.route')."""
        if isinstance(decorator.func, ast.Attribute):
            return f"{self._get_decorator_name(decorator.func.value)}.{decorator.func.attr}"
        elif isinstance(decorator.func, ast.Name):
            return decorator.func.id
        return None

    def _extract_route_info(self, node, decorator, decorator_name):
        """Extracts path, methods, and params from a route decorator."""
        path = decorator.args[0].s if decorator.args and isinstance(decorator.args[0], ast.Str) else "/"

        methods = ['GET'] # Default method
        if decorator_name == 'app.route':
            for keyword in decorator.keywords:
                if keyword.arg == 'methods' and isinstance(keyword.value, (ast.List, ast.Tuple)):
                    methods = [elt.s for elt in keyword.value.elts if isinstance(elt, ast.Str)]
        elif decorator_name.startswith('app.'):
             methods = [decorator_name.split('.')[1].upper()]


        params = [arg.arg for arg in node.args.args if arg.arg != 'self']

        return {
            "path": path,
            "methods": methods,
            "params": params,
            "name": node.name
        }


@app.route('/api/analyze', methods=['POST'])
def analyze_code():
    """
    Analyzes Python code from a POST request to extract web routes.
    It uses Python's AST module to safely parse the code without executing it.
    """
    code = request.json.get('code')
    if not code:
        return jsonify({"error": "No code provided"}), 400

    try:
        tree = ast.parse(code)
        visitor = RouteVisitor()
        visitor.visit(tree)
        return jsonify({"routes": visitor.routes})
    except SyntaxError as e:
        return jsonify({"error": f"Syntax error in code: {e}"}), 400

import io
import zipfile
from flask import send_file

@app.route('/api/export', methods=['POST'])
def export_code():
    """
    Receives generated code (HTML, CSS, JS) and returns it as a zip file.
    """
    data = request.json
    html_content = data.get('html', '')
    css_content = data.get('css', '')
    js_content = data.get('js', '')

    # Create a zip file in memory
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('index.html', html_content)
        zf.writestr('style.css', css_content)
        zf.writestr('script.js', js_content)
    memory_file.seek(0)

    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name='frontend.zip'
    )

if __name__ == '__main__':
    app.run(debug=True, port=5001)
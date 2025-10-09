import tkinter as tk
from parser import parse_code
from renderer import render_ui

def main():
    root = tk.Tk()
    root.title("Live UI Renderer")
    root.geometry("1200x800") # Increased height for better view

    # --- UI Setup ---
    code_editor_frame = tk.Frame(root, width=600, bg='white')
    code_editor_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    code_editor_frame.pack_propagate(False)

    render_frame = tk.Frame(root, width=600, bg='lightgrey')
    render_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    render_frame.pack_propagate(False)

    editor = tk.Text(code_editor_frame, wrap=tk.WORD, undo=True, font=("Courier New", 10))
    editor.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

    canvas = tk.Canvas(render_frame, bg='white')
    canvas.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

    # --- Live Update Logic ---
    def update_ui(event=None):
        """
        Gets code from editor, parses it, and renders the UI on the canvas.
        """
        code = editor.get("1.0", tk.END)
        components = parse_code(code)
        render_ui(canvas, components)

    # Bind the update function to text changes
    editor.bind("<KeyRelease>", update_ui)

    # Insert some initial example code
    initial_code = """# Escreva seu código de UI aqui!
# Exemplo:
Label(texto="Olá, Mundo!", x=50, y=20, cor_texto="blue")
Botao(texto="Clique Aqui", x=50, y=50, largura=120, altura=40, cor_fundo="green", cor_texto="white")
CaixaDeTexto(texto="Digite algo...", x=50, y=100, largura=200)
"""
    editor.insert("1.0", initial_code)

    # Initial render
    update_ui()

    root.mainloop()

if __name__ == "__main__":
    main()
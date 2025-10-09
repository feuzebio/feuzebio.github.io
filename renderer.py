import tkinter as tk

def render_ui(canvas, components):
    """
    Renders the UI components on the given canvas.
    """
    canvas.delete("all")

    for comp in components:
        props = comp.get('propriedades', {})
        comp_type = comp.get('tipo')

        # Default values
        x = props.get('x', 10)
        y = props.get('y', 10)
        texto = props.get('texto', '')
        cor_fundo = props.get('cor_fundo', 'lightgray')
        cor_texto = props.get('cor_texto', 'black')

        if comp_type == 'botao':
            largura = props.get('largura', 80)
            altura = props.get('altura', 30)
            canvas.create_rectangle(x, y, x + largura, y + altura, fill=cor_fundo, outline='black')
            canvas.create_text(x + largura / 2, y + altura / 2, text=texto, fill=cor_texto)

        elif comp_type == 'label':
            canvas.create_text(x, y, text=texto, fill=cor_texto, anchor='nw')

        elif comp_type == 'caixadetexto':
            largura = props.get('largura', 150)
            altura = props.get('altura', 25)
            canvas.create_rectangle(x, y, x + largura, y + altura, fill='white', outline='gray')
            # Placeholder text inside the box
            canvas.create_text(x + 5, y + altura / 2, text=texto, fill='gray', anchor='w')

        elif comp_type == 'janela':
            # The 'janela' could define the canvas properties, but for now, we'll ignore it
            # as the main window is already created. Or it could represent inner frames.
            # For this version, we'll just print a note.
            print(f"Componente 'Janela' recebido, mas a renderização no canvas não é aplicável nesta versão.")

        else:
            print(f"Componente desconhecido: {comp_type}")
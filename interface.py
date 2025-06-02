import tkinter as tk

def create_scientific_calculator_interface():
    root = tk.Tk()
    root.title("Calculadora em python")
    root.geometry("400x600") # Tamanho inicial da janela
    root.resizable(False, False) # Impede o redimensionamento

    # --- Configuração das cores e fontes ---
    bg_color = "#333333" # Cor de fundo escura
    button_color = "#555555" # Cor dos botões
    operator_color = "#FF9900" # Laranja para operadores
    function_color = "#777777" # Cinza mais claro para funções científicas
    text_color = "white"
    font_large = ("Arial", 24)
    font_medium = ("Arial", 16)

    root.configure(bg=bg_color)

    # --- Tela de exibição ---
    display_frame = tk.Frame(root, bg=bg_color)
    display_frame.pack(expand=True, fill="both", padx=10, pady=10)

    display = tk.Entry(display_frame, width=20, font=font_large, bd=0,
                       bg="#1a1a1a", fg=text_color, justify="right",
                       insertbackground=text_color)
    display.pack(expand=True, fill="both", ipady=10)
    display.insert(0, "0") # Valor inicial

    # --- Frame para os botões ---
    button_frame = tk.Frame(root, bg=bg_color)
    button_frame.pack(expand=True, fill="both")

    # --- Layout dos botões ---
    buttons = [
        # Linha 1
        ("Rad", function_color), ("Deg", function_color), ("x!", function_color), ("(", function_color), (")", function_color), ("%", operator_color), ("AC", operator_color),
        # Linha 2
        ("sin", function_color), ("cos", function_color), ("tan", function_color), ("ln", function_color), ("log", function_color), ("sqrt", operator_color), ("/", operator_color),
        # Linha 3
        ("e", function_color), ("pi", function_color), ("^", function_color), ("7", button_color), ("8", button_color), ("9", button_color), ("*", operator_color),
        # Linha 4
        ("abs", function_color), ("exp", function_color), ("deg", function_color), ("4", button_color), ("5", button_color), ("6", button_color), ("-", operator_color),
        # Linha 5
        ("inv", function_color), ("hyp", function_color), ("ans", function_color), ("1", button_color), ("2", button_color), ("3", button_color), ("+", operator_color),
        # Linha 6
        ("x²", function_color), ("x³", function_color), ("+/-", button_color), ("0", button_color), (".", button_color), ("=", operator_color),
    ]

    row = 0
    col = 0
    for (text, color) in buttons:
        button = tk.Button(button_frame, text=text, font=font_medium,
                           bg=color, fg=text_color, bd=0, padx=20, pady=20,
                           activebackground="#888888", activeforeground="white")
        if text == "0":
            button.grid(row=row, column=col, columnspan=2, sticky="nsew", padx=2, pady=2)
            col += 1
        else:
            button.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

        col += 1
        if col > 6: # 7 colunas por linha (0 a 6)
            col = 0
            row += 1

    # Configura o redimensionamento das linhas e colunas dentro do button_frame
    for i in range(7): # 7 colunas
        button_frame.grid_columnconfigure(i, weight=1)
    for i in range(row + 1): # número de linhas criadas
        button_frame.grid_rowconfigure(i, weight=1)

    root.mainloop()

if __name__ == "__main__":
    create_scientific_calculator_interface()



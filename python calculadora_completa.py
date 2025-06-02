import tkinter as tk
import math

class CalculadoraCientifica:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Científica Completa")
        self.root.geometry("400x600")
        self.root.configure(bg="#1e1e1e")

        self.expressao = ""
        self.entrada_texto = tk.StringVar()

        self.criar_interface()

    def criar_interface(self):
        entrada = tk.Entry(self.root, textvariable=self.entrada_texto, font=('Arial', 24), bg="white", bd=5, relief="sunken", justify="right")
        entrada.pack(fill="both", padx=10, pady=10)

        botoes = [
            ['7', '8', '9', '/', 'sqrt'],
            ['4', '5', '6', '*', '^'],
            ['1', '2', '3', '-', 'log'],
            ['0', '.', '(', ')', '+'],
            ['π', 'e', 'sin', 'cos', 'tan'],
            ['C', '⌫', '=', '', '']
        ]

        for linha in botoes:
            frame = tk.Frame(self.root, bg="#1e1e1e")
            frame.pack(expand=True, fill="both")
            for texto in linha:
                if texto:
                    btn = tk.Button(frame, text=texto, font=("Arial", 16), bg="#333", fg="white",
                                    command=lambda t=texto: self.clique(t))
                    btn.pack(side="left", expand=True, fill="both")

    def clique(self, tecla):
        if tecla == 'C':
            self.expressao = ''
        elif tecla == '⌫':
            self.expressao = self.expressao[:-1]
        elif tecla == '=':
            try:
                resultado = self.calcular(self.expressao)
                self.expressao = str(resultado)
            except Exception:
                self.expressao = 'Erro'
        elif tecla == 'π':
            self.expressao += str(math.pi)
        elif tecla == 'e':
            self.expressao += str(math.e)
        elif tecla == 'sqrt':
            self.expressao += 'sqrt('
        elif tecla in ['sin', 'cos', 'tan', 'log']:
            self.expressao += f"{tecla}("
        elif tecla == '^':
            self.expressao += '**'
        else:
            self.expressao += str(tecla)

        self.entrada_texto.set(self.expressao)

    def calcular(self, exp):
        return eval(exp, {"__builtins__": None}, {
            "sin": lambda x: math.sin(math.radians(x)),
            "cos": lambda x: math.cos(math.radians(x)),
            "tan": lambda x: math.tan(math.radians(x)),
            "log": lambda x: math.log10(x),
            "sqrt": math.sqrt,
            "pi": math.pi,
            "e": math.e
        })

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraCientifica(root)
    root.mainloop()
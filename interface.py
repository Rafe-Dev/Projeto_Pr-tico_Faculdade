# interface.py
import tkinter as tk
import math
import datetime

class CalculadoraGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Científica com Histórico")
        self.root.geometry("400x720")

        # Detectar modo inicial
        self.modo = self.detectar_modo()
        self.estilos = self.definir_cores(self.modo)

        self.root.configure(bg=self.estilos["bg"])

        self.expressao = ""
        self.entrada_texto = tk.StringVar()

        self.criar_interface()

    def detectar_modo(self):
        hora = datetime.datetime.now().hour
        return "claro" if 6 <= hora < 18 else "escuro"

    def definir_cores(self, modo):
        if modo == "claro":
            return {
                "bg": "#ffffff",
                "fg": "#000000",
                "btn_bg": "#e0e0e0",
                "btn_fg": "#000000",
                "display_bg": "#ffffff",
                "hist_bg": "#f0f0f0"
            }
        else:
            return {
                "bg": "#1e1e1e",
                "fg": "#ffffff",
                "btn_bg": "#333333",
                "btn_fg": "#ffffff",
                "display_bg": "#2e2e2e",
                "hist_bg": "#3a3a3a"
            }

    def criar_interface(self):
        # Botão alternar tema
        self.botao_tema = tk.Button(
            self.root, text="Alternar Tema", font=("Arial", 12),
            bg=self.estilos["btn_bg"], fg=self.estilos["btn_fg"],
            command=self.alternar_tema
        )
        self.botao_tema.pack(pady=(10, 0), padx=10, anchor="ne")

        # Campo de entrada
        self.entrada = tk.Entry(
            self.root, textvariable=self.entrada_texto, font=('Arial', 24),
            bg=self.estilos["display_bg"], fg=self.estilos["fg"],
            bd=5, relief="sunken", justify="right"
        )
        self.entrada.pack(fill="both", padx=10, pady=10)

        botoes = [
            ['7', '8', '9', '/', 'sqrt'],
            ['4', '5', '6', '*', '^'],
            ['1', '2', '3', '-', 'log'],
            ['0', '.', '(', ')', '+'],
            ['π', 'e', 'sin', 'cos', 'tan'],
            ['C', '⌫', '=', '', '']
        ]

        self.frames_botoes = []

        for linha in botoes:
            frame = tk.Frame(self.root, bg=self.estilos["bg"])
            self.frames_botoes.append(frame)
            frame.pack(expand=True, fill="both")
            for texto in linha:
                if texto:
                    btn = tk.Button(
                        frame, text=texto, font=("Arial", 16),
                        bg=self.estilos["btn_bg"], fg=self.estilos["btn_fg"],
                        command=lambda t=texto: self.clique(t)
                    )
                    btn.pack(side="left", expand=True, fill="both")

        # Histórico
        self.label_hist = tk.Label(self.root, text="Histórico de Cálculos", font=("Arial", 14),
                                   bg=self.estilos["bg"], fg=self.estilos["fg"])
        self.label_hist.pack(pady=(10, 0))

        self.caixa_hist = tk.Text(self.root, height=8, font=("Arial", 12),
                                  bg=self.estilos["hist_bg"], fg=self.estilos["fg"],
                                  state='disabled', wrap='word')
        self.caixa_hist.pack(fill="both", padx=10, pady=5, expand=False)

        scrollbar = tk.Scrollbar(self.caixa_hist)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.caixa_hist.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.caixa_hist.yview)

    def alternar_tema(self):
        self.modo = "escuro" if self.modo == "claro" else "claro"
        self.estilos = self.definir_cores(self.modo)
        self.atualizar_tema()

    def atualizar_tema(self):
        self.root.configure(bg=self.estilos["bg"])
        self.entrada.configure(bg=self.estilos["display_bg"], fg=self.estilos["fg"])
        self.label_hist.configure(bg=self.estilos["bg"], fg=self.estilos["fg"])
        self.caixa_hist.configure(bg=self.estilos["hist_bg"], fg=self.estilos["fg"])

        self.botao_tema.configure(bg=self.estilos["btn_bg"], fg=self.estilos["btn_fg"])

        # Atualizar botões
        for frame in self.frames_botoes:
            for btn in frame.winfo_children():
                btn.configure(bg=self.estilos["btn_bg"], fg=self.estilos["btn_fg"])
            frame.configure(bg=self.estilos["bg"])

    def clique(self, tecla):
        if tecla == 'C':
            self.expressao = ''
        elif tecla == '⌫':
            self.expressao = self.expressao[:-1]
        elif tecla == '=':
            try:
                resultado = self.calcular(self.expressao)
                self.adicionar_historico(f"{self.expressao} = {resultado}")
                self.expressao = str(resultado)
            except Exception:
                self.adicionar_historico(f"{self.expressao} = Erro")
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

    def adicionar_historico(self, texto):
        self.caixa_hist.config(state='normal')
        self.caixa_hist.insert(tk.END, texto + "\n")
        self.caixa_hist.see(tk.END)
        self.caixa_hist.config(state='disabled')
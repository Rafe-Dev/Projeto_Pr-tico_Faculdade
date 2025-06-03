import tkinter as tk
import math
import datetime

class CalculadoraGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Científica com Histórico")
        self.root.geometry("400x720")

        self.modo = self.detectar_modo()
        self.estilos = self.definir_cores(self.modo)

        self.root.configure(bg=self.estilos["bg"])

        self.expressao = ""
        self.entrada_texto = tk.StringVar()
        self.ultimo_resultado = None
        self.limpar_ao_digitar = False  # limpa display após resultado/erro

        self.criar_interface()
        self.root.bind("<Key>", self.tecla_digitada)

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
        self.botao_tema = tk.Button(
            self.root, text="Alternar Tema", font=("Arial", 12),
            bg=self.estilos["btn_bg"], fg=self.estilos["btn_fg"],
            command=self.alternar_tema
        )
        self.botao_tema.pack(pady=(10, 0), padx=10, anchor="ne")

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
            ['C', '⌫', '=', 'ans', 'x!']
        ]

        self.frame_botoes = tk.Frame(self.root, bg=self.estilos["bg"])
        self.frame_botoes.pack(expand=True, fill="both", padx=10, pady=5)

        for i, linha in enumerate(botoes):
            for j, texto in enumerate(linha):
                btn = tk.Button(
                    self.frame_botoes, text=texto, font=("Arial", 16),
                    bg=self.estilos["btn_bg"], fg=self.estilos["btn_fg"],
                    command=lambda t=texto: self.clique(t)
                )
                btn.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)

        for i in range(len(botoes)):
            self.frame_botoes.rowconfigure(i, weight=1)
        for j in range(len(botoes[0])):
            self.frame_botoes.columnconfigure(j, weight=1)

        self.label_hist = tk.Label(self.root, text="Histórico de Cálculos", font=("Arial", 14),
                                   bg=self.estilos["bg"], fg=self.estilos["fg"])
        self.label_hist.pack(pady=(10, 0))

        self.caixa_hist = tk.Text(self.root, height=8, font=("Arial", 12),
                                  bg=self.estilos["hist_bg"], fg=self.estilos["fg"],
                                  state='disabled', wrap='word')
        self.caixa_hist.pack(fill="both", padx=10, pady=5)

        self.scrollbar = tk.Scrollbar(self.caixa_hist)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.caixa_hist.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.caixa_hist.yview)

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
        self.frame_botoes.configure(bg=self.estilos["bg"])

        for btn in self.frame_botoes.winfo_children():
            btn.configure(bg=self.estilos["btn_bg"], fg=self.estilos["btn_fg"])

    def clique(self, tecla):
        if self.limpar_ao_digitar and tecla not in ['=', 'C', '⌫', 'ans']:
            self.expressao = ''
            self.limpar_ao_digitar = False

        if tecla == 'C':
            self.expressao = ''
            self.limpar_ao_digitar = False
        elif tecla == '⌫':
            self.expressao = self.expressao[:-1]
        elif tecla == '=':
            try:
                resultado = self.calcular(self.expressao)
                self.adicionar_historico(f"{self.expressao} = {resultado}")
                self.expressao = str(resultado)
                self.ultimo_resultado = resultado
                self.limpar_ao_digitar = True
            except ZeroDivisionError:
                self.adicionar_historico(f"{self.expressao} = Erro: Divisão por zero")
                self.expressao = 'Erro: Divisão por zero'
                self.limpar_ao_digitar = True
            except SyntaxError:
                self.adicionar_historico(f"{self.expressao} = Erro: Sintaxe inválida")
                self.expressao = 'Erro: Sintaxe inválida'
                self.limpar_ao_digitar = True
            except ValueError as ve:
                self.adicionar_historico(f"{self.expressao} = Erro: {ve}")
                self.expressao = f'Erro: {ve}'
                self.limpar_ao_digitar = True
            except Exception as e:
                self.adicionar_historico(f"{self.expressao} = Erro: {e}")
                self.expressao = 'Erro'
                self.limpar_ao_digitar = True
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
        elif tecla == 'ans':
            if self.ultimo_resultado is not None:
                self.expressao += str(self.ultimo_resultado)
        elif tecla == 'x!':
            self.expressao += 'factorial('
        else:
            self.expressao += str(tecla)

        self.entrada_texto.set(self.expressao)

    def calcular(self, exp):
        def safe_factorial(x):
            if not (isinstance(x, int) and x >= 0):
                raise ValueError("Fatorial só para inteiros >= 0")
            return math.factorial(x)

        funcoes = {
            "sin": lambda x: math.sin(math.radians(x)),
            "cos": lambda x: math.cos(math.radians(x)),
            "tan": lambda x: math.tan(math.radians(x)),
            "log": math.log10,
            "sqrt": math.sqrt,
            "factorial": safe_factorial,
            "pi": math.pi,
            "e": math.e,
        }
        # Avalia expressão com funções e constantes permitidas
        return eval(exp, {"__builtins__": None}, funcoes)

    def adicionar_historico(self, texto):
        self.caixa_hist.config(state='normal')
        self.caixa_hist.insert(tk.END, texto + "\n")
        self.caixa_hist.see(tk.END)
        self.caixa_hist.config(state='disabled')

    def tecla_digitada(self, evento):
        tecla = evento.keysym

        if tecla in "0123456789":
            self.clique(tecla)
        elif tecla in ("plus", "KP_Add"):
            self.clique('+')
        elif tecla in ("minus", "KP_Subtract"):
            self.clique('-')
        elif tecla in ("asterisk", "KP_Multiply"):
            self.clique('*')
        elif tecla in ("slash", "KP_Divide"):
            self.clique('/')
        elif tecla == "parenleft":
            self.clique('(')
        elif tecla == "parenright":
            self.clique(')')
        elif tecla == "period":
            self.clique('.')
        elif tecla == "Return":
            self.clique('=')
        elif tecla == "BackSpace":
            self.clique('⌫')
        elif tecla == "Escape":
            self.clique('C')

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraGUI(root)
    root.mainloop()
# main.py
import tkinter as tk
from interface import CalculadoraGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraGUI(root)
    root.mainloop()
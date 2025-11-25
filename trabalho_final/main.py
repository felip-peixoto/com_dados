import tkinter as tk
from tkinter import font
from gui.emissor import EmissorGUI
from gui.receptor import ReceptorGUI

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Transmissão HDB3 - Trabalho Final")
        self.root.geometry("500x400")
        self.root.configure(bg="#f0f0f0")

        # Estilos de Fonte
        title_font = font.Font(family="Helvetica", size=16, weight="bold")
        btn_font = font.Font(family="Helvetica", size=12, weight="bold")

        # Container Central
        frame = tk.Frame(root, bg="#f0f0f0")
        frame.pack(expand=True)

        tk.Label(frame, text="Escolha o Modo de Operação", 
                 font=title_font, bg="#f0f0f0", fg="#333").pack(pady=30)

        # Botão Emissor
        btn_emissor = tk.Button(frame, text="Host A - EMISSOR", 
                                command=self.iniciar_emissor,
                                bg="#4CAF50", fg="white", 
                                font=btn_font, width=25, height=2,
                                activebackground="#45a049")
        btn_emissor.pack(pady=10)

        # Botão Receptor
        btn_receptor = tk.Button(frame, text="Host B - RECEPTOR", 
                                 command=self.iniciar_receptor,
                                 bg="#2196F3", fg="white", 
                                 font=btn_font, width=25, height=2,
                                 activebackground="#1e88e5")
        btn_receptor.pack(pady=10)

        tk.Label(frame, text="Engenharia de Redes - UTFPR", 
                 bg="#f0f0f0", fg="#777").pack(pady=40)

    def iniciar_emissor(self):
        self.limpar_janela()
        # Inicia a GUI do Emissor na mesma janela (root)
        EmissorGUI(self.root)

    def iniciar_receptor(self):
        self.limpar_janela()
        # Inicia a GUI do Receptor na mesma janela (root)
        ReceptorGUI(self.root)

    def limpar_janela(self):
        # Remove todos os widgets do Menu Principal (botões, labels)
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
import tkinter as tk
from tkinter import font
from gui.emissor import EmissorGUI
from gui.receptor import ReceptorGUI

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Transmissão HDB3")
        self.root.geometry("600x450")
        self.root.configure(bg="#f0f2f5") # Um cinza bem clarinho, moderno

        # --- Definição de Fontes ---
        # Fonte para Títulos (Moderna e Limpa)
        self.font_titulo = font.Font(family="Segoe UI", size=18, weight="bold")
        # Fonte para Texto Geral
        self.font_texto = font.Font(family="Segoe UI", size=11)
        # Fonte para Botões (Levemente maior)
        self.font_botao = font.Font(family="Segoe UI", size=12, weight="bold")
        
        # --- Layout ---
        # Container Central (Frame) com efeito de "cartão" (borda suave)
        frame = tk.Frame(root, bg="white", bd=1, relief="solid")
        frame.pack(expand=True, padx=20, pady=20, ipadx=20, ipady=20)
        
        # Borda decorativa interna (opcional, truque visual)
        frame.configure(highlightbackground="#d1d5db", highlightthickness=1)

        # Título
        lbl_titulo = tk.Label(frame, text="Codificação de Linha HDB3", 
                              font=self.font_titulo, bg="white", fg="#1f2937")
        lbl_titulo.pack(pady=(10, 5))
        
        lbl_sub = tk.Label(frame, text="Comunicação de Dados - Trabalho Final", 
                           font=("Segoe UI", 10), bg="white", fg="#6b7280")
        lbl_sub.pack(pady=(0, 30))

        # Botão Emissor (Verde Moderno)
        btn_emissor = tk.Button(frame, text="Iniciar HOST A (Emissor)", 
                                command=self.iniciar_emissor,
                                bg="#10b981", fg="white", # Verde Esmeralda
                                font=self.font_botao, 
                                relief="flat", cursor="hand2",
                                width=30, height=2)
        btn_emissor.pack(pady=10)

        # Botão Receptor (Azul Moderno)
        btn_receptor = tk.Button(frame, text="Iniciar HOST B (Receptor)", 
                                 command=self.iniciar_receptor,
                                 bg="#3b82f6", fg="white", # Azul Real
                                 font=self.font_botao,
                                 relief="flat", cursor="hand2",
                                 width=30, height=2)
        btn_receptor.pack(pady=10)

        # Rodapé
        tk.Label(frame, text="Engenharia de Redes • UTFPR", 
                 font=("Consolas", 9), bg="white", fg="#9ca3af").pack(pady=(40, 0))

    def iniciar_emissor(self):
        self.limpar_janela()
        EmissorGUI(self.root)

    def iniciar_receptor(self):
        self.limpar_janela()
        ReceptorGUI(self.root)

    def limpar_janela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
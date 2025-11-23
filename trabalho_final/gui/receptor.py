import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
from core.hdb3 import decode_hdb3
from core.conversor import binario_para_texto
from core.vigenere import decifrar_vigenere
from core.network import receber_sinal
from gui.plot_utils import plotar_hdb3

class ReceptorGUI:
    def __init__(self, master):
        master.title("Host B - Receptor")
        master.geometry("900x750")
        
        # Config
        frame_cfg = tk.Frame(master)
        frame_cfg.pack(pady=10)
        tk.Label(frame_cfg, text="Porta:").pack(side='left')
        self.entry_porta = tk.Entry(frame_cfg, width=10)
        self.entry_porta.insert(0, "5000")
        self.entry_porta.pack(side='left', padx=5)
        tk.Button(frame_cfg, text="Aguardar Sinal", command=self.iniciar_recepcao, bg='blue', fg='white').pack(side='left', padx=10)
        
        # Gráfico recebido
        tk.Label(master, text="Gráfico HDB3 Recebido:").pack(anchor='w', padx=10)
        self.frame_plot = tk.Frame(master, height=200)
        self.frame_plot.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Binário decodificado
        tk.Label(master, text="Mensagem Binária Decodificada:").pack(anchor='w', padx=10)
        self.txt_bin = scrolledtext.ScrolledText(master, height=3, width=100, state='disabled')
        self.txt_bin.pack(padx=10, pady=5)
        
        # Criptografado
        tk.Label(master, text="Mensagem Criptografada:").pack(anchor='w', padx=10)
        self.txt_cripto = scrolledtext.ScrolledText(master, height=3, width=100, state='disabled')
        self.txt_cripto.pack(padx=10, pady=5)
        
        # Chave para decifrar
        tk.Label(master, text="Chave Vigenère:").pack(anchor='w', padx=10)
        self.entry_chave = tk.Entry(master, width=100)
        self.entry_chave.pack(padx=10, pady=5)
        tk.Button(master, text="Decifrar", command=self.decifrar).pack(pady=5)
        
        # Mensagem final
        tk.Label(master, text="Mensagem Final (Texto Claro):").pack(anchor='w', padx=10)
        self.txt_final = scrolledtext.ScrolledText(master, height=3, width=100, state='disabled')
        self.txt_final.pack(padx=10, pady=5)
        
        self.sinal_recebido = None
        self.texto_cifrado = None
    
    def iniciar_recepcao(self):
        porta = int(self.entry_porta.get().strip())
        threading.Thread(target=self.receber, args=(porta,), daemon=True).start()
        messagebox.showinfo("Aguardando", f"Escutando na porta {porta}...")
    
    def receber(self, porta):
        self.sinal_recebido = receber_sinal(porta)
        if self.sinal_recebido:
            self.processar_sinal()
        else:
            messagebox.showerror("Erro", "Falha ao receber sinal.")
    
    def processar_sinal(self):
        # Plot
        for widget in self.frame_plot.winfo_children():
            widget.destroy()
        plotar_hdb3(self.frame_plot, self.sinal_recebido, "Sinal HDB3 Recebido")
        
        # Decodificar HDB3
        binario = decode_hdb3(self.sinal_recebido)
        self.txt_bin.config(state='normal')
        self.txt_bin.delete("1.0", tk.END)
        self.txt_bin.insert("1.0", binario)
        self.txt_bin.config(state='disabled')
        
        # Binário -> Texto cifrado
        self.texto_cifrado = binario_para_texto(binario)
        if self.texto_cifrado:
            self.txt_cripto.config(state='normal')
            self.txt_cripto.delete("1.0", tk.END)
            self.txt_cripto.insert("1.0", self.texto_cifrado)
            self.txt_cripto.config(state='disabled')
    
    def decifrar(self):
        if not self.texto_cifrado:
            messagebox.showwarning("Aviso", "Nenhum sinal recebido ainda.")
            return
        
        chave = self.entry_chave.get().strip()
        if not chave:
            messagebox.showwarning("Aviso", "Insira a chave.")
            return
        
        texto_final = decifrar_vigenere(self.texto_cifrado, chave)
        self.txt_final.config(state='normal')
        self.txt_final.delete("1.0", tk.END)
        self.txt_final.insert("1.0", texto_final)
        self.txt_final.config(state='disabled')
import tkinter as tk
from tkinter import messagebox, scrolledtext
from core.vigenere import cifrar_vigenere
from core.conversor import texto_para_binario
from core.hdb3 import encode_hdb3
from core.network import enviar_sinal
from gui.plot_utils import plotar_hdb3

class EmissorGUI:
    def __init__(self, master):
        master.title("Host A - Emissor")
        master.geometry("900x700")
        
        # Mensagem original
        tk.Label(master, text="Mensagem Original:").pack(anchor='w', padx=10, pady=(10,0))
        self.txt_msg = tk.Text(master, height=3, width=100)
        self.txt_msg.pack(padx=10, pady=5)
        
        # Chave Vigenère
        tk.Label(master, text="Chave Vigenère:").pack(anchor='w', padx=10)
        self.entry_chave = tk.Entry(master, width=100)
        self.entry_chave.pack(padx=10, pady=5)
        
        # Mensagem criptografada
        tk.Label(master, text="Mensagem Criptografada:").pack(anchor='w', padx=10)
        self.txt_cripto = scrolledtext.ScrolledText(master, height=3, width=100, state='disabled')
        self.txt_cripto.pack(padx=10, pady=5)
        
        # Binário
        tk.Label(master, text="Mensagem em Binário:").pack(anchor='w', padx=10)
        self.txt_bin = scrolledtext.ScrolledText(master, height=3, width=100, state='disabled')
        self.txt_bin.pack(padx=10, pady=5)
        
        # Frame do gráfico
        tk.Label(master, text="Gráfico HDB3:").pack(anchor='w', padx=10)
        self.frame_plot = tk.Frame(master, height=250)
        self.frame_plot.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Config de rede
        frame_rede = tk.Frame(master)
        frame_rede.pack(pady=10)
        tk.Label(frame_rede, text="IP Destino:").pack(side='left')
        self.entry_ip = tk.Entry(frame_rede, width=20)
        self.entry_ip.insert(0, "192.168.0.100")
        self.entry_ip.pack(side='left', padx=5)
        tk.Label(frame_rede, text="Porta:").pack(side='left')
        self.entry_porta = tk.Entry(frame_rede, width=10)
        self.entry_porta.insert(0, "5000")
        self.entry_porta.pack(side='left', padx=5)
        
        # Botão enviar
        tk.Button(master, text="ENVIAR", command=self.enviar, bg='green', fg='white', font=('Arial', 14, 'bold')).pack(pady=10)
        
        self.sinal_hdb3 = None
    
    def enviar(self):
        msg = self.txt_msg.get("1.0", tk.END).strip()
        chave = self.entry_chave.get().strip()
        
        if not msg or not chave:
            messagebox.showwarning("Aviso", "Preencha mensagem e chave.")
            return
        
        # 1. Cifrar
        cifrado = cifrar_vigenere(msg, chave)
        self.txt_cripto.config(state='normal')
        self.txt_cripto.delete("1.0", tk.END)
        self.txt_cripto.insert("1.0", cifrado)
        self.txt_cripto.config(state='disabled')
        
        # 2. Binário
        binario = texto_para_binario(cifrado)
        if not binario:
            messagebox.showerror("Erro", "Falha ao converter para binário.")
            return
        self.txt_bin.config(state='normal')
        self.txt_bin.delete("1.0", tk.END)
        self.txt_bin.insert("1.0", binario)
        self.txt_bin.config(state='disabled')
        
        # 3. HDB3
        self.sinal_hdb3 = encode_hdb3(binario)
        
        # 4. Plot
        for widget in self.frame_plot.winfo_children():
            widget.destroy()
        plotar_hdb3(self.frame_plot, self.sinal_hdb3, "Sinal HDB3 Gerado")
        
        # 5. Enviar
        ip = self.entry_ip.get().strip()
        porta = int(self.entry_porta.get().strip())
        
        if enviar_sinal(ip, porta, self.sinal_hdb3):
            messagebox.showinfo("Sucesso", "Sinal enviado!")
        else:
            messagebox.showerror("Erro", "Falha ao enviar sinal.")
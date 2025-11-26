import tkinter as tk
from tkinter import messagebox, scrolledtext, font
from core.vigenere import cifrar_vigenere
from core.conversor import texto_para_binario
from core.hdb3 import encode_hdb3
from core.network import enviar_sinal
from gui.plot_utils import plotar_hdb3

class EmissorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Host A - Emissor")
        master.geometry("950x850")
        master.configure(bg="#f0f2f5") # Fundo moderno

        f_titulo = font.Font(family="Segoe UI", size=11, weight="bold")
        f_texto = font.Font(family="Segoe UI", size=10)
        f_code = font.Font(family="Consolas", size=10) # Para binário e cripto

        
        tk.Label(master, text="Mensagem Original:", font=f_titulo, bg="#f0f2f5").pack(anchor='w', padx=20, pady=(15,5))
        self.txt_msg = tk.Text(master, height=3, width=100, font=f_texto)
        self.txt_msg.pack(padx=20, pady=0)
        
        frame_chave = tk.Frame(master, bg="#f0f2f5")
        frame_chave.pack(fill='x', padx=20, pady=10)
        
        tk.Label(frame_chave, text="Chave Vigenère:", font=f_titulo, bg="#f0f2f5").pack(side='left')
        self.entry_chave = tk.Entry(frame_chave, width=40, font=f_texto)
        self.entry_chave.pack(side='left', padx=10)
        
        self.var_usar_cripto = tk.BooleanVar(value=True)
        self.chk_cripto = tk.Checkbutton(frame_chave, text="Ativar Criptografia", 
                                       variable=self.var_usar_cripto, 
                                       font=("Segoe UI", 10), bg="#f0f2f5", 
                                       activebackground="#f0f2f5")
        self.chk_cripto.pack(side='left', padx=20)

        tk.Label(master, text="Mensagem Criptografada:", font=f_titulo, bg="#f0f2f5").pack(anchor='w', padx=20, pady=(5,5))
        self.txt_cripto = scrolledtext.ScrolledText(master, height=3, width=100, state='disabled', font=f_code)
        self.txt_cripto.pack(padx=20, pady=0)
        
        tk.Label(master, text="Mensagem em Binário:", font=f_titulo, bg="#f0f2f5").pack(anchor='w', padx=20, pady=(15,5))
        self.txt_bin = scrolledtext.ScrolledText(master, height=3, width=100, state='disabled', font=f_code)
        self.txt_bin.pack(padx=20, pady=0)
        
        tk.Label(master, text="Gráfico HDB3:", font=f_titulo, bg="#f0f2f5").pack(anchor='w', padx=20, pady=(15,5))
        self.frame_plot = tk.Frame(master, height=250, bg="white", bd=1, relief="solid")
        self.frame_plot.pack(fill='both', expand=True, padx=20, pady=5)
        
        frame_rede = tk.Frame(master, bg="#e5e7eb", bd=1, relief="solid")
        frame_rede.pack(pady=20, ipadx=10, ipady=5)
        
        tk.Label(frame_rede, text="IP Destino:", font=("Segoe UI", 10), bg="#e5e7eb").pack(side='left', padx=5)
        self.entry_ip = tk.Entry(frame_rede, width=15, font=f_code)
        self.entry_ip.insert(0, "192.168.0.100")
        self.entry_ip.pack(side='left', padx=5)
        
        tk.Label(frame_rede, text="Porta:", font=("Segoe UI", 10), bg="#e5e7eb").pack(side='left', padx=5)
        self.entry_porta = tk.Entry(frame_rede, width=8, font=f_code)
        self.entry_porta.insert(0, "5000")
        self.entry_porta.pack(side='left', padx=5)
        
        tk.Button(master, text="ENVIAR DADOS", command=self.enviar, 
                  bg='#10b981', fg='white', font=("Segoe UI", 12, "bold"), 
                  relief='flat', cursor='hand2', padx=20, pady=5).pack(pady=(0, 20))
        
        self.sinal_hdb3 = None

    def enviar(self):
        msg = self.txt_msg.get("1.0", tk.END).strip()
        chave = self.entry_chave.get().strip()
        usar_cripto = self.var_usar_cripto.get()
        
        if not msg:
            messagebox.showwarning("Aviso", "Preencha a mensagem.")
            return
        
        texto_para_processar = ""

        if usar_cripto:
            if not chave:
                messagebox.showwarning("Aviso", "Preencha a chave para criptografar.")
                return
            
            cifrado = cifrar_vigenere(msg, chave)
            texto_para_processar = cifrado
            
            self.txt_cripto.config(state='normal')
            self.txt_cripto.delete("1.0", tk.END)
            self.txt_cripto.insert("1.0", cifrado)
            self.txt_cripto.config(state='disabled')
        else:
            texto_para_processar = msg
            
            self.txt_cripto.config(state='normal')
            self.txt_cripto.delete("1.0", tk.END)
            self.txt_cripto.insert("1.0", f"[SEM CRIPTOGRAFIA]: {msg}")
            self.txt_cripto.config(state='disabled')
        
        binario = texto_para_binario(texto_para_processar)
        if not binario:
            messagebox.showerror("Erro", "Falha ao converter para binário.")
            return
            
        self.txt_bin.config(state='normal')
        self.txt_bin.delete("1.0", tk.END)
        self.txt_bin.insert("1.0", binario)
        self.txt_bin.config(state='disabled')
        
        self.sinal_hdb3 = encode_hdb3(binario)
        
        for widget in self.frame_plot.winfo_children():
            widget.destroy()
        plotar_hdb3(self.frame_plot, self.sinal_hdb3, "Sinal HDB3 Gerado")
        
        ip = self.entry_ip.get().strip()
        try:
            porta = int(self.entry_porta.get().strip())
        except ValueError:
            messagebox.showerror("Erro", "Porta inválida.")
            return
        
        if enviar_sinal(ip, porta, self.sinal_hdb3):
            messagebox.showinfo("Sucesso", "Sinal enviado!")
        else:
            messagebox.showerror("Erro", "Falha ao enviar sinal.")
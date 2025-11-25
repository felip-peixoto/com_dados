import tkinter as tk
from tkinter import messagebox, scrolledtext, font
import threading
from core.hdb3 import decode_hdb3
from core.conversor import binario_para_texto
from core.vigenere import decifrar_vigenere
from core.network import receber_sinal
from gui.plot_utils import plotar_hdb3

class ReceptorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Host B - Receptor")
        master.geometry("950x850")
        master.configure(bg="#f0f2f5") # Fundo moderno

        # --- Estilos de Fonte ---
        f_titulo = font.Font(family="Segoe UI", size=11, weight="bold")
        f_texto = font.Font(family="Segoe UI", size=10)
        f_code = font.Font(family="Consolas", size=10) # Para binário e cripto

        # --- Layout ---

        # 1. Configuração de Porta e Botão Aguardar
        frame_cfg = tk.Frame(master, bg="#e5e7eb", bd=1, relief="solid")
        frame_cfg.pack(pady=15, ipadx=10, ipady=5)
        
        tk.Label(frame_cfg, text="Porta de Escuta:", font=("Segoe UI", 10), bg="#e5e7eb").pack(side='left', padx=5)
        self.entry_porta = tk.Entry(frame_cfg, width=10, font=f_code)
        self.entry_porta.insert(0, "5000")
        self.entry_porta.pack(side='left', padx=5)
        
        tk.Button(frame_cfg, text="AGUARDAR SINAL", command=self.iniciar_recepcao, 
                  bg='#3b82f6', fg='white', font=("Segoe UI", 10, "bold"), 
                  relief='flat', cursor='hand2').pack(side='left', padx=15)
        
        # 2. Gráfico Recebido
        tk.Label(master, text="Gráfico HDB3 Recebido:", font=f_titulo, bg="#f0f2f5").pack(anchor='w', padx=20, pady=(10,5))
        self.frame_plot = tk.Frame(master, height=200, bg="white", bd=1, relief="solid")
        self.frame_plot.pack(fill='both', expand=True, padx=20, pady=5)
        
        # 3. Binário Decodificado
        tk.Label(master, text="Mensagem Binária Decodificada:", font=f_titulo, bg="#f0f2f5").pack(anchor='w', padx=20, pady=(15,5))
        self.txt_bin = scrolledtext.ScrolledText(master, height=3, width=100, state='disabled', font=f_code)
        self.txt_bin.pack(padx=20, pady=0)
        
        # 4. Mensagem Criptografada (Intermediária)
        tk.Label(master, text="Mensagem Criptografada (Ou Texto Puro):", font=f_titulo, bg="#f0f2f5").pack(anchor='w', padx=20, pady=(15,5))
        self.txt_cripto = scrolledtext.ScrolledText(master, height=3, width=100, state='disabled', font=f_code)
        self.txt_cripto.pack(padx=20, pady=0)
        
        # 5. Área de Descriptografia
        frame_chave = tk.Frame(master, bg="#f0f2f5")
        frame_chave.pack(fill='x', padx=20, pady=15)
        
        tk.Label(frame_chave, text="Chave Vigenère:", font=f_titulo, bg="#f0f2f5").pack(side='left')
        self.entry_chave = tk.Entry(frame_chave, width=40, font=f_texto)
        self.entry_chave.pack(side='left', padx=10)
        
        tk.Button(frame_chave, text="DECIFRAR", command=self.decifrar, 
                  bg='#8b5cf6', fg='white', font=("Segoe UI", 10, "bold"), # Roxo
                  relief='flat', cursor='hand2').pack(side='left', padx=10)
        
        # 6. Mensagem Final
        tk.Label(master, text="Mensagem Final (Texto Claro):", font=f_titulo, bg="#f0f2f5").pack(anchor='w', padx=20, pady=(5,5))
        self.txt_final = scrolledtext.ScrolledText(master, height=3, width=100, state='disabled', font=f_texto)
        self.txt_final.pack(padx=20, pady=(0, 20))
        
        self.sinal_recebido = None
        self.texto_cifrado = None
    
    def iniciar_recepcao(self):
        try:
            porta = int(self.entry_porta.get().strip())
        except ValueError:
            messagebox.showerror("Erro", "Porta inválida.")
            return
            
        threading.Thread(target=self.receber, args=(porta,), daemon=True).start()
        messagebox.showinfo("Aguardando", f"Escutando na porta {porta}...\nO programa pode parecer travado até receber algo.")
    
    def receber(self, porta):
        # Nota: receber_sinal é bloqueante, por isso roda em thread separada
        self.sinal_recebido = receber_sinal(porta)
        if self.sinal_recebido:
            # Tkinter não é thread-safe, usamos after ou processamos direto se não houver conflito de loop
            # Aqui chamamos direto pois a thread vai morrer logo em seguida
            self.processar_sinal()
        else:
            messagebox.showerror("Erro", "Falha ao receber sinal ou timeout.")
    
    def processar_sinal(self):
        # Limpa o campo final para evitar confusão de mensagens anteriores
        self.txt_final.config(state='normal')
        self.txt_final.delete("1.0", tk.END)
        self.txt_final.config(state='disabled')

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
        
        # Binário -> Texto cifrado (ou texto puro se não houve criptografia)
        self.texto_cifrado = binario_para_texto(binario)
        
        self.txt_cripto.config(state='normal')
        self.txt_cripto.delete("1.0", tk.END)
        if self.texto_cifrado:
            self.txt_cripto.insert("1.0", self.texto_cifrado)
        else:
            self.txt_cripto.insert("1.0", "[ERRO DE DECODIFICAÇÃO BINÁRIA]")
        self.txt_cripto.config(state='disabled')
    
    def decifrar(self):
        if not self.texto_cifrado:
            messagebox.showwarning("Aviso", "Nenhum sinal recebido ainda.")
            return
        
        chave = self.entry_chave.get().strip()
        
        # LÓGICA CORRIGIDA E SEM DUPLICAÇÃO
        if not chave:
            # Modo Teste (Sem Criptografia)
            # Apenas copia o texto intermediário para o final
            self.txt_final.config(state='normal')
            self.txt_final.delete("1.0", tk.END)
            self.txt_final.insert("1.0", self.texto_cifrado)
            self.txt_final.config(state='disabled')
            messagebox.showinfo("Modo Teste", "Texto copiado sem descriptografar (Chave vazia).")
            return
        
        # Modo Normal (Com Criptografia)
        try:
            texto_final = decifrar_vigenere(self.texto_cifrado, chave)
            self.txt_final.config(state='normal')
            self.txt_final.delete("1.0", tk.END)
            self.txt_final.insert("1.0", texto_final)
            self.txt_final.config(state='disabled')
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao decifrar: {e}")
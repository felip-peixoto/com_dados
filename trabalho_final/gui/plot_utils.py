import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plotar_hdb3(parent_frame, sinal_hdb3, titulo="Sinal HDB3"):
    """
    Plota forma de onda HDB3 em degraus dentro de um frame Tkinter.
    """
    fig, ax = plt.subplots(figsize=(10, 3))
    
    x = list(range(len(sinal_hdb3)))
    ax.step(x, sinal_hdb3, where='post', linewidth=2, color='blue')
    ax.set_xlabel('Tempo')
    ax.set_ylabel('Tensão')
    ax.set_title(titulo)
    ax.set_ylim(-1.5, 1.5)
    ax.grid(True, alpha=0.3)
    ax.axhline(0, color='black', linewidth=0.5)
    
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
    
    return canvas
import tkinter as tk
from gui.emissor import EmissorGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = EmissorGUI(root)
    root.mainloop()
import tkinter as tk
from gui.receptor import ReceptorGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = ReceptorGUI(root)
    root.mainloop()
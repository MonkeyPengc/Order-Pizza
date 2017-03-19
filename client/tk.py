
try:
    # Python2
    from Tkinter import *
    import ttk
    from tkMessageBox import showinfo, askokcancel
except ImportError:
    # Python3
    from tkinter import *
    from tkinter import ttk
    from tkinter.messagebox import showinfo, askokcancel

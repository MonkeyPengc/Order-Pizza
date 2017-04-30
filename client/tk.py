
try:
    # Python2
    from Tkinter import *
    import ttk
    import tkFont
    from tkMessageBox import showinfo, askokcancel

except ImportError:
    # Python3
    from tkinter import *
    from tkinter import ttk
    import tkinter.font as tkFont
    from tkinter.messagebox import showinfo, askokcancel

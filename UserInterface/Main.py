from tkinter import *
import tkinter as tk
from tkinter import ttk
import sqlite3
class GUI():
    def __init__(self, Frame, *args, **kwargs):
        self.work_window = Toplevel()
        self.q = (StringVar(), 'Schwierigkeit'), (StringVar(), 'Typ'), (StringVar(), 'Titel'), (StringVar(), 'Author'), (StringVar(), 'Datum'), (StringVar(), 'Author2'), (StringVar(), 'Datum2')
        self.titel = StringVar()
        WIDTH = int(Frame.winfo_screenwidth() / 2)
        HEIGHT = int(Frame.winfo_screenheight() / 2)
        self.work_window.title("DB_List")
        self.work_window.resizable(False, False)
        self.work_window.geometry("%dx%d" % (WIDTH, HEIGHT))
        #self.UI_Elemente()

        self.Read_Entry_btn = Button(self.work_window, text="read entry", command=self.printSelf)
        self.Read_Entry_btn.pack(side=tk.TOP, padx=6, anchor="s")

        self.Add_Entry_btn = Button(self.work_window, text="Frage in DB erstellen", command=self.printSelf)
        self.Add_Entry_btn.pack(side=tk.TOP, padx=6, anchor="s")

        self.Save_btn = Button(self.work_window, text="Save Changes", command=self.printSelf)
        self.Save_btn.pack(side=tk.TOP, padx=6, anchor="s")

        self.Search_Entry = Entry(self.work_window, textvariable=self.titel)
        self.Search_Entry.pack(side=tk.TOP, padx=6, anchor="s")

    def printSelf(self):
        print("Self")
if __name__ == "__main__":
    root = tk.Tk()
    WIDTH = int(root.winfo_screenwidth() / 1.5)
    HEIGHT = int(root.winfo_screenheight() / 2)
    root.title("DB_List")
    root.resizable(False, False)
    root.geometry("%dx%d" % (WIDTH, HEIGHT))
    gesucht = 'Spannungsteiler 2'
    dbname = '../testdb.db'
    lbl = tk.Label(text="Das ist das Main Window")
    Fragen_Frame = GUI(root, gesucht)
    root.mainloop()
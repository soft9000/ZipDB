#!/usr/bin/python3

# Mission: Opportunity to create a ZipDB "Note Maker".

# Status: Work in progress
# Date Created: 2019-02-16

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from tkinter import *
from tkinter import messagebox
from collections import OrderedDict

from ZipNotes.RowArray import RowArray
from ZipNotes.ZipBase import ZipArchiveBase

class AppGUI(Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.title("ZipDB: My Notes")
        self.frames = list()
        self.entTime = None
        self.entSubject = None
        self.entText = None
        self.lbEvent = None
        self.lbSel = None
        self.setup()

    def setup(self):
        self.set_center()
        self.frames.append(Frame(self, background='red'))
        self.frames.append(Frame(self, background='green'))
        
        self.set_menu()
        self.set_list(self.frames[0])
        self.set_detail(self.frames[1])

        self.frames[0].pack(side=LEFT, fill=BOTH)
        self.frames[1].pack(fill=BOTH)

        
    def set_center(self):
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        x = (width - self.winfo_reqwidth()) / 2
        y = (height - self.winfo_reqheight()) / 2
        self.geometry("+%d+%d" % (x/2, y/2))
        self.resizable(width=False, height=False)

    def set_menu(self):
        menubar = Menu(self)

        zmenu = Menu(menubar, tearoff=0)
        zmenu.add_command(label="Archive...", command=self.do_open)
        zmenu.add_command(label="New Entry...", command=self.do_new)
        zmenu.add_command(label="Quit...", command=self.do_quit)
        menubar.add_cascade(label="File", menu=zmenu)

        zmenu = Menu(menubar, tearoff=0)
        zmenu.add_command(label="Edit...", command=self.do_edit)
        zmenu.add_command(label="Delete...", command=self.do_delete)
        zmenu.add_command(label="Clone...", command=self.do_clone)
        menubar.add_cascade(label="Selection", menu=zmenu)

        zmenu = Menu(menubar, tearoff=0)
        zmenu.add_command(label="About...", command=self.do_about)
        menubar.add_cascade(label="Help", menu=zmenu)
        
        self.config(menu=menubar)

    def set_list(self, frame):
        zlb = Listbox(frame, fg='blue', background='aqua')
        for ref in range(200):
            zlb.insert(END, "Entry " + str(ref))
        zlb.bind('<<ListboxSelect>>', self.on_lbclicked)
        zlb.pack(expand=True, fill=BOTH, anchor=NW)
        self.lbEvent = zlb

    def set_detail(self, frame):
        zlb = Label(frame, text="Changed:  ", background='Green', anchor=W)
        zlb.grid(row=0, column=0, sticky=E)        
        self.entTime = Entry(frame, bd=5, width=50, fg='blue')
        self.entTime.grid(row=0, column=1, sticky=W)
        self.read_only(self.entTime, "Time")

        zlb = Label(frame, text="Subject:  ", background='Green', anchor=W)
        zlb.grid(row=1, column=0, sticky=E)        
        self.entSubject = Entry(frame, bd=5, width=60, validate="key", vcmd=self.on_delta)
        self.entSubject.grid(row=1, column=1)
        self.entSubject.insert(0, "Subject")

        self.entText = Text(frame, height=25, width=50)
        self.entText.grid(row=2, column=0, columnspan=2, sticky=NSEW)
        self.entText.insert(END, "Just\n\tsome text!")
        self.entText.bind("<KeyRelease>",  self.on_delta_text)

    def do_open(self):
        pass

    def do_new(self):
        pass

    def do_edit(self):
        pass

    def do_delete(self):
        pass

    def do_clone(self):
        pass

    def do_quit(self):
        self.destroy()

    def do_about(self):
        messagebox.showinfo("ZipDB", "Work In Process!")

    def on_lbclicked(self, ve):
        w = ve.widget
        values = w.curselection()
        if len(values):
            index = int(values[0])
            self.lbSel = w.get(index)
            self.read_only(self.entTime, self.lbSel)

    def on_ignore(self, ve):
        print("on_ignore")

    def on_delta(self):
        print("on_delta")
        return True

    def on_delta_text(self, ve):
        print("on_delta_text")
        return True

    def read_only(slef, obj, text):
        obj.config(state='normal')
        obj.delete(0, last=END)
        obj.insert(0, text)
        obj.config(state='readonly')


if __name__ == '__main__':
    app = AppGUI()
    app.mainloop()
    


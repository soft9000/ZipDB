#!/usr/bin/python3

# Mission: Opportunity to create a ZipDB "Note Maker".

# Status: Work in progress
# Date Created: 2019-02-16

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from collections import OrderedDict

from ZipNotes.Row import RowOne
from ZipNotes.RowArray import RowArray
from ZipNotes.ZipBase import ZipArchiveBase
from GUI.Preferences import *

class AppGUI(Tk):

    FILE_TYPE = ".zdb"
    NOTE_FILE = "ZibDB.txt"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.title("ZipDB: My Notes")
        self.changed = False
        self.frames = list()
        self.entTime = None
        self.entSubject = None
        self.entText = None
        self.lbEvent = None
        self.lbSel = None
        self.archive = None
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
        zmenu.add_command(label="Create Archive...", command=self.do_archive_create)
        zmenu.add_command(label="Open Archive...", command=self.do_archive_open)
        zmenu.add_command(label="Quit...", command=self.do_quit)
        menubar.add_cascade(label="File", menu=zmenu)

        zmenu = Menu(menubar, tearoff=0)
        zmenu.add_command(label="New Entry...", command=self.do_edit_new)
        zmenu.add_command(label="Delete...", command=self.do_edit_delete)
        zmenu.add_command(label="Clone...", command=self.do_edit_clone)
        menubar.add_cascade(label="Selection", menu=zmenu)

        zmenu = Menu(menubar, tearoff=0)
        zmenu.add_command(label="Locations...", command=self.do_tool_locations)
        menubar.add_cascade(label="Tools", menu=zmenu)

        zmenu = Menu(menubar, tearoff=0)
        zmenu.add_command(label="About...", command=self.do_about)
        menubar.add_cascade(label="Help", menu=zmenu)
        
        self.config(menu=menubar)

    def set_list(self, frame):
        zlb = Listbox(frame, fg='blue', background='aqua')
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

    def show_archive_title(self):
        if not self.archive:
            return
        archive = self.archive.file
        if len(archive) > 30:
            archive = "..." + archive[-27:]
        self.title(archive)

    def do_archive_create(self):
        self._save_edit()
        location = Dp1.Load('.')['Database']
        archive = simpledialog.askstring(location, "Archive name:")
        if not archive:
            return
        if not archive.lower().endswith(AppGUI.FILE_TYPE):
            archive = archive + AppGUI.FILE_TYPE
        archive = os.path.join(location, archive)
        archive = archive.replace("\\", "/")
        if os.path.exists(archive):
            messagebox.showerror("Archive Creation Error", "Refusing to overwrite " + archive)
            return
        try:
            with open(archive, 'w') as fh:
                pass
            os.unlink(archive)
            self.archive = ZipArchiveBase(archive)
            if self._create_archive():
                self.show_archive_first()
            self.show_archive_title()
        except Exception as ex:
            print(ex)
            messagebox.showerror("Archive Creation Error", "Unable to create " + archive)

    def do_archive_open(self):
        self._save_edit()
        location = Dp1.Load('.')['Database']
        archive = filedialog.askopenfilename(
            initialdir = location,
            filetypes=[("ZibDB Archives", AppGUI.FILE_TYPE)])
        if not archive:
            return
        self.archive = ZipArchiveBase(archive)
        self.show_archive_first()
        self.show_archive_title()

    def do_tool_locations(self):
        pref = Dp1(self, '.')       

    def do_edit_new(self):
        pass

    def do_edit_sel(self):
        if self.changed:
            self._save_edit()
        self._load_edit()
        self.changed = False

    def do_edit_delete(self):
        pass

    def do_edit_clone(self):
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
            self.do_edit_sel()

    def on_delta(self):
        self.changed = True
        return True

    def on_delta_text(self, ve):
        self.changed = True
        return True

    def _create_archive(self):
        if not self.archive:
            return
        note = RowOne()
        note.subject = "Welcome"
        note.data = "Created archive " + self.archive.file
        notes = RowArray()
        notes.append(note)
        bOkay = self.archive.archive_first(
            RowArray.ToString(notes),
            AppGUI.NOTE_FILE)
        if not bOkay:
            messagebox.showerror("Archive Creation Error", "Unable to create archive.")
            self.archive = None
            return False
        return True

    def show_archive_first(self):
        # TODO - Show the first entry
        messagebox.showinfo("TODO", "Show the first entry.")

    def _save_edit(self):
        pass

    def _load_edit(self):
        if self.lbSel:
            self.read_only(self.entTime, self.lbSel)

    def read_only(self, obj, text):
        obj.config(state='normal')
        obj.delete(0, last=END)
        obj.insert(0, text)
        obj.config(state='readonly')


if __name__ == '__main__':
    app = AppGUI()
    app.mainloop()
    


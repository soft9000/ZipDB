#!/usr/bin/env python3
#
# Author: Soft9000.com
# 2019/02/17: Cloned from PyDAO.

# Mission: Permit user preferences for locations & other options, as they arise.
# Status: Code Complete. Alpha.

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from tkinter import simpledialog

from collections import OrderedDict

from GUI.StandardEntry import LabelEntryAction

class Preferences:
    ''' Opportunity to create the official class to manage end-user preferences. '''

    def __init__(self, zdict):
        self._zdict = zdict
        
    def __iter__(self):
        ''' Classic usage requires that we make it scriptable... '''
        for key in self._zdict.keys():
            yield key
        
    def __getitem__(self, key):
        ''' Classic usage requires that we make it scriptable... '''
        return self._zdict[key]
        
    def __setitem__(self, key, value):
        ''' Classic usage requires that we make it scriptable... '''
        self._zdict[key] = value
    

class Dp1(simpledialog.Dialog):

    FILE_NAME = "MyPref.dp1"
    KEYS = ['Database']

    def __init__(self, parent, home_dir):
        self.home_dir = Dp1.MkHome(home_dir)
        self.bChanged = False
        self.options = OrderedDict()
        for key in Dp1.KEYS:
            print(key)
            self.options[key] = StringVar()
        for line in self.options:
            self.options[line].set(self.home_dir)
        super().__init__(parent=parent)
        
    def has_changed(self):
        return self.bChanged

    def get_folder(self, key):
        var = self.options[key].get()
        self.attributes('-topmost',False)
        var = askdirectory(initialdir=var)
        self.attributes('-topmost',True)
        if not var:
            return
        self.options[key].set(var)

    def _on_project(self):
        self.get_folder('Database')

    def body(self, zframe):
        self.title("PyDAO Locations")
        legacy = Dp1.Load(self.home_dir)
        if legacy:
            for key in self.options:
                try:
                    self.options[key].set(legacy[key])
                except:
                    continue
        order = LabelEntryAction()
        order.add_entry('Database Folder', tv=self.options['Database'], action=self._on_project)
        LabelEntryAction.CreateLframe(self,order, title=' Folder Locations ').pack(fill=BOTH)
        self.attributes('-topmost',True)

    def __dict__(self):
        order = OrderedDict()
        for key in self.options:
            order[key] = self.options[key].get()
        return order

    def __iter__(self):
        order = self.__dict__()
        for key in order:
            yield key, order[key]

    def apply(self):
        self.bChanged = True
        order = self.__dict__()    
        ofile = self.home_dir + '/' + Dp1.FILE_NAME
        with open(ofile, 'w') as fh:
            fh.write(str(order))

    @staticmethod
    def MkHome(home_dir):
        home_dir = os.path.abspath(home_dir)
        home_dir = os.path.normpath(home_dir)
        if not os.path.exists(home_dir):
            home_dir = os.path.abspath('.')
            home_dir = os.path.normpath(home_dir)
        home_dir = home_dir.replace('\\', '/')
        if home_dir.endswith('/'):
            return home_dir[:-1]
        return home_dir

    @staticmethod
    def Load(home_dir):
        ''' Returns a dictionary if preferences are found. Defaults to home location if none. '''
        home_dir = Dp1.MkHome(home_dir)
        ofile = home_dir + '/' + Dp1.FILE_NAME
        try:
            with open(ofile) as fh:
                return Preferences(eval(fh.readline()))
        except:
            result = OrderedDict()
            for key in Dp1.KEYS:
                result[key] = home_dir
            return Preferences(result)


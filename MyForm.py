'''
    Program: FlashGen
    File: MyForm.py
    Team: Brendan Cicchi, Remington Maxwell, Sara Woods

    Summary: Class MyForm
        Provides the initial file upload dialogue to obtain file path
        Creates the outermost shell of the GUI
        Calls the Haskell parser which returns formatted JSON
        
'''
import wx
import os
import json
import sys
from subprocess import check_output
from Cards import Cards
from LeftPanel import LeftPanel
from RightPanel import RightPanel

import  wx.lib.scrolledpanel as scrolled

# calls the haskell parser on the specified file path to parse notes as json
def getNotes(path):
    # once user selects file to open store that file in a variable
    notesFile = path
    # run haskell program to get JSON string
    noteselftring = check_output(["runhaskell", "parse.hs", notesFile])
    # convert the string into a JSON object
    noteCardJSON = json.loads(noteselftring)
    return noteCardJSON

class MyForm(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self):
        displaySize=wx.DisplaySize()
        no_resize = wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER | 
                                               wx.RESIZE_BOX | 
                                                wx.MAXIMIZE_BOX)
        wx.Frame.__init__(self, None, title="FlashGen", size=(displaySize[0], displaySize[1]/8 * 7), style=no_resize)
        #self.panel = wx.ScrolledWindow(self, wx.ID_ANY)
        #self.panel.SetScrollbars(1, 1, 1,1)


        wildcard = "Text File (*.txt)|*.txt"
        dialog = wx.FileDialog(None, "Choose a file", os.getcwd(), "", wildcard, wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath() 
        else:
            sys.exit("No text file selected") 

        dialog.Destroy()

        noteCardJSON = getNotes(path)
 
        #self.scroll.splitter = wx.SplitterWindow(self)
        splitter = wx.SplitterWindow(self)
        #splitter = self.scroll.splitter
        splitter.cards = Cards(noteCardJSON)
        splitter.rightP = RightPanel(splitter,self)
        splitter.leftP = LeftPanel(splitter, self)

 
        # split the window
        splitter.SplitVertically(splitter.leftP, splitter.rightP)
        splitter.SetMinimumPaneSize(250)
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        newitem = fileMenu.Append(wx.ID_OPEN, 'Open', 'Open New TextFile')
        helpitem = fileMenu.Append(wx.ID_HELP, 'Help', 'Help')
        aboutitem = fileMenu.Append(wx.ID_ABOUT, 'About This Program', 'About This Program')
        fitem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)
        
        
        self.Bind(wx.EVT_MENU, self.OnQuit, fitem)
        #self.Bind(wx.EVT_MENU, self.OnOpen, newitem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutitem)
        self.Bind(wx.EVT_MENU, self.OnHelp, helpitem)
        self.Bind(wx.EVT_MENU, lambda event: self.OnOpen(event, splitter))

    def OnQuit(self, e):
        self.Close()

        #to be completed
    def OnAbout(self, e):
        self.Close()
        #to be completed
    def OnHelp(self, e):
        self.Close()

    def OnOpen(self, e, splitthis):
        wildcard = "Text File (*.txt)|*.txt"
        dialog = wx.FileDialog(None, "Choose a file", os.getcwd(), "", wildcard, wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath() 
        else:
            sys.exit("No text file selected") 

        dialog.Destroy()
        #splitthis.Clear()
        noteCardJSON = getNotes(path)
        #self.scroll.splitter = wx.SplitterWindow(self)
        splitter = wx.SplitterWindow(self)
        #splitter = self.scroll.splitter
        splitter.cards = Cards(noteCardJSON)
        splitter.rightP = RightPanel(splitter,self)
        splitter.leftP = LeftPanel(splitter)

 
        # split the window
        splitter.SplitVertically(splitter.leftP, splitter.rightP)
        splitter.SetMinimumPaneSize(250)
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)
        

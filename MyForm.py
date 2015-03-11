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

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.splitter = wx.SplitterWindow(self)

        noteCardJSON = getNotes(path)
 
        #self.scroll.splitter = wx.SplitterWindow(self)
        
        #splitter = self.scroll.splitter
        self.splitter.cards = Cards(noteCardJSON)
        self.splitter.rightP = RightPanel(self.splitter,self)
        self.splitter.leftP = LeftPanel(self.splitter, self)

        # split the window
        self.splitter.SplitVertically(self.splitter.leftP, self.splitter.rightP)

        self.splitter.SetMinimumPaneSize(250)
        self.sizer.Add(self.splitter, 1, wx.EXPAND)
        self.sizer.Add(self.splitter,1, wx.EXPAND)
        self.SetSizer(self.sizer)

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        helpMenu = wx.Menu()
        newitem = fileMenu.Append(wx.ID_OPEN, 'Open', 'Open New TextFile')
        helpitem = helpMenu.Append(wx.ID_HELP, 'Help', 'Help')
        aboutitem = helpMenu.Append(wx.ID_ABOUT, 'About This Program', 'About This Program')
        fitem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        
        menubar.Append(fileMenu, '&File')
        menubar.Append(helpMenu, '&Help')


        self.SetMenuBar(menubar)
        
        
        self.Bind(wx.EVT_MENU, self.OnQuit, fitem)
        self.Bind(wx.EVT_MENU, self.OnOpen, newitem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutitem)
        self.Bind(wx.EVT_MENU, self.OnHelp, helpitem)

    def OnQuit(self, e):
        self.Close()

        #to be completed
    def OnAbout(self, e):
        self.Close()
        
        #to be completed
    def OnHelp(self, e):
        self.Close()

    def OnOpen(self, e):
        wildcard = "Text File (*.txt)|*.txt"
        dialog = wx.FileDialog(None, "Choose a file", os.getcwd(), "", wildcard, wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath() 
        else:
            sys.exit("No text file selected") 
        dialog.Destroy()

        newCards = getNotes(path)
        # destroy all the card buttons in the left panel
        for i in range (0, len(self.splitter.cards.JSON)):
            button = self.FindWindowByName(str(i))
            button.Destroy()
        # set the new cards, create buttons for the left panel, update the card for the right panel
        self.splitter.cards = Cards(newCards)
        LeftPanel.createButtons(self.splitter.leftP, self.splitter, self)
        RightPanel.updateText(self.splitter.rightP, self.splitter.cards)
        #self.splitter.leftP.SetSizer(self.splitter.leftP.sizer)
        self.splitter.leftP.SetupScrolling()
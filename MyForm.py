'''
    Program: FlashGen
    File: MyForm.py
    Team: Brendan Cicchi, Remington Maxwell, Sara Woods

    Summary: Class MyForm
        Provides the initial file upload dialogue to obtain file path
        Creates the outermost shell of the GUI including the menubar
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
        wx.Frame.__init__(self, None, title="FlashGen", size=(displaySize[0], displaySize[1]/12 * 11), style= no_resize)
        ico = wx.Icon('images/icons/FlashGen.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)

        # create the file dialog to get a file path from the user
        wildcard = "Text File (*.txt)|*.txt"
        dialog = wx.FileDialog(None, "Choose a file", os.getcwd(), "", wildcard, wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath() 
        else:
            sys.exit("No text file selected") 
        dialog.Destroy()

        # create formatting for window
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.splitter = wx.SplitterWindow(self)

        noteCardJSON = getNotes(path)

        self.splitter.cards = Cards(noteCardJSON)
        self.splitter.rightP = RightPanel(self.splitter,self)
        self.splitter.leftP = LeftPanel(self.splitter, self)

        # split the window for the separate panels
        self.splitter.SplitVertically(self.splitter.leftP, self.splitter.rightP)
        self.splitter.SetMinimumPaneSize(250)
        self.sizer.Add(self.splitter, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        # create the menu bar at the top of the GUI
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        helpMenu = wx.Menu()

        # create open option in file menu with image and hotkey
        qmi = wx.MenuItem(fileMenu, wx.ID_OPEN, '&Open\tCtrl+O')
        qmi.SetBitmap(wx.Bitmap('images/icons/open.png'))
        fileMenu.AppendItem(qmi)
        self.Bind(wx.EVT_MENU, self.OnOpen, id=wx.ID_OPEN)
        # create quit option in file menu with image and hotkey
        qmi = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit\tCtrl+Q')
        qmi.SetBitmap(wx.Bitmap('images/icons/exit.png'))
        fileMenu.AppendItem(qmi)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=wx.ID_EXIT)
        # create about option in help menu with image
        qmi = wx.MenuItem(helpMenu, wx.ID_ABOUT, '&About')
        qmi.SetBitmap(wx.Bitmap('images/icons/about.png'))
        helpMenu.AppendItem(qmi)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)
        # create help option in help menu with image and hotkey
        qmi = wx.MenuItem(helpMenu, wx.ID_HELP, '&Help\tCtrl+H')
        qmi.SetBitmap(wx.Bitmap('images/icons/help.png'))
        helpMenu.AppendItem(qmi)
        self.Bind(wx.EVT_MENU, self.OnHelp, id=wx.ID_HELP)

        menubar.Append(fileMenu, '&File')
        menubar.Append(helpMenu, '&Help')
        self.SetMenuBar(menubar)

    # quit event
    def OnQuit(self, e):
        self.Close()

    #display an about dialog to the user
    def OnAbout(self, e):
        description = """
        FlashGen is a flash card generator designed to accept
        a user specified .txt file to be parsed into note cards
        displayed by the GUI.
        This application is designed to replace existing generators
        which require users to enter their cards manually in the GUI.
        FlashGen looks to simplify this process, while providing a
        more friendly and practical learning environment.
        """
        info = wx.AboutDialogInfo()

        info.SetIcon(wx.Icon('images/FlashGen.png', wx.BITMAP_TYPE_PNG))
        info.SetName('FlashGen')
        info.SetVersion('1.0')
        info.SetDescription(description)
        info.SetWebSite('http://www.github.com/sarawoods/FlashGen')
        info.AddDeveloper('Brendan Cicchi\nRemington Maxwell\nSara Woods')

        wx.AboutBox(info)

        
    #display help dialog to the user on how to format .txt file
    def OnHelp(self, e):
        help_txt = """
        Here is how to format your text file:

        ~ This is a question
        | This is an option to the question
        > This is my answer to the question
            Text on a new line will not be taken
                > indentation does not matter
        > (~ | >) must be at the beginning of the line

        This > | ~ will not work but don't worry,
        nothing will crash.

        Any extraneous lines with no symbol will never
        become a card, so feel free to enter these
        anywhere in the .txt file.

        | This is invalid syntax and will be ignored

        ~ You can also have a question by itself
        but you can't do this with answers or options
    

        Check out our github to see the README
        """
        help = wx.AboutDialogInfo()
        help.SetName('FlashGen')
        help.SetVersion('1.0')
        help.SetIcon(wx.Icon('images/icons/FlashGen.ico', wx.BITMAP_TYPE_ICO))
        help.SetDescription(help_txt)
        help.SetWebSite('http://www.github.com/sarawoods/FlashGen')

        wx.AboutBox(help)

    # display open dialog to user to get a new file path
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
        self.splitter.leftP.SetupScrolling()
import wx
import os
import wx.grid as gridlib
import  cStringIO
import sys

import random

from subprocess import check_output
import json

import  wx.lib.scrolledpanel as scrolled
from wx.lib.wordwrap import wordwrap

class Cards:
    def __init__(self, JSON):
        self.JSON = JSON
        self.index = 0
        self.face = "question"
	
    def next(self):
        if self.index == len(self.JSON) - 1:
            self.index = 0
        else:
            self.index = self.index + 1
        self.face = "question"
		
    def prev(self):
        if self.index == 0:
            self.index = len(self.JSON) -1
        else:
            self.index = self.index - 1;
        self.face = "question"
		
    # flip -> gets the face of the current card not currently shown
    def flip(self):
        if self.face == 'question':
            self.face = "answers"
        elif (self.face == 'answers'):
            self.face = "question"
        else:
            raise NameError("Error: Flip has a bad type -> " + type)

	# shuffle -> returns the elements of array in a random order 
    def shuffle(self):
        random.shuffle(self.JSON)
		
    def getInfo(self):
        if len(self.JSON) > 0:
            if self.face == "question":
                question = self.JSON[self.index][self.face]
                options = ""
                for opt in self.JSON[self.index]["options"]:
                    options = "\n" + options + "    - " + opt
                return question + options
            else:
                answers = ""
                if len(self.JSON[self.index][self.face]) == 1:
                    answers = self.JSON[self.index][self.face][0]
                else:
                    for ans in self.JSON[self.index][self.face]:
                        answers = answers + "- " + ans + "\n"
                return answers
        else:
		  return "Sorry, the file you uploaded did not parse any questions.\n" + \
                 "Please check your formatting or try uploading another file." + \
                 "Check out our tutorial for help."


def getNotes(path):
    # once user selects file to open store that file in a variable
    notesFile = path
    # run haskell program to get JSON string
    noteselftring = check_output(["runhaskell", "parse.hs", notesFile])
    # convert the string into a JSON object
    noteCardJSON = json.loads(noteselftring)
    # generate GUI using the JSON


    return noteCardJSON
 

########################################################################
class LeftPanel(scrolled.ScrolledPanel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        scrolled.ScrolledPanel.__init__(self, parent=parent)

 
        #grid = gridlib.Grid(self)
        #grid.CreateGrid(100,2)
 
        imageFile='images\\borders\\Notecard Border 1.png'
        data = open(imageFile, "rb").read()
        # convert to a data stream
        stream = cStringIO.StringIO(data)
        sizer = wx.BoxSizer(wx.VERTICAL)
        # convert to a bitmap
        bmp = wx.BitmapFromImage( wx.ImageFromStream( stream ))
        i=1
        a = "note"
        test = a + str(i)
        
        sizer.AddSpacer(10)
        notecardText="Notecard Text Appears Here"
        #use test to loop through and add the notecards dynamically
        # show the bitmap, (5, 5) are upper left corner coordinates
        note=wx.StaticBitmap(self, -1, bmp, (0, 140))
        displaySize=wx.DisplaySize()
        text = wx.StaticText(self, -1, notecardText,(0, 140))
        text.SetFont(wx.Font(5, wx.SWISS, wx.NORMAL, wx.BOLD))
        text.SetSize(text.GetBestSize())
        sizer.Add(text,0,wx.EXPAND)
        sizer.Add(note, 0, wx.EXPAND)
        sizer.AddSpacer(10)
        test=wx.StaticBitmap(self, -1, bmp, (0, 140))
        sizer.Add(test, 0, wx.EXPAND)
        sizer.AddSpacer(10)
        note2=wx.StaticBitmap(self, -1, bmp, (0, 140))
        sizer.Add(note2, 0, wx.EXPAND)
        sizer.AddSpacer(10)
        note3=wx.StaticBitmap(self, -1, bmp, (0, 140))
        sizer.Add(note3, 0, wx.EXPAND)
        sizer.AddSpacer(10)
        note4=wx.StaticBitmap(self, -1, bmp, (0, 140))
        sizer.Add(note4, 0, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()
        
        
        #self.SetScrollbar(wx.VERTICAL, 0, 10, 500);
 
########################################################################
class RightPanel(wx.Panel):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
				# get the data

        wildcard = "Text File (*.txt)|*.txt"
        dialog = wx.FileDialog(None, "Choose a file", os.getcwd(), "", wildcard, wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath() 
        else:
            sys.exit("No text file selected") 

        dialog.Destroy()
        noteCardJSON = getNotes(path)
        cards = Cards(noteCardJSON)
        wx.Panel.__init__(self, parent=parent)
        #load buttons
        # panel needed to display button correctly
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        nextImage = "images\\buttons\\NextButtonNew.png"
        previousImage="images\\buttons\\BackButtonNew.png"
        flipImage="images\\buttons\\FlipButton1.png"
        #Need to loop if at start of list or end of list

        #Next Button Init
        image1 = wx.Image(nextImage, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.nextButton = wx.BitmapButton(self, id=-1, bitmap=image1,
        pos=(990, 305), size=(image1.GetWidth()+5, image1.GetHeight()+5), style=wx.BU_AUTODRAW)
        self.nextButton.Bind(wx.EVT_BUTTON, lambda event: self.nextButtonClick(event, cards))
        self.nextButton.SetToolTip(wx.ToolTip("Go to Next Flashcard"))



        #Back Button Init
        image2 = wx.Image(previousImage, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.backButton = wx.BitmapButton(self, id=-1, bitmap=image2,
        pos=(15, 305), size=(image2.GetWidth()+5, image2.GetHeight()+5), style=wx.BU_AUTODRAW)
        self.backButton.Bind(wx.EVT_BUTTON, lambda event: self.backButtonClick(event, cards))
        self.backButton.SetToolTip(wx.ToolTip("Go to Previous Flashcard"))

        #Flip Button Init
        image3 = wx.Image(flipImage, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.flipButton = wx.BitmapButton(self, id=-1, bitmap=image3,
        pos=(970, 520), size=(image2.GetWidth()+5, image2.GetHeight()+5), style=wx.BU_AUTODRAW)
        self.flipButton.Bind(wx.EVT_BUTTON, lambda event: self.flipButtonClick(event, cards))
        self.flipButton.SetToolTip(wx.ToolTip("Go to Front/Back of Flashcard"))

        #self.nextButton = wx.Button(self,label='Next', pos=(990,305), size=(80,50))
        #Binds the trigger event fror going to previous flashcard
        #self.backButton.Bind(wx.EVT_BUTTON, self.backButtonClick)
        
        # optional tooltip
        
        #Binds the trigger event for going to previous flashcard
        #self.nextButton.Bind(wx.EVT_BUTTON, self.nextButtonClick)
                
        #for displaying notecard image
        imageFile1='images\\borders\\Notecard Border.png'
        data = open(imageFile1, "rb").read()
        # convert to a data stream
        stream = cStringIO.StringIO(data)
        # convert to a bitmap
        self.bmp1 = wx.BitmapFromImage( wx.ImageFromStream( stream ))
        # show the bitmap, (5, 5) are upper left corner coordinates
        noteFront=wx.StaticBitmap(self, -1, self.bmp1, (100, 15))

        self.width = self.bmp1.GetWidth()-70
        self.height = self.bmp1.GetHeight()/2-(14*(len(cards.getInfo())/85))

        #self.text = wx.StaticText(self, -1, "", (self.width, self.height), style=(wx.ALIGN_CENTRE_HORIZONTAL| wx.TE_MULTILINE ))
        self.text = wx.StaticText(self, label="", size = (self.width, self.height), style=(wx.ALIGN_CENTRE_HORIZONTAL| wx.TE_MULTILINE ))
        self.text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.text.SetSize(self.text.GetBestSize())
        #self.text.Wrap(self.width)

        self.updateText(cards)

    # Gets the new text for the card, centers it, wraps it, and displays
    def updateText(self, cards):
        self.height = self.bmp1.GetHeight()/2-(14*(len(cards.getInfo())/85))
        newText = wordwrap(cards.getInfo(), 450, wx.ClientDC(self), breakLongWords=True, margin=0)
        #newText = cards.getInfo()

        #displaySize=wx.DisplaySize()

        self.text.Label = newText
        self.text.SetBackgroundColour((0,0,255))

        self.text.SetSize(self.text.GetBestSize())

        sizer_v = wx.BoxSizer(wx.VERTICAL)
        sizer_h = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h.Add(self.text, 1, wx.CENTER)
        sizer_v.Add(sizer_h, 1, wx.CENTER)
        self.SetSizer(sizer_v)

        

    #back button click event
    def backButtonClick(self,event, cards):
        cards.prev()
        #self.updateText.Label = cards.getInfo()
        self.updateText(cards)

    #next button click event
    def nextButtonClick(self,event, cards):
        cards.next()
        #self.updateText.Label = cards.getInfo()
        self.updateText(cards)



    #next button click event
    def flipButtonClick(self,event, cards):
        cards.flip()
        #self.updateText.Label = cards.getInfo()
        self.updateText(cards)



########################################################################        
     

########################################################################
class MyForm(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self ):
        displaySize=wx.DisplaySize()
        wx.Frame.__init__(self, None, title="FlashGen", size=(displaySize[0], displaySize[1]/8 * 7))
 
        splitter = wx.SplitterWindow(self)
        leftP = LeftPanel(splitter)
        rightP = RightPanel(splitter)
 
        # split the window
        splitter.SplitVertically(leftP, rightP)
        splitter.SetMinimumPaneSize(250)
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
#----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.App(False)

    frame = MyForm()
    frame.Show()
    loadButton = wx.Button(frame, label='Open',pos=(225, 5), size=(80, 25))
    saveButton = wx.Button(frame, label='Save',pos=(315, 5), size=(80, 25))
    #filename = wx.TextCtrl(frame, pos=(5, 5), size=(210, 25))
    #contents = wx.TextCtrl(frame, pos=(5, 35), size=(390, 260),style=wx.TE_MULTILINE | wx.HSCROLL)
    app.MainLoop()

'''
    Program: FlashGen
    File: RightPanel.py
    Team: Brendan Cicchi, Remington Maxwell, Sara Woods

    Summary: Class RightPanel
        Displays the large card on the right hand side for the main flash card
        
        Buttons:
            Next    -> go to next card
            Prev    -> go to previous card
            Flip    -> flip the face of the current card showing
            Shuffle -> rearrange cards to random order and update left Panel buttons
'''
import wx
import os
import  cStringIO
from wx.lib.wordwrap import wordwrap
from panelHelpers import trimText

class RightPanel(wx.Panel):
    """Constructor"""
    def __init__(self, parent,frame):
        wx.Panel.__init__(self, parent=parent)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        nextImage = "images\\buttons\\NextButtonNew.png"
        previousImage="images\\buttons\\BackButtonNew.png"
        flipImage="images\\buttons\\FlipButton1.png"
        shuffleImage="images\\buttons\\ShuffleButton1.png"

        #Next Button Init
        image1 = wx.Image(nextImage, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.nextButton = wx.BitmapButton(self, id=-1, bitmap=image1,
        pos=(990, 305), size=(image1.GetWidth()+5, image1.GetHeight()+5), style=wx.BU_AUTODRAW)
        self.nextButton.Bind(wx.EVT_BUTTON, lambda event: self.nextButtonClick(event, parent.cards))
        self.nextButton.SetToolTip(wx.ToolTip("Go to Next Flashcard"))

        #Back Button Init
        image2 = wx.Image(previousImage, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.backButton = wx.BitmapButton(self, id=-1, bitmap=image2,
        pos=(15, 305), size=(image2.GetWidth()+5, image2.GetHeight()+5), style=wx.BU_AUTODRAW)
        self.backButton.Bind(wx.EVT_BUTTON, lambda event: self.backButtonClick(event, parent.cards))
        self.backButton.SetToolTip(wx.ToolTip("Go to Previous Flashcard"))

        #Flip Button Init
        image3 = wx.Image(flipImage, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.flipButton = wx.BitmapButton(self, id=-1, bitmap=image3,
        pos=(970, 520), size=(image2.GetWidth()+5, image2.GetHeight()+5), style=wx.BU_AUTODRAW)
        self.flipButton.Bind(wx.EVT_BUTTON, lambda event: self.flipButtonClick(event, parent.cards))
        self.flipButton.SetToolTip(wx.ToolTip("Go to Front/Back of Flashcard"))

        #Shuffle Button Init
        image4 = wx.Image(shuffleImage, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.shuffleButton = wx.BitmapButton(self, id=-1, bitmap=image4,
        pos=(10, 520), size=(image2.GetWidth()+5, image2.GetHeight()+5), style=wx.BU_AUTODRAW)
        self.shuffleButton.Bind(wx.EVT_BUTTON, lambda event: self.shuffleButtonClick(event, parent.cards, frame))
        self.shuffleButton.SetToolTip(wx.ToolTip("Shuffle the Deck of Cards"))
                
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
        self.height = self.bmp1.GetHeight()/2-(14*(len(parent.cards.getInfo())/85))

        self.text = wx.StaticText(self, label="",  style=(wx.TE_MULTILINE ))
        self.text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.text.SetSize(self.text.GetBestSize())

        self.updateText(parent.cards)


    # Gets the new text for the card, centers it, wraps it, and displays
    def updateText(self, cards):
        #set label to empty string so that no weird lag display problems can be seen
        self.text.Label = ""
        newText = wordwrap(cards.getInfo(), 450, wx.ClientDC(self), breakLongWords=True, margin=0)
    
        sizer_h = wx.BoxSizer(wx.HORIZONTAL)
        sizer_v = wx.BoxSizer(wx.VERTICAL)
        sizer_v.Add(self.text, 1, wx.CENTER)
        sizer_h.Add(sizer_v, 1, wx.CENTER)
        self.SetSizer(sizer_h) 
        sizer_h.Fit(self)
        self.text.Label = newText
    
    #back button click event
    def backButtonClick(self,event,cards):
        cards.prev()
        self.updateText(cards)
    
    #next button click event
    def nextButtonClick(self,event,cards):
        cards.next()
        self.updateText(cards)
    
    #fliip button click event
    def flipButtonClick(self,event,cards):
        cards.flip()
        self.updateText(cards)
    
    #shuffle button click event // reassign every button to the appropriate card
    def shuffleButtonClick(self,event,cards,frame):
        cards.shuffle()
        self.updateText(cards)
        for i in range (0, len(cards.JSON)):
            buttonText = wordwrap(cards.JSON[i]['question'], 250, wx.ClientDC(self), breakLongWords=True, margin=0)
            buttonText = trimText(buttonText)
            button = frame.FindWindowByName(str(i))
            button.Show(False)
            button.SetLabel(buttonText)
            #refresh the button
            button.Show(True)
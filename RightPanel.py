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
            Up      -> move card up in the stack
            Down    -> move card down in the stack
'''
import wx
import os
import  cStringIO
from wx.lib.wordwrap import wordwrap
from panelHelpers import trimText
import  wx.lib.scrolledpanel as scrolled

class RightPanel(scrolled.ScrolledPanel):
    """Constructor"""
    def __init__(self, parent,frame):

        scrolled.ScrolledPanel.__init__(self, parent=parent, style=wx.ALWAYS_SHOW_SB)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        nextImage = "images\\buttons\\NextButtonNew.png"
        previousImage="images\\buttons\\BackButtonNew.png"
        flipImage="images\\buttons\\FlipButton1.png"
        shuffleImage="images\\buttons\\ShuffleButton1.png"
        upImage="images\\buttons\\UpButton.png"
        downImage="images\\buttons\\DownButton.png"


        #Move Up Button Init
        image5 = wx.Image(upImage, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.upButton = wx.BitmapButton(self, id=-1, bitmap=image5,
        pos=(0, 0), size=(image5.GetWidth()+5, image5.GetHeight()+5), style=wx.BU_AUTODRAW)
        self.upButton.Bind(wx.EVT_BUTTON, lambda event: self.upButtonClick(event, parent.cards, frame))
        self.upButton.SetToolTip(wx.ToolTip("Move current flash card up in the stack"))
        sizer.Add(self.upButton, 0, wx.CENTER|wx.ALL, 5)
        #Move Down Button Init
        image6 = wx.Image(downImage, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.downButton = wx.BitmapButton(self, id=-1, bitmap=image6,
        pos=(0, image5.GetHeight()+5), size=(image6.GetWidth()+5, image6.GetHeight()+5), style=wx.BU_AUTODRAW)
        self.downButton.Bind(wx.EVT_BUTTON, lambda event: self.downButtonClick(event, parent.cards, frame))
        self.downButton.SetToolTip(wx.ToolTip("Move current flash card down in the stack"))
        sizer.Add(self.downButton, 0, wx.CENTER|wx.ALL, 5)

        #Next Button Init
        image1 = wx.Image(nextImage, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.nextButton = wx.BitmapButton(self, id=-1, bitmap=image1,
        pos=(990, 305), size=(image1.GetWidth()+5, image1.GetHeight()+5), style=wx.BU_AUTODRAW)
        self.nextButton.Bind(wx.EVT_BUTTON, lambda event: self.nextButtonClick(event, parent.cards, frame))
        self.nextButton.SetToolTip(wx.ToolTip("Go to Next Flashcard"))
        sizer.Add(self.nextButton, 0, wx.CENTER|wx.ALL, 5)

        #Back Button Init
        image2 = wx.Image(previousImage, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.backButton = wx.BitmapButton(self, id=-1, bitmap=image2,
        pos=(15, 305), size=(image2.GetWidth()+5, image2.GetHeight()+5), style=wx.BU_AUTODRAW)
        self.backButton.Bind(wx.EVT_BUTTON, lambda event: self.backButtonClick(event, parent.cards, frame))
        self.backButton.SetToolTip(wx.ToolTip("Go to Previous Flashcard"))
        sizer.Add(self.backButton, 0, wx.CENTER|wx.ALL, 5)

        #Flip Button Init
        image3 = wx.Image(flipImage, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.flipButton = wx.BitmapButton(self, id=-1, bitmap=image3,
        pos=(970, 520), size=(image2.GetWidth()+5, image2.GetHeight()+5), style=wx.BU_AUTODRAW)
        self.flipButton.Bind(wx.EVT_BUTTON, lambda event: self.flipButtonClick(event, parent.cards))
        self.flipButton.SetToolTip(wx.ToolTip("Go to Front/Back of Flashcard"))
        sizer.Add(self.flipButton, 0, wx.CENTER|wx.ALL, 5)

        #Shuffle Button Init
        image4 = wx.Image(shuffleImage, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.shuffleButton = wx.BitmapButton(self, id=-1, bitmap=image4,
        pos=(10, 520), size=(image2.GetWidth()+5, image2.GetHeight()+5), style=wx.BU_AUTODRAW)
        self.shuffleButton.Bind(wx.EVT_BUTTON, lambda event: self.shuffleButtonClick(event, parent.cards, frame))
        self.shuffleButton.SetToolTip(wx.ToolTip("Shuffle the Deck of Cards"))
        sizer.Add(self.shuffleButton, 0, wx.CENTER|wx.ALL, 5)
                
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

        self.text = wx.StaticText(self, label="",  style=(wx.TE_MULTILINE))
        self.text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.text.SetSize(self.text.GetBestSize())
        self.messButton = wx.BitmapButton(self, id=-1, bitmap=image4,
        pos=(1500, 3520), size=(image2.GetWidth()+5, image2.GetHeight()+5), style=wx.BU_AUTODRAW)
        
        self.updateText(parent.cards)
        #self.SetAutoLayout(1)

        self.SetupScrolling()

    # Gets the new text for the card, centers it, wraps it, and displays
    def updateText(self, cards):
        #set label to empty string so that no weird lag display problems can be seen
        self.text.Label = ""
        newText = wordwrap(cards.getInfo(), 450, wx.ClientDC(self), breakLongWords=True, margin=0)
        newText = trimText(newText, 23)
    
        sizer_h = wx.BoxSizer(wx.HORIZONTAL)
        sizer_v = wx.BoxSizer(wx.VERTICAL)
        sizer_v.Add(self.text, 1, wx.CENTER)
        sizer_h.Add(sizer_v, 1, wx.CENTER| wx.BOTTOM, border=15 )
        self.SetSizer(sizer_h) 
        sizer_h.Fit(self)
        self.text.Label = newText
    
    #back button click event
    def backButtonClick(self,event,cards, frame):
        self.removeHighlight(cards, frame)
        cards.prev()
        self.updateText(cards)
        self.addHighlight(cards, frame)
    
    #next button click event
    def nextButtonClick(self,event,cards, frame):
        self.removeHighlight(cards, frame)
        cards.next()
        self.updateText(cards)
        self.addHighlight(cards, frame)
    
    #fliip button click event
    def flipButtonClick(self,event,cards):
        cards.flip()
        self.updateText(cards)
    
    #shuffle button click event // reassign every button to the appropriate card
    def shuffleButtonClick(self,event,cards,frame):
        self.removeHighlight(cards, frame)
        cards.shuffle()
        self.updateText(cards)
        self.updateLeftPanel(cards,frame)
        self.addHighlight(cards, frame)

    def upButtonClick(self, event, cards, frame):
        self.removeHighlight(cards, frame)
        cards.moveUp()
        self.updateLeftPanel(cards, frame)
        self.addHighlight(cards, frame)

    def downButtonClick(self, event, cards, frame):
        self.removeHighlight(cards, frame)
        cards.moveDown()
        self.updateLeftPanel(cards, frame)
        self.addHighlight(cards, frame)

    def updateLeftPanel(self, cards, frame):
        for i in range (0, len(cards.JSON)):
            buttonText = wordwrap(cards.JSON[i]['question'], 250, wx.ClientDC(self), breakLongWords=True, margin=0)
            buttonText = trimText(buttonText, 14)
            button = frame.FindWindowByName(str(i))
            button.Show(False)
            button.SetLabel(buttonText)
            #refresh the button
            button.Show(True)

    def removeHighlight(self, cards, frame):
        button = frame.FindWindowByName(str(cards.index))
        button.Show(False)
        button.SetBackgroundColour('#022331')
        button.Show(True)

    def addHighlight(self, cards, frame):
        button = frame.FindWindowByName(str(cards.index))
        button.Show(False)
        button.SetBackgroundColour('#007db1')
        button.Show(True)

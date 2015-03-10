
'''
    Program: FlashGen
    File: LeftPanel.py
    Team: Brendan Cicchi, Remington Maxwell, Sara Woods

    Summary: Class LeftPanel
        Displays the small cards on the left hand side
        Can be used similar to powerpoint to go to a specific card
        
        Buttons:
            Each card is actually a button
'''
import wx
import  cStringIO
import  wx.lib.scrolledpanel as scrolled
import wx.lib.buttons as buttons
import wx.lib.agw.aquabutton as AB
import wx.lib.agw.gradientbutton as GB
import wx.lib.platebtn as platebtn
from wx.lib.wordwrap import wordwrap
from panelHelpers import trimText

class LeftPanel(scrolled.ScrolledPanel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent, frame):
        """Constructor"""
        scrolled.ScrolledPanel.__init__(self, parent=parent)


 
        #grid = gridlib.Grid(self)
        #grid.CreateGrid(100,2)
 
        imageFile='images\\borders\\Notecard Border 1.png'
        data = open(imageFile, "rb").read()
        # convert to a data stream
        stream = cStringIO.StringIO(data)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        # convert to a bitmap
        bmp = wx.BitmapFromImage( wx.ImageFromStream( stream ))
        image2 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        bmp1 = wx.Bitmap(imageFile, wx.BITMAP_TYPE_ANY)
        notecardText = "Display Notecard text here"
        self.spacer = self.sizer.AddSpacer(10)
        displaySize=wx.DisplaySize()

        self.createButtons(parent, frame)

        self.SetSizer(self.sizer)
        #self.SetAutoLayout(1)
        self.SetupScrolling()


    def selectButtonClick(self, event, parent, frame):
        parent.rightP.removeHighlight(parent.cards, frame)
        parent.cards.index = event.GetEventObject().GetId()
        parent.cards.face = 'question'
        parent.rightP.updateText(parent.cards)
        parent.rightP.addHighlight(parent.cards, frame)

    def createButtons(self, parent, frame):
        for i in range (0, len(parent.cards.JSON)):
            buttonText = wordwrap(parent.cards.JSON[i]['question'], 250, wx.ClientDC(self), breakLongWords=True, margin=0)
            buttonText = trimText(buttonText, 14)
            parent.button = AB.AquaButton(self, label=buttonText, name=str(i), size=(220,170), id=i)
            parent.button.SetFont(wx.Font(6, wx.SWISS, wx.NORMAL, wx.BOLD))
            if i == 0:
                parent.button.SetBackgroundColour('#007db1')
            else:
                parent.button.SetBackgroundColour('#022331')
            parent.button.SetForegroundColour("black")
            parent.button.SetHoverColour('#C3E6F3')
            parent.button.Bind(wx.EVT_BUTTON, lambda event: self.selectButtonClick(event, parent, frame))
            parent.button.SetPulseOnFocus(True)

            parent.button.SetPulseOnFocus(False)
            self.sizer.Add(parent.button, 0, wx.CENTER|wx.ALL, 5)
            #self.sizer.AddSpacer(10)
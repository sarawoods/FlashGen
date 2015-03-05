
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
        image2 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        bmp1 = wx.Bitmap(imageFile, wx.BITMAP_TYPE_ANY)
        notecardText = "Display Notecard text here"
        sizer.AddSpacer(10)
        displaySize=wx.DisplaySize()
        for i in range (0,1):
            b="text"
            buttonText = b +str(i)
            buttonText = AB.AquaButton(self, label=notecardText, size=(220,170))
            buttonText.SetFont(wx.Font(6, wx.SWISS, wx.NORMAL, wx.BOLD))
            buttonText.SetBackgroundColour('#007db1')
            buttonText.SetForegroundColour("black")
            buttonText.SetHoverColour('#70caef')

            buttonText.SetPulseOnFocus(False)
            sizer.Add(buttonText, 0, wx.CENTER|wx.ALL, 5)
            sizer.AddSpacer(10)


        self.SetSizer(sizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()
        
        
        #self.SetScrollbar(wx.VERTICAL, 0, 10, 500);
 
########################################################################

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
        notecardText= parent.cards.getInfo()
        #use test to loop through and add the notecards dynamically
        # show the bitmap, (5, 5) are upper left corner coordinates

        #self.note=wx.StaticBitmap(self, -1, bmp, (0, 140))

        #self.text = wx.StaticText(self, -1, "", (self.width, self.height), style=(wx.ALIGN_CENTRE_HORIZONTAL| wx.TE_MULTILINE ))
        #self.text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        #self.text.SetSize(self.text.GetBestSize())

        #font =  dc.GetFont()
        #font.SetPointSize(15)
        #font.SetWeight(wx.FONTWEIGHT_BOLD)
        displaySize=wx.DisplaySize()

        #next three lines work for a static bitmap
        #text1 = wx.StaticText(self.note, -1, notecardText, style=(wx.ALIGN_CENTRE_HORIZONTAL))
        #text1.SetFont(wx.Font(5, wx.SWISS, wx.NORMAL, wx.BOLD))
        #text1.SetSize(text1.GetBestSize())
        ###

        #sizer.Add(text1,0,wx.EXPAND)
        '''sizer.Add(self.note, 0, wx.EXPAND)
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
        sizer.Add(note4, 0, wx.EXPAND)'''
        
        #button testing
        image2 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.testButton = wx.BitmapButton(self, id=-1, bitmap=image2,
         size=(image2.GetWidth()+5, image2.GetHeight()+5), style=wx.BU_AUTODRAW)
        text = wx.StaticText(self.testButton, -1, notecardText, style=(wx.ALIGN_CENTRE_HORIZONTAL|wx.TE_MULTILINE))
        text.SetFont(wx.Font(5, wx.SWISS, wx.NORMAL, wx.BOLD))
        text.SetSize(text.GetBestSize())
        sizer.Add(text,0,wx.EXPAND)
        sizer.Add(self.testButton,0,wx.EXPAND)
        sizer.AddSpacer(10)
        
        self.testButton1 = wx.BitmapButton(self, id=-1, bitmap=image2,
         size=(image2.GetWidth()+5, image2.GetHeight()+5), style=wx.BU_AUTODRAW)
        text1 = wx.StaticText(self, -1, notecardText, style=(wx.ALIGN_CENTRE_HORIZONTAL|wx.TE_MULTILINE))
        text1.SetFont(wx.Font(5, wx.SWISS, wx.NORMAL, wx.BOLD))
        text1.SetSize(text1.GetBestSize())
        sizer.Add(text1,0,wx.EXPAND)
        sizer.Add(self.testButton1,0,wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()
        
        
        #self.SetScrollbar(wx.VERTICAL, 0, 10, 500);
 
########################################################################
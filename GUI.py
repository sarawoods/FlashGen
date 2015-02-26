import wx
import wx.grid as gridlib
import  cStringIO
import  wx.lib.scrolledpanel as scrolled
 
########################################################################
class LeftPanel(scrolled.ScrolledPanel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        scrolled.ScrolledPanel.__init__(self, parent=parent)

 
        #grid = gridlib.Grid(self)
        #grid.CreateGrid(100,2)
 
        imageFile='Notecard Border 1.png'
        data = open(imageFile, "rb").read()
        # convert to a data stream
        stream = cStringIO.StringIO(data)
        sizer = wx.BoxSizer(wx.VERTICAL)
        # convert to a bitmap
        bmp = wx.BitmapFromImage( wx.ImageFromStream( stream ))
        i=1
        a = "note"
        test = a + str(i)
        notecardText="Notecard Text Appears Here"
        sizer.AddSpacer(10)
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
        wx.Panel.__init__(self, parent=parent)
        #load buttons
        # panel needed to display button correctly
        
 
        nextImage = "NextButtonNew.png"
        previousImage="BackButtonNew.png"
        flipImage="FlipButton1.png"
        #Need to disable button if add end of list or start of list
        #self.backButton = wx.Button(self, label='Previous',pos=(20, 305), size=(80, 50))
        image1 = wx.Image(nextImage, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.nextButton = wx.BitmapButton(self, id=-1, bitmap=image1,
        pos=(990, 305), size=(image1.GetWidth()+5, image1.GetHeight()+5))
        image2 = wx.Image(previousImage, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.backButton = wx.BitmapButton(self, id=-1, bitmap=image2,
        pos=(15, 305), size=(image2.GetWidth()+5, image2.GetHeight()+5))
        image3 = wx.Image(flipImage, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.flipButton = wx.BitmapButton(self, id=-1, bitmap=image3,
        pos=(970, 520), size=(image2.GetWidth()+5, image2.GetHeight()+5))
        #self.nextButton = wx.Button(self,label='Next', pos=(990,305), size=(80,50))
        #Binds the trigger event fror going to previous flashcard
        self.backButton.Bind(wx.EVT_BUTTON, self.backButtonClick)
        # optional tooltip
        self.backButton.SetToolTip(wx.ToolTip("Go to Previous Flashcard"))
        #Binds the trigger event fror going to previous flashcard
        self.nextButton.Bind(wx.EVT_BUTTON, self.nextButtonClick)
        # optional tooltip
        self.nextButton.SetToolTip(wx.ToolTip("Go to Next Flashcard"))
        self.flipButton.Bind(wx.EVT_BUTTON, self.flipButtonClick)
        # optional tooltip
        self.flipButton.SetToolTip(wx.ToolTip("Go to Next Flashcard"))
        #for displaying notecard image
        imageFile1='Notecard Border.png'
        data = open(imageFile1, "rb").read()
        # convert to a data stream
        stream = cStringIO.StringIO(data)
        # convert to a bitmap
        bmp1 = wx.BitmapFromImage( wx.ImageFromStream( stream ))
        # show the bitmap, (5, 5) are upper left corner coordinates
        noteFront=wx.StaticBitmap(self, -1, bmp1, (100, 15))

        # and a few controls
        notecardText="Notecard Text Appears Here"
        displaySize=wx.DisplaySize()
        text = wx.StaticText(self, -1, notecardText,(displaySize[0]/3-40, displaySize[1]/3+40))
        text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        text.SetSize(text.GetBestSize())

    #back button click event
    def backButtonClick(self,event):
        self.backButton.Hide()
        changeText()

    #next button click event
    def nextButtonClick(self,event):
        self.nextButton.Hide()

    #next button click event
    def flipButtonClick(self,event):
        self.flipButton.Hide()

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
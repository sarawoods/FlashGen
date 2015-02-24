import wx
import wx.grid as gridlib
import  cStringIO
 
########################################################################
class LeftPanel(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)

 
        grid = gridlib.Grid(self)
        grid.CreateGrid(10,42)
 
        imageFile='Notecard Border Small.png'
        data = open(imageFile, "rb").read()
        # convert to a data stream
        stream = cStringIO.StringIO(data)
        # convert to a bitmap
        bmp = wx.BitmapFromImage( wx.ImageFromStream( stream ))
        # show the bitmap, (5, 5) are upper left corner coordinates
        note=wx.StaticBitmap(self, -1, bmp, (0, 140))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(note, 0, wx.EXPAND)
        note1=wx.StaticBitmap(self, -1, bmp, (0, 140))
        sizer.Add(note1, 1, wx.EXPAND)
        note2=wx.StaticBitmap(self, -1, bmp, (0, 140))
        sizer.Add(note2, 2, wx.EXPAND)
        note3=wx.StaticBitmap(self, -1, bmp, (0, 140))
        sizer.Add(note3, 3, wx.EXPAND)
        self.SetSizer(sizer)
 
########################################################################
class RightPanel(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        
        #txt = wx.TextCtrl(self)
        #for displaying notecard image
        imageFile1='Notecard Border.png'
        data = open(imageFile1, "rb").read()
        # convert to a data stream
        stream = cStringIO.StringIO(data)
        # convert to a bitmap
        bmp1 = wx.BitmapFromImage( wx.ImageFromStream( stream ))
        # show the bitmap, (5, 5) are upper left corner coordinates
        noteFront=wx.StaticBitmap(self, -1, bmp1, (100, 15))
        imageFile2='Notecard Border.png'
        data = open(imageFile2, "rb").read()
        # convert to a data stream
        stream = cStringIO.StringIO(data)
        # convert to a bitmap
        bmp2 = wx.BitmapFromImage( wx.ImageFromStream( stream ))
        # show the bitmap, (5, 5) are upper left corner coordinates
        noteBack=wx.StaticBitmap(self, -1, bmp2, (100, 715))
        # and a few controls
        notecardText="Notecard Text Appears Here"
        displaySize=wx.DisplaySize()
        text = wx.StaticText(self, -1, notecardText,(displaySize[0]/3-40, displaySize[1]/3+40))
        text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        text.SetSize(text.GetBestSize())
        
 
########################################################################
class MyForm(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self, ):
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
    app.MainLoop()
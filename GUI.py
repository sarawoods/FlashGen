import wx
import wx.grid as gridlib
import  cStringIO
import random

from subprocess import check_output
import json

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
		print self.index
		print self.face
		print self.JSON[self.index][self.face]
		return self.JSON[self.index][self.face]
		


def getNotes():
    # once user selects file to open store that file in a variable
    notesFile = "story.txt"
    # run haskell program to get JSON string
    noteselftring = check_output(["runhaskell", "parse.hs", notesFile])
    # convert the string into a JSON object
    noteCardJSON = json.loads(noteselftring)
    # generate GUI using the JSON
    '''
    for card in noteCardJSON:
        print ""

        question = card["question"]
        print "question: " + question

        options = card["options"]
        for opt in options:
            print "   option: " + opt

        answers = card["answers"]
        for ans in answers:
            print "   answer: " + ans
    '''

    return noteCardJSON
'''
# getInfo -> gets a face specified by type for a particular card
def getInfo(JSON, index, type):
	return (JSON[index][type], index)

# next -> gets next card, gets first card if next is clicked on last card
def next(JSON, index):
	if index == len(JSON) - 1:
		index = 0;
	else:
		index += 1;
	return (JSON[index]['question'], index)

# prev -> gets previous card, gets last card if prev is clicked on prev card
def prev(JSON, index):
	if index == 0:
		index = len(JSON) - 1
	else:
		index -= 1;
	return (JSON[index]['question'], index)

# flip -> gets the face of the current card not currently shown
def flip(JSON, index, type):
	if type == 'question':
		return JSON[index]['answers']
	elif (type == 'answer'):
		return JSON[index]['question']
	else:
		raise NameError("Error: Flip has a bad type -> " + type)

# shuffle -> returns the elements of array in a random order 
def shuffle(JSON):
	random.shuffle(JSON)
	return JSON
 '''
########################################################################
class LeftPanel(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)

 
        grid = gridlib.Grid(self)
        grid.CreateGrid(10,42)
 
        imageFile='Notecard Border 1.png'
        data = open(imageFile, "rb").read()
        # convert to a data stream
        stream = cStringIO.StringIO(data)
        sizer = wx.BoxSizer(wx.VERTICAL)
        # convert to a bitmap
        bmp = wx.BitmapFromImage( wx.ImageFromStream( stream ))
        # show the bitmap, (5, 5) are upper left corner coordinates
        note=wx.StaticBitmap(self, -1, bmp, (0, 140))
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
				# get the data
        noteCardJSON = getNotes()
	cards = Cards(noteCardJSON)
        wx.Panel.__init__(self, parent=parent)
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)
        #load buttons
        #Need to disable button if add end of list or start of list
        self.backButton = wx.Button(self, label='Previous',pos=(20, 305), size=(80, 50))
        self.nextButton = wx.Button(self,label='Next', pos=(990,305), size=(80,50))
        #Binds the trigger event fror going to previous flashcard
        #self.backButton.Bind(wx.EVT_BUTTON, self.backButtonClick)
	self.backButton.Bind(wx.EVT_BUTTON, lambda event: self.backButtonClick(event, cards))
        # optional tooltip
        self.backButton.SetToolTip(wx.ToolTip("Go to Previous Flashcard"))
        #Binds the trigger event for going to previous flashcard
        #self.nextButton.Bind(wx.EVT_BUTTON, self.nextButtonClick)
	self.nextButton.Bind(wx.EVT_BUTTON, lambda event: self.nextButtonClick(event, cards))
        # optional tooltip
        self.nextButton.SetToolTip(wx.ToolTip("Go to Next Flashcard"))
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
		
	self.updateText = wx.StaticText(self, -1, "", (displaySize[0]/3-40, displaySize[1]/3+40))
		

		######################################################
		##				Testing functionality				##
		######################################################


    #back button click event
    def backButtonClick(self,event, cards):
		cards.prev()
		self.updateText.Label = cards.getInfo()

    #next button click event
    def nextButtonClick(self,event, cards):
		cards.next()
		self.updateText.Label = cards.getInfo()


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
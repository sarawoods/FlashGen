'''
	Program: FlashGen
	File: FlashGen.py
	Team: Brendan Cicchi, Remington Maxwell, Sara Woods

	Summary: __main__ file
'''

import wx
from MyForm import MyForm
 
#----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.App(False)

    frame = MyForm()
    frame.Show()
    
    #loadButton = wx.Button(frame, label='Open',pos=(225, 5), size=(80, 25))
    #saveButton = wx.Button(frame, label='Save',pos=(315, 5), size=(80, 25))
    #filename = wx.TextCtrl(frame, pos=(5, 5), size=(210, 25))
    #contents = wx.TextCtrl(frame, pos=(5, 35), size=(390, 260),style=wx.TE_MULTILINE | wx.HSCROLL)
    app.MainLoop()
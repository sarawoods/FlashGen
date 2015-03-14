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
 
    app.MainLoop()
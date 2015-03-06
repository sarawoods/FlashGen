'''
    Program: FlashGen
    File: panelHelpers.py
    Team: Brendan Cicchi, Remington Maxwell, Sara Woods

    Summary:
        Contains helper functions used in both left and right panels
	        
	        Functions:
	            trimText -> cuts text off at 14 lines for left panel buttons
	            
'''
def trimText(text):
    newLines = 0
    for index in range(0, len(text)):
        if text[index] == "\n":
            newLines += 1
            if newLines == 14:
                return text[0:index]
    return text
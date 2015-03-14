'''
    Program: FlashGen
    File: Cards.py
    Team: Brendan Cicchi, Remington Maxwell, Sara Woods

    Summary: Class Cards
        Methods:
            next     -> move to next card in the array
                        go to first card if past last
            prev     -> move to previous card in the array
                         go to last card if past zero
            flip     -> change the face of the card, flip it
            shuffle  -> rearrange the array of cards randomly
            moveUp   -> move the selected card on the left panel up
            moveDown -> move the selected card on the left panel down
            getInfo  -> return the string to be shown on the card face
'''
import random

class Cards:
    def __init__(self, JSON):
        self.JSON = JSON
        self.index = 0
        self.face = "question"
	
    # next -> increments the index of the list of cards
    def next(self):
        if self.index == len(self.JSON) - 1:
            self.index = 0
        else:
            self.index = self.index + 1
        self.face = "question"
	
    # prev -> decrements the index of the list of cards
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

    # moveUp -> switches the content of the cards object at the index with the content of the previous element
    def moveUp(self):
        if self.index != 0:
            self.JSON[self.index], self.JSON[self.index-1] = self.JSON[self.index-1], self.JSON[self.index]
            self.index = self.index-1

    # moveDown -> switches the content of the cards object at the index with the content of the next element
    def moveDown(self):
        if self.index != len(self.JSON)-1:
            self.JSON[self.index], self.JSON[self.index+1] = self.JSON[self.index+1], self.JSON[self.index]
            self.index = self.index+1
		
    # getInfo -> returns the text of the current face of the card at index
    def getInfo(self):
        if len(self.JSON) > 0:
            if self.face == "question":
                question = self.JSON[self.index][self.face]
                options = "\n"
                for opt in self.JSON[self.index]["options"]:
                    options =  options + "\n" + "    - " + opt
                return question + options
            else:
                answers = ""
                if len(self.JSON[self.index][self.face]) == 1:
                    answers = self.JSON[self.index][self.face][0]
                else:
                    for ans in self.JSON[self.index][self.face]:
                        answers = answers + "- " + ans + "\n"
                return answers
        else:
		  return "Sorry, the file you uploaded did not parse any questions.\n" + \
                 "Please check your formatting or try uploading another file." + \
                 "Check out our tutorial for help." 
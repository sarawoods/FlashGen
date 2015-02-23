# Main Python Program

from subprocess import call
import json

def main():
	# run GUI
	# once user selects file to open store that file in a variable
	notesFile = ""
	# run haskell program to get JSON string
	noteCardString = call(["runhaskell", "parse.hs", notesFile])
	# convert the string into a JSON object
	noteCardJSON = json.loads(noteCardString)
	# generate GUI using the JSON


if __name__ == '__main__':
	main()
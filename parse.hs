{-
	Program: FlashGen
	File: parse.hs
	Author: Brendan Cicchi
	
	Summary: 
		1) reads contents of input file
		2) removes leading white space from the lines of file
		3) filters lines which have the relevent symbols attached to them:
			~ question
			| front question options
			> answer
			> multiple answers
		4) uses a regular expr to parse lines to make sure all input is valid
			N.B. ignores all non valid input
				if part of the input is invalid,
					everything after that point will be invalid till the next ~\
		5) output valid lines to a file
-}

import System.Environment
import Text.Regex

main = do
   args <- getArgs
   content <- readFile (args !! 0)
   -- convert lines of File to Text type for easy management
   let linesOfFiles = lines content
   -- grab relevant lines from removed beginning whitespace lines
   let imp_lines = tup2str_rec$ regex$ unlines$ filter line_check (map strip linesOfFiles)
   -- write the results to a file
   writeFile (args !! 1) (imp_lines)

-- function to discern relevant lines in the file
line_check :: String -> Bool
line_check [] = False
line_check (x:xs)
	| (x == '~' || x == '>' || x == '|') = True
	| otherwise = False

-- function to remove all leading white space from line in file
strip :: String -> String
strip [] = []
strip (x:xs)
	| (x == ' ' || x == '\t') = strip xs
	| otherwise = (x:xs)

-- recursive call to continue parsing after invalid data
tup2str_rec :: Maybe (String, String, String, [String]) -> String
tup2str_rec Nothing = []
tup2str_rec (Just(_,m,nm,_)) = m ++ tup2str_rec (regex nm)

-- use a regular expression to parse input
regex :: String -> Maybe (String, String, String, [String])
regex [] = Nothing
regex x = matchRegexAll (mkRegexWithOpts "(~[^|>]+)+([|][^~>]+)*(>[^~|]+)*" False False) x
{-
regular expression: 
(~[^|>]+)+ 		accept one or more "~"s with no "|" or ">"
([|][^~>]+)*	followed by zero or more "|"s with no "~" or ">"
(>[^~|]+)*		followed by zero or more ">"" with no "~" or "|"
-}
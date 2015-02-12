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
			N.B. ignores all non valid input without error
				if part of the input is invalid,
					everything after that point will be invalid till the next ~
		5) form a tuple of form [(question,[options],[answers])]
		5) output tuple as a string to a file or console
-}

import System.Environment
import Text.Regex

main = do
   args <- getArgs
   content <- readFile (args !! 0)
   -- convert lines of File to Text type for easy management
   let fLines = lines content
   -- grab relevant lines from removed beginning white space lines
   let imp_lines = tup2str_rec$ regex$ unlines$ filter pass1 (map strip fLines)
   -- group lines by (quest,[opt],[ans])in tuple (String, [String], [String])
   let tup_list = group $ lines imp_lines
   -- output tuple as string
   putStrLn $ show tup_list
   -- write the results to a file
--   writeFile (args !! 1) (tup_list)

-- strip -> function to remove all leading white space from line in file
strip :: String -> String
strip [] = []
strip (x:xs)
	| (x == ' ' || x == '\t') = strip xs
	| otherwise = (x:xs)
	
-- pass1 -> takes any line with "~" "|" or ">" symbols at the front
pass1 :: String -> Bool
pass1 [] = False
pass1 (x:xs)
	| (x == '~' || x == '>' || x == '|') = True
	| otherwise = False

-- tup2str_rec -> recursive call to continue parsing after invalid data
tup2str_rec :: Maybe (String, String, String, [String]) -> String
tup2str_rec Nothing = []
tup2str_rec (Just(_,m,nm,_)) = m ++ tup2str_rec (regex nm)

-- group -> form the tuples (String, [String], [String]) to be passed to py
group :: [String] -> [(String,[String],[String])]
group [] = []
group (x:xs)
	| (head x == '~') = [(x,(getList xs '|'),(getList xs '>'))] ++ group xs
	| otherwise = group xs

-- getList -> form a list of all c's following '~' before the next one
getList :: [String] -> Char -> [String]
getList [] _ = []
getList (x:xs) c
	| head x == c = [x] ++ getList xs c
	| otherwise = []

-- regex -> use a regular expression to parse input
regex :: String -> Maybe (String, String, String, [String])
regex [] = Nothing
regex x = matchRegexAll (mkRegexWithOpts "(~[^|>]+)+([|][^~>]+)*(>[^~|]+)*" False False) x
{-
regular expression: 
(~[^|>]+)+ 		accept one or more "~"s with no "|" or ">"
([|][^~>]+)*	followed by zero or more "|"s with no "~" or ">"
(>[^~|]+)*		followed by zero or more ">"" with no "~" or "|"
-}
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
		5) Output JSON to stdout in form
			[
				{
					question : "...",
					"option" : ["option1", "option2",....],
					"answer" : ["answer1", "answer2", ....]
				}
			]
-}

import System.Environment
import Text.Regex
import Data.List

main = do
   args <- getArgs
   content <- readFile (args !! 0)
   -- convert lines of File to Text type for easy management
   let fLines = lines content
   -- grab relevant lines from removed beginning white space lines
   let imp_lines = tup2str_rec$ regex$ unlines$ filter pass1 (map strip fLines)
   -- group lines by (quest,[opt],[ans])in tuple (String, [String], [String])
   let tup_list = group1 (lines imp_lines)
   -- convert formatted tuple to json
   let json =  "[ " ++ (intercalate " " $ map jsonize tup_list) ++ " ]"
   -- output json as string
   putStrLn $ json
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
group1 :: [String] -> [(String,[String],[String])]
group1 [] = []
group1 (x:xs)
	| (head x == '~') = [(x,(getList xs '|'),(getList xs '>'))] ++ group1 xs
	| otherwise = group1 xs

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

jsonize :: (String, [String], [String]) -> String
jsonize (q,o,a) = "{ "++"'question': "++show q++" 'option': "++ show (intercalate " " o)++ "'answer': "++show (intercalate " " a)++ " },"
{-
regular expression: 
(~[^|>]+)+ 		accept one or more "~"s with no "|" or ">"
([|][^~>]+)*	followed by zero or more "|"s with no "~" or ">"
(>[^~|]+)*		followed by zero or more ">"" with no "~" or "|"
-}
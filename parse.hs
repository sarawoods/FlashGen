{-
	Program: FlashGen
	File: parse.hs
	Author: Brendan Cicchi
	Team: Brendan Cicchi, Remington Maxwell, Sara Woods
	
	Summary: 
		1) reads contents of input file
		2) removes leading white space from the lines of file
		3) filters lines which have the relevant symbols attached to them:
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
					"options" : ["option1", "option2",....],
					"answers" : ["answer1", "answer2", ....]
				}
			]
-}
import System.Environment
import Text.Regex
import Data.List

main = do
   args <- getArgs
   -- get the content of file as string
   content <- readFile (args !! 0)
   -- convert lines of File to Text type for easy management
   let fLines = lines content
   -- grab relevant lines from removed beginning white space lines
   let imp_lines = tup2str_rec$ regex$ unlines$ filter pass1 (map strip fLines)
   -- group lines by (quest,[opt],[ans])in tuple (String, [String], [String])
   let tup_list = list2tup (lines imp_lines)
   -- convert formatted tuple to json
   let json =  "[ " ++ (intercalate ", " $ map jsonize tup_list) ++ " ]"
   -- output json as string
   putStrLn json
   

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

-- list2tup -> form the tuples (String, [String], [String]) to be passed to python
list2tup :: [String] -> [(String,[String],[String])]
list2tup [] = []
list2tup (x:xs)
	| (head x == '~') = [(rm_mark x,(getList xs '|'),(getList xs '>'))] {-
						-} ++ list2tup xs
	| otherwise = list2tup xs

-- getList -> form a list of all c's following '~' before the next one
getList :: [String] -> Char -> [String]
getList [] _ = []
getList (x:xs) c
	| head x == c = [(rm_mark x)] ++ getList xs c
	| otherwise = []

-- rem_mark -> remove the markers from the string
rm_mark :: String -> String
rm_mark [] = []
rm_mark (x:xs) = strip xs


-- regex -> use a regular expression to parse input
regex :: String -> Maybe (String, String, String, [String])
regex [] = Nothing
regex x = matchRegexAll {-
	-}(mkRegexWithOpts "(~[^|>]+)+([|][^~>]+)*(>[^~|]+)*" False False) x

--jsonize -> convert tuple to json (question, options and answers are keys)
jsonize :: (String, [String], [String]) -> String
jsonize (q,o,a) = "{ " ++ "\"question\": " ++ show q ++ ", \"options\": " ++{-
					-} show o ++ ",\"answers\": " ++ show a ++ " }"
{-	Regular Expression: 
	(~[^|>]+)+ 		accept one or more "~"s with no "|" or ">"
	([|][^~>]+)*	followed by zero or more "|"s with no "~" or ">"
	(>[^~|]+)*		followed by zero or more ">"" with no "~" or "|"
-}

-- ["The", "The quick", "The quick brown", ...]
concats = scanl1 (\s v -> s ++ " " ++ v)

-- takes list of words, returns list of lines
wordwrap :: Int -> [String] -> [String]
wordwrap maxwidth [] = []
wordwrap maxwidth ws = sentence : (wordwrap maxwidth restwords)
    where
        zipped = zip (concats ws) ws
        (sentences, rest) = span (\(s,w) -> (length s) <= maxwidth) zipped
        sentence = last (map fst sentences)
        restwords = map snd rest

spacer:: (String, [String], [String]) -> (String, [String], [String])
spacer (q, o, a) = (fs q, (map fs o), (map fs  a))
	where
		fs = (intercalate "\n") . (wordwrap 85) . words



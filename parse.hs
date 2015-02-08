{-
	~ question
	| front question options
	> answer
	> multiple answers
-}
import System.Environment


main = do
   args <- getArgs
   content <- readFile (args !! 0)
   -- convert lines of File to Text type for easy management
   let linesOfFiles = lines content
   -- grab relevant lines from removed beginning whitespace lines
   let imp_lines = filter line_check (map strip linesOfFiles)
   
   -- write the important lines to a file
   writeFile (args !! 1) (unlines imp_lines)
  
line_check :: String -> Bool
line_check [] = False
line_check (x:xs)
	| x == '~' = True
	| x == '>' = True
	| x == '|' = True
	| otherwise = False

strip :: String -> String
strip [] = []
strip "\n" = []
strip (x:xs)
	| x == ' ' = strip xs
	| x == '\t' = strip xs
	| otherwise = (x:xs)
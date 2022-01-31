import System.Environment 
import System.IO

data Node =
    Node {  type :: String,
            name :: String,
            contents :: [Node] }

isDirectory :: String -> Bool
isDirectory "" = False
isDirectory cs = last cs == '/'

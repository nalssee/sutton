module Main where

import Helper(add)

main :: IO ()
main = do
    putStrLn "Hello, Haskell!"
    print $ add 3 4



-- foo :: Num a => a -> a 
-- foo x = x + 3
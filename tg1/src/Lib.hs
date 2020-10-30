module Lib where

import Control.Monad
import System.Random

names = [
    (1, "Johannes"),
    (2, "Helena"),
    (4, "Antero"),
    (8, "Anneli"),
    (16, "Kalevi"),
    (32, "Marjatta"),
    (64, "Matti"),
    (128, "Liisa"),
    (256, "Ilmari"),
    (-1, "Juhani"),
    (-2, "Marja"),
    (-4, "Olavi"),
    (-8, "Johanna"),
    (-16, "Tapani"),
    (-32, "Kaarina"),
    (-64, "Tapio"),
    (-128, "Anna"),
    (-256, "Mikael")]

type Actor = Int
data StoryTree = StoryNode StoryAction [StoryTree] | StoryLeaf StoryAction deriving Show
data StoryAction =
    Harm Actor Actor |
    Help Actor Actor |
    Hate Actor Actor |
    Love Actor Actor
    deriving Show

deepenTree :: StoryTree -> IO StoryTree
deepenTree (StoryNode x cs) = StoryNode x <$> (mapM deepenTree cs)
deepenTree (StoryLeaf x) = do xs <- deepenStory x
                              return . StoryNode x $ map StoryLeaf xs

deepenStory :: StoryAction -> IO [StoryAction]
deepenStory (Harm a b) = choose [[Love c b, Harm a c, Hate b a],
                                 [Help a d, Harm d b, Hate b d]]
    where c = newActorAgainst a [b]
          d = newActorFor a [b]
deepenStory (Help a b) = return [Help a c, Help c b, Love b a] where c = newActorFor b [a]
deepenStory (Hate a b) = return [Harm a b]
deepenStory (Love a b) = return [Help a b]

newActorAgainst i as = -2*i * sum as
newActorFor i as = 2*i * sum as

printTree :: String -> StoryTree -> IO ()
printTree indent (StoryNode x cs) = do putStrLn $ indent ++ showStory x
                                       forM_ cs (printTree $ "  " ++ indent)
printTree indent (StoryLeaf x) = putStrLn $ indent ++ showStory x

showStory :: StoryAction -> String
showStory (Help a b) = (showActor a) ++ " auttaa " ++ (showActor b) ++ ":ta"
showStory (Harm a b) = (showActor a) ++ " kiusaa " ++ (showActor b) ++ ":ta"
showStory (Hate a b) = (showActor a) ++ " vihaa " ++ (showActor b) ++ ":ta"
showStory (Love a b) = (showActor a) ++ " rakastaa " ++ (showActor b) ++ ":ta"

showActor :: Int -> String
showActor i = case lookup i names of
                Just a -> a
                Nothing -> "Tuntematon"

choose :: [a] -> IO a
choose as = do n <- getStdRandom (randomR (1,length as))
               return $ as !! (n - 1)
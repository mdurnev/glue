module SampleModule where

fibonacci :: Int -> Int
fibonacci n = fibs !! n
    where fibs = 0 : 1 : zipWith (+) fibs (tail fibs)

func_div :: Int -> Int -> Double 
func_div x y = fromIntegral x / fromIntegral y

func_zero :: Int
func_zero = 0

func_foo :: Int -> Float -> Double
func_foo x y = realToFrac (fromIntegral x + y)

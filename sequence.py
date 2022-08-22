import numpy as np
from PIL import Image

SIZE = 10

c = {0: (0, 0, 0),       #blank
	 1: (255, 175, 0),   #blue
	 2: (100, 255, 0),   #green
	 3: (255, 255, 255)} #white, free space

board = {}
for y in range(SIZE):
	for x in range(SIZE):
		if x == 0 and y == 0:
			board[(x+1, y+1)] = 3
		elif x == 9 and y == 0:
			board[(x+1, y+1)] = 3
		elif x == 0 and y == 9:
			board[(x+1, y+1)] = 3
		elif x == 9 and y == 9:
			board[(x+1, y+1)] = 3
		else: 	
			board[(x+1, y+1)] = 0 
			
print(board)
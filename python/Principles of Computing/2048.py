"""
Clone of 2048 game.
"""

#import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
		   DOWN: (-1, 0),
		   LEFT: (0, 1),
		   RIGHT: (0, -1)}

NUL_VAL = 0

def right_zeros(line):
	"""
	Move all non-zero values to the front and append zeroes to the end
	"""
	list_zero = [_ for _ in line if _ == 0 ]
	list_copy = [_ for _ in line if _ > 0 ]
	list_copy.extend(list_zero)
	return list_copy
	
def merge(line):
	"""
	Function that merges a single row or column in 2048.
	"""
	tmp_list = []
	working_list = right_zeros(line[:])
	for index, item in enumerate(working_list):
		if index < len(working_list)-1: #in the list and not at the end of the list
			if item == working_list[index + 1]:
				tmp_list.append(item * 2)
				working_list[index+1]=0 # append matched * 2 and change next item to 0
			else:
				tmp_list.append(item) # append nonzero non matched
		else: 
			tmp_list.append(item) # append last item
			
	return right_zeros(tmp_list)

class TwentyFortyEight:
	"""
	Class to run the game logic.
	"""

	def __init__(self, grid_height, grid_width):
		# replace with your code
		self.height = grid_height
		self.width = grid_width
		self.game_board = [[]]
		self.reset()

	def reset(self):
		"""
		Reset the game so the grid is empty except for two
		initial tiles.
		"""
		self.game_board = [ [ NUL_VAL for dummy_col in range(self.width) ] for dummy_row in range(self.height) ]
		for tile in range(0,2):
			self.new_tile()


	def __str__(self):
		"""
		Return a string representation of the grid for debugging.
		"""
		# replace with your code
		board_str = "Game table:\n==========\n"
		for row in self.game_board:
				board_str = board_str +  str(row) + "\n"
		return board_str

	def get_grid_height(self):
		"""
		Get the height of the board.
		"""
		# replace with your code
		return self.height
		
	
	def get_grid_width(self):
		"""
		Get the width of the board.
		"""
		# replace with your code
		return self.width
		

	def move(self, direction):
		"""
		Move all tiles in the given direction and add
		a new tile if any tiles moved.
		"""
		# replace with your code
		pass

	def new_tile(self):
		"""
		Create a new tile in a randomly selected empty
		square.  The tile should be 2 90% of the time and
		4 10% of the time.
		"""
		# replace with your code
		row_coord = random.randint(0, self.height - 1 )
		col_coord = random.randint(0, self.width - 1)

		while self.game_board[row_coord][col_coord] != NUL_VAL:
			self.new_tile

		self.game_board[row_coord][col_coord] = 2 if random.random() < 0.9 else 4

	def set_tile(self, row, col, value):
		"""
		Set the tile at position row, col to have the given value.
		"""
		# replace with your code
		self.game_board[row][col] = value


	def get_tile(self, row, col):
		"""
		Return the value of the tile at position row, col.
		"""
		# replace with your code
		return self.game_board[row][col]


game = TwentyFortyEight(4,4)
print game
#poc_2048_gui.run_gui(TwentyFortyEight(4, 4))

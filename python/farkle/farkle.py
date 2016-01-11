import random, sys
import operator

def interpreter(command):
	pass

def score(dice_roll):
	"""
		4 of a kind: 3 of a kind * 2
		3 of a kind: 100 * face value
		3 1's: 1,000
		1: 100
		5: 50
	"""
	score = 0
	dice_set = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
	for key in dice_set:
		dice_set[key] = dice_roll.count(key)
	max_roll = max(dice_set, key=lambda i:dice_set[i])
	if dice_set[max_roll] == 3:
		if max_roll == 1:
			 score = 1000
		else:
			score = max_roll * 100
	elif dice_set[max_roll] == 4:
		score = max_roll * 200
	elif dice_set[max_roll] == 2 and max_roll == 5:
		score = 100
	elif dice_set[max_roll] == 1 and max_roll == 5:
		score = 50

	print (dice_set)
	print (score)
	
	return None
		
def dice_roll(sides = 6):
	the_roll = [None] * my_game.num_dice
	for i in range(sides):
		the_roll[i] = random.randint(1,sides)
	print (the_roll)
	return score(the_roll)	
			
class Game(object):
	def __init__(self, num_dice = 4):
		self.play_to = 10000
		self.started = False
		self.turns = 0
		self.num_dice = num_dice
		self.in_play = False
		self.num_players = -1
		self.players = []
	
	def setup(self):
		print ("Let's set up the game...")

		while self.num_players < 0 or self.num_players > 6:
			try:
				self.num_players = int(input("Number of players [1-6]: "))
			except ValueError:
				self.num_players = -1
		
		self.players = [None] * self.num_players

		for i in range(0, self.num_players):
			self.players[i] = Player(input("Enter a name of player %i: "% (i+1)))
			#self.players.append()
						
		self.in_play = True
		return True
			
	def play(self):
		command = ""
		player_up = ""
		turn = 1
		
		if self.started != True:
			self.setup()
		while command != "exit":
			player_up = self.players[turn % self.num_players]
			command = input("%s : "% (player_up.name))
			if command == "roll": print (dice_roll())
			turn += 1

				
class Player(object):
	def __init__(self, name="Player"):
		self.name = name
		self.score = 0
		self.on_board = False
		self.has_roll = False
		
my_game = Game(6)
my_game.play()
		
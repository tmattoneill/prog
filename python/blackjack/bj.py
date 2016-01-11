# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

FIRST_CARD_X = 80
HOLE_CARD_POS = (FIRST_CARD_X + (CARD_SIZE[0]/2), 184)

TITLE_CHAR_SIZE = 36
MESSAGE_CHAR_SIZE = 24
SCORE_CHAR_SIZE = 24
OUTCOME_CHAR_SIZE = 24
PLAYER_CHAR_SIZE = 18
FONT_WIDTH_FACTOR = 3.2
NAME = "Blackjack"

# initialize some useful global variables
in_play = False
outcome = ""
message = ""
score = [0, 0]
dealer = []
player = []
deck = []

# define globals for cards
SUITS = ('C', 'S', 'H', 'D') #clubs spades hearts diamonds
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
		def __init__(self, suit, rank):
				if (suit in SUITS) and (rank in RANKS):
						self.suit = suit
						self.rank = rank
				else:
						self.suit = None
						self.rank = None
						outcome = "Invalid card: ", suit, rank

		def __str__(self):
				return self.suit + self.rank

		def get_suit(self):
				return self.suit

		def get_rank(self):
				return self.rank

		def draw(self, canvas, pos):
				card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
										CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
				canvas.draw_image(card_images, 
													card_loc, 
													CARD_SIZE, 
													[pos[0] + CARD_CENTER[0], 
													 pos[1] + CARD_CENTER[1]], 
													CARD_SIZE)
				
# define hand class
class Hand:
		def __init__(self):
				self.hand = []
				
		def __str__(self):
				cards = ""
				for card in self.hand:
						cards += str(card) + " "
				return cards

		def add_card(self, card):
				self.hand.append(card)
				return card

		def get_value(self):
				value = 0

				for c in self.hand:
						value += VALUES[c.get_rank()]

				for c in self.hand:
						if c.get_rank() == "A" and value <= 11:
								value += 10
				return value
	 
		def draw(self, canvas, pos):
				p = pos
				
				if in_play:
						canvas.draw_image(card_back, 
															CARD_BACK_CENTER, 
															CARD_BACK_SIZE, 
															HOLE_CARD_POS, 
															CARD_BACK_SIZE)
						
				for c in self.hand:
						c.draw(canvas, p)
						p[0] = p[0] + 45
	 

				
# define deck class 
# Student should insert code for Deck class here
class Deck:
		def __init__(self):
				bottom_card = []
				self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS] 
				self.shuffle
				
		def shuffle(self):
				# shuffle the deck 
				random.shuffle(self.cards)

		def deal_card(self):
				bottom_card = self.cards.pop()
				return bottom_card
						
		def __str__(self):
				s = ''
				for c in self.cards:
						s += str(c) + " "
						
				return s


#define event handlers for buttons
def deal():
		global outcome, in_play, deck, player, dealer, score, message

		deck = Deck()
		player = Hand()
		dealer = Hand()
		deck.shuffle()  
		
		if in_play:
				outcome = "Player loses."
				score[1] += 1 
		else:
				in_play = True
				message = "Hit or stand?"
		
		player.add_card(deck.deal_card())
		dealer.add_card(deck.deal_card())
		player.add_card(deck.deal_card())
		dealer.add_card(deck.deal_card())        

		if player.get_value() == 21:
				outcome = "Player wins!"
				message = "Deal again?"
				score[0] += 1
				in_play = False
		elif dealer.get_value() == 21:
				outcome = "Dealer wins!"
				message = "Deal again?"
				score[1] += 1
				in_play = False
		else:
				outcome = "Player hand value: " + str(player.get_value())
				in_play = True
						
def hit():
		global outcome, score, in_play, message
		message = ""
		
		if in_play:
				c = player.add_card(deck.deal_card())
				
				if player.get_value() > 21:
						outcome = "Player busts with " + str(player.get_value())
						message = "Deal again?"
						in_play = False
						score[1] += 1
				elif player.get_value() == 21:
						outcome = "Player wins with " + str(player.get_value())
						message = "Deal again?"
						score[0] += 1       
						in_play = False
				else:
						outcome = "Player hand value: " + str(player.get_value())
						message = "Hit or stand?"

		else:
				message = "No game in play. Deal again."
				outcome = ""

#Player is done       
def stand():
		global player, dealer, in_play, score, outcome, message
		
		if in_play:
				while dealer.get_value() < 17:
						dealer.add_card(deck.deal_card())
						
				if dealer.get_value() > 21:
						outcome = "Dealer busts with a " + str(dealer.get_value())
						score[0] += 1
						
				elif dealer.get_value() >= player.get_value():
						outcome = "Dealer wins with a " + str(dealer.get_value())  
						score[1] += 1
						
				else:
						outcome = "Player wins with a " + str(player.get_value())
						score[0] += 1
				message = "Deal again?"
				in_play = False
		else:
				outcome = ""
				message = "No game in play. Deal again."        

def text_center(num_chars, char_size, factor_w, container_w):  
		return (container_w / 2) - (num_chars * ((char_size / factor_w) / 2))

# draw handler    
def draw(canvas):
		canvas.draw_text(message, [text_center(len(message), 
																					 MESSAGE_CHAR_SIZE, 
																					 FONT_WIDTH_FACTOR, 
																					 600), 65], MESSAGE_CHAR_SIZE, "White")
		
		canvas.draw_text("Dealer", [80, 130], 18, "White")
		dealer.draw(canvas, [80,135])
		canvas.draw_text("Player", [80, 320], 18, "White")
		player.draw(canvas, [80,325])
		
		canvas.draw_text("Player : " + str(score[0]), [80,520], 36, "Black")
		canvas.draw_text("Dealer : " + str(score[1]), [250, 520], 36, "Black")
		canvas.draw_text(outcome, [80, 560], 36, "Black")
		canvas.draw_text(NAME, [text_center(len(NAME),
																				TITLE_CHAR_SIZE,
																				FONT_WIDTH_FACTOR,
																				600),36], TITLE_CHAR_SIZE, "Black")
		
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
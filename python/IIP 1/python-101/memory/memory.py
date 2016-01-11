# implementation of card game - Memory

import simplegui
import random

NUM_CARDS = 16 #How many cards total do you want?
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 100
CHAR_SIZE = 36

# helper function to initialize globals
def new_game():
    """
        Initialise all the lists, messages, and flags
    """
    global deck, exposed #set up the lists
    global state, index_c1, index_c2 #set up the flags
    global turns, game_message #global messaging variables

    cards1 = range(NUM_CARDS / 2)
    cards2 = cards1
    deck = list(cards1 + cards2)
    random.shuffle(deck)

    exposed = [False for i in range(0, NUM_CARDS)]

    state = 0
    
    index_c1 = 0
    index_c2 = 0
 
    turns = 0
    game_message = ""
    
# define event handlers
def mouseclick(pos):
    global state, deck, index_c1, index_c2, turns, game_message
    """
        Game logic: If new game, expose a card. If one card exposed, reveal second card.
        If two cards are exposed either leave them exposed if they match or flip them 
        both back over and leave exposed the latest clicked card.
    """
    card_index = pos[0] / (CANVAS_WIDTH / NUM_CARDS)

    if not exposed[card_index]:
        if state == 0:
            index_c1 = card_index
            exposed[index_c1] = True        
            game_message = ""
            state = 1

        elif state == 1:
            index_c2 = card_index
            exposed[index_c2] = True
            turns += 1
            game_message = ""
            state = 2

        else:   
            if deck[index_c1] != deck[index_c2]:
                exposed[index_c1] = False
                exposed[index_c2] = False
                game_message = "No match!"
            else:
                game_message = "Match!"

            index_c1 = card_index
            exposed[index_c1] = True        

            state = 1
        if not (False in exposed):
            game_message = "You win!"
           
    else:
        game_message = "Invalid move.\nTry Again."
                  
# cards are logically 50x100 pixels in size    
def draw(canvas):
    
    y_loc = ((CANVAS_HEIGHT - CHAR_SIZE) / 2) + (CHAR_SIZE)
    x_loc = 10
    indent = 0    
    h_space = CANVAS_WIDTH / NUM_CARDS
    
    for card in deck:
        canvas.draw_text(str(card), (x_loc, y_loc), CHAR_SIZE, "Green")
        x_loc = x_loc + h_space    
        
    for visible in exposed:
        canvas.draw_polygon([(indent, 0), (indent + h_space, 0), 
                             (indent + h_space, CANVAS_HEIGHT), 
                             (indent, CANVAS_HEIGHT)], 1, "White", "Green") if not visible else None
        indent = indent + h_space

    label_turns.set_text("Turns: %s"%str(turns))
    label_msg.set_text(game_message)
    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_canvas_background('White')
frame.add_button("Reset", new_game)
label_turns = frame.add_label("")
label_msg = frame.add_label("")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
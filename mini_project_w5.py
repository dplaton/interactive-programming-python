# implementation of card game - Memory

import simpleguitk as simplegui
import random

# constants
# Canvas dimensions
WIDTH = 800
HEIGHT = 100
# Card dimensions
CARD_W = 50
CARD_H = HEIGHT
# game states
NO_CARDS_EXPOSED = 0
ONE_CARD_EXPOSED = 1
TWO_CARDS_EXPOSED = 2

# our deck of cards
deck = []
exposed_cards = []
game_state = NO_CARDS_EXPOSED
last_exposed_cards = []
turns = 0

# helper function to initialize globals
def new_game():
    global deck, exposed_cards, turns
    turns = 0
    deck = list(range(8))
    deck.extend(list(range(8)))
    random.shuffle(deck)
    exposed_cards = [False for card in deck]
     
# define event handlers
def mouseclick(pos):
    global last_exposed_cards, game_state, turns
    # add game state logic here
    # detect where we clicked
    clicked_index = pos[0] / 50

    # ignore if we clicked on an exposed card
    if (exposed_cards[clicked_index]):
        return

    exposed_cards[clicked_index] = True

    # switch the game state appropriately
    if (game_state == NO_CARDS_EXPOSED):
        last_exposed_cards.append(clicked_index);

        game_state = ONE_CARD_EXPOSED
    elif (game_state == ONE_CARD_EXPOSED):
        last_exposed_cards.append(clicked_index);
        turns +=1

        game_state = TWO_CARDS_EXPOSED
    else:
        if (deck[last_exposed_cards[0]] != deck[last_exposed_cards[1]]):
            exposed_cards[last_exposed_cards[0]] = exposed_cards[last_exposed_cards[1]] = False   
        last_exposed_cards = []
        last_exposed_cards.append(clicked_index)

        game_state = ONE_CARD_EXPOSED

# cards are logically 50x100 pixels in size    
def draw(canvas):
    # draw the cards on the screen
    for idx in range(len(deck)):
        x = CARD_W * idx
        canvas.draw_text(str(deck[idx]),(x + 15, HEIGHT-50), 30, "White")
        canvas.draw_line((x,0), (x, HEIGHT), 2, "#FFAAAA")
        # draw the "cover" of the card
        if (not exposed_cards[idx]):
            canvas.draw_polygon([[x,0], [CARD_W + x, 0], [CARD_W + x, HEIGHT], [x, HEIGHT]], 1, "Green","Green")

    label.set_text("Turns = " + str(turns)) 

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", WIDTH, HEIGHT)
frame.add_button("  Restart  ", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
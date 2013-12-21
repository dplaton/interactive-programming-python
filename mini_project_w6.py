# Mini-project #6 - Blackjack

import simpleguitk as simplegui
import random

# canvas size
CANVAS_H = 600
CANVAS_W = 600

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
player_hand = None
dealer_hand = None

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
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
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):       
        hand_string = ""
        for card in self.cards:
            hand_string = hand_string + " " + str(card)
        return "Cards in hand:" + hand_string

    def add_card(self, card):
       self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value=0
        got_ace=False
        for card in self.cards:
            value += VALUES[card.get_rank()]
            if (card.get_rank() == 'A'):
                got_ace = True
                
        if (got_ace and value + 10 <= 21):
            value += 10
        
        return value
    
    
    def draw(self, canvas, pos):
        # iterate through cards in hand, draw each one:
        # allow a space between cards:
        SPACER = 20
        for card in self.cards:
            card.draw(canvas,pos)
            pos[0] += CARD_SIZE[0] + SPACER
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.cards=[]
        # build the deck
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit,rank))

    def shuffle(self):
       # shuffle the deck
       random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop(0)
    
    def __str__(self):
        deck_str = ""
        for card in self.cards:
            deck_str += str(card) + " "
        return "Deck contains: " + deck_str


# helper functions
def player_wins():
    global score, outcome, in_play
    score += 1
    outcome = "You win!"
    in_play = False
    
def player_loses():
    global score, outcome, in_play
    score -= 1
    outcome = "You lost!"
    in_play = False
    
#define event handlers for buttons
def deal():
    global outcome, in_play, player_hand, dealer_hand, deck

    if in_play:
        player_loses()
        return
    
    # create the deck and shuffle it
    deck = Deck()
    deck.shuffle()
    
    # create the player's hand
    player_hand = Hand()
    
    # create the dealer's hand
    dealer_hand = Hand()
    
    # deal cards, alternately:
    for i in [0,1]:
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
    
    in_play = True
    outcome = ""

def hit():
    global in_play, score, outcome
    # deal the player one card
    if in_play:
        player_hand.add_card(deck.deal_card())
    # if busted, assign a message to outcome, update in_play and score
    if player_hand.get_value() > 21:
        player_loses()
       
def stand():
    global in_play, score, outcome
    
    if not in_play:
        return
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    while dealer_hand.get_value() <= 17:
        dealer_hand.add_card(deck.deal_card())
    
    if (dealer_hand.get_value() > 21) or (player_hand.get_value() > dealer_hand.get_value()):
        player_wins()
    elif (player_hand.get_value() <= dealer_hand.get_value()):
        player_loses()

# draw handler    
def draw(canvas):
    
    # draw the layout of the board: title, score etc.
    canvas.draw_text("Blackjack", (60, 60 ),36,"#FFAAAA","monospace")
    canvas.draw_text("Score:",(450, 60), 24,"#FFAAAA","monospace")
    canvas.draw_text(str(score),(550,60), 24,"#FFAAAA","monospace")
    if outcome != "":
        canvas.draw_text(outcome, (230, 330), 36,"#FF4444","monospace") 
        canvas.draw_text("New deal?", (240,370), 30, "#FFAAAA","monospace") 
    else:
        canvas.draw_text("Hit or stand?", (230, 330), 24,"#FFAAAA","monospace")   
               
    player_hand.draw(canvas, [60,400])
    dealer_hand.draw(canvas, [60,150])
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [60+CARD_CENTER[0], 150+CARD_CENTER[1]], CARD_BACK_SIZE)
    
        
# initialization frame
frame = simplegui.create_frame("Blackjack", CANVAS_H, CANVAS_W)
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
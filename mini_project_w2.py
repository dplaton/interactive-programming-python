# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import random
import simpleguitk as simplegui
import math


# initialize global variables used in your code
# the generated random number
random_number=0

# the high end of the range
high = 100

# the tries counter
tries = 0

# helper function to start and restart the game
def new_game():
    """ Initializes a new game: computes the number or retries based on the high value and resets the UI """

    global random_number
    random_number = random.randint(0,high)
    label.set_text("Enter a number between 0 and " + str(high) + ":")
    label_retries.set_text("")
    compute_tries() 
    print "Range is now 0 -", high  
    
def compute_tries():
    """ Compute the number of retries based on the high value """
    global tries
    # we ignore the low value in the formula below because low = 0
    tries = math.ceil(math.log(high + 1) / math.log(2))

# define event handlers for control panel
def range100():
    """ Sets the high value to 100 and starts a new game """
    global high
    high = 100 
    new_game()

def range1000():
    """ Sets the high value to 10000 and starts a new game """
    global high
    high = 1000
    new_game()

def input_guess(guess):
    """ 
        Checks the value entered by the user against the randomly generated number.
        If the user guessed the number or there are no more retries left it starts a new game using the same range.
    """
    global tries
    
    # We should check the input here in case we didn't receive a number
    guess_no = int(guess)
    print "Your input is ", guess_no
    if (guess_no < random_number):
        print "Higher!"
        tries = tries - 1
    elif (guess_no > random_number):
        print "Lower!"
        tries = tries - 1
    else: 
        print "Hey, you guessed! Congratulations!"
        print "------------"        
        new_game()
    
    if (tries == 0):
        print "Sorry, you didn't guess. The number was " + str(random_number) + ". Better luck next time!"    
        print "------------"
        new_game()
    else:
        print "You have " + str(int(tries)) + " retries left."
        
    # print an empty line between retries
    print ""
    # reset the input field value
    number_input.set_text("")
    label_retries.set_text("You have " + str(int(tries)) + " retries left.")

# create frame
frame = simplegui.create_frame("Guess the number",320,240);

# register event handlers for control elements
range_100 = frame.add_button("New game (range 0 - 100)", range100)
range_1000 = frame.add_button("New game (range 0 - 1000)", range1000)

# create an empty label, text will be set in new_game()
label = frame.add_label("")
number_input = frame.add_input("",input_guess,80)
label_retries = frame.add_label("")

# call new_game and start frame
new_game()
frame.start()
# always remember to check your completed program against the grading rubric

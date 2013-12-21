# 
# Mini project week 1:
# Rock-paper-scissors-lizzard-spock
#
# Author: Daniel Platon <dplaton@gmail.com>
#

# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

import random

def number_to_name(number):   
    """
    Returns the name corresponding to a number
    """
    retValue = ''

    if (number == 0):
        retValue = 'rock'
    elif (number == 1):
        retValue = 'Spock'
    elif (number == 2):
        retValue = 'paper'
    elif (number == 3):
        retValue = 'lizzard'
    elif (number == 4):
        retValue = 'scissors'
    else:
        print 'No name corresponding to number', number

    return retValue
  
def name_to_number(name):
    """ 
        Returns the number corresponding to a certain choice
    """
    retValue = -1;

    if (name == 'rock'):
        retValue = 0
    elif (name == 'Spock'):
        retValue = 1
    elif (name == 'paper'):
        retValue = 2
    elif (name == 'lizzard'):
        retValue = 3
    elif (name == 'scissors'):
        retValue = 4
    else:
        print 'No number corresponding to name', name
    return retValue

def rpsls(name): 
    """
    The main function of the program
    """
    # convert the name to the corresponding number
    player_number = name_to_number(name)
    print 'Player chooses', name

    # choose a random number between 0 and 4
    computer_number = random.randrange(0,4)
    print 'Computer choses', number_to_name(computer_number)

    # determine winner
    diff = (computer_number - player_number) % 5

    if (diff == 0):
        print 'Player and computer ties!'
    elif (diff <= 2):
        print 'Computer wins!'
    else:
        print 'Player wins!'

    
# test your code
rpsls("rock")
print '--------'
rpsls("Spock")
print '--------'
rpsls("paper")
print '--------'
rpsls("lizard")
print '--------'
rpsls("scissors")

# always remember to check your completed program against the grading rubric



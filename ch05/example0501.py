# Blackjack, Monte Carlo

# Constants 
STICK = 1
HIT = 0


def generate_episode():

    state = init_blackjack()

    while not finished(state):
        
        next_state()


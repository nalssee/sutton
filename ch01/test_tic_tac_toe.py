import random

import pytest

from .tic_tac_toe import TicTacToe

# Initial values are important.
# Need to decide the number of trainings
# sometimes it trains poorly

@pytest.fixture
def ttt_game_history1():
    # player1: random
    ttt = TicTacToe(epsilon1=0.01, epsilon2=0.01) 
    history_book = []
    for i in range(40_000):
        ttt.train1()

    print(ttt.wincount['player1'], ttt.wincount['player2'], ttt.wincount['draw'])    

    for _ in range(5):   
        ttt.play(2)
    
    
     
    return history_book

def test_simple(ttt_game_history1):
    pass
    
    

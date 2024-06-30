from random import choice, random


def place_stone(board, pos, stone_type):
    pass

def gen_candidates(board):
    pass 

def update_valfn(valfn, board, val):
    pass 
    
def onestep(player, env):
    board = env.board
    # o / x 
    stone_type = player.stone_type
    # dict
    candidates = gen_candidates(board)
    valfn = player.valfn
    pos_vals = [(pos, valfn[place_stone(board, pos, stone_type)]) for pos in candidates]
    
    epsilon = player.epsilon 
    is_epsilon = False if random() > epsilon else True
    
    if random() < epsilon:
        pos = choice(candidates)
        env.board = place_stone(board, pos, stone_type)
    
    else:
        (mpos, mval) = max(pos_vals, key=lambda x: x[1])
        # update_valfn could be a method for the player
        update_valfn(valfn, board, mval)
        env.board = place_stone(board, mpos, stone_type)        
        


def tran(player, env, n=100):
    def train1(player, env):
        board = env.board
        # env starts first 
        switch = True
        while not is_done(board):
            if switch:
                onestep(env.player, env)
                switch = tick_switch(switch)
            else:
                onestep(player, env)
                switch = tick_switch(switch)
        
    for i in range(n):
        train1(player, env)

def is_done(board):
    pass 

def tick_switch(switch):
    return False if switch else True

def play(player, env):
    pass
        
        
class Player:
    def __init__(self, stone_type, epsilon=0.1):
        self.epsilon = epsilon
        self.stone_type = stone_type 
        self.valfn = gen_init_valfn(stone_type)

class Env:
    def __init__(self):
        self.board = gen_board() 
#%%
from random import choice, random


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def all_same(items):
    return all(x == items[0] for x in items)
#%%
class TicTacToe:
    def __init__(self, epsilon1=0.01, epsilon2=0.01):
        self._empty_mark = "."
        self._board_data = list(self._empty_mark * 9)

        self._winval = 1
        self._loseval = 0
        self._default_val = 0.5        

        self._epsilon1 = epsilon1
        self._epsilon2 = epsilon2  
        self._mark1 = 'O'
        self._mark2 = 'X'
        self._alpha1 = 0.5
        self._alpha2 = 0.5
        self._valfn1 = {} 
        self._valfn2 = {}
        self._player1 = (self._valfn1, self._epsilon1, self._alpha1, self._mark1)
        self._player2 = (self._valfn2, self._epsilon2, self._alpha2, self._mark2)
    
    def play(self, human=2):
        """Play against the computer

        Args:
            human (int, optional): Human player. 
                Defaults to 2 (which means you play the second)
        """
        
        self.init_board()
         
        print("""              
            Tic-Tac-Toe board position starts from 1 to 9
            1 2 3
            4 5 6 
            7 8 9
        """)

        computer = self._player1 if human == 2 else self._player2
        
        if human == 2:
            self._step(computer)
            self.show() 
        
        while not self.finished():
            # human player
            pos = self._prompt()
            self._place(pos, self._mark2 if human == 2 else self._mark1)
            self.show()
            
            # computer player 
            self._step(computer)
            self.show() 
        self.announce_the_result()

    def _prompt(self):
        empty_positions = self._empty_positions() 

        while True:
            pos = int(input("Input the position: "))
            if pos in empty_positions:
                return pos
            print("Only the empty positions, again")
            
    def announce_the_result(self):
        flag = self.finished()         
        if flag == True:
            print("Game Draw")
        else:
            print(f"Player {flag} won!!")

    def show(self):
        print()
        for line in chunks(self._board_data, 3):
            print(" ".join(line))

    def finished(self, board=None):
        """Returns 
        self.mark1: player1 win, 
        self.mark2: player2 wins, 
        True: finished with a draw
        False: not finished yet
        """
        if not board:
            board = ''.join(self._board_data)
            
        lines = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            [1, 4, 7],
            [2, 5, 8],
            [3, 6, 9],
            [1, 5, 9],
            [3, 5, 7]
        ]
 
        for line in lines:
            if all(board[pos - 1] == self._mark1 for pos in line):
                return self._mark1
            elif all(board[pos - 1] == self._mark2 for pos in line):
                return self._mark2

        # check draw 
        empty_positions = self._empty_positions()
        if not empty_positions:
            return True  
        return False      

    def _place(self, pos, mark):
        self._board_data[pos - 1] = mark
        
    def _next_board(self, pos, mark):
        "Returns a board(str) with an additional mark on the position"
        board = list(self._board_data) 
        board[pos - 1] = mark
        return "".join(board)
    
    def _empty_positions(self):
        return [pos 
            for pos, mark in enumerate(self._board_data, 1) 
            if mark == self._empty_mark]

    def _step(self, player):
        valfn, epsilon, alpha, mark = player

        positions = self._empty_positions()
        pos_vals = []
        for pos in positions:
            next_board = self._next_board(pos, mark)
            fin = self.finished(next_board)
            if not fin:
                pos_vals.append((pos, valfn.get(next_board, self._default_val)))
            elif fin == mark:
                pos_vals.append((pos, self._winval))
            else:
                # draw is considered a lost
                pos_vals.append((pos, self._loseval))
        if random() < epsilon:
            pos = choice(positions)
            self._place(pos, mark)
        else:
            mval = max(val for _, val in pos_vals) 
            # one of the maxval moves
            (mpos, mval) =  choice([(p, v) for p, v in pos_vals if v == mval])
            # update_valfn could be a method for the player
            self._update_valfn(valfn, alpha, mval)
            self._place(mpos, mark)

    def _update_valfn(self, valfn, alpha, val):
        current_board = "".join(self._board_data)
        vt = valfn.get(current_board, self._default_val) 
        valfn[current_board] = vt + alpha * (val - vt)
    
    def init_board(self):
        self._board_data = list(self._empty_mark * 9) 
        
    def train(self, n=100):
        for i in range(n):
            self._train1()
            self.init_board()     
   
    def _train1(self):
        turn = 1 
        while not self.finished():
            if turn == 1:
                self._step(self._player1)
            else:
                self._step(self._player2)
            turn = 2 if turn == 1 else 1
          
#%%
ttt = TicTacToe()

ttt.train(1000)
ttt.play()
# %%

ttt._valfn1
# %%
ttt._valfn2
# %%
# %%

# def show(board):
#     print()
#     for line in chunks(list(board), 3):
#         print(" ".join(line))


# for k, v in ttt._valfn1.items():
#     if v > 0.8 and v < 0.9:
#         show(k)
#         print(v)
# # %%
# ttt._valfn2['.OX...O..']
# # %%

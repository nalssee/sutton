from random import choice, random

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def all_same(items):
    return all(x == items[0] for x in items)


class TicTacToe:
    def __init__(self, epsilon1=0.1, epsilon2=0.1):
        self._empty_mark = "."
        self._board_data = list(self._empty_mark * 9)

        self._winval = 1
        self._loseval = 0
        self._default_val = 0.5        

        self.player1 = {
            'epsilon': epsilon1,
            'mark': 'O',
            'alpha': 0.5,
            'valfn': {},
            'prev_board': None 
        }
        self.player2 = {
            'epsilon': epsilon2,
            'mark': 'X',
            'alpha': 0.5,
            'valfn': {},
            'prev_board': None 
        }


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

        computer = self.player1 if human == 2 else self.player2
        
        if human == 2:
            self._step(computer)
            self.show() 
        
        while not self.finished():
            # human player
            pos = self._prompt()
            self._place(pos, self.player2 if human == 2 else self.player1)
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
        self.player1['mark']: player1 win, 
        self.player2['mark']: player2 wins, 
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

        mark1, mark2 = self.player1['mark'], self.player2['mark']
        for line in lines:
            if all(board[pos - 1] == mark1 for pos in line):
                return mark1
            elif all(board[pos - 1] == mark2 for pos in line):
                return mark2

        # check draw 
        empty_positions = self._empty_positions()
        if not empty_positions:
            return True  
        return False      

    def _place(self, pos, player):
        mark = player['mark']
        self._board_data[pos - 1] = mark 
        # update previous board
        if mark == self.player1['mark']:
            self.player1['prev_board'] = "".join(self._board_data)
        else:
            self.player2['prev_board'] = "".join(self._board_data)
        
        
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
        valfn = player['valfn']
        epsilon = player['epsilon']
        alpha = player['alpha']
        mark = player['mark']
        prev_board = player['prev_board']
         
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
            self._place(pos, player)
        else:
            mval = max(val for _, val in pos_vals) 
            # one of the maxval moves
            (mpos, mval) =  choice([(p, v) for p, v in pos_vals if v == mval])
            # update_valfn could be a method for the player
            self._update_valfn(valfn, alpha, mval, prev_board)
            self._place(mpos, player)

    def _update_valfn(self, valfn, alpha, val, prev_board):
        vt = valfn.get(prev_board, self._default_val)
        valfn[prev_board] = vt + alpha * (val - vt)
        if prev_board:
        show(prev_board)
        print(vt, vt + alpha * (val - vt))

    
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
                self._step(self.player1)
            else:
                self._step(self.player2)
            turn = 2 if turn == 1 else 1
 
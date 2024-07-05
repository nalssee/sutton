from random import choice, random


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def all_same(items):
    return all(x == items[0] for x in items)


class TicTacToe:
    def __init__(self, epsilon1=1, epsilon2=0.1):
        self.empty_mark = "."
        self.board_data = list(self.empty_mark * 9)

        self.winval = 1
        self.loseval = 0
        self.default_val = 0.5
        self.wincount = {
            'player1': 0,
            'player2': 0,
            'draw': 0 
        }
        self.game_history = []
        self.player1 = {
            "epsilon": epsilon1,
            "mark": "O",
            "alpha": 0.5,
            "valfn": {},
            "prev_board": None,
        }
        self.player2 = {
            "epsilon": epsilon2,
            "mark": "X",
            "alpha": 0.5,
            "valfn": {},
            "prev_board": None,
        }

    def play(self, human=2):
        """Play against the computer

        Args:
            human (int, optional): Human player.
                Defaults to 2 (which means you play the second)
        """

        self.init_game()

        print(
            """              
            Tic-Tac-Toe board position starts from 1 to 9
            1 2 3
            4 5 6 
            7 8 9
        """
        )

        if human == 1:
            human_player, computer = self.player1, self.player2
        else:
            human_player, computer = self.player2, self.player1

        turn = 1
        while not self.finished():
            if human == turn:
                pos = self.prompt()
                self.place(pos, human_player)
                self.show()
            else:
                self.step(computer)
                self.show()

            turn = 2 if turn == 1 else 1

        self.announce_the_result()

    def prompt(self):
        empty_positions = self.empty_positions()

        while True:
            try:
                pos = int(input("Input the position: "))
            except ValueError:
                continue

            if pos in empty_positions:
                return pos
            print("Only the empty positions, again")

    def announce_the_result(self):
        flag = self.finished()
        if flag == True:
            print("Game Draw")
        else:
            print(f"Player {flag} won!!")

    def show(self, board=None):
        board_data = list(board) if board else self.board_data
        print()
        for line in chunks(board_data, 3):
            print(" ".join(line))

    def finished(self, board=None):
        """Returns
        self.player1['mark']: player1 win,
        self.player2['mark']: player2 wins,
        True: finished with a draw
        False: not finished yet
        """
        if not board:
            board = "".join(self.board_data)

        lines = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            [1, 4, 7],
            [2, 5, 8],
            [3, 6, 9],
            [1, 5, 9],
            [3, 5, 7],
        ]

        mark1, mark2 = self.player1["mark"], self.player2["mark"]
        for line in lines:
            if all(board[pos - 1] == mark1 for pos in line):
                return mark1
            elif all(board[pos - 1] == mark2 for pos in line):
                return mark2

        # check draw
        empty_positions = self.empty_positions()
        if not empty_positions:
            return True
        return False

    def place(self, pos, player):
        mark = player["mark"]
        if not (self.board_data[pos - 1] == self.empty_mark):
            raise ValueError

        self.board_data[pos - 1] = mark
        # update previous board
        board = "".join(self.board_data)
        if mark == self.player1["mark"]:
            self.player1["prev_board"] = board
        else:
            self.player2["prev_board"] = board
        return board

    def next_board(self, pos, mark):
        "Returns a board(str) with an additional mark on the position"
        board = list(self.board_data)
        board[pos - 1] = mark
        return "".join(board)

    def empty_positions(self):
        return [
            pos
            for pos, mark in enumerate(self.board_data, 1)
            if mark == self.empty_mark
        ]

    def step(self, player):
        valfn = player["valfn"]
        epsilon = player["epsilon"]
        alpha = player["alpha"]
        mark = player["mark"]
        prev_board = player["prev_board"]

        positions = self.empty_positions()
        pos_vals = []
        for pos in positions:
            next_board = self.next_board(pos, mark)
            fin = self.finished(next_board)
            if not fin:
                pos_vals.append((pos, valfn.get(next_board, self.default_val)))
            elif fin == mark:
                pos_vals.append((pos, self.winval))
            else:
                # draw is considered a lost
                pos_vals.append((pos, self.loseval))
        if random() < epsilon:
            pos = choice(positions)
            newboard = self.place(pos, player)
            return (newboard, None)
        else:
            mval = max(val for _, val in pos_vals)
            # one of the maxval moves
            (mpos, mval) = choice([(p, v) for p, v in pos_vals if v == mval])
            # update_valfn could be a method for the player
            newval = self.update_valfn(valfn, alpha, mval, prev_board)
            newboard = self.place(mpos, player)
            return (newboard, newval)

    def update_valfn(self, valfn, alpha, val, prev_board):
        vt = valfn.get(prev_board, self.default_val)
        newval = vt + alpha * (val - vt)
        valfn[prev_board] = newval
        return newval

    def init_game(self):
        self.board_data = list(self.empty_mark * 9)
        self.game_history = []
        self.player1["prev_board"] = None
        self.player2["prev_board"] = None

    def train1(self):
        self.init_game()
        turn = 1

        while not self.finished():
            if turn == 1:
                self.game_history.append(self.step(self.player1))
            else:
                self.game_history.append(self.step(self.player2))
            turn = 2 if turn == 1 else 1

        result = self.finished()
        if result == self.player1["mark"]:
            self.wincount['player1'] += 1
        elif result == self.player2["mark"]:
            self.wincount['player2'] += 1 
        elif result == True:
            self.wincount['draw'] += 1

        return self.game_history

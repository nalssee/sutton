# Grid world with linear systems
# 25 elements column vector(X) composes the elements of grid world values
# The following eq represents the relations among the values
# X = B + AX 

import numpy as np

GAMMA = 0.9


def is_proper_move(i, move):
    if abs(i - move) == 5:
        return 0 <= move < 25

    q1, q2 = i // 5, move // 5 
    return q1 == q2 and 0 <= move < 25    
     
def build_coeff_matrices():
    A = np.zeros((25, 25))
    B = np.zeros((25, 1))
    for i in range(25):
        if i == 1:
            A[i, 21] = 4 * GAMMA 
            B[i] = 40
        elif i == 3:
            A[i, 13] = 4 * GAMMA 
            B[i] = 20
        else:
            moves = [i + 1, i + 5, i - 1, i - 5]
            
            for move in moves:
                if is_proper_move(i, move):
                    A[i, move] += GAMMA 
                else:
                    A[i, i] += GAMMA
                    B[i] += -1
                    
    # equal probability for all direction
    return 1/4 * A, 1/4 * B

def solve():
    A, B = build_coeff_matrices()
    return np.linalg.inv(A - np.eye(25)) @ (- B)


print(solve())

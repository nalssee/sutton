from itertools import product

import numpy as np


def rent():
    V = np.zeros((21, 21))
    policy = np.zeros((21, 21))
    
    while True:
        policy_evaluation(V, policy)

        if is_policy_stable(V, policy):
            return V
        update_policy(V, policy) 


def policy_evaluation(V, policy):
    while True:
        delta = 0
        for i, j in product(range(21), range(21)):
            v = V[i, j]
            a, val = search_best_action(V, policy)
            V[i, j] = val 
            delta = max(delta, abs(V[i, j] - v))

        if delta < 0.001:
            break
        
    
def update_policy(V, policy):
    pass 

def search_best_action(V, policy):
    pass

def is_policy_stable(V, policy):
    pass



from itertools import product
import numpy as np
from scipy.stats import poisson


GAMMA = 1
REQLAMBDA1 = 3
RETLAMBDA1 = 3
REQLAMBDA2 = 4
RETLAMBDA2 = 2


def rent():
    V = np.zeros((21, 21))
    policy = np.zeros((21, 21), dtype=int)

    while True:
        policy_evaluation(V, policy)

        if not update_policy(V, policy):
            break
    return V, policy


# action: int, from location1 to location2
def policy_evaluation(V, policy):
    while True:
        delta = 0
        for i, j in product(range(21), range(21)):
            v = V[i, j]
            action = policy[i, j]

            V[i, j] = qval((i, j), action, V)
            delta = max(delta, abs(V[i, j] - v))
        if delta < 0.001:
            return V


def req_ret_prob(i0, l1, l2):
    for req in range(i0 + 1):
        p1 = poisson.pmf(req, l1)
        ret = 0
        while True:
            p2 = poisson.pmf(ret, l2)
            yield (req, ret, p1 * p2)
            if p2 < 0.0001:
                break


def update_policy(V, policy):
    "returns True if updated, False otherwise"
    for i, j in product(range(21), range(21)):
        old_action = policy[i, j]
        actions = possible_actions(i, j)
        # argmax
        best_action_value, best_action = 0, 0
        for action in actions:
            aval = qval((i, j), action, V)
            if aval > best_action_value:
                best_action_value, best_action = aval, action

        if old_action != best_action:
            policy[i, j] = best_action
            return True
    return False


def possible_actions(i, j):
    actions = []
    for a in range(-5, 6):
        if i - a >= 0 and j + a >= 0:
            actions.append(a)
    return actions


def qval(state, action, V):
    i, j = state
    newval = 0
    for rrp1, rrp2 in product(
        req_ret_prob(i - action, REQLAMBDA1, RETLAMBDA1),
        req_ret_prob(j + action, REQLAMBDA2, RETLAMBDA2),
    ):
        req1, ret1, prob1 = rrp1
        req2, ret2, prob2 = rrp2
        reward = (req1 + req2) * 10 - action * 2
        i1, j1 = (i - action - req1 + ret1), (j + action - req2 + ret2)
        newval += prob1 * prob2 * (reward + GAMMA * V[i1, j1])

    return newval


V = np.zeros((21, 21))
policy = np.zeros((21, 21), dtype=int)


if __name__ == "__main__":
    # print(float(poisson(3, 3)))
    # print(qval((10, 14), 3, V))
    # print(rent())
    print("hello")

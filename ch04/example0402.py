from dataclasses import dataclass
from itertools import product

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import poisson

GAMMA = 0.9


@dataclass(frozen=True)
class Transition:
    req: int
    ret: int
    prob: float


def build_transition_table(req_lambda, ret_lambda):
    def transition_seq(n_of_morning_cars):
        for req in range(n_of_morning_cars + 1):
            p1 = poisson.pmf(req, req_lambda)
            if p1 < 0.000001:
                break
            ret = 0
            while True:
                p2 = poisson.pmf(ret, ret_lambda)
                if p2 < 0.0001 or (n_of_morning_cars - req + ret) > 20:
                    break
                yield Transition(req, ret, p1 * p2)
                ret += 1

    return [list(transition_seq(i)) for i in range(26)]


transition_table1 = build_transition_table(3, 3)
transition_table2 = build_transition_table(4, 2)


def example0402():
    V = np.zeros((21, 21))
    policy = np.zeros((21, 21), dtype=int)

    while True:
        show_policy(policy)
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
        if delta < 0.00001:
            return V


def update_policy(V, policy):
    "returns True if updated, False otherwise"
    update_done = False
    for i, j in product(range(21), range(21)):
        old_action = policy[i, j]

        # best_action
        maxval, best_action = float('-inf'), None 
        for action in possible_actions(i, j):
            newval = qval((i, j), action, V)
            if newval > maxval:
                maxval, best_action = newval, action

        if old_action != best_action:
            policy[i, j] = best_action
            update_done = True
    return update_done



def possible_actions(i, j):
    actions = []
    for a in range(-5, 6):
        if i - a >= 0 and j + a >= 0:
            actions.append(a)
    return actions


# action value from value function (arrays actually)
def qval(state, action, V):
    i, j = state
    newval = -2 * abs(action)
    for t1, t2 in product(transition_table1[i - action], transition_table2[j + action]):
        reward = (t1.req + t2.req) * 10
        i1, j1 = (i - action - t1.req + t1.ret), (j + action - t2.req + t2.ret)
        newval += t1.prob * t2.prob * (reward + GAMMA * V[i1, j1])
    return newval


def show_policy(policy):
    fig, ax = plt.subplots(figsize=(10, 8))

    cmap = plt.cm.get_cmap("RdBu_r", 11)  # 11 levels for -5 to 5

    mesh = ax.pcolormesh(policy, cmap=cmap, vmin=-5.5, vmax=5.5)

    ax.set_xticks(np.arange(0, 21, 1))
    ax.set_yticks(np.arange(0, 21, 1))
    ax.grid(True, which="major", color="k", linestyle="-", linewidth=0.5)

    ax.set_title("20x20 Discrete Matrix Plot")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")

    cbar = fig.colorbar(mesh, ticks=range(-5, 6))
    cbar.set_label("Value")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    example0402()
    # print(poisson.pmf(18, 4))

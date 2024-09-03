# %%

import matplotlib.pyplot as plt

ph = 0.45
gamma = 1

def gamble():
    # value function
    V = [0] * 101
    V[100] = 1
    while True:
        delta = 0
        for i in range(1, 100):
            v = V[i]
            _, maxval = best_action(i, V)
            V[i] = maxval
            delta = max(delta, abs(V[i] - v))

        if delta < 0.000001:
            return V


def best_action(state, V):
    maxval = 0
    act = 0
    for a in range(1, min(state, 100 - state) + 1):
        newval = qval(state, a, V)
        # adding a small number to make the similar plot as in the textbook
        if newval > maxval + 0.00001:
            act = a
            maxval = newval
    return act, maxval


def qval(state, action, V):
    return ph * gamma * V[state + action] + (1 - ph) * gamma * V[state - action]


def plotvals(V):
    fig, ax = plt.subplots(2, 1)
    ax[0].plot(V)

    p = [0] * 100
    for i in range(100):
        a, _ = best_action(i, V)
        p[i] = a
    ax[1].plot(p)
    plt.show()


# %%
if __name__ == "__main__":
    v = gamble()
    plotvals(v)

    # print(best_action(51, v), v[52], v[50])

# %%

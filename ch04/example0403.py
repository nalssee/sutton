# %%

import matplotlib.pyplot as plt


def gamble():
    # value function
    V = [0] * 101
    # prob of heads
    ph = 0.4
    # undiscounted
    gamma = 1
    while True:
        delta = 0
        for i in range(100):
            v = V[i]
            _, maxval = search_best_action(i, V, ph, gamma)
            V[i] = maxval
            delta = max(delta, abs(V[i] - v))

        if delta < 0.001:
            return V
        


def search_best_action(state, V, ph, gamma):
    maxval = 0
    best_action = 0
    for a in range(min(state, 100 - state) + 1):
        reward = 1 if state + a == 100 else 0
        newval = ph * (reward + gamma * V[state + a])\
            + (1 - ph) * (reward + gamma * V[state - a])
       
        if newval > maxval:
            best_action = a
            maxval = newval
    return best_action, maxval

# V = [0] * 101
# ph = 0.4
# gamma = 1
# print(search_best_action(52, V, ph, gamma))

def plotvals(V):
    plt.plot(V) 
    plt.show()
    p = [0] * 100
    for i in range(100):
        a, _ = search_best_action(i, V, 0.4, 1)
        p[i] = a
    plt.plot(p)
    plt.show()



# %%
if __name__ == "__main__":
    v = gamble()
    plotvals(v)
# %%

# the result is quite different if we use 1/n as a step_size !!!!
# think why

# the misterious spike is not significant as well

# %%
import matplotlib.pyplot as plt
import numpy as np


def argmax_multiple(lst):
    arr = np.array(lst)
    return np.where(arr == arr.max())[0]


def n_centers(n=10):
    centers = np.random.normal(loc=0, scale=1, size=n)
    return centers


def bandit(epsilon, runs=2000, steps=1000, actions=10, init_qstar=0):
    rewards = [0] * steps
    optimal_actions = [0] * steps

    for i in range(runs):
        rewards1, optimal_actions1 = onerun(
            epsilon=epsilon, steps=steps, actions=actions, init_qstar=init_qstar
        )

        for pos, r1 in enumerate(rewards1):
            rewards[pos] += r1
        for pos, oa1 in enumerate(optimal_actions1):
            optimal_actions[pos] += oa1
    return [r / runs for r in rewards], [oa / runs for oa in optimal_actions]


def onerun(epsilon, actions=10, steps=1000, init_qstar=0):
    centers = n_centers(actions)
    best_action_pos = np.argmax(centers)

    # qstars (init estimate of q* is 0)
    qstars = [init_qstar] * actions
    # number of each action
    counts = [0] * actions

    # rewards for each step
    rewards = []
    # 1/0 for each step: 1 for optimal action, 0 for the otherwise
    optimal_actions = []
    for i in range(steps):
        if np.random.uniform(0, 1) < epsilon:
            pos = np.random.randint(0, actions)
        else:
            best_actions = argmax_multiple(qstars)
            pos = np.random.choice(best_actions)

        center = centers[pos]
        reward = np.random.normal(loc=center, scale=1)
        update(qstars, pos, reward)

        rewards.append(reward)

        optimal_actions.append(1 if pos == best_action_pos else 0)

    return rewards, optimal_actions


def update(qstars, pos, reward):
    # update counts first
    alpha = 0.1
    qstars[pos] += alpha * (reward - qstars[pos])


# %%
avg_rewards01, optimal_actions01 = bandit(0.1, init_qstar=0)
avg_rewards0, optimal_actions0 = bandit(0, init_qstar=5)


# %%
def plot1():
    fig, ax = plt.subplots(figsize=(10, 5))
    xs = range(1, len(avg_rewards01) + 1)

    ax.plot(xs, avg_rewards01, label="epsilon=0.1, Q1=0")
    ax.plot(xs, avg_rewards0, label="epsilon=0, Q1=5")
    ax.legend(loc="lower right")
    ax.set_xlabel("Steps")
    ax.set_ylabel("Avg Reward")
    plt.show()


plot1()


#
# %%
def plot2():
    fig, ax = plt.subplots(figsize=(10, 5))
    xs = range(1, len(avg_rewards01) + 1)

    ax.plot(xs, optimal_actions01, label="epsilon=0.1, Q1=0")
    ax.plot(xs, optimal_actions0, label="epsilon=0, Q1=5")
    ax.legend(loc="lower right")
    ax.set_xlabel("Steps")
    ax.set_ylabel("Optimal Actions")
    plt.show()


plot2()


# %%
for i, val in enumerate(optimal_actions0[:300], 1):
    print(i, val)
    
# %%

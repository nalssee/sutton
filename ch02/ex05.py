# %%
import matplotlib.pyplot as plt
import numpy as np


def argmax_multiple(lst):
    arr = np.array(lst)
    return np.where(arr == arr.max())[0]


# def n_centers(n=10):
#     centers = np.random.normal(loc=0, scale=1, size=n)
#     return centers


def bandit(
    epsilon, runs=2000, steps=1000, actions=10, alpha=0.1, update_method="sample_mean"
):
    rewards = [0] * steps
    optimal_actions = [0] * steps

    for i in range(runs):
        rewards1, optimal_actions1 = onerun(
            epsilon=epsilon,
            steps=steps,
            actions=actions,
            alpha=alpha,
            update_method=update_method,
        )

        for pos, r1 in enumerate(rewards1):
            rewards[pos] += r1
        for pos, oa1 in enumerate(optimal_actions1):
            optimal_actions[pos] += oa1
    return [r / runs for r in rewards], [oa / runs for oa in optimal_actions]


def onerun(epsilon, update_method="sample_mean", actions=10, steps=1000, alpha=0.1):
    centers = [0] * actions

    # qstars (init estimate of q* is 0)
    qstars = [0] * actions
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

        best_action_pos = np.argmax(centers)

        center = centers[pos]
        reward = np.random.normal(loc=center, scale=1)

        if update_method == "const":
            update_const(qstars, pos, reward, alpha)
        elif update_method == "sample_mean":
            update_mean(qstars, pos, reward, counts)

        rewards.append(reward)

        optimal_actions.append(1 if pos == best_action_pos else 0)

        # update centers
        for idx in range(actions):
            centers[idx] += np.random.normal(loc=0, scale=0.01)

    return rewards, optimal_actions


def update_mean(qstars, pos, reward, counts):
    # update counts first
    counts[pos] += 1
    n = counts[pos]
    qstars[pos] += (1 / n) * (reward - qstars[pos])


def update_const(qstars, pos, reward, alpha=0.1):
    # update counts first
    qstars[pos] += alpha * (reward - qstars[pos])


# %%

# took 24 mins

from multiprocessing import Pool


def worker1(epsilon):
    return bandit(epsilon, steps=10_000, update_method="sample_mean")


def worker2(epsilon):
    return bandit(epsilon, steps=10_000, update_method="const", alpha=0.1)


with Pool() as pool:
    epsilons = [0.1, 0.01, 0]
    result1 = pool.map(worker1, epsilons)
    result2 = pool.map(worker2, epsilons)


# %%


def plot1(results):
    fig, ax = plt.subplots(figsize=(10, 5))
    xs = range(1, len(results[0][0]) + 1)

    ax.plot(xs, results[0][0], label="epsilon=0.1")
    ax.plot(xs, results[1][0], label="epsilon=0.01")
    ax.plot(xs, results[2][0], label="epsilon=0")
    ax.legend(loc="lower right")
    ax.set_xlabel("Steps")
    ax.set_ylabel("Avg Reward")
    plt.show()


plot1(result1)

plot1(result2)


#
# %%
def plot2(result):
    fig, ax = plt.subplots(figsize=(10, 5))
    xs = range(1, len(result[0][1]) + 1)

    ax.plot(xs, result[0][1], label="epsilon=0.1")
    ax.plot(xs, result[1][1], label="epsilon=0.01")
    ax.plot(xs, result[2][1], label="epsilon=0")
    ax.legend(loc="lower right")
    ax.set_xlabel("Steps")
    ax.set_ylabel("Optimal Actions")
    plt.show()


plot2(result1)

plot2(result2)


#
# %%

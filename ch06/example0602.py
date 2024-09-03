# %%

import random
import matplotlib.pyplot as plt
import numpy as np


def rms_error(list1: list[float], list2: list[float]) -> float:
    squared_diff = [(a - b) ** 2 for a, b in zip(list1, list2)]
    mean_squared_diff = sum(squared_diff) / len(squared_diff)
    rms = np.sqrt(mean_squared_diff)
    return rms


class RandomWalk:
    def __init__(self, update_method: str) -> None:
        self.alpha = 0.1
        self.gamma = 1.0
        self.n_episodes = 100
        self.n_batches = 100
        self.update_method = update_method 
        self.value_table = [0.5] * 5
        
    def generate_episode(self) -> list[int]:
        """state: 0 ~ 4, terminate at -1 and 5, 0 and 1 for rewards, respectably"""

        result = [2]
        state = result[-1]
        while state != -1 and state != 5:
            step = -1 if random.uniform(0, 1) < 0.5 else 1
            state += step
            result.append(state)
        return result

    def update_MC(self, episode: list[int]) -> None:
        for state in episode[:-1]:
            G = 1 if episode[-1] == 5 else 0
            self.value_table[state] += self.alpha * (G - self.value_table[state])

    def update_tdzero(self, episode: list[int]) -> None:
        for state, state1 in zip(episode, episode[1:]):
            reward = 1 if state1 == 5 else 0
            v1 = 0 if state1 == -1 or state1 == 5 else self.value_table[state1]
            # gamma = 1.0
            self.value_table[state] += self.alpha * (reward + v1 - self.value_table[state])

    def one_batch(self) -> None:
        update_fn = if  
        for _ in range(n_episodes):
                episode = self.generate_episode
            update_fn(episode, value_table, alpha)
        return value_table


def run_batches(
    update_fn, n_batches=100, n_episodes=100, alpha=0.1
) -> tuple(list[float], list[float]):
    value_table_accum = [0.0] * 5
    for _ in range(n_batches):
        value_table = one_batch(update_fn, n_episodes, alpha)




def plot1() -> None:
    td01, _ = run_episodes(update_tdzero, 1)
    td10, _ = run_episodes(update_tdzero, 10)
    td100, _ = run_episodes(update_tdzero, 100)

    trueval = [x / 6.0 for x in [1, 2, 3, 4, 5]]
    plt.plot(td01, label="1")
    plt.plot(td10, label="10")
    plt.plot(td100, label="100")
    plt.plot(trueval, label="true")
    plt.legend()
    plt.show()


def plot2() -> None:
    _, rms1 = run_episodes(update_MC, 100)
    plt.plot(rms1, label="MC")
    _, rms2 = run_episodes(update_tdzero, 100)
    plt.plot(rms2, label="tdzero, 0.1")
    _, rms3 = run_episodes(update_tdzero, 100, alpha=0.15)
    plt.plot(rms3, label="tdzero, 0.15")
    _, rms4 = run_episodes(update_tdzero, 100, alpha=0.05)
    plt.plot(rms4, label="tdzero, 0.05")

    plt.legend()
    plt.show()


plot1()
plot2()
# %%

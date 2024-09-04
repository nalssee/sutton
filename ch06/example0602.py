# %%

import random
from typing import Callable

import matplotlib.pyplot as plt
import numpy as np


class Config:
    def __init__(
        self,
        update_method="update_tdzero",
        alpha=0.1,
        gamma=1.0,
        n_episodes=100,
        n_batches=100,
        V=[0.5] * 5,
        rmse_series=[],
    ) -> None:

        self.update_method = update_method
        self.alpha = alpha
        self.gamma = gamma
        self.n_episodes = n_episodes

        self.n_batches = n_batches
        self.V = V
        self.rmse_series = rmse_series

    def reset(self):
        self.V = [0.5] * 5
        self.rmse_series = []

    def get_update_method(self) -> Callable[[list[int]], None]:
        return getattr(self, self.update_method)

    def update_monte_carlo(self, episode: list[int]) -> None:
        for state in episode[:-1]:
            G = 1 if episode[-1] == 5 else 0
            self.V[state] += self.alpha * (G - self.V[state])

    def update_tdzero(self, episode: list[int]) -> None:
        for state, state1 in zip(episode, episode[1:]):
            reward = 1 if state1 == 5 else 0
            v1 = 0 if state1 == -1 or state1 == 5 else self.V[state1]
            self.V[state] += self.alpha * (reward + self.gamma * v1 - self.V[state])


def rmse(list1: list[float], list2: list[float]) -> float:
    squared_diff = [(a - b) ** 2 for a, b in zip(list1, list2)]
    mean_squared_diff = sum(squared_diff) / len(squared_diff)
    rms = np.sqrt(mean_squared_diff)
    return rms


def generate_episode() -> list[int]:
    """state: 0 ~ 4, terminate at -1 and 5, 0 and 1 for rewards, respectably"""
    result = [2]
    state = result[-1]
    while state != -1 and state != 5:
        step = -1 if random.uniform(0, 1) < 0.5 else 1
        state += step
        result.append(state)
    return result


def one_batch(conf: Config) -> None:
    updatefn = conf.get_update_method()
    true_values = [x / 6.0 for x in range(1, 6)]
    for _ in range(conf.n_episodes):
        episode = generate_episode()
        updatefn(episode)
        conf.rmse_series.append(rmse(true_values, conf.V))


def run_batches(conf: Config) -> list[float]:
    total_rmse_series = [0] * conf.n_batches
    for _ in range(conf.n_batches):
        conf.reset()
        one_batch(conf)
        for i, rmse in enumerate(conf.rmse_series):
            total_rmse_series[i] += rmse
    return [rmse / conf.n_batches for rmse in total_rmse_series]


def plot1() -> None:
    conf = Config(update_method="update_tdzero", n_episodes=1)
    one_batch(conf)
    plt.plot(conf.V, label="1")

    conf = Config(update_method="update_tdzero", n_episodes=10)
    one_batch(conf)
    plt.plot(conf.V, label="10")

    conf = Config(update_method="update_tdzero", n_episodes=100)
    one_batch(conf)
    plt.plot(conf.V, label="100")

    true_values = [x / 6.0 for x in range(1, 6)]
    plt.plot(true_values, label="true")

    plt.legend()
    plt.show()


def plot2() -> None:
    conf = Config(update_method="update_monte_carlo", alpha=0.01)
    rmse_series = run_batches(conf)
    plt.plot(rmse_series, label="MC, 0.01")

    conf = Config(update_method="update_monte_carlo", alpha=0.02)
    rmse_series = run_batches(conf)
    plt.plot(rmse_series, label="MC, 0.02")

    conf = Config(update_method="update_monte_carlo", alpha=0.03)
    rmse_series = run_batches(conf)
    plt.plot(rmse_series, label="MC, 0.03")

    conf = Config(update_method="update_tdzero", alpha=0.1)
    rmse_series = run_batches(conf)
    plt.plot(rmse_series, label="TDZero, 0.1")

    conf = Config(update_method="update_tdzero", alpha=0.15)
    rmse_series = run_batches(conf)
    plt.plot(rmse_series, label="TDZero, 0.15")

    conf = Config(update_method="update_tdzero", alpha=0.05)
    rmse_series = run_batches(conf)
    plt.plot(rmse_series, label="TDZero, 0.05")

    plt.legend()
    plt.show()


if __name__ == "__main__":
    conf = Config()
    print(type(conf.get_update_method()))
    # plot1()
    # plot2()


# %%

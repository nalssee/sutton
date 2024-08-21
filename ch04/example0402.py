# %%
from dataclasses import dataclass
from itertools import product

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colormaps, colors
from matplotlib.gridspec import GridSpec
from scipy.stats import poisson

GAMMA = 0.9

# %%
@dataclass(frozen=True)
class Transition:
    req: int
    ret: int
    prob: float


def transition_list(req_lambda, ret_lambda):
    result = []
    req = 0
    while True:
        p1 = poisson.pmf(req, req_lambda)
        if p1 < 0.000001:
            break
        ret = 0
        while True:
            p2 = poisson.pmf(ret, ret_lambda)
            if p2 < 0.000001:
                break
            if p1 * p2 >= 0.0001:
                result.append(Transition(req, ret, p1 * p2))
            ret += 1

        req += 1
    return result


tlist1 = transition_list(3, 3)
tlist2 = transition_list(4, 2)


def example0402():
    V = np.zeros((21, 21))
    policy = np.zeros((21, 21), dtype=int)
    policies = []
    while True:
        policy_evaluation(V, policy)
        policies.append(policy.copy())
        if not update_policy(V, policy):
            break
    return V, policies


# action: int, from location1 to location2
def policy_evaluation(V, policy):
    while True:
        delta = 0
        for i, j in product(range(21), range(21)):
            v = V[i, j]
            action = policy[i, j]
            V[i, j] = qval((i, j), action, V)
            delta = max(delta, abs(V[i, j] - v))
        if delta < 1:
            return V


def update_policy(V, policy):
    "returns True if updated, False otherwise"
    update_done = False
    for i, j in product(range(21), range(21)):
        old_action = policy[i, j]

        # best_action
        maxval, best_action = float("-inf"), None
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

    i0, j0 = i - action, j + action

    newval = -2 * abs(action)
    for t1, t2 in product(tlist1, tlist2):
        reward = (min(t1.req, i0) + min(t2.req, j0)) * 10
        i1 = min(max(0, i0 - t1.req) + t1.ret, 20)
        j1 = min(max(0, j0 - t2.req) + t2.ret, 20)
        p = t1.prob * t2.prob
        newval += p * (reward + GAMMA * V[i1, j1])
    return newval


def show_policy(ax, policy, title):
    cmap = colormaps["RdBu_r"]
    bounds = np.arange(-5.5, 6.5, 1)
    norm = colors.BoundaryNorm(bounds, cmap.N)

    mesh = ax.pcolormesh(policy, cmap=cmap, norm=norm)
    ax.set_xticks(np.arange(0, 21, 5))
    ax.set_yticks(np.arange(0, 21, 5))
    ax.set_xticklabels(range(0, 21, 5))
    ax.set_yticklabels(range(0, 21, 5))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 20)
    ax.grid(True, which="major", color="k", linestyle="-", linewidth=0.5)
    ax.set_title(title)
    return mesh


def show_multiple_policies(policies, titles, save_path):
    fig = plt.figure(figsize=(18, 16))
    gs = GridSpec(2, 3, figure=fig, width_ratios=[1, 1, 0.05])

    axs = []
    for i in range(2):
        for j in range(2):
            ax = fig.add_subplot(gs[i, j])
            axs.append(ax)

    meshes = []
    for ax, policy, title in zip(axs, policies, titles):
        mesh = show_policy(ax, policy, title)
        meshes.append(mesh)

    # color bar
    cax = fig.add_subplot(gs[:, -1])
    cbar = fig.colorbar(meshes[0], cax=cax, ticks=range(-5, 6))
    cbar.set_label("Move")

    for ax in axs[2:]:
        ax.set_xlabel("Cars at location 1")
    for ax in [axs[0], axs[2]]:
        ax.set_ylabel("Cars at location 2")

    plt.tight_layout()

    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    print(f"Figure saved to {save_path}")


# %%

if __name__ == "__main__":
    v, policies = example0402()
    titles = ["P1", "P2", "P3", "P4"]
    show_multiple_policies(policies[1:], titles, "example0402.png")

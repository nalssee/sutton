import pytest 

from .bandit import onerun 

def test_n_centers():
    rewards, optimal_actions = onerun(0.1) 
    print(rewards, optimal_actions)
from random import choice


######################
# Monte-Carlo method #
######################

def random_walk_mc_value(max_size=6, start=3, n_episodes=100):
    # initiate values
    values = [0] * 5
    rms_series = []
    for i in range(n_episodes):
        mc_update(values, max_size, start, i)
        rms_series.append(rms(values))
    return values, rms_series


def mc_update(values, max_size, start, i):
    path = generate_episode(max_size, start)

    ret = 0 if path[-1] == 0 else 1

    for state in set(path[:-1]):
        oldval = values[state - 1]
        values[state - 1] = oldval + (ret - oldval) / (i + 1)


# you may want to define it as a generator function if it's endless 
def generate_episode(max_size, start):
    current = start
    path = [current]
    while current != 0 and current != max_size:
        current += choice([-1, 1])
        path.append(current)
    return path

def rms(values):
    sum = 0
    for val, true_val in zip(values, [1/6, 2/6, 3/6, 4/6, 5/6]):
        sum += (val - true_val) ** 2
    return (sum / len(values)) ** 0.5



################
# TD(0) method # 
################

def random_walk_td_zero(max_size=6, start=3, n_episodes=100, alpha=0.05):
    # initiate values
    values = [0.5] * 5
    rms_series = []
    for i in range(n_episodes):
        episode = generate_episode(max_size, start)
        for state1, state2 in zip(episode, episode[1:]):
            ret = 1 if state2 == max_size else 0
            val1 = values[state1 - 1]
            if state2 == 0 or state2 == max_size:
                val2 = 0
            else:
                val2 = values[state2 - 1]
            # gamma is zero            
            values[state1 - 1] = val1 + alpha * (ret + val2 - val1) 
    return values

print(random_walk_td_zero())



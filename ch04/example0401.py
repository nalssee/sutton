# %%
def example0401():
    """
    Returns a history of value functions for gridword with random policy
    """
    history = []
    value_fn = [0.0] * 16

    while True:
        new_value_fn = update_value_fn(value_fn)
        history.append(new_value_fn)
        if distance(new_value_fn, value_fn) < 0.001:
            return history

        value_fn = new_value_fn 
        # if cnt == 100:
        #     return history
 
def update_value_fn(value_fn):
    new_value_fn = [0.0] * 16
    for s, val in enumerate(value_fn):
        # 0, 15 are terminal states
        if s not in [0, 15]:
            next_states = get_next_states(s)
            new_val = compute_new_value(next_states, value_fn)
            new_value_fn[s] = new_val
    return new_value_fn 


def get_next_states(state):
    next_states = []
    for next_state in [state - 4, state + 4, state - 1, state + 1]:
        next_state = next_state if valid_move(state, next_state) else state
        next_states.append(next_state) 
    return next_states

def valid_move(state, next_state):
    if next_state > 15 or next_state < 0:
        return False
    if (state, next_state) in [(3, 4), (7, 8), (11, 12), (4, 3), (8, 7), (12, 11)]:
        return False
    return True

def compute_new_value(next_states, value_fn):
    gamma = 1.0
    total = 0
    for s1 in next_states:
        total += (-1 + gamma * value_fn[s1]) * 0.25 
    return total


def distance(new_value_fn, old_value_fn):
    return max(abs(v1 - v0) for v1, v0 in zip(new_value_fn, old_value_fn))

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def show_value_fn(value_fn):
    for row in chunks(value_fn, 4):
        for val in row:
            val = float(val)
            print(f"{val: 5.1f}", end=' ')
        print()



# %%

if __name__ == "__main__":
    # example0401()
    history = example0401()

    for i in [0, 1, 2, 3, 10]:
        print(i)
        show_value_fn(history[i])
    print('final')
    show_value_fn(history[-1])
# %%
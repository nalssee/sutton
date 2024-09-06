# Blackjack, Monte Carlo
# %%
import random
import copy 


def generate_episode() -> tuple[list[State], int]:
    state = State()
    episode = [state]

    while True:
        # bust
        if state.player > 21:
            return (episode, -1)
        # stick
        if state.player >= 20:
            # dealer's turn
            reward = compute_reward(state)
            return (episode, reward)
        # hit
        new_state = copy.copy(state)
        new_state.next_step()
        episode.append(new_state)
        state = new_state


class State:
    def __init__(self):
        self.dealer = random.randint(1, 10)
        self.player = random.randint(12, 21)
        # 1 represents "usable"
        self.usable_ace = random.randint(0, 1)
    
    def __str__(self):
        return f'({self.dealer}, {self.player}, {self.usable_ace})' 

    def next_step(self):
        card = draw_card()
        
        if self.player + card > 21 and self.usable_ace == 1:
            self.usable_ace = 0
            self.player += card - 10
        else:
            self.player += card   


def compute_total(cards: list[int]) -> int:
    """
    >>> compute_total([1, 2, 3, 1])
    17
    >>> compute_total([1, 10, 1, 1])
    13
    """
    non_ace_sum = sum(x for x in cards if x != 1)
    n_aces = sum(1 for x in cards if x == 1) 
    if n_aces == 0:
        return non_ace_sum 
    ace_sum = n_aces + 10
    if non_ace_sum + ace_sum > 21:
        return non_ace_sum + ace_sum - 10
    return non_ace_sum + ace_sum 


def compute_reward(state):
    # hidden card
    card = draw_card()
    cards = [state.dealer, card]
    tot = compute_total(cards) 
    while tot < 17:
        card = draw_card()
        cards.append(card)
        tot = compute_total(cards)

    if tot > 21:
        # player wins
        return 1 
    if state.player > tot:
        return 1
    if state.player == tot:
        return 0 
    if state.player < tot:
        return -1
   
def draw_card() -> int:
    return random.choices([x for x in range(1, 11)], [1.0 / 13] * 9 + [4.0 / 13])[0]



# %%
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    
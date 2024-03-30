import functools
import itertools
import multiprocessing as mp

import numpy as np

from game import base_agent, helpers


class Agent(base_agent.BaseAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Jankas"
        # self.pool = mp.Pool(processes=4)

    def select_cards(self):
        self.deck = dict(
            plus1=4,
            plus5=5,
            plus10=3,
            mult3=6,
            mult10=3,
            div5=2,
            div10=1,
        )

    def play_turn(self, hand, energy, game_info, locked_term, current_term):
        return highest_value_play(hand, energy, locked_term, current_term)


def card_permutations(hand):
    for indexes in itertools.permutations(range(len(hand))):
        yield [hand[index] for index in indexes]


def highest_value_play(hand, energy, locked_term, current_term):
    candidate = []
    candidate_value = locked_term + current_term
    candidate_cost = 0
    kernel = functools.partial(check_play, energy=energy, locked_term=locked_term, current_term=current_term)
    # results = pool.map(kernel, card_permutations(hand), chunksize=20)
    # results = pool.imap(kernel, card_permutations(hand), chunksize=20)
    results = map(kernel, card_permutations(hand))

    for to_play, score, cost in results:
        if (score > candidate_value) or (
                score == candidate_value and (len(to_play) < len(candidate) or cost < candidate_cost)):
            candidate = to_play
            candidate_value = score
            candidate_cost = cost
    return candidate


def check_play(cards, energy, locked_term, current_term):
    to_play = []
    intermediate_values = []
    total_cost = 0
    for card in cards:
        if card.cost > energy:
            break
        energy -= card.cost
        locked_term, current_term = helpers.apply_card(card, locked_term, current_term)
        to_play.append(card)
        intermediate_values.append(locked_term + current_term)
        total_cost += card.cost
    if not intermediate_values:
        return [], locked_term + current_term, 0
    best_index = np.argmax(intermediate_values)
    return to_play[:best_index + 1], intermediate_values[best_index], total_cost

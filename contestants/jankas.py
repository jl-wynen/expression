import functools
import itertools
import random

import numpy as np

from game import base_agent, helpers


class Agent(base_agent.BaseAgent):
    def __init__(self, deck=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Jankas"
        self._user_deck = deck

    def select_cards(self):
        if self._user_deck is not None:
            self.deck = dict(self._user_deck)
        else:
            choices = [
                {'plus5': 5, 'plus10': 3, 'div10': 2, 'plus1': 2, 'div5': 1, 'mult10': 3},
                {'plus5': 5, 'plus10': 3, 'div10': 1, 'plus1': 2, 'div5': 1, 'mult10': 3},
            ]
            self.deck = choices[random.randint(0, len(choices) - 1)]

    def play_turn(self, hand, energy, game_info, locked_term, current_term):
        eligible = [card for card in hand if card.cost <= energy]
        play = highest_value_play(eligible, energy, locked_term, current_term)

        cost = sum(card.cost for card in play)
        remaining_energy = energy - cost
        remaining = list(hand)
        for card in play:
            remaining.remove(card)
        remaining = [card for card in remaining if card.cost <= remaining_energy]

        # finalize the current_term if possible
        cards_finalizing_term = [card for card in remaining if card.operator == '+']
        if cards_finalizing_term:
            finalizer = sorted(cards_finalizing_term, key=lambda card: card.cost)[0]
            play.append(finalizer)

        return play


def card_permutations(hand):
    for indexes in itertools.permutations(range(len(hand))):
        yield [hand[index] for index in indexes]


def highest_value_play(hand, energy, locked_term, current_term):
    candidate = []
    candidate_value = locked_term + current_term
    candidate_cost = 0
    kernel = functools.partial(check_play, energy=energy, locked_term=locked_term, current_term=current_term)
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

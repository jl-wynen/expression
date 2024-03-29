import random
from game import base_agent
from game import helpers


class Agent(base_agent.BaseAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Reckless"

    def select_cards(self):
        self.deck = dict(plus1=2, mult3=2, div5=0, plus5=4, mult10=9, div10=0, plus10=5)

    def play_turn(self, hand, energy, game_info, locked_term, current_term):

        played_cards = []  # prepare list for played cards

        # Figure out which cards could be played now (sufficient energy)
        can_play = helpers.can_be_played(hand, energy)

        # Search for cards to play, taking into account use of energy and changing expression
        while len(can_play) > 0 and len(hand) > 0:

            n_cards_being_played = len(played_cards)  # Number of cards currently being played

            # Decide what kind of card to play now
            if current_term > 0:
                desired_operator = "*"
            else:
                desired_operator = "+"

            # Search for such a card that we can play
            for card in can_play:
                if card.operator == desired_operator:
                    # If found, move it to played_cards
                    played_cards.append(card)
                    hand.remove(card)  # removes from hand
                    energy -= card.cost  # remember we use some energy

                    # update expression
                    locked_term, current_term = helpers.apply_card(card, locked_term, current_term)
                    break

            if len(played_cards) == n_cards_being_played:
                # Didn't play anything new this iteration, time to quit with break
                break

            # See which cards we can play now that we have reduced our hand and spent some energy
            can_play = helpers.can_be_played(hand, energy)

        return played_cards

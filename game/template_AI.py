import random
from . import base_agent


def apply_card(card, current_value, current_term):
    # Assume card is of card class
    if card.operator == "+":
        current_value += current_term
        current_term = card.value
    elif card.operator == "-":
        current_value += current_term
        current_term = -1 * card.value
    elif card.operator == "*":
        current_term *= card.value
    elif card.operator == "/":
        current_term /= card.value
    else:
        print("Error, unknown operator: ", end="")
        print(card.operator)

    return current_value, current_term


#deck_A = dict(plus1=8, mult3=5, div2=0, plus5=0, mult10=3, div8=0, plus10=0)
#deck_B = dict(plus1=8, mult3=5, div2=0, plus5=0, mult10=3, div8=0, plus10=0)

deck_A = dict(plus1=3, mult3=5, div5=0, plus5=5, mult10=3, div10=0, plus10=0)
deck_B = dict(plus1=6, mult3=0, div5=0, plus5=5, mult10=10, div10=0, plus10=5)

# Easy to make a deck that beats only plus cards
#deck_B = dict(plus1=0, mult3=0, div2=0, plus5=0, mult10=10, div8=0, plus10=20)

# Slow deck with large numbers of big cost cards are very good
deck_B = dict(plus1=0, mult3=0, div5=0, plus5=5, mult10=10, div10=0, plus10=10)

# Quick deck can beat it?
deck_A = dict(plus1=5, mult3=20, div5=0, plus5=2, mult10=2, div10=0, plus10=4)
deck_B = dict(plus1=5, mult3=20, div5=0, plus5=2, mult10=2, div10=0, plus10=4)


# Normal deck
deck_A = dict(plus1=6, mult3=8, div5=0, plus5=5, mult10=4, div10=0, plus10=3)
deck_B = dict(plus1=6, mult3=8, div5=0, plus5=5, mult10=4, div10=0, plus10=3)

# Archetypes I want:

# quick decks with low value cards that hope to end the game quickly
# slow decks that hope the game lasts long enough to use their expensive cards

# Almost impossible to have a quick deck that wins with the high 100 limit
#  and the most expensive cards being just 4-5


# aggresive decks that only care about increasing their points

# defensive decks that also include dividers to slow aggresive decks

# combo decks that wait until they can have big moves



#deck_A = dict(plus1=15, mult3=5, div2=2, plus5=3, mult10=4, div8=2, plus10=5)
#deck_B = dict(plus1=13, mult3=7, div2=0, plus5=7, mult10=4, div8=0, plus10=5)
#deck_B = dict(plus1=15, mult3=5, div2=2, plus5=3, mult10=4, div8=2, plus10=5)

class template_AI_A(base_agent.BaseAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.only_play_when_able_to_win = False

    def select_cards(self):
        #self.deck = dict(plus1=20, mult3=5, div2=0, plus5=0, mult10=5, div8=0, plus10=0)
        self.deck = deck_A

    def multipliers_used(self):
        return self.deck["mult3"] + self.deck["mult10"] > 0

    def dividers_used(self):
        return self.deck["div5"] + self.deck["div10"] > 0

    def play_turn(self, hand, energy, game_info, current_value, current_term):


        can_play = []
        for card in hand:
            if card.cost <= energy:
                can_play.append(card)

        can_play = sorted(can_play, key=lambda card: card.cost, reverse=True)

        played_cards = []
        continue_searching = True
        while len(can_play) > 0 and len(hand) > 0 and continue_searching:
            use_multiplier = current_term > 0

            if use_multiplier and self.multipliers_used():
                desired_operator = "*"
            elif abs(current_term) > 10 and self.dividers_used():
                desired_operator = "/"
            else:
                desired_operator = "+"

            continue_searching = False
            for card in can_play:
                if card.operator == desired_operator:
                    played_cards.append(card)
                    hand.remove(card)
                    continue_searching = True
                    break

            if len(played_cards) > 0:
                energy -= played_cards[-1].cost
            else:
                break

            can_play = []
            for card in hand:
                if card.cost <= energy:
                    if card not in played_cards:
                        can_play.append(card)

            can_play = sorted(can_play, key=lambda card: card.cost, reverse=True)

            if continue_searching:
                # Update current value and term based on played card
                current_value, current_term = apply_card(played_cards[-1], current_value, current_term)

            #print("played_cards:", played_cards)
            #print("played_cards:", current_value + current_term)

        #print("played_cards:", played_cards)

        if len(played_cards) > 0:
            if abs(current_value + current_term) >= abs(self.goal_limit) or not self.only_play_when_able_to_win:
                return played_cards


class template_AI_B(base_agent.BaseAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.only_play_when_able_to_win = False

    def select_cards(self):
        #self.deck = dict(plus1=20, mult3=5, div2=0, plus5=0, mult10=0, div8=0, plus10=0)
        self.deck = deck_B

    def multipliers_used(self):
        return self.deck["mult3"] + self.deck["mult10"] > 0

    def dividers_used(self):
        return self.deck["div5"] + self.deck["div10"] > 0

    def play_turn(self, hand, energy, game_info, current_value, current_term):

        can_play = []
        for card in hand:
            if card.cost <= energy:
                can_play.append(card)

        can_play = sorted(can_play, key=lambda card: card.cost, reverse=True)

        played_cards = []
        continue_searching = True
        while len(can_play) > 0 and len(hand) > 0 and continue_searching:
            use_multiplier = current_term > 0

            if use_multiplier and self.multipliers_used():
                desired_operator = "*"
            elif abs(current_term) > 10 and self.dividers_used():
                desired_operator = "/"
            else:
                desired_operator = "+"

            continue_searching = False
            for card in can_play:
                if card.operator == desired_operator:
                    played_cards.append(card)
                    hand.remove(card)
                    continue_searching = True
                    break

            if len(played_cards) > 0:
                energy -= played_cards[-1].cost
            else:
                break

            can_play = []
            for card in hand:
                if card.cost <= energy:
                    if card not in played_cards:
                        can_play.append(card)

            can_play = sorted(can_play, key=lambda card: card.cost, reverse=True)

            if continue_searching:
                # Update current value and term based on played card
                current_value, current_term = apply_card(played_cards[-1], current_value, current_term)

            #print("played_cards:", played_cards)
            #print("played_cards:", current_value + current_term)

        if len(played_cards) > 0:
            if abs(current_value + current_term) >= abs(self.goal_limit) or not self.only_play_when_able_to_win:
                return played_cards


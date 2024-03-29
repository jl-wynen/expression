import copy

from . import card


def make_deck(plus1=0, mult3=0, div5=0, plus5=0, mult10=0, div10=0, plus10=0):
    # create a test deck
    plus1_card = card.Card("+", 1, 1)

    mult3_card = card.Card("*", 3, 2)
    div5_card = card.Card("/", 5, 2)

    plus5_card = card.Card("+", 5, 3)

    mult10_card = card.Card("*", 10, 4)
    div10_card = card.Card("/", 10, 4)

    plus10_card = card.Card("+", 10, 5)

    start_deck = card.Deck()

    for index in range(plus1):
        start_deck.add_card(copy.copy(plus1_card))

    for index in range(mult3):
        start_deck.add_card(copy.copy(mult3_card))

    for index in range(div5):
        start_deck.add_card(copy.copy(div5_card))

    for index in range(plus5):
        start_deck.add_card(copy.copy(plus5_card))

    for index in range(mult10):
        start_deck.add_card(copy.copy(mult10_card))

    for index in range(div10):
        start_deck.add_card(copy.copy(div10_card))

    for index in range(plus10):
        start_deck.add_card(copy.copy(plus10_card))

    return start_deck

import copy

from . import card
from . import resources

def test_deck():
    # create a test deck
    plus1 = card.Card("+", 1, 1)
    minus1 = card.Card("-", 1, 1)

    mult3 = card.Card("*", 3, 2)
    div2 = card.Card("/", 2, 2)

    plus5 = card.Card("+", 5, 3)
    minus5 = card.Card("-", 5, 3)

    mult10 = card.Card("*", 10, 4)
    div8 = card.Card("/", 8, 4)

    plus10 = card.Card("+", 10, 5)
    minus10 = card.Card("-", 10, 5)

    """
    plus1 = card.Card("+", 1, 1, resource=resources.plus_1_1)
    minus1 = card.Card("-", 1, 1, resource=resources.minus_1_1)

    mult3 = card.Card("*", 3, 2, resource=resources.mult_3_2)
    div2 = card.Card("/", 2, 2, resource=resources.div_2_2)

    plus5 = card.Card("+", 5, 3, resource=resources.plus_5_3)
    minus5 = card.Card("-", 5, 3, resource=resources.minus_5_3)

    mult10 = card.Card("*", 10, 4, resource=resources.mult_10_5)
    div8 = card.Card("/", 8, 4, resource=resources.div_8_4)

    plus10 = card.Card("+", 10, 5, resource=resources.plus_10_5)
    minus10 = card.Card("-", 10, 5, resource=resources.minus_10_5)
    """

    start_deck = card.Deck()

    for index in range(6):
        start_deck.add_card(copy.copy(plus1))
        start_deck.add_card(copy.copy(minus1))

    for index in range(5):
        start_deck.add_card(copy.copy(mult3))
        start_deck.add_card(copy.copy(div2))

    for index in range(4):
        start_deck.add_card(copy.copy(plus5))
        start_deck.add_card(copy.copy(minus5))

    for index in range(3):
        start_deck.add_card(copy.copy(mult10))
        start_deck.add_card(copy.copy(div8))

    for index in range(2):
        start_deck.add_card(copy.copy(plus10))
        start_deck.add_card(copy.copy(minus10))

    return start_deck


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


def give_me_cards():
    cards = []

    plus1 = card.Card("+", 1, 1)
    cards.append(plus1)

    """
    # create a test deck
    plus1 = card.Card("+", 1, 1, filename="plus1.png")
    cards.append(plus1)
    minus1 = card.Card("-", 1, 1, filename="minus1.png")
    cards.append(minus1)

    mult3 = card.Card("*", 3, 2, filename="mult3.png")
    cards.append(plus1)
    div2 = card.Card("/", 2, 2, filename="div2.png")
    cards.append(plus1)

    plus5 = card.Card("+", 5, 3, filename="plus5.png")
    cards.append(plus1)
    minus5 = card.Card("-", 5, 3, filename="minus5.png")
    cards.append(plus1)

    mult10 = card.Card("*", 10, 4, filename="mult10.png")
    cards.append(plus1)
    div8 = card.Card("/", 8, 4, filename="div8.png")
    cards.append(plus1)

    plus10 = card.Card("+", 10, 5, filename="plus10.png")
    cards.append(plus1)
    minus10 = card.Card("-", 10, 5, filename="minus10.png")
    cards.append(plus1)
    """

    return plus1

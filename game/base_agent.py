import random
from . import make_deck

class BaseAgent:
    def __init__(self):
        self.point_limit = None
        self.goal_limit = None
        self.deck = None

        self.name = "BaseAgent"

    def set_goal(self, point_limit, goal_limit):
        self.point_limit = point_limit
        self.goal_limit = goal_limit

    def make_deck(self):
        if self.deck is None:
            raise ValueError("select_cards need to be executed before make_deck")

        deck = make_deck.make_deck(**self.deck)

        if deck.n_cards() < 15:
            raise ValueError("To few cards in deck!")

        return deck


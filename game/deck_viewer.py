import numpy as np
import pyglet

from . import card

class DeckView:
    def __init__(self, top_deck, bottom_deck, batch,
                 player_top_name, player_bottom_name):
        self.top_deck = top_deck
        self.bottom_deck = bottom_deck
        self.batch = batch

        self.active_cards_top = []
        self.active_cards_bottom = []
        self.n_cards_labels = []

        self.player_top_name = player_top_name
        self.player_bottom_name = player_bottom_name

    def setup(self):

        # The current possible cards to choose
        plus1_card = card.Card("+", 1, 1)
        mult3_card = card.Card("*", 3, 2)
        div5_card = card.Card("/", 5, 2)
        plus5_card = card.Card("+", 5, 3)
        mult10_card = card.Card("*", 10, 4)
        div10_card = card.Card("/", 10, 4)
        plus10_card = card.Card("+", 10, 5)

        current_cards = [card.Card("+", 1, 1), card.Card("*", 3, 2),
                         card.Card("/", 5, 2), card.Card("+", 5, 3),
                         card.Card("*", 10, 4), card.Card("/", 10, 4),
                         card.Card("+", 10, 5)]

        card_x_positions = np.linspace(150, 1280 - 150, 7)

        font_size = 20

        y_displace = 150
        y = 600

        number_of_cards_map = {}
        for check_card in current_cards:
            n_of_this = 0
            for a_card in self.top_deck.stack:
                if a_card == check_card:
                    n_of_this += 1

            number_of_cards_map[str(check_card)] = n_of_this

        for this_card, x_pos in zip(current_cards, card_x_positions):
            active_card = card.ActiveCard(card=this_card, batch=self.batch, x=x_pos, y=y, window=None)
            active_card.x = x_pos
            active_card.y = y
            active_card.scale = 0.5

            self.active_cards_top.append(active_card)

            n_cards = number_of_cards_map[str(this_card)]
            n_cards_label = pyglet.text.Label(text=str(n_cards), font_size=font_size,
                                              x=x_pos, y=y - y_displace,
                                              anchor_x='center', anchor_y="center", batch=self.batch,
                                              color=(255, 255, 255, 255))

            self.n_cards_labels.append(n_cards_label)

            if n_cards == 0:
                active_card.opacity = 120

        y = 200

        number_of_cards_map = {}
        for check_card in current_cards:
            n_of_this = 0
            for a_card in self.bottom_deck.stack:
                if a_card == check_card:
                    n_of_this += 1

            number_of_cards_map[str(check_card)] = n_of_this

        for a_card in current_cards:
            if a_card.operator == "+":
                a_card.operator = "-"

        for this_card, x_pos in zip(current_cards, card_x_positions):
            active_card = card.ActiveCard(card=this_card, batch=self.batch, x=x_pos, y=y, window=None)
            active_card.x = x_pos
            active_card.y = y
            active_card.scale = 0.5

            self.active_cards_bottom.append(active_card)

            if this_card.operator == "-":
                this_card.operator = "+"

            n_cards = number_of_cards_map[str(this_card)]
            n_cards_label = pyglet.text.Label(text=str(n_cards), font_size=font_size,
                                              x=x_pos, y=y + y_displace,
                                              anchor_x='center', anchor_y="center", batch=self.batch,
                                              color=(255, 255, 255, 255))

            self.n_cards_labels.append(n_cards_label)

            if n_cards == 0:
                active_card.opacity = 120

        self.player_bottom_name_label = pyglet.text.Label(text="   " + self.player_bottom_name,
                                               font_size=28, x=15, y=30,
                                               anchor_x='left', anchor_y="center", batch=self.batch,
                                               color=(255, 255, 255, 255))

        self.player_top_name_label = pyglet.text.Label(text="   " + self.player_top_name,
                                                       font_size=28, x=15, y=800 - 30,
                                                       anchor_x='left', anchor_y="center", batch=self.batch,
                                                       color=(255, 255, 255, 255))

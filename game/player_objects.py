import copy

from . import util
from . import card
from . import energy_bar


class Hand:
    def __init__(self):
        self.cards = []

    def to_hand(self, card):
        self.cards.append(card)

    def away_from_hand(self, index):
        self.cards.pop(index)

    def return_hand(self):
        return [self.cards[i].card for i in range(len(self.cards)) ]

    def empty_hand(self):
        self.cards = []

    def n_cards(self):
        return len(self.cards)

    def reset(self):
        pass

    def __repr__(self):
        card_string = ""
        for this_card in self.cards:
            card_string += this_card.return_print() + " | "

        return f"Hand object with {len(self.cards)} cards: " + card_string


class ActiveHand:
    def __init__(self, start_pos=None, end_pos=None, max_scale=0.5):

        # Hand of cards
        self.cards = []

        # Information for gui
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.max_scale = max_scale
        self.current_scale = 0.25

    def to_hand(self, card):
        self.cards.append(card)
        self.provide_card_positions()

    def away_from_hand(self, index):
        self.cards.pop(index)
        self.provide_card_positions()

    def empty_hand(self):
        self.cards = []

    def n_cards(self):
        return len(self.cards)

    def return_hand(self):
        return [self.cards[i].card for i in range(len(self.cards)) ]

    def set_positions(self, start_pos, end_pos, max_scale=None):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.max_scale = max_scale

    def provide_card_positions(self):
        hand_direction = self.end_pos - self.start_pos

        if len(self.cards) == 0:
            return
        elif len(self.cards) == 1:
            hand_direction = self.end_pos
        else:
            hand_direction = hand_direction.multiply(1/(len(self.cards)-1))

        desired_card_width = abs(self.end_pos.x - self.start_pos.x)/(len(self.cards) - 0.9)
        current_scale = self.cards[0].scale
        current_width = self.cards[0].width
        new_scale = desired_card_width / current_width * current_scale
        self.current_scale = min([self.max_scale, new_scale])

        for index in range(len(self.cards)):
            card_pos = self.start_pos + hand_direction.multiply(index)
            self.cards[index].set_target(card_pos)
            self.cards[index].scale_goal = self.current_scale

    def reset(self):
        # Need to delete all cards in hand
        pass

    def __repr__(self):
        card_string = ""
        for this_card in self.cards:
            card_string += this_card.return_print()

        return "Hand object: " + card_string


class PlayerObjects:
    def __init__(self, deck, objects=None, batch=None, window=None):
        """
        This class needs to be either only for display or be able
        to turn display off.
        """

        self.original_deck = copy.deepcopy(deck)
        self.deck = deck
        self.discard = card.Deck()

        if objects is not None or batch is not None or window is not None:
            self.active_mode = True
        else:
            self.active_mode = False

        if not self.active_mode:
            self.hand = Hand()
            self.stack = Hand()
        else:

            self.hand = ActiveHand()

            self.objects = objects
            self.batch = batch
            self.window = window

            self.stack = None
            self.stack_position = None

            self.deck_position = None
            self.deck_object = None

            self.discard_position = None
            self.discard_object = None

            self.energy_bar = None

            self.term_text_position = None

            self.commit_circle = None

    def return_hand(self):
        return self.hand.return_hand()

    def return_hand_size(self):
        return self.hand.n_cards()

    def draw_card(self):
        new_card = self.deck.draw_card(self.discard)

        # If no cards available, no cards drawn
        if new_card is None:
            return

        if not self.active_mode:
            self.hand.to_hand(new_card)
        else:
            self.discard_object.update_count(self.discard.n_cards())

            new_sprite = card.ActiveCard(card=new_card, batch=self.batch, window=self.window)
            new_sprite.x = self.deck_position.x
            new_sprite.y = self.deck_position.y
            new_sprite.scale = self.deck_object.scale

            self.objects.append(new_sprite)
            self.hand.to_hand(new_sprite)
            self.deck_object.update_count(self.deck.n_cards())

        return new_card

    def discard_card(self, index):
        discard_card = self.hand.cards[index]
        self.hand.away_from_hand(index)
        self.discard.add_card(discard_card)

        if self.active_mode:
            discard_card.set_target(self.discard_position)
            discard_card.final_target = True
            self.discard_object.update_count(self.discard.n_cards())

    def send_card_to_stack(self, index):
        played_card = self.hand.cards[index]
        self.hand.away_from_hand(index)
        self.stack.to_hand(played_card)

        if self.active_mode:
            self.stack.provide_card_positions()
            played_card.set_target(self.stack_position)
            played_card.to_stack = True
            self.stack.provide_card_positions()

    def send_card_to_stack_ref(self, ref):
        for index, this_card in enumerate(self.hand.cards):
            if this_card is ref:
                self.send_card_to_stack(index)
                return

        raise ValueError("No card with this reference!")

    def send_card_from_stack_to_hand(self, index):
        unplayed_card = self.stack.cards[index]
        self.stack.away_from_hand(index)
        self.hand.to_hand(unplayed_card)

        if self.active_mode:
            self.hand.provide_card_positions()
            #unplayed_card.set_target(self.stack_position)
            unplayed_card.to_stack = False
            self.hand.provide_card_positions()

    def send_card_from_stack_to_hand_ref(self, ref):
        for index, this_card in enumerate(self.stack.cards):
            if this_card is ref:
                self.send_card_from_stack_to_hand(index)
                return

        raise ValueError("No card with this reference!")

    def play_stack(self):
        for played_card in self.stack.cards:
            self.discard.add_card(played_card)

            if self.active_mode:
                played_card.set_target(self.discard_position)
                played_card.to_stack = False
                played_card.final_target = True
                played_card.my_speed = 200
                played_card.scale_goal = self.discard_object.scale
                played_card.scale_speed *= 2.0

        self.stack.empty_hand()

        if self.active_mode:
            self.discard_object.update_count(self.discard.n_cards())

    def play_card(self, index):
        played_card = self.A_hand.cards[index]
        self.hand.away_from_hand(index)

    def shuffle(self):
        self.deck.shuffle()

    def draw_hand(self, n_cards):
        cards = []
        for index in range(n_cards):
            self.draw_card()

        return cards

    def reset(self):
        # Fresh deck
        self.deck = copy.deepcopy(self.original_deck)
        self.deck.shuffle()

        # Clear discard
        self.discard.clear()

        # Empty hand and stack
        self.stack.empty_hand()
        self.hand.empty_hand()

    ##### Methods only called in active mode below this point #####
    def set_hand_position(self, start_pos, end_pos, max_scale=None):
        self.hand.set_positions(start_pos=start_pos, end_pos=end_pos, max_scale=max_scale)

    def set_deck_position(self, pos, count_below=False):
        self.deck_position = pos

        initial_count = self.deck.n_cards()
        self.deck_object = card.DeckVisual(x=self.deck_position.x, y=self.deck_position.y,
                                           window=self.window, batch=self.batch,
                                           initial_count=initial_count, count_below=count_below)

    def set_stack_position(self, pos, width=100, max_scale=0.6):
        if not isinstance(pos, util.Point):
            pos = util.Point(pos)

        self.stack_position = pos
        displacement_start = util.Point(-width//2, 0)
        displacement_end = util.Point(width//2, 0)
        self.stack = ActiveHand(pos + displacement_start, pos + displacement_end,
                                max_scale=max_scale)

    def set_commit_circle(self, commit_circle):
        self.commit_circle = commit_circle

    def set_term_position(self, pos):
        self.term_text_position = pos

    def set_discard_position(self, pos, count_below=False):
        self.discard_position = pos

        initial_count = self.discard.n_cards()
        self.discard_object = card.DeckVisual(x=self.discard_position.x, y=self.discard_position.y,
                                              window=self.window, batch=self.batch, count_enabled=False,
                                              initial_count=initial_count, count_below=count_below)

    def set_energy_max(self, new_max):
        if self.active_mode:
            self.energy_bar.set_new_maximum(new_max)

    def set_energy_bar_position(self, start_pos, end_pos):
        self.energy_bar = energy_bar.EnergyBar(batch=self.batch, start_pos=start_pos, end_pos=end_pos)


import math
import copy

from . import player_objects


class Game:
    def __init__(self, point_limit, positive_player, negative_player):
        # Set up a game
        self.point_limit = point_limit
        self.current_value = 0.0
        self.current_term = 0.

        # Statistics saved
        self.score_history = []
        self.term_history = []
        self.positive_hand_history = []
        self.positive_energy_spent = []
        self.negative_hand_history = []
        self.negative_energy_spent = []

        self.positive_player = positive_player
        self.positive_player.set_goal(self.point_limit)
        self.positive_player.set_recorders(positive_hand_history=self.positive_hand_history,
                                           positive_energy_spent=self.positive_energy_spent,
                                           negative_hand_history=self.negative_hand_history,
                                           negative_energy_spent=self.negative_energy_spent)

        self.negative_player = negative_player
        self.negative_player.set_goal(-1*self.point_limit)
        self.negative_player.set_recorders(positive_hand_history=self.positive_hand_history,
                                           positive_energy_spent=self.positive_energy_spent,
                                           negative_hand_history=self.negative_hand_history,
                                           negative_energy_spent=self.negative_energy_spent)

        self.current_player = self.positive_player
        self.other_player = self.negative_player

        self.expression = ""
        self.turn = 0
        self.last_hand = []

        self.game_over = False
        self.resources_left = None

    def apply_card(self, card):
        old_value = self.current_value + self.current_term
        # Assume card is of card class
        if card.operator == "+":
            self.current_value += self.current_term
            self.current_term = card.value
        elif card.operator == "-":
            self.current_value += self.current_term
            self.current_term = -1*card.value
        elif card.operator == "*":
            self.current_term *= card.value
        elif card.operator == "/":
            self.current_term /= card.value
        else:
            print("Error, unknown operator: ", end="")
            print(card.operator)

        self.expression += card.operator
        self.expression += str(card.value)

        """
        print("Card applied: ", end="")
        card.print()
        print("")

        #print(self.expression)

        print("Value went from " + str(old_value) + " to "
              + str(self.current_value + self.current_term) + "!")
        """

    def switch_current_player(self):

        # Switch between which player is active
        if self.current_player is self.positive_player:
            self.current_player = self.negative_player
            self.other_player = self.positive_player
        else:
            self.current_player = self.positive_player
            self.other_player = self.negative_player

    def setup_game(self):
        self.positive_player.reset(5)
        self.negative_player.reset(5)

    def ready_turn(self):

        # Balance first and second player by giving an energy sooner to second player (positive)
        if self.current_player.is_negative:
            gain_turn = [0, 1, 3, 6, 9, 12, 15, 18, 21, 24]
        else:
            # Get a resource earlier, back on normal track after
            gain_turn = [0, 1, 3, 6, 8, 12, 15, 18, 21, 24]

        gain_this_turn = self.current_player.turn_number in gain_turn

        # increase energy
        self.current_player.turn_number += 1

        if self.current_player.max_resources < 10 and gain_this_turn:
            self.current_player.increment_max_resources()

        # Give the second player a faster energy increase
        #if self.turn == 1:
        #    self.current_player.increment_max_resources()

        self.resources_left = self.current_player.max_resources

        # draw card
        if self.turn != -1:
            self.current_player.po.draw_card()

        self.turn += 1

    def take_turn(self):

        # Assemble game_info
        game_info = dict(turn_number=self.turn,
                         n_opponent_cards=self.other_player.get_hand_size(),
                         last_played_hand=self.last_hand)
                         # Could add info on score

        safe_game_info = copy.copy(game_info)
        safe_current_value = copy.copy(self.current_value)
        safe_current_term = copy.copy(self.current_term)

        # Select cards to play
        played_card_indices = self.current_player.turn(current_value=safe_current_value,
                                                       current_term=safe_current_term,
                                                       game_info=safe_game_info)

        self.last_hand = []
        if played_card_indices is not None:
            # Get card objects and apply to stack
            hand = self.current_player.po.hand.cards
            played_cards = []
            for index in played_card_indices:
                played_card = hand[index]
                self.apply_card(played_card)
                played_cards.append(played_card)
                self.resources_left -= played_card.cost

            for card in played_cards:
                self.current_player.po.send_card_to_stack_ref(card)
                self.last_hand.append(card.return_simple_copy())

        total_value = self.current_value + self.current_term
        if abs(total_value) >= self.point_limit:
            self.game_over = True

        self.score_history.append(total_value)
        self.term_history.append(self.current_term)

    def take_turn_human_gui(self):

        for card_element in self.current_player.po.stack.cards:
            self.apply_card(card_element)

        total_value = self.current_value + self.current_term
        if abs(total_value) >= self.point_limit:
            self.game_over = True

    def empty_stack(self):
        self.current_player.po.play_stack()

    def full_turn(self):
        # Loop this with while not game.game_over to play
        self.switch_current_player()
        self.ready_turn()
        self.take_turn()
        self.empty_stack()


    """
    def start_game(self):
        # Play a game!

        # Opening hand with N cards
        self.positive_player.reset(1)
        self.negative_player.reset(1)

        while abs(self.current_value + self.current_term) < self.point_limit:
            # Alternate between giving each player a turn

            print(self.expression)
            played_cards = self.current_player.turn(self.current_value)

            for card in played_cards:
                self.apply_card(card)

            self.switch_current_player()

        if self.current_value + self.current_term > self.point_limit:
            print("Positive player won!")
        else:
            print("Negative player won!")
    """
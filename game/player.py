import copy

from . import card
from . import player_objects
from . import make_deck


class AnswerChecker:
    def __init__(self, hand, energy):
        self.cards = hand
        self.energy = energy
        self.played_indices = []
        self.max_resources = energy

    def check_answer(self, agent_answer):
        if isinstance(agent_answer, int):
            if abs(agent_answer) > len(self.cards):
                raise ValueError("Agent asked to play integer outside hand size")

            if agent_answer in self.played_indices:
                raise ValueError("Agent already played this card")

            played_card_index = agent_answer
            self.played_indices.append(played_card_index)

        elif isinstance(agent_answer, (card.Card, card.ActiveCard)):
            found = False
            for index, check_card in enumerate(self.cards):
                if card.cards_equal(check_card, agent_answer) and index not in self.played_indices:
                    played_card_index = index
                    self.played_indices.append(played_card_index)
                    found = True
                    break

            if not found:
                raise ValueError("Agent tried to play card they did not have")

        else:
            raise ValueError("agent didn't return card / integer index")

        self.energy -= self.cards[played_card_index].cost
        if self.energy < 0:
            print(agent_answer, "max resources: ", self.max_resources)
            raise ValueError("Agent tried to play cards for more resource than available")

        return played_card_index


class Player:
    def __init__(self, name, deck, is_negative, agent=None, objects=None, batch=None, window=None):
        self.agent = agent

        if self.agent is None:
            self.name = name
        else:
            self.name = self.agent.name

        self.is_negative = bool(is_negative)

        self.goal_limit = None

        self.max_resources = 0
        self.turn_number = 0

        if self.is_negative:
            # All decks are made as if positive, if the player is negative, flip it
            deck.make_negative()

        self.po = player_objects.PlayerObjects(deck, objects=objects, batch=batch, window=window)

        self.positive_hand_history = None
        self.positive_energy_spent = None
        self.negative_hand_history = None
        self.negative_energy_spent = None

    def set_recorders(self, positive_hand_history, positive_energy_spent,
                      negative_hand_history, negative_energy_spent):

        self.positive_hand_history = positive_hand_history
        self.positive_energy_spent = positive_energy_spent

        self.negative_hand_history = negative_hand_history
        self.negative_energy_spent = negative_energy_spent

    def record_hand_size(self, hand_size):
        if self.is_negative:
            self.negative_hand_history.append(hand_size)
        else:
            self.positive_hand_history.append(hand_size)

    def record_energy_spent(self, energy_spent):
        if self.is_negative:
            self.negative_energy_spent.append(energy_spent)
        else:
            self.positive_energy_spent.append(energy_spent)

    def set_hand_positions(self, start_pos, end_pos, max_scale=None):
        self.po.set_hand_position(start_pos=start_pos, end_pos=end_pos, max_scale=max_scale)

    def set_goal(self, goal_limit):
        self.goal_limit = goal_limit
        if self.agent is not None:
            self.agent.set_goal(point_limit=abs(goal_limit), goal_limit=goal_limit)

    def reset(self, n_cards):
        self.max_resources = 0
        self.turn_number = 0
        self.po.reset()
        self.po.draw_hand(n_cards)

    def set_max_resources(self, max_energy):
        self.max_resources = max_energy
        self.po.set_energy_max(max_energy)

    def increment_max_resources(self):
        self.set_max_resources(self.max_resources + 1)

    def get_hand_size(self):
        return self.po.return_hand_size()

    def turn(self, current_value, current_term, game_info={}):
        if self.agent is None:
            return self.turn_terminal(current_value, current_term)
        else:
            return self.turn_AI(current_value, current_term, game_info)

    def turn_AI(self, current_value, current_term, game_info):

        given_hand = []
        for card_element in self.po.hand.cards:
            given_hand.append(card_element.return_simple_copy())

        reference_hand = copy.copy(given_hand)
        energy = copy.copy(self.max_resources)

        self.record_hand_size(len(given_hand))

        # Exchange negative cards to positive
        if self.is_negative:
            for card_element in given_hand:
                if card_element.operator == "-":
                    card_element.operator = "+"

            # Provide opposite score too
            current_value = -current_value
            current_term = -current_term

            # Ensure last hand looks like a negative players
            if "last_played_hand" in game_info:
                for card_element in game_info["last_played_hand"]:
                    card_element.make_negative()

        agent_answer = self.agent.play_turn(hand=given_hand, energy=energy, game_info=game_info,
                                            current_value=current_value, current_term=current_term)

        if agent_answer is None:
            self.record_energy_spent(0)
            return

        # Exchange positive cards back to negative
        if self.is_negative:
            for card_element in agent_answer:
                if isinstance(card_element, (card.Card, card.ActiveCard)):
                    if card_element.operator == "+":
                        card_element.operator = "-"

        checker = AnswerChecker(reference_hand, self.max_resources)
        played_cards = []
        if not isinstance(agent_answer, list):
            played_cards.append(checker.check_answer(agent_answer))
        else:
            for answer in agent_answer:
                played_cards.append(checker.check_answer(answer))

        self.record_energy_spent(self.max_resources - checker.energy)

        return played_cards

    def turn_terminal(self, current_value, current_term):
        """
        Turn with terminal interface
        """

        print(self.name + ", make your play, you have "
              + str(self.max_resources) + " resources available.")
        print("Your goal limit is: " + str(self.goal_limit))

        print("Displaying hand:")

        current_hand = self.po.return_hand()
        for card_number, card in enumerate(current_hand):
            print("Card nr " + str(card_number) + ":", end="")
            card.print()
            print("")

        allowed_play = False
        while not allowed_play:
            play = input()
            play_cost = 0
            try:
                played_cards = []
                if play == "":
                    allowed_play = True # allow skipping your turn by not playing a card
                else:
                    indices = play.split(",")
                    for index in indices:
                        index = int(index)
                        if index in played_cards:
                            print("You can't play the same card twice")
                            raise ValueError("Playing a card twice")
                        played_cards.append(index)
                        play_cost += current_hand[index].cost

                    if play_cost <= self.max_resources:
                        allowed_play = True
                    else:
                        print("The total cost of this play is " + str(play_cost)
                              + " yet only " + str(self.max_resources) + " are available. Try again.")

            except:
                allowed_play = False
                print("Input not understood or invalid, try again.")

        cards_to_play = []
        for index in played_cards:
            cards_to_play.append(current_hand[index])

        return cards_to_play

import copy
import random
import json

from game import player
from game import engine
from game import make_deck
from game import template_AI


def run_expression_terminal(n_runs=2000, verbose=False, pause=True, save=True,
                            top_agent=None, bottom_agent=None):
    # Make decks
    if top_agent is None:
        top_agent = template_AI.template_AI_A()

    top_agent.select_cards()
    top_deck = top_agent.make_deck()

    if bottom_agent is None:
        bottom_agent = template_AI.template_AI_B()

    bottom_agent.select_cards()
    bottom_deck = bottom_agent.make_deck()

    player_top = player.Player("positive", copy.deepcopy(top_deck), is_negative=False, agent=top_agent)
    player_bottom = player.Player("negatives", copy.deepcopy(bottom_deck), is_negative=True, agent=bottom_agent)

    player_top_score = player_bottom_score = 0

    game_histories = []
    detailed_game_histories = []

    for _ in range(n_runs):
        game = engine.Game(100.0, player_top, player_bottom)

        game.setup_game()

        while not game.game_over:

            game.switch_current_player()
            c_player = game.current_player

            if verbose:
                print("")
                print(f"{c_player.name}'s turn")
                print(f"hand: {c_player.po.hand.n_cards()} deck: {c_player.po.deck.n_cards()} discard: {c_player.po.discard.n_cards()} stack: {c_player.po.stack.n_cards()}")
                #print(f"total cards: {c_player.po.deck.n_cards() + c_player.po.discard.n_cards() + c_player.po.hand.n_cards()}")

            game.ready_turn()
            if verbose:
                print(f"energy: {c_player.max_resources} {c_player.po.hand}")

            game.take_turn()
            if verbose:
                print(f"Played: {c_player.po.stack}")

            game.empty_stack()
            if verbose:
                print("expression: \t", game.current_value + game.current_term, "\t = ", game.expression)
                if pause:
                    input()

        if (game.current_value + game.current_term) > game.point_limit:
            player_top_score += 1
            #print(f"Positive player won {player_top_score}:{player_bottom_score}")
        else:
            player_bottom_score += 1
            #print(f"Negative player won {player_top_score}:{player_bottom_score}")

        game_histories += [game.score_history]
        detailed_history = dict(score=game.score_history, term=game.term_history,
                                positive_hand_size=game.positive_hand_history,
                                positive_energy_spent=game.positive_energy_spent,
                                negative_hand_size=game.negative_hand_history,
                                negative_energy_spent=game.negative_energy_spent)

        detailed_game_histories.append(detailed_history)

    if save:
        with open("data.json", "w") as f:
            json.dump(detailed_game_histories, f)

    return player_top_score, player_bottom_score, detailed_game_histories


if __name__ == "__main__":
    run_expression_terminal(n_runs=5, verbose=True)


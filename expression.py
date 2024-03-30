import copy
import random

import pyglet
from pyglet.window import key
from pyglet.shapes import Circle

from game import card
from game import player
from game import engine
from game import make_deck
from game import util
from game import player_objects
from game import graph
from game import moving_text
from game.bracket import DoubleBracket
from game.deck_viewer import DeckView

from contestants import template_fast
from contestants import template_reckless


def run_expression(game_window, score_limit=2, tournament_state=None, match_number=None,
                   negative_player=None, negative_deck=None,
                   positive_player=None, positive_deck=None,
                   auto_play_input=False):

    #inputs_global
    global global_negative_player, global_positive_player, global_negative_deck, global_positive_deck
    global_negative_player = negative_player
    global_negative_deck = negative_deck
    global_positive_player = positive_player
    global_positive_deck = positive_deck

    global global_tournament_state, global_match_number
    global_tournament_state = tournament_state
    global_match_number = match_number

    # Set up game window
    #game_window = pyglet.window.Window(1280, 800)

    # Solid background color, grey
    R,G,B,A = 30,30,30,255
    image = pyglet.image.SolidColorImagePattern((R,G,B,A)).create_image(1280, 800)

    main_batch = pyglet.graphics.Batch()
    text_batch = pyglet.graphics.Batch()
    bracket_batch = pyglet.graphics.Batch()
    deck_view_batch = pyglet.graphics.Batch()

    global player_top_score, player_bottom_score, global_score_limit
    global_score_limit = score_limit
    player_top_score = 0
    player_bottom_score = 0

    global turn_time, turn_time_left, stack_time, stack_time_left, card_speed, card_scale_speed
    turn_time = 1.0
    turn_time_left = 2.5 # Setting first turn to be longer
    stack_time = 0.5
    stack_time_left = stack_time
    card_speed = 200
    card_scale_speed = 0.15

    expression_text = pyglet.text.Label(text="", font_size=30,
                                        x=game_window.width // 2, y=game_window.height // 2,
                                        anchor_x='right', anchor_y="center", batch=text_batch)

    """
    expression_evaluation_text = pyglet.text.Label(text=" = 0", font_size=30,
                                                   x=game_window.width // 2, y=game_window.height // 2,
                                                   anchor_x='left', anchor_y="center")
    """
    expression_evaluation_text = pyglet.text.Label(text=" = 0", font_size=30,
                                                   x=1050, y=game_window.height // 2,
                                                   anchor_x='left', anchor_y="center", batch=text_batch)

    term_text = moving_text.MovingText(text="", font_size=30,
                                       x=900, y=game_window.height // 2,
                                       anchor_x='center', anchor_y="center", batch=text_batch)

    one_graph = False

    if one_graph:
        graph_instance = graph.Graph(x_axis_length=300, x_axis_max=20,
                                     y_axis_length=300, y_axis_max=100,
                                     batch=main_batch, origin=(50, 50), rolling=True)
    else:
        center_y = 800//2
        x_start = 20 #400
        y_length=300
        split = 80
        graph_top = graph.Graph(x_axis_length=500, x_axis_max=20.5,
                                y_axis_length=y_length, y_axis_max=100,
                                axis_width=2, bar=True, rolling=True,
                                origin=(x_start, center_y + split // 2),
                                line_width=10, line_color=(100, 100, 255),
                                batch=main_batch)

        graph_bottom = graph.Graph(x_axis_length=500, x_axis_max=20.5,
                                   y_axis_length=-y_length, y_axis_max=-100,
                                   axis_width=2, bar=True, rolling=True,
                                   origin=(x_start, center_y-split//2),
                                   line_width=10, line_color=(255, 100, 100),
                                   batch=main_batch)

    global positive_player_won, negative_player_won, game_over_timer
    positive_player_won = negative_player_won = False
    game_over_timer = None
    positive_win_label = pyglet.text.Label('Positive player Wins!',
                                           font_name='Times New Roman',
                                           font_size=42,
                                           x=game_window.width // 2, y=2*game_window.height // 3,
                                           anchor_x='center', anchor_y='center',
                                           color=(255, 255, 255, 255))

    negative_win_label = pyglet.text.Label('Negative player Wins!',
                                           font_name='Times New Roman',
                                           font_size=42,
                                           x=game_window.width // 2, y=game_window.height // 3,
                                           anchor_x='center', anchor_y='center',
                                           color=(255, 255, 255, 255))

    global game_objects
    game_objects = []

    def init():
        reset_board()

    def reset_board():

        global time
        time = 0

        global game_objects
        for obj in game_objects:
            obj.delete()
        game_objects = []

        global player_top_score, player_bottom_score
        if player_top_score == global_score_limit or player_bottom_score == global_score_limit:
            pyglet.clock.unschedule(update)
            pyglet.app.exit()

        # Reset visual elements
        expression_text.text = ""
        expression_evaluation_text.text = " = 0"
        term_text.text = ""

        if one_graph:
            graph_instance.clear()
        else:
            graph_top.clear()
            graph_bottom.clear()

        # Human interactable info
        global commit_pressed, circle_on_color, circle_off_color
        commit_pressed = False
        circle_off_color = (180, 180, 180)
        circle_on_color = (255, 153, 25)

        global player_top_name, player_bottom_name

        # Stack info
        x_stack = 0.5*(expression_text.x + expression_evaluation_text.x)
        stack_position = util.Point(x_stack, 407)
        stack_width = 0.5*(expression_evaluation_text.x - expression_text.x)
        stack_max_scale = 0.5

        # Initialize players
        global global_negative_player, global_positive_player, global_negative_deck, global_positive_deck

        # top
        if global_positive_player is not None:
            top_agent = global_positive_player
            top_agent.select_cards()
            global_positive_deck = top_agent.make_deck()
        elif global_positive_deck is None:
            tmp_agent = template_fast.Agent()
            tmp_agent.select_cards()
            global_positive_deck = tmp_agent.make_deck()

        player_top = player.Player("Human positive", copy.deepcopy(global_positive_deck), is_negative=False,
                                   agent=global_positive_player,
                                   objects=game_objects, batch=main_batch, window=game_window)

        s_pos = util.Point(1280 - 100, 800-170)
        e_pos = util.Point(1280 - 700, 800-100)
        player_top.set_hand_positions(start_pos=s_pos, end_pos=e_pos, max_scale=0.3)

        player_top.po.set_deck_position(util.Point(1280 - 700, 550), count_below=True)
        player_top.po.set_discard_position(util.Point(1280 - 100, 500), count_below=True)
        player_top.po.set_stack_position(stack_position, width=stack_width, max_scale=stack_max_scale)
        player_top.po.set_term_position(util.Point(900, 550))
        s_pos = util.Point(1280 - 400, 800 -30)
        e_pos = util.Point(1280 - 50, 800 - 60)
        player_top.po.set_energy_bar_position(s_pos, e_pos)
        top_circle = Circle(1280, 800, 40, color=circle_off_color, batch=main_batch)

        if player_top.agent is None:
            top_circle.opacity = 225
        else:
            top_circle.opacity = 0

        player_top.po.set_commit_circle(top_circle)

        player_top_name = pyglet.text.Label(text=str(player_top_score) + " "+ player_top.name, font_size=28,
                                            x=15, y=800-30,
                                            anchor_x='left', anchor_y="center", batch=text_batch,
                                            color=(255, 255, 255, 255))
        positive_win_label.text = f"Positive player: {player_top.name} won!"

        # bottom
        if global_negative_player is not None:
            bottom_agent = global_negative_player
            bottom_agent.select_cards()
            global_negative_deck = bottom_agent.make_deck()
        elif global_negative_deck is None:
            tmp_agent = template_reckless.Agent()
            tmp_agent.select_cards()
            global_negative_deck = tmp_agent.make_deck()

        player_bottom = player.Player("Human negative", copy.deepcopy(global_negative_deck), is_negative=True,
                                      agent=global_negative_player,
                                      objects=game_objects, batch=main_batch, window=game_window)
        s_pos = util.Point(1280 - 100, 170)
        e_pos = util.Point(1280 - 700, 100)
        player_bottom.set_hand_positions(start_pos=s_pos, end_pos=e_pos, max_scale=0.3)

        player_bottom.po.set_deck_position(util.Point(1280 - 700, 250))
        player_bottom.po.set_discard_position(util.Point(1280 - 100, 300))
        player_bottom.po.set_stack_position(stack_position, width=stack_width, max_scale=stack_max_scale)
        player_bottom.po.set_term_position(util.Point(900, 250))
        s_pos = util.Point(1280 - 400, 30)
        e_pos = util.Point(1280 - 50, 60)
        player_bottom.po.set_energy_bar_position(s_pos, e_pos)
        bottom_circle = Circle(1280, 0, 40, color=circle_off_color, batch=main_batch)

        if player_bottom.agent is None:
            bottom_circle.opacity = 225
        else:
            bottom_circle.opacity = 0

        player_bottom.po.set_commit_circle(bottom_circle)

        player_bottom_name = pyglet.text.Label(text=str(player_bottom_score) + " "+ player_bottom.name,
                                               font_size=28, x=15, y=30,
                                               anchor_x='left', anchor_y="center", batch=text_batch,
                                               color=(255, 255, 255, 255))
        negative_win_label.text = f"Negative player: {player_bottom.name} won!"

        """
        player_top.po.set_deck_position(util.Point(800, 700))
        player_top.po.set_discard_position(util.Point(100, 500))
        player_top.po.set_stack_position(util.Point(1280 // 2, 800 // 2))

        player_bottom.po.set_deck_position(util.Point(1280 - 800, 100))
        player_bottom.po.set_discard_position(util.Point(1280 - 100, 800 - 500))
        player_bottom.po.set_stack_position(util.Point(1280 // 2, 800 // 2))
        """

        """
        if global_tournament_state is not None:
            print("given tournament state")
            print(global_tournament_state)
            print("*" * 50)
        """

        # bracket
        global bracket, bracket_mode, global_match_number
        bracket = DoubleBracket(tournament_state=global_tournament_state,
                                batch=bracket_batch, match_number=global_match_number)
        bracket.setup()
        bracket.update_with_state()
        if tournament_state is not None and player_top_score == 0 and player_bottom_score == 0:
            bracket_mode = True
        else:
            bracket_mode = False

        # deck viewer
        global deck_viewer, deck_mode
        deck_viewer = DeckView(global_positive_deck, global_negative_deck, deck_view_batch,
                               player_top_name=player_top.name, player_bottom_name=player_bottom.name)
        deck_viewer.setup()
        deck_mode = False

        # Start a game
        global game
        game = engine.Game(100.0, player_top, player_bottom)
        game.setup_game()

        # continue_turn: used to manually click through turns
        # turn_ready: False while time counts down to next action or cards still moving
        # took_turn: Set to True after player took action (which sets drew_card to False)
        # drew_card: Set to True after player drew their card (which sets took_turn to False)

        global turn_ready, continue_turn, took_turn, drew_card, auto_play
        turn_ready = drew_card = False
        took_turn = True

        # Set these to False to have default mode being manual
        auto_play = continue_turn = auto_play_input

    @game_window.event
    def on_mouse_press(x, y, button, modifiers):
        global game_objects, commit_pressed

        for game_object in game_objects:
            if isinstance(game_object, card.ActiveCard):
                pressed_this_card = game_object.mouse_position_on_card(x, y, button, modifiers)

        circle = game.current_player.po.commit_circle
        circle_pos = util.Point(circle.x, circle.y)
        if circle_pos.distance_to(util.Point(x, y)) < circle.radius:
            commit_pressed = True

    @game_window.event
    def on_key_press(symbol, modifiers):
        global continue_turn, auto_play, turn_time, stack_time, card_speed, card_scale_speed
        global bracket_mode, bracket, deck_mode

        if symbol == key.SPACE:
            continue_turn = True

        if symbol == key.B:
            bracket_mode = not bracket_mode

            if bracket.tournament_state is None:
                bracket_mode = False

        if symbol == key.D:
            deck_mode = not deck_mode

        if symbol == key.ENTER:
            auto_play = not auto_play

            if auto_play:
                if not continue_turn:
                    continue_turn = True
            else:
                continue_turn = False

        if symbol == key.UP:
            turn_time += 0.5
            stack_time += 0.5

        if symbol == key.DOWN:
            if turn_time >= 1.0:
                turn_time -= 0.5
            if stack_time >= 1.0:
                stack_time -= 0.5

        if symbol == key.RIGHT:
            card_speed *= 1.1
            card_scale_speed *= 1.1

        if symbol == key.LEFT:
            card_speed *= 0.9
            card_scale_speed *= 0.9


    @game_window.event
    def on_draw():
        game_window.clear()

        # Draw background
        image.blit(0, 0)

        global bracket, bracket_mode, deck_mode

        if deck_mode:
            deck_view_batch.draw()
            return

        if bracket_mode:
            bracket_batch.draw()
            return

        if one_graph:
            graph_instance.draw()
        else:
            graph_top.draw()
            graph_bottom.draw()

        #expression_text.draw()
        #expression_evaluation_text.draw()
        #term_text.draw()
        text_batch.draw()
        main_batch.draw()

        global positive_player_won, negative_player_won
        if positive_player_won:
            positive_win_label.draw()
        if negative_player_won:
            negative_win_label.draw()

    def update(dt):
        global player_top_score, player_bottom_score, time

        global time, turn_time, stack_time, stack_time_left, turn_time_left, card_speed, card_scale_speed
        global turn_ready, continue_turn, took_turn, drew_card
        global negative_player_won, positive_player_won, game_over_timer
        global commit_pressed, circle_on_color, circle_off_color
        global bracket, bracket_mode, deck_mode

        wait_for_human = False

        if bracket_mode or deck_mode:
            return

        time += dt

        if turn_ready:
            turn_time_left -= dt

        if turn_time_left < 0 and turn_ready and continue_turn and took_turn:
            game.switch_current_player()
            term_text.target_pos = game.current_player.po.term_text_position
            game.ready_turn()
            game.current_player.po.energy_bar.set_used(game.current_player.max_resources)

            turn_time_left = turn_time
            took_turn = False
            drew_card = True
            if not auto_play:
                continue_turn = False

        if turn_time_left < 0 and turn_ready and continue_turn and drew_card:
            if game.current_player.agent is None:
                # Human player
                wait_for_human = True
                game.current_player.po.commit_circle.color = circle_on_color
                if commit_pressed:
                    # Execute stack
                    commit_pressed = False
                    game.take_turn_human_gui()

                    wait_for_human = False
                    game.current_player.po.commit_circle.color = circle_off_color
                    turn_ready = drew_card = False
                    took_turn = True
                    turn_time_left = turn_time
                    if not auto_play:
                        continue_turn = False

                else:
                    # Prepare stack
                    player_resources = game.current_player.max_resources
                    stack_cost = 0  # Tally up current cards on stack
                    for card_element in game.current_player.po.stack.cards:
                        stack_cost += card_element.cost

                    for card_element in game.current_player.po.hand.cards:
                        if card_element.card_pressed:
                            if card_element.cost <= player_resources - stack_cost:
                                game.current_player.po.send_card_to_stack_ref(card_element)
                            card_element.reset_card_pressed()

                    for card_element in game.current_player.po.stack.cards:
                        if card_element.card_pressed:
                            game.current_player.po.send_card_from_stack_to_hand_ref(card_element)
                            card_element.reset_card_pressed()

                    game.current_player.po.energy_bar.set_used(player_resources - stack_cost)

            else:
                # AI player
                game.take_turn()
                game.current_player.po.energy_bar.set_used(game.resources_left)

                turn_ready = drew_card = False
                took_turn = True
                turn_time_left = turn_time
                if not auto_play:
                    continue_turn = False

        object_towards_stack = False
        object_towards_discard = False
        object_on_stack = False
        for obj in game_objects:
            if isinstance(obj, card.ActiveCard):

                # update card speed with left / right arrow
                obj.my_speed = card_speed
                obj.scale_speed = card_scale_speed

                if obj.target_pos is not None:
                    if obj.to_stack:
                        object_towards_stack = True

                    if obj.final_target:
                        object_towards_discard = True

                else:
                    if obj.to_stack:
                        object_on_stack = True

                if obj.reached_final_target:
                    obj.delete()
                    game_objects.remove(obj)

        term_text.update(dt)
        for obj in game_objects:
            obj.update(dt)

        if object_on_stack and not object_towards_stack and not object_towards_discard and not wait_for_human:
            stack_time_left -= dt

            game_finished = positive_player_won or negative_player_won
            if stack_time_left < 0 and continue_turn and not game_finished:
                stack_time_left = stack_time
                if not auto_play:
                    continue_turn = False

                if not game.game_over:
                    game.empty_stack()

                if game.current_term > 0:
                    sign_text = "+"
                else:
                    sign_text = ""
                expression_text.text = game.expression

                evaluation = game.current_value + game.current_term
                expression_evaluation_text.text = " = " + f"{evaluation:.1f}"
                term_text.text = sign_text + f"{game.current_term:.1f}"
                term_text.opacity = 0
                term_text.target_pos = game.other_player.po.term_text_position

                if one_graph:
                    graph_instance.add_point(game.turn, evaluation)
                else:
                    if evaluation > 0:
                        graph_top.add_point(game.turn, evaluation)
                        graph_bottom.add_point(game.turn, 0)
                    else:
                        graph_top.add_point(game.turn, 0)
                        graph_bottom.add_point(game.turn, evaluation)

                if game.game_over:
                    turn_ready = False  # Stops game
                    if (game.current_value + game.current_term) > 0:
                        # positive player won
                        positive_player_won = True
                        player_top_score += 1
                    else:
                        # negative player won
                        negative_player_won = True
                        player_bottom_score += 1

                    if game_over_timer is None:
                        game_over_timer = 10

        elif not object_towards_stack and not object_towards_discard and not wait_for_human:
            turn_ready = True

        if game_over_timer is not None:
            if auto_play:
                game_over_timer -= dt

            if game_over_timer < 0 or (not auto_play and continue_turn):
                game_over_timer = None
                negative_player_won = positive_player_won = False
                reset_board()

    #####################################################################################
    #                                RUNNING THE GAME                                   #
    #####################################################################################


    init()
    pyglet.clock.schedule_interval(update, 1/30.0)
    pyglet.app.run()

    print("final score = " + str(player_top_score) + " - " + str(player_bottom_score))

    return [player_top_score, player_bottom_score]

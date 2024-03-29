import pyglet

from expression import run_expression
from game import make_deck

from contestants import template_careful, template_reckless, template_fast

custom_deck = make_deck.make_deck(plus1=8, mult3=6, div5=4, plus5=4, mult10=4, div10=2, plus10=2)

game_window = pyglet.window.Window(1280, 800)
result = run_expression(game_window=game_window,
                        positive_player=template_reckless.Agent(), # If None, human can play top player
                        positive_deck=custom_deck, # Only used when humans play
                        negative_player=template_fast.Agent(), # If None, human can play bottom player
                        negative_deck=None, # Only used when humans play
                        auto_play_input=True # Runs game automatically, if False step through with spacebar
                        )

import pyglet

from expression import run_expression

from contestants import template_careful, template_reckless, template_fast

game_window = pyglet.window.Window(1280, 800)
result = run_expression(game_window=game_window,
                        positive_player=template_reckless.Agent(),
                        negative_player=template_fast.Agent())

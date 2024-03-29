import pyglet

from . import card
from . import make_deck

def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

#pyglet.resource.path = ['../resources']
pyglet.resource.path = ['resources']
pyglet.resource.reindex()

"""
list = make_deck.test_deck()
for card in cards:
    card.resource = pyglet.resource.image(card.filename)
    center_image(card.resource)
"""

card_back = pyglet.resource.image("back.png")
center_image(card_back)

plus_1_1 = pyglet.resource.image("plus1.png")
center_image(plus_1_1)
minus_1_1 = pyglet.resource.image("minus1.png")
center_image(minus_1_1)

mult_3_2 = pyglet.resource.image("mult3.png")
center_image(mult_3_2)
div_5_2 = pyglet.resource.image("div5.png")
center_image(div_5_2)

plus_5_3 = pyglet.resource.image("plus5.png")
center_image(plus_5_3)
minus_5_3 = pyglet.resource.image("minus5.png")
center_image(minus_5_3)

mult_10_4 = pyglet.resource.image("mult10.png")
center_image(mult_10_4)
div_10_4 = pyglet.resource.image("div10.png")
center_image(div_10_4)

plus_10_5 = pyglet.resource.image("plus10.png")
center_image(plus_10_5)
minus_10_5 = pyglet.resource.image("minus10.png")
center_image(minus_10_5)

mult_m1_6 = pyglet.resource.image("reverse.png")
center_image(mult_m1_6)

card_art = {}
card_art[("+", 1, 1)] = plus_1_1
card_art[("-", 1, 1)] = minus_1_1
card_art[("*", 3, 2)] = mult_3_2
card_art[("/", 5, 2)] = div_5_2
card_art[("+", 5, 3)] = plus_5_3
card_art[("-", 5, 3)] = minus_5_3
card_art[("*", 10, 4)] = mult_10_4
card_art[("/", 10, 4)] = div_10_4
card_art[("+", 10, 5)] = plus_10_5
card_art[("-", 10, 5)] = minus_10_5

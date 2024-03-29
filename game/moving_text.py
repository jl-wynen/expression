import pyglet
from . import util


class MovingText(pyglet.text.Label):

    def __init__(self, *args, my_speed=300, **kwargs):
        super(MovingText, self).__init__(*args, **kwargs)

        self.my_speed = my_speed
        self.target_pos = None
        self.alpha_decrease_speed = 800
        self.alpha_distance_threshold = 100

    def update(self, dt):

        if self.target_pos is None:
            self.opacity = 255
        else:
            current_pos = util.Point(self.x, self.y)
            move_dist = self.my_speed*dt

            current_distance = current_pos.distance_to(self.target_pos)

            if current_distance > move_dist:
                # Move towards target
                target_dir = self.target_pos - current_pos
                target_dir.normalize()
                new_pos = current_pos + target_dir.multiply(move_dist)

                # Does not work for some reason
                #self.card_label.x = new_pos.x
                #self.card_label.y = new_pos.y

                self.x = new_pos.x
                self.y = new_pos.y

            else:
                # Just snap to position if in range
                self.x = self.target_pos.x
                self.y = self.target_pos.y

                self.target_pos = None # Stops movement

            if current_distance < self.alpha_distance_threshold:
                self.opacity = int(255*(1 - current_distance/self.alpha_distance_threshold))

            else:
                self.opacity = 0
                """
                if self.opacity > 0:
                    current_alpha = self.opacity
                    new_alpha = current_alpha - self.alpha_decrease_speed*dt
                    if new_alpha < 0:
                        self.opacity = 0
                    else:
                        self.opacity = int(new_alpha)
                """

import pyglet
from pyglet.shapes import Circle


class EnergyBar:
    def __init__(self, batch, start_pos, end_pos,
                 off_color=(180, 180, 180), on_color=(255, 153, 25), used_color=(255, 200, 85),
                 radius=16, current_energy=1, max_energy=1, limit_energy=10):

        direction = end_pos - start_pos

        length = direction.length()
        direction.normalize()

        displacement = length / (limit_energy - 1)


        self.off_color = off_color
        self.on_color = on_color
        self.used_color = used_color

        self.max_energy = max_energy
        self.limit_energy = limit_energy

        self.circles = []
        for index in range(self.limit_energy):
            pos = start_pos + direction.multiply(displacement*index)
            circle = Circle(pos.x, pos.y, radius, color=off_color, batch=batch)
            self.circles.append(circle)

    def set_index_color(self, index, color):
        self.circles[index].color = color

    def set_new_maximum(self, energy):

        self.max_energy = energy
        for index in range(self.limit_energy):
            if index < energy:
                self.set_index_color(index, self.on_color)
            else:
                self.set_index_color(index, self.off_color)

    def set_used(self, energy):

        for index in range(self.limit_energy):
            if index < energy:
                self.set_index_color(index, self.on_color)
            elif index < self.max_energy:
                self.set_index_color(index, self.used_color)
            else:
                self.set_index_color(index, self.off_color)





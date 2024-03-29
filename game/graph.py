import pyglet
from pyglet.shapes import Line


class Graph:
    def __init__(self,
                 x_axis_length, x_axis_max,
                 y_axis_length, y_axis_max,
                 batch, axis_width=1,
                 origin=(0, 0), color=(255, 255, 255),
                 line_color=(255, 255, 255), line_width=1,
                 rolling=False, bar=False):

        self.x_axis_length = x_axis_length
        self.y_axis_length = y_axis_length
        self.x_axis_max = x_axis_max
        self.y_axis_max = y_axis_max

        self.batch = batch
        self.axis_width = axis_width
        self.origin = origin
        self.color = color
        self.line_color = line_color
        self.line_width = line_width
        self.rolling = rolling
        self.bar = bar

        self.clear()

        self.x_axis_normalization = x_axis_length / x_axis_max
        self.y_axis_normalization = y_axis_length / y_axis_max

        # Create x-axis and y-axis lines
        self.x_axis = Line(self.origin[0], self.origin[1],
                           self.origin[0] + self.x_axis_length, self.origin[1],
                           width=self.axis_width, color=self.color, batch=self.batch)
        self.y_axis = Line(self.origin[0], self.origin[1],
                           self.origin[0], self.origin[1] + self.y_axis_length,
                           width=self.axis_width, color=self.color, batch=self.batch)

    def clear(self):
        self.points = []
        self.lines = []
        self.rolling_x_difference = 0

    def add_point(self, x, y):
        self.points.append([x, y])

        if self.rolling:
            new_lower_limit = x - self.x_axis_max
            if new_lower_limit > 0:
                for index, point in enumerate(self.points):
                    if point[0] > new_lower_limit:
                        break

                self.points = self.points[index:]

                self.rolling_x_difference = new_lower_limit + 0.25

    def draw(self):

        # Draw points and lines connecting them
        vertex_list = []
        colors = []
        for point in self.points:
            x_value = (point[0] - self.rolling_x_difference)*self.x_axis_normalization
            y_value = point[1]*self.y_axis_normalization

            vertex = [self.origin[0] + x_value,
                      self.origin[1] + y_value]
            vertex_list.append(vertex)
            #colors.extend(self.color)

        self.lines = []
        last_point = None
        for index, point in enumerate(vertex_list):
            if self.bar:
                line = Line(point[0], self.origin[1], point[0], point[1],
                            width=self.line_width, color=self.line_color, batch=self.batch)
                self.lines.append(line)

            else:
                if last_point is not None:
                    line = Line(last_point[0], last_point[1], point[0], point[1],
                                width=self.line_width, color=self.line_color, batch=self.batch)
                    self.lines.append(line)

            last_point = point
            


import numpy as np
import pyglet
from pyglet.shapes import Line



class Match:
    def __init__(self, end_x, end_y, width, height, fontsize,
                 top_name, bottom_name, match_n, batch, extra_length=None):
        self.end_x = end_x
        self.end_y = end_y
        self.width = width
        self.height = height
        self.fontsize = fontsize
        self.top_name = top_name
        self.bottom_name = bottom_name
        self.match_n = match_n
        self.batch = batch
        self.extra_length = extra_length

        self.match_winner = None

        self.make_match()

    def make_match(self):

        left_space = 15
        left_space_number = 5

        further_space = 20
        if self.extra_length is not None:
            further_space = self.extra_length

        self.top_player_label = pyglet.text.Label(text=self.top_name, font_size=self.fontsize,
                                       x=self.end_x - left_space - 2, y=self.end_y + 0.5 * self.height + 1,
                                       anchor_x='right', anchor_y="center", batch=self.batch,
                                       color=(255,255,255,255))

        self.bottom_player_label = pyglet.text.Label(text=self.bottom_name, font_size=self.fontsize,
                                          x=self.end_x - left_space - 2, y=self.end_y - 0.5 * self.height + 1,
                                          anchor_x='right', anchor_y="center", batch=self.batch,
                                          color=(255,255,255,255))

        self.match_label = pyglet.text.Label(text=str(self.match_n), font_size=self.fontsize,
                                  x=self.end_x - left_space_number, y=self.end_y,
                                  anchor_x='right', anchor_y="center", batch=self.batch,
                                  color=(255,255,255, 255))

        self.line1 = Line(self.end_x, self.end_y + 0.5 * self.height,
                          self.end_x, self.end_y - 0.5 * self.height,
                    width=2, color=(255, 255, 255), batch=self.batch)

        self.line2 = Line(self.end_x - left_space*0.9, self.end_y + 0.5 * self.height,
                          self.end_x, self.end_y + 0.5 * self.height,
                    width=2, color=(255, 255, 255), batch=self.batch)

        self.line3 = Line(self.end_x - left_space*0.9, self.end_y - 0.5 * self.height,
                          self.end_x, self.end_y - 0.5 * self.height,
                    width=2, color=(255, 255, 255), batch=self.batch)

        self.line4 = Line(self.end_x, self.end_y,
                          self.end_x + further_space, self.end_y,
                          width=2, color=(255, 255, 255), batch=self.batch)

    def __repr__(self):

        return f"M {self.top_name} {self.bottom_name} {self.match_n}"


def find_match(string, match_list):

    if string[0] in ["L", "W"]:
        number = string[1:]
    else:
        number = string

    for match in match_list:
        if match.match_n == number:
            return match

    raise ValueError("Didnt find " + string)

class DoubleBracket:
    def __init__(self, batch, tournament_state=None, match_number=None):
        self.batch = batch
        self.tournament_state = tournament_state
        self.all_matches = []
        self.match_number = match_number

    def setup(self):
        player_names = player_names = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]

        column_width = 130

        fontsize=11

        initial_matches = []
        heights = np.linspace(800-50, 300+50, 8)
        height = abs(0.7*(heights[1] - heights[0]))
        width = 350
        for index, center_y in enumerate(heights):

            top_name = player_names.pop(0)
            bottom_name = player_names.pop(0)
            #print("top:", top_name, "bottom:", bottom_name)

            match = Match(end_x=160, end_y=center_y, width=width, height=height, fontsize=fontsize,
                          top_name=top_name, bottom_name=bottom_name,
                          match_n=str(index + 1), batch=self.batch)
            initial_matches.append(match)

        self.initial_matches = initial_matches
        self.all_matches += self.initial_matches

        initial_match_pairs = []
        for index in range(4):
            match_pair = (self.initial_matches[index*2], self.initial_matches[index*2+1])
            initial_match_pairs.append(match_pair)

        self.second_round = []
        for index, match_pair in enumerate(initial_match_pairs):
            height = abs(match_pair[0].end_y - match_pair[1].end_y)
            center_y = 0.5*(match_pair[0].end_y + match_pair[1].end_y)
            new_x = match_pair[0].end_x + column_width

            match = Match(end_x=new_x, end_y=center_y, width=width, height=height, fontsize=fontsize,
                          top_name="W" + str(match_pair[0].match_n),
                          bottom_name="W" + str(match_pair[1].match_n),
                          match_n=str(index + 13), batch=self.batch)

            self.second_round.append(match)

        self.all_matches += self.second_round

        second_match_pairs = []
        for index in range(2):
            match_pair = (self.second_round[index * 2], self.second_round[index * 2 + 1])
            second_match_pairs.append(match_pair)

        self.third_round = []
        for index, match_pair in enumerate(second_match_pairs):
            height = abs(match_pair[0].end_y - match_pair[1].end_y)
            center_y = 0.5 * (match_pair[0].end_y + match_pair[1].end_y)
            new_x = match_pair[0].end_x + column_width

            match = Match(end_x=new_x, end_y=center_y, width=width, height=height, fontsize=fontsize,
                          top_name="W" + str(match_pair[0].match_n),
                          bottom_name="W" + str(match_pair[1].match_n),
                          match_n=str(index + 21), batch=self.batch, extra_length=column_width + 20)

            self.third_round.append(match)

        self.all_matches += self.third_round

        self.fourth_round = []
        match_pair = (self.third_round[0], self.third_round[1])
        height = abs(match_pair[0].end_y - match_pair[1].end_y)
        center_y = 0.5 * (match_pair[0].end_y + match_pair[1].end_y)
        new_x = match_pair[0].end_x + column_width*2

        match = Match(end_x=new_x, end_y=center_y, width=width, height=height, fontsize=fontsize,
                      top_name="W" + str(match_pair[0].match_n),
                      bottom_name="W" + str(match_pair[1].match_n),
                      match_n=str(27), batch=self.batch, extra_length=column_width + 20)

        self.fourth_round.append(match)
        self.all_matches += self.fourth_round



        initial_loser_matches = []
        heights = np.linspace(230, 40, 4)
        height = abs(0.7*(heights[1] - heights[0]))
        width = 120
        for index, center_y in enumerate(heights):
            match = Match(160, center_y, width, height, 10,
                          "L" + str(index*2 + 1), "L" + str(index*2 + 2),
                          match_n=str(index + 9), batch=self.batch)
            initial_loser_matches.append(match)

        self.initial_loser_matches = initial_loser_matches
        self.all_matches += self.initial_loser_matches

        losers_second_match_library = [("L16", "W9", "17"),
                                       ("L15", "W10", "18"),
                                       ("L14", "W11", "19"),
                                       ("L13", "W12", "20")]

        self.second_round_losers = []
        for top, bottom, number in losers_second_match_library:

            losers_origin = find_match(bottom, self.all_matches)

            height = 40
            center_y = losers_origin.end_y + 0.5 * height
            new_x = losers_origin.end_x + column_width

            match = Match(end_x=new_x, end_y=center_y, width=width, height=height, fontsize=fontsize,
                          top_name=top,
                          bottom_name=bottom,
                          match_n=number, batch=self.batch)

            self.second_round_losers.append(match)

        self.all_matches += self.second_round_losers

        third_round_losers = []
        for index in range(2):
            match_pair = (self.second_round_losers[index * 2], self.second_round_losers[index * 2 + 1])
            third_round_losers.append(match_pair)

        self.third_round_losers = []
        for index, match_pair in enumerate(third_round_losers):
            height = abs(match_pair[0].end_y - match_pair[1].end_y)
            center_y = 0.5 * (match_pair[0].end_y + match_pair[1].end_y)
            new_x = match_pair[0].end_x + column_width

            match = Match(end_x=new_x, end_y=center_y, width=width, height=height, fontsize=fontsize,
                          top_name="W" + str(match_pair[0].match_n),
                          bottom_name="W" + str(match_pair[1].match_n),
                          match_n=str(index + 23), batch=self.batch)

            self.third_round_losers.append(match)

        self.all_matches += self.third_round_losers

        losers_fourth_match_library = [("L21", "W23", "25"),
                                       ("W24", "L22", "26")]

        self.fourth_round_losers = []
        for top, bottom, number in losers_fourth_match_library:
            height = 70
            if top[0] == "L":
                losers_origin = find_match(bottom, self.all_matches)
                center_y = losers_origin.end_y + 0.5 * height
            else:
                losers_origin = find_match(top, self.all_matches)
                center_y = losers_origin.end_y - 0.5 * height

            new_x = losers_origin.end_x + column_width

            match = Match(end_x=new_x, end_y=center_y, width=width, height=height, fontsize=fontsize,
                          top_name=top,
                          bottom_name=bottom,
                          match_n=number, batch=self.batch)

            self.fourth_round_losers.append(match)

        self.all_matches += self.fourth_round_losers

        self.losers_semi_finals = []

        match_pair = (self.fourth_round_losers[0], self.fourth_round_losers[1])
        height = abs(match_pair[0].end_y - match_pair[1].end_y)
        center_y = 0.5 * (match_pair[0].end_y + match_pair[1].end_y)
        new_x = match_pair[0].end_x + column_width
        match = Match(end_x=new_x, end_y=center_y, width=width, height=height, fontsize=fontsize,
                      top_name="W" + str(match_pair[0].match_n),
                      bottom_name="W" + str(match_pair[1].match_n),
                      match_n=str(28), batch=self.batch)

        self.losers_semi_finals.append(match)
        self.all_matches += self.losers_semi_finals

        self.losers_finals = []
        losers_origin = self.losers_semi_finals[0]
        height = 150
        center_y = losers_origin.end_y + 0.5 * height
        new_x = losers_origin.end_x + column_width

        match = Match(end_x=new_x, end_y=center_y, width=width, height=height, fontsize=fontsize,
                      top_name="L27",
                      bottom_name="W28",
                      match_n=str(29), batch=self.batch)

        self.losers_finals.append(match)
        self.all_matches += self.losers_finals

        self.first_finals = []
        match_pair = (self.fourth_round[0], self.losers_finals[0])
        height = abs(match_pair[0].end_y - match_pair[1].end_y)
        center_y = 0.5 * (match_pair[0].end_y + match_pair[1].end_y)
        new_x = match_pair[0].end_x + column_width * 2

        match = Match(end_x=new_x, end_y=center_y, width=width, height=height, fontsize=fontsize,
                      top_name="W" + str(match_pair[0].match_n),
                      bottom_name="W" + str(match_pair[1].match_n),
                      match_n=str(30), batch=self.batch)

        self.first_finals.append(match)
        self.all_matches += self.first_finals

        winners_origin = self.first_finals[0]
        height = 200
        center_y = winners_origin.end_y - 0.5 * height
        new_x = winners_origin.end_x + column_width

        match = Match(end_x=new_x, end_y=center_y, width=width, height=height, fontsize=fontsize,
                      top_name="W30",
                      bottom_name="L30",
                      match_n=str(31), batch=self.batch)

        match.line1.opacity = 80
        match.line3.opacity = 80
        match.line2.opacity = 80
        match.line4.opacity = 80

        self.second_finals = [match]
        self.all_matches += self.second_finals

        if self.match_number is not None:
            self.match_number_label = pyglet.text.Label(text=str(self.match_number), font_size=30,
                                                        x=1200, y=700,
                                                        anchor_x='right', anchor_y="center",
                                                        batch=self.batch,
                                                        color=(255, 255, 255, 255))

    def update_with_state(self):

        if self.tournament_state is None:
            return

        for match in self.all_matches:
            if match.top_name in self.tournament_state:
                match.top_player_label.text = self.tournament_state[match.top_name]

            if match.bottom_name in self.tournament_state:
                match.bottom_player_label.text = self.tournament_state[match.bottom_name]

            if self.match_number is not None:
                if int(match.match_n) == int(self.match_number):
                    on_color = (255, 153, 25)
                    match.line1.color = on_color
                    match.line2.color = on_color
                    match.line3.color = on_color
                    match.line4.color = on_color

        for match_code in self.tournament_state:
            if match_code[0] == "L" and len(match_code) > 1:
                match = find_match(match_code, self.all_matches)

                player_name = self.tournament_state[match_code]

                print("adjusting: ", match, match_code, player_name)
                print(match.top_player_label.text)
                print(match.bottom_player_label.text)
                if match.top_player_label.text == player_name:
                    print("top sat")
                    match.top_player_label.opacity = 130

                if match.bottom_player_label.text == player_name:
                    print("bottom sat")
                    match.bottom_player_label.opacity = 130
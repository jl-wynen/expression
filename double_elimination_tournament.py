import os
import pyglet
import random
import json

from expression import run_expression
from contestants import template_fast, template_reckless, template_careful

class Match:
    def __init__(self, top, bottom, number):
        self.top = top
        self.bottom = bottom
        self.number = number

        self.winner = None
        self.looser = None

        self.top_score = None
        self.bottom_score = None

    def update(self, status):
        if self.top in status:
            self.top = status[self.top]

        if self.bottom in status:
            self.bottom = status[self.bottom]

    def __repr__(self):
        return f"top:{self.top}, bottom:{self.bottom}, number: {self.number}"

code_names = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]
match_plan = [Match("A", "B", 1),
              Match("C", "D", 2),
              Match("E", "F", 3),
              Match("G", "H", 4),
              Match("I", "J", 5),
              Match("K", "L", 6),
              Match("M", "N", 7),
              Match("O", "P", 8),
              Match("L1", "L2", 9),
              Match("L3", "L4", 10),
              Match("L5", "L6", 11),
              Match("L7", "L8", 12),
              Match("W1", "W2", 13),
              Match("W3", "W4", 14),
              Match("W5", "W6", 15),
              Match("W7", "W8", 16),
              Match("L16", "W9", 17),
              Match("L15", "W10", 18),
              Match("L14", "W11", 19),
              Match("L13", "W12", 20),
              Match("W13", "W14", 21),
              Match("W15", "W16", 22),
              Match("W17", "W18", 23),
              Match("W19", "W20", 24),
              Match("L21", "W23", 25),
              Match("L22", "W24", 26),
              Match("W21", "W22", 27),
              Match("W25", "W26", 28),
              Match("L27", "W28", 29),
              Match("W27", "W29", 30)
              ]

second_finals = Match("W30", "L30", 31)

contestants = [template_fast.Agent, template_reckless.Agent, template_careful.Agent]


contestant_names = []
contestant_agents = {}
for contestant in contestants:
    contestant_name = contestant().name
    contestant_names.append(contestant_name)
    contestant_agents[contestant_name] = contestant

# get to 16 with buy's
contestants_and_buys = contestant_names + (16 - len(contestant_names)) * [10*"-"]
assert len(contestants_and_buys) == 16

tournament_plan = "spot_assignments"
tournament_results = "tournament_state"
tournament_plan += ".json"
tournament_results += ".json"

mirror_match = False
score_limit = 2

# Write tournament plan to file
if not os.path.isfile(tournament_plan):
    random.shuffle(contestants_and_buys)
    spot_assignments = {}
    for contestant_name, code_name in zip(contestants_and_buys, code_names):
        spot_assignments[code_name] = contestant_name

    with open(tournament_plan, "w") as f:
        json.dump(spot_assignments, f)

else:
    with open(tournament_plan) as f:
        spot_assignments = json.load(f)

    # check this corresponds to our players
    for name in spot_assignments.values():
        if name not in contestants_and_buys:
            ValueError("mismatch in contestants and tournament plan.")

    for name in contestants_and_buys:
        if name not in spot_assignments.values():
            ValueError("mismatch in contestants and tournament plan.")


# Run tournament with filename, produce result file
if os.path.isfile(tournament_results):

    # exchange letters with agent names
    for match in match_plan:
        match.update(spot_assignments)

    with open(tournament_results) as f:
        tournament_status = json.load(f)

    # include information on tournament up till now
    for match in match_plan:
        match.update(tournament_status)

    highest_match_index = 0
    for match_string in tournament_status:
        number_part = match_string[1:]
        if int(number_part) > highest_match_index:
            highest_match_index = int(number_part)

    # start from next match
    highest_match_index += 1

else:
    # exchange letters with agent names
    print("spot assignments")
    print(spot_assignments)
    print("--"*100)

    for match in match_plan:
        match.update(spot_assignments)

    tournament_status = {}
    highest_match_index = 1


for match in match_plan:
    print(match)


game_window = pyglet.window.Window(1280, 800)
game_window.set_vsync(False)
for match_index in range(highest_match_index, 31):
    this_match = match_plan[match_index - 1]

    top_empty = this_match.top == 10*"-"
    bottom_empty = this_match.bottom == 10*"-"

    if not top_empty and not bottom_empty:
        top_contestant_agent = contestant_agents[this_match.top]()
        bottom_contestant_agent = contestant_agents[this_match.bottom]()

        tournament_state = {}
        tournament_state.update(spot_assignments)
        tournament_state.update(tournament_status)

        print(f"player {this_match.top} vs {this_match.bottom}")

        game_window.clear()
        top_score, bottom_score = run_expression(game_window=game_window,
                                                 tournament_state=tournament_state,
                                                 match_number=match_index,
                                                 positive_player=top_contestant_agent,
                                                 negative_player=bottom_contestant_agent)

    elif top_empty and not bottom_empty:
        bottom_score = 2
        top_score = 0
    elif not top_empty and bottom_empty:
        top_score = 2
        bottom_score = 0
    elif top_empty and bottom_empty:
        # Doesn't mattter who proceeds
        top_score = 2
        bottom_score = 2

    if top_score > bottom_score:
        tournament_status["W" + str(match_index)] = this_match.top
        tournament_status["L" + str(match_index)] = this_match.bottom
    else:
        tournament_status["L" + str(match_index)] = this_match.top
        tournament_status["W" + str(match_index)] = this_match.bottom

    # match was not updated with the newest results
    for match in match_plan:
        match.update(tournament_status)

    with open(tournament_results, "w") as f:
        json.dump(tournament_status, f)

"""
class Match:
    def __init__(self, player1_name, player1, player2_name, player2):
        self.player1_name = player1_name
        self.player1 = player1
        self.player2_name = player2_name
        self.player2 = player2

matches = []
with open(tournament_plan, "r") as plan_file:
    match_line = plan_file.readline() # ignore first line with best of number
    match_line = plan_file.readline() # ignore second line with contestants names
    match_line = plan_file.readline()
    while match_line:
        player1_name = match_line.split(" ", 1)[0].strip()
        player2_name = match_line.split(" ")[-1].strip()

        player1 = None
        player2 = None
        for contestant in contestants:
            contestant_name = contestant.__module__.split(".")[1].strip()
            if contestant_name == player1_name:
                player1 = contestant
            if contestant_name == player2_name:
                player2 = contestant
        if player1 is None or player2 is None:
            print("ERROR, didn't find both players for match!")
            print("player1: " + player1_name)
            print("player2: " + player2_name)
        matches.append(Match(player1_name, player1, player2_name, player2))
        match_line = plan_file.readline()

# Run tournament with filename, produce result file
if os.path.isfile(tournament_results):
    match_index_start = sum(1 for line in open(tournament_results))
else:
    match_index_start = 0
    result_file = open(tournament_results, "w")
    result_file.close()


game_window = pyglet.window.Window(1280, 800)
game_window.set_vsync(False)
for match_index in range(match_index_start, len(matches)):
    match = matches[match_index]
    print("Running " + match.player1_name + " vs " + match.player2_name)
    game_window.clear()
    result = run_expression(game_window=game_window,
                            negative_player=match.player1(), positive_player=match.player2())
    #game_window.close()
    # Need to check max result = score limit
    result_file = open(tournament_results, "a")
    result_file.write(match.player1_name + " vs " + match.player2_name + ": " + str(result[0]) + " - " + str(result[1]) + "\n")
    result_file.close()
"""


import os
import pyglet
import random

from expression import run_expression
from contestants import template_fast, template_reckless, template_careful

contestants = [template_fast.Agent, template_reckless.Agent, template_careful.Agent]
tournament_plan = "event_all"
tournament_results = tournament_plan + "_results"
tournament_plan += ".txt"
tournament_results += ".txt"

mirror_match = False
score_limit = 2

# Write tournament plan to file
if not os.path.isfile(tournament_plan):
    with open(tournament_plan, "w") as plan_file:
    
        plan_file.write("Score limit " + str(score_limit) + "\n")

        name_line = "Contestants: "
        for player in contestants:
            name_line += player.__module__.split(".")[1].strip() + " "

        plan_file.write(name_line + "\n")

        matches = []
        for player1 in contestants:
            player1_name = player1.__module__.split(".")[1].strip()
            for player2 in contestants:
                player2_name = player2.__module__.split(".")[1].strip()
                
                if not mirror_match and player1_name == player2_name:
                    # Skip mirror matches if mirror match is false
                    continue

                print(player1_name + " vs " + player2_name)
                matches.append(player1_name + " vs " + player2_name + "\n")
    
        random.shuffle(matches)
        for match in matches:
            plan_file.write(match)


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



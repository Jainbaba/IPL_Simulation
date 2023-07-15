import json
import random
from Players import Player
from Tracking import Tracker
from Utils import Utils


class Team:
    """
    Team class to represent a cricket team.

    Parameters:
      - name (str): Name of the team

    Attributes:

      - name (str): Name of the team
      - roster (list): List of Player objects
      - match_trackers (dict): Dict mapping player name to match Tracker
      - utils (Utils): Utils object
      - catcher_probabilities (list): Probabilities of each player catching ball

    Methods:

    __init__():
      - Loads team roster and player data
      - Initializes match trackers for each player
      - Calculates catcher probabilities

    batting_order():
      - Returns roster sorted by batting average for batting order

    bowling_order():
      - Returns roster sorted by bowling out rate

    calculate_catcher_probabilities():
      - Calculates normalized probabilities for each player to catch ball based on catch rates

    determine_catcher():
      - Randomly chooses fielder to take catch based on catcher probabilities
    """

    def __init__(self, name: str):
        self.name = name
        self.roster = []
        self.match_trackers = {}
        with open("teams.json") as fl:
            team_info = json.load(fl)[name]
        with open("playerInfo.json") as f:
            player_data = json.load(f)

        self.utils = Utils()
        for player in team_info:
            player_info = player_data[player]
            player = Player(player_info)
            self.roster.append(player)
            self.match_trackers[player.name] = Tracker(player)

        total_catch_rate = sum(player.catch_rate for player in self.roster)
        self.catcher_probabilities = self.calculate_catcher_probabilities(
            total_catch_rate
        )

    def batting_order(self):
        return sorted(self.roster, key=lambda player: player.pos_avg)

    def bowling_order(self):
        return self.utils._extracted_from_blowers(self.roster, "bowl_out_rate")

    def calculate_catcher_probabilities(self, total_catch_rate):
        return [player.catch_rate / total_catch_rate for player in self.roster]

    def determine_catcher(self):
        catcher = random.choices(self.roster, weights=self.catcher_probabilities, k=1)
        return catcher[0] if catcher else None

    def __str__(self) -> str:
        return [p.name for p in self.roster]

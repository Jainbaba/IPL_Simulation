from collections import Counter
from Tracking import Tracker


class Player:
    """
    Player class to represent a cricket player.

    Parameters:
      - player_data (dict): Player stats data

    Attributes:
      - _id (str): Player ID
      - initials (str): Player initials
      - name (str): Player name
      - batting_style (str): Batting style
      - bowling_style (str): Bowling style
      - bat_runs (int): Total batting runs
      - bat_balls_faced (int): Total balls faced batting
      - bowl_runs (int): Total bowling runs conceded
      - bowl_balls_bowled (int): Total balls bowled
      - bat_outs (int): Total batting outs
      - bowl_outs (int): Total bowling outs
      - bowl_no_balls (int): Total no balls bowled
      - bowl_wides (int): Total wide balls bowled
      - catches (int): Total catches taken
      - bat_out_counts (dict): Batting dismissal types
      - bowl_out_counts (dict): Bowling dismissal caused
      - bat_run_counts (dict): Batting runs scored
      - bowl_run_counts (dict): Bowling runs conceded
      - overs_bowled (list): Overs bowled
      - run_outs (int): Total run outs
      - positions (list): Batting positions
      - by_batsman (dict): Dismissals by batsman
      - by_bowler (dict): Dismissals by bowler
      - captaincies (int): Matches captained
      - wicketkeeper (bool): Is player a wicketkeeper
      - matches_played (int): Total matches played
      - tracker (Tracker): Player match tracker object
      - bat_run_probabilities (dict): Batting run probabilities
      - bat_out_probabilities (dict): Batting dismissal probabilities
      - bat_out_rate (float): Batting dismissal rate
      - run_out_probability (float): Batting run out probability
      - pos_averages_all (dict): Batting average by position
      - pos_avg (float): Overall batting average
      - bowl_run_probabilities (dict): Bowling run concession probabilities
      - bowl_out_probabilities (dict): Bowling dismissal probabilities
      - bowl_out_rate (float): Bowling dismissal rate
      - bowl_balls_faced_rate (float): Balls bowled per match rate
      - catch_rate (float): Catches per match rate
      - bowl_wide_rate (float): Wide delivery rate
      - bowl_no_ball_rate (float): No ball delivery rate
      - overs_avg (dict): Overs bowled per match averages

    Methods:

      __init__():
        Initializes Player object with stats data

      calculate_batting_points():
        Calculates batting stats like probabilities and averages

      calculate_bowling_points():
        Calculates bowling stats like probabilities and averages
    """

    def calculate_batting_points(self):
        self.bat_run_probabilities = {
            run: self.bat_run_counts[run] / self.bat_balls_faced
            for run in self.bat_run_counts
        }
        self.bat_out_probabilities = {
            out: self.bat_out_counts[out] / self.bat_balls_faced
            for out in self.bat_out_counts
        }
        self.bat_out_rate = self.bat_outs / self.bat_balls_faced
        self.run_out_probability = (
            self.run_outs / self.bat_balls_faced if self.bat_out_rate != 1 else 0.01
        )

        pos_total = 0
        count = 0
        self.pos_averages_all = None
        for pos, value in Counter(self.positions).items():
            if pos != "null":
                self.pos_averages_all = {pos: value / self.matches_played}
                pos_total += pos * value
                count += value

        self.pos_avg = pos_total / self.matches_played if count != 0 else 9.0

    def calculate_bowling_points(self):
        self.bowl_balls_faced_rate = self.bowl_balls_bowled / self.matches_played
        self.catch_rate = self.catches / self.matches_played
        self.bowl_wide_rate = self.bowl_wides / self.bowl_balls_bowled
        self.bowl_no_ball_rate = self.bowl_no_balls / self.bowl_balls_bowled
        self.bowl_run_probabilities = {
            run: self.bowl_run_counts[run] / self.bowl_balls_bowled
            for run in self.bowl_run_counts
        }
        self.bowl_out_probabilities = {
            out: self.bowl_out_counts[out] / self.bowl_balls_bowled
            for out in self.bowl_out_counts
        }
        self.bowl_out_rate = self.bowl_outs / self.bowl_balls_bowled

        self.overs_avg = {str(over): 0 for over in range(21)}

        for over, value in Counter(self.overs_bowled).items():
            self.overs_avg[over] = (
                value / self.matches_played if self.matches_played != 0 else -1
            )

    def __init__(self, player_data):
        self._id = player_data["_id"]
        self.initials = player_data["playerInitials"]
        self.name: str = player_data["displayName"]
        self.batting_style = player_data["batStyle"]
        self.bowling_style = player_data["bowlStyle"]
        self.bat_runs = player_data["batRunsTotal"]
        self.bat_balls_faced = (
            player_data["batBallsTotal"] if player_data["batBallsTotal"] != 0 else 1
        )
        self.bowl_runs = player_data["bowlRunsTotal"]
        self.bowl_balls_bowled = (
            player_data["bowlBallsTotal"] if player_data["bowlBallsTotal"] != 0 else 1
        )
        self.bat_outs = player_data["batOutsTotal"]
        self.bowl_outs = player_data["bowlOutsTotal"]
        self.bowl_no_balls = player_data["bowlNoballs"]
        self.bowl_wides = player_data["bowlWides"]
        self.catches = player_data["catches"]
        self.bat_out_counts = player_data["batOutTypes"]
        self.bowl_out_counts = player_data["bowlOutTypes"]
        self.bat_run_counts = player_data["batRunDenominations"]
        self.bowl_run_counts = player_data["bowlRunDenominations"]
        self.overs_bowled = player_data["overNumbers"]
        self.run_outs = player_data["runnedOut"]
        self.positions = player_data["position"]
        self.by_batsman = player_data["byBatsman"]
        self.by_bowler = player_data["byBowler"]
        self.captaincies = player_data["captained"]
        self.wicketkeeper = player_data["wicketkeeper"]
        self.matches_played = player_data["matches"]
        self.tracker = Tracker(self.name)
        self.calculate_batting_points()
        self.calculate_bowling_points()

    # def __str__(self):
    #     return (
    #         f"Player Information:\n"
    #         f"ID: {self._id}\n"
    #         f"Player Initials: {self.initials}\n"
    #         f"Display Name: {self.name}\n"
    #         f"Batting Style: {self.batting_style}\n"
    #         f"Bowling Style: {self.bowling_style}\n"
    #         f"Bat Runs Total: {self.bat_runs}\n"
    #         f"Bat Balls Total: {self.bat_balls_faced}\n"
    #         f"Bowl Runs Total: {self.bowl_runs}\n"
    #         f"Bowl Balls Total: {self.bowl_balls_bowled}\n"
    #         f"Bat Outs Total: {self.bat_outs}\n"
    #         f"Bowl Outs Total: {self.bowl_outs}\n"
    #         f"Bowl No Balls: {self.bowl_no_balls}\n"
    #         f"Bowl Wides: {self.bowl_wides}\n"
    #         f"Catches: {self.catches}\n"
    #         f"Bat Out Types: {self.bat_out_counts}\n"
    #         f"Bowl Out Types: {self.bowl_out_counts}\n"
    #         f"Bat Run Denominations: {self.bat_run_counts}\n"
    #         f"Bowl Run Denominations: {self.bowl_run_counts}\n"
    #         f"Over Numbers: {self.overs_bowled}\n"
    #         f"Runned Out: {self.run_outs}\n"
    #         f"Position: {self.positions}\n"
    #         f"By Batsman: {self.by_batsman}\n"
    #         f"By Bowler: {self.by_bowler}\n"
    #         f"Captained: {self.captaincies}\n"
    #         f"Wicketkeeper: {self.wicketkeeper}\n"
    #         f"Matches: {self.matches_played}\n"
    #         f"Batting Run Probabilities: {self.bat_run_probabilities}\n"
    #         f"Batting Out Probabilities: {self.bat_out_probabilities}\n"
    #         f"Batting Out Rates: {self.bat_out_rate}\n"
    #         f"Run Out Probilities: {self.run_out_probability}\n"
    #         f"Position Average: {self.pos_averages_all}\n"
    #         f"Position Overall Average: {self.pos_avg}\n"
    #         f"Bowling Run Probabilities: {self.bowl_run_probabilities}\n"
    #         f"Bowling Out Probabilities: {self.bowl_out_probabilities}\n"
    #         f"Bowling Out Rates: {self.bowl_out_rate}\n"
    #         f"bowlBallsTotalRate: {self.bowl_balls_faced_rate}\n"
    #         f"catchRate: {self.catch_rate}\n"
    #         f"bowlWideRate: {self.bowl_wide_rate}\n"
    #         f"bowlNoballRate: {self.bowl_no_ball_rate}\n"
    #         f"Overs Average: {self.overs_avg}\n"
    #     )

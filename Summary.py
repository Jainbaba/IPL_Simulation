from ast import List
from tabulate import tabulate

from Tracking import Tracker

class MatchSummary:
    """
    MatchSummary class to summarize the match stats for all players.

    Parameters:
      - players (list): List of player instances

    Attributes:
      - players (list): List of player instances
    """
    def get_bowling_stats_table(self,players):
        def balls_to_overs(balls):
            overs = balls // 6
            balls_remaining = balls % 6
            return f"{overs}.{balls_remaining}"
        headers = ["Player", "Runs Conceded", "Balls Faced","Wickets Taken", "Economy"]
        data = []
        for player in players:
            runs_conceded = player.runs_conceded
            overs_bowled = balls_to_overs(player.balls_bowled)
            balls = player.balls_bowled
            economy = runs_conceded / balls if balls > 0 else 0
            wickets_taken = player.wickets_taken
            data.append([player.name, runs_conceded,overs_bowled,wickets_taken, f"{economy:.2f}"])
        sorted_data = sorted(data, key=lambda x: float(x[3]),reverse=True)
        return tabulate(sorted_data, headers, tablefmt="grid")

    def get_batting_stats_table(self,players):
        headers = ["Player", "Runs Scored", "Balls Faced", "Strike Rate", "Wickets Taken"]
        data = []
        for player in players:
            runs_scored = player.runs_scored
            balls_faced = player.balls_faced
            strike_rate = (runs_scored / balls_faced) * 100 if balls_faced > 0 else 0
            wicket_taken = ""
            if len(player.batting_log) > 0:
                last_event = player.batting_log[-1]
                if last_event.startswith("W"):
                    wicket_taken = last_event[1:].split(":")[0][1:-1]  
            data.append([player.name, runs_scored, balls_faced, f"{strike_rate:.2f}", wicket_taken])
        sorted_data = sorted(data, key=lambda x: float(x[3]), reverse=True)
        return tabulate(sorted_data, headers, tablefmt="grid")
    
    def get_summary(self,batting_players,bowling_players):
        print(self.get_batting_stats_table(batting_players))
        print(self.get_bowling_stats_table(bowling_players))
    
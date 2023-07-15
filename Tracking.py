class Tracker:
    """
    Tracker class to track player stats for a match.

    Parameters:
      - player_name (str): Name of the player

    Attributes:
      - name (str): Name of the player
      - runs_scored (int): Runs scored by player batting
      - runs_conceded (int): Runs conceded by player bowling
      - balls_faced (int): Balls faced by player batting
      - balls_bowled (int): Balls bowled by player bowling
      - overs_bowled (int): Overs bowled by player bowling
      - wickets_taken (int): Wickets taken by player bowling
      - catches_taken (int): Catches taken by player fielding
      - batting_log (list): Log of batting events
      - bowling_log (list): Log of bowling events
    """

    def __init__(self, player_name):
        self.name = player_name
        self.runs_scored = 0
        self.runs_conceded = 0
        self.balls_faced = 0
        self.balls_bowled = 0
        self.overs_bowled = 0
        self.wickets_taken = 0
        self.catches_taken = 0
        self.batting_log = []
        self.bowling_log = []

from Tracking import Tracker


class Utils:
    """
    Utils class containing utility functions.

    Methods:
    _extracted_from_blowers(bowling, arg1, arg2=None):
      Returns top 7 bowlers sorted by given arg1 and optional arg2.

      Parameters:
        bowling (list): List of bowler objects
        arg1 (str): Attribute to sort by
        arg2 (str, optional): Secondary attribute to sort by
      Returns:
        list: Top 7 bowlers by sorting criteria

    update_batter_tracker():
      Updates batter Tracker with info from delivery.

      Parameters:
        player_tracker (Tracker): Player Tracker object
        runs_scored (int): Runs scored
        balls_faced (int): Balls faced
        batting_log (str): Description of delivery outcome

      Returns:
        None

    update_bowler_tracker():
      Updates bowler Tracker with info from delivery.

      Parameters:
        player_tracker (Tracker): Player Tracker object
        runs_conceded (int): Runs conceded
        balls_bowled (int): Balls bowled
        overs_completed (bool): If over completed
        wickets_taken (bool): If wicket taken
        catches (bool): If catch taken
        bowling_log (str): Description of delivery outcome

      Returns:
        None
    """

    def _extracted_from_blowers(self, bowling, arg1, arg2=None):
        return (
            (sorted(bowling, key=lambda k: getattr(k, arg1)[arg2], reverse=True))[:7]
            if arg2 is not None
            else (sorted(bowling, key=lambda k: getattr(k, arg1), reverse=True))[:7]
        )

    def update_batter_tracker(
        self, player_tracker: Tracker, runs_scored, balls_faced, batting_log
    ):
        player_tracker.runs_scored += runs_scored
        player_tracker.balls_faced += balls_faced
        player_tracker.batting_log.append(batting_log)

    def update_bowler_tracker(
        self,
        player_tracker: Tracker,
        runs_conceded,
        balls_bowled,
        overs_completed,
        wickets_taken,
        catches,
        bowling_log,
    ):
        player_tracker.runs_conceded += runs_conceded
        player_tracker.balls_bowled += balls_bowled
        player_tracker.overs_bowled += 1 if overs_completed else 0
        player_tracker.wickets_taken += 1 if wickets_taken else 0
        player_tracker.catches_taken += 1 if catches else 0
        player_tracker.bowling_log.append(bowling_log)

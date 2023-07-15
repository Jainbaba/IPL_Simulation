import random

from Players import Player
from Tracking import Tracker


class Setting:
    """
    Settings class containing functions to adjust player stats based on match situation.

    Methods:
    first_innings_settings():
        Adjusts striker stats for first innings based on balls bowled and wickets fallen.

        Parameters:
            striker (Player): Striker batter object.
            balls_bowled (int): Balls bowled so far in innings.
            wickets_fallen (int): Wickets fallen so far in innings.
            out_probability (float): Striker's current out probability.

        Returns:
            None

    second_innings_settings():
        Adjusts striker stats for second innings based on match situation.

        Parameters:
            striker (Player): Striker batter object.
            balls_bowled (int): Balls bowled so far in innings.
            wickets_fallen (int): Wickets fallen so far in innings.
            out_probability (float): Striker's current out probability.
            score (int): Batting team's current score.
            target (int): Target score to win.

        Returns:
            None
    adjust_batsman_settings():
      Adjusts batter stats based on match situation.

      Parameters:
        batter (Tracker): Batter player tracker object
        striker (Player): Striker batter player object
        wickets_fallen (int): Wickets fallen so far
        balls_bowled (int): Balls bowled so far
        score (int): Batting team's score
        out_probability (float): Striker's out probability
        target (int, optional): Target score (for 2nd innings)

      Returns:
        None

    adjust_bowler_settings():
      Adjusts bowler stats based on pitch factors.

      Parameters:
        bowler (Player): Bowler player object
        spin_factor (float): Spin pitch factor
        pace_factor (float): Pace pitch factor

      Returns:
        None"""

    def first_innings_settings(
        self, striker: Player, balls_bowled, wickets_fallen, out_probability
    ):
        if balls_bowled < 12:
            sixes_adjustment = random.uniform(0.02, 0.05)
            out_probability = 0 if (out_probability < 0.07) else out_probability - 0.07
            sixes_adjustment = (
                striker.bat_run_counts["6"]
                if sixes_adjustment > striker.bat_run_counts["6"]
                else sixes_adjustment
            )
            striker.bat_run_counts["6"] -= sixes_adjustment
            striker.bat_run_counts["0"] += sixes_adjustment * (1 / 3)
            striker.bat_run_counts["1"] += sixes_adjustment * (2 / 3)
        elif 12 <= balls_bowled < 36:
            if wickets_fallen == 0:
                defense_and_single_adjustment = random.uniform(0.05, 0.11)
                striker.bat_run_counts["0"] -= defense_and_single_adjustment * (2 / 3)
                striker.bat_run_counts["1"] -= defense_and_single_adjustment * (1 / 3)
                striker.bat_run_counts["4"] += defense_and_single_adjustment * (2 / 3)
                striker.bat_run_counts["6"] += defense_and_single_adjustment * (1 / 3)
            else:
                defense_and_single_adjustment = random.uniform(0.02, 0.08)
                striker.bat_run_counts["0"] -= defense_and_single_adjustment * (2 / 3)
                striker.bat_run_counts["1"] -= defense_and_single_adjustment * (1 / 3)
                striker.bat_run_counts["4"] += defense_and_single_adjustment * (2.5 / 3)
                striker.bat_run_counts["6"] += defense_and_single_adjustment * (0.5 / 3)
                out_probability -= 0.03
        elif 36 <= balls_bowled < 102:
            if wickets_fallen < 3:
                defense_and_single_adjustment = random.uniform(0.05, 0.11)
                striker.bat_run_counts["0"] -= defense_and_single_adjustment * (1.5 / 3)
                striker.bat_run_counts["1"] -= defense_and_single_adjustment * (1 / 3)
                striker.bat_run_counts["4"] += defense_and_single_adjustment * (1.5 / 3)
                striker.bat_run_counts["6"] += defense_and_single_adjustment * (1 / 3)
            else:
                defense_and_single_adjustment = random.uniform(0.02, 0.07)
                striker.bat_run_counts["0"] -= defense_and_single_adjustment * (1.6 / 3)
                striker.bat_run_counts["1"] -= defense_and_single_adjustment * (1.2 / 3)
                striker.bat_run_counts["4"] += defense_and_single_adjustment * (2.1 / 3)
                striker.bat_run_counts["6"] += defense_and_single_adjustment * (0.9 / 3)
                out_probability -= 0.03
        else:
            if wickets_fallen < 7:
                defense_and_single_adjustment = random.uniform(0.07, 0.1)
                striker.bat_run_counts["0"] -= defense_and_single_adjustment * (0.4 / 3)
                striker.bat_run_counts["1"] -= defense_and_single_adjustment * (1 / 3)
                striker.bat_run_counts["4"] += defense_and_single_adjustment * (1.4 / 3)
                striker.bat_run_counts["6"] += defense_and_single_adjustment * (1.8 / 3)
            else:
                defense_and_single_adjustment = random.uniform(0.07, 0.09)
                striker.bat_run_counts["0"] -= defense_and_single_adjustment * (0.4 / 3)
                striker.bat_run_counts["1"] -= defense_and_single_adjustment * (1.8 / 3)
                striker.bat_run_counts["4"] += defense_and_single_adjustment * (1.5 / 3)
                striker.bat_run_counts["6"] += defense_and_single_adjustment * (1.5 / 3)
            out_probability += 0.01

    def second_innings_settings(
        self,
        striker: Player,
        balls_bowled,
        wickets_fallen,
        out_probability,
        score,
        target: int,
    ):  # sourcery skip: low-code-quality
        if balls_bowled < 120:
            required_run_rate = (target - score) / (120 - balls_bowled)

        if balls_bowled < 12:
            if required_run_rate < 1.5:
                sixes_adjustment = random.uniform(0.02, 0.05)
                out_probability = (
                    0 if (out_probability < 0.07) else out_probability - 0.07
                )
                sixes_adjustment = min(sixes_adjustment, striker.bat_run_counts["6"])
                striker.bat_run_counts["6"] -= sixes_adjustment
                striker.bat_run_counts["0"] += sixes_adjustment * (1 / 3)
                striker.bat_run_counts["1"] += sixes_adjustment * (2 / 3)
        elif balls_bowled < 36:
            if required_run_rate < 8 / 6:
                adjustment = random.uniform(0.05, 0.09)
                striker.bat_run_counts["6"] -= adjustment * (2 / 3)
                striker.bat_run_counts["4"] -= adjustment * (1 / 3)
                striker.bat_run_counts["1"] += adjustment
                out_probability -= 0.04
            elif required_run_rate <= 1.74:
                adjustment = random.uniform(0.04, 0.08)
                striker.bat_run_counts["6"] += adjustment * (0.6 / 3)
                striker.bat_run_counts["4"] += adjustment * (1 / 3)
                striker.bat_run_counts["0"] += adjustment * (1 / 3)
                striker.bat_run_counts["1"] -= adjustment * (1 / 3)
                striker.bat_run_counts["2"] -= adjustment * (0.6 / 3)
                out_probability -= 0.03

            else:
                adjustment = random.uniform(0.04, 0.08)
                adjustment += ((required_run_rate * 6) * 1.1) / 1000
                striker.bat_run_counts["6"] += adjustment * (1.5 / 3)
                striker.bat_run_counts["4"] += adjustment * (1 / 3)
                striker.bat_run_counts["0"] += adjustment * (0.5 / 3)
                striker.bat_run_counts["1"] -= adjustment * (2 / 3)
                striker.bat_run_counts["2"] -= adjustment * (1 / 3)
                out_probability += 0.02 + (((required_run_rate * 6) * 1.1) / 1000)
        elif balls_bowled < 102:
            if required_run_rate < 8 / 6:
                if wickets_fallen < 3:
                    adjustment = random.uniform(0.05, 0.09)
                    striker.bat_run_counts["6"] -= adjustment * (0.8 / 3)
                    striker.bat_run_counts["0"] -= adjustment * (1 / 3)
                    striker.bat_run_counts["2"] += adjustment * (1 / 3)
                    striker.bat_run_counts["1"] += adjustment * (1.5 / 3)
                    out_probability -= 0.02
                else:
                    adjustment = random.uniform(0.05, 0.09)
                    striker.bat_run_counts["1"] += adjustment
                    out_probability -= 0.04

            elif required_run_rate <= 1.7333333333333334:
                if wickets_fallen < 3:
                    adjustment = random.uniform(0.6, 0.08)
                    striker.bat_run_counts["6"] += adjustment * (1 / 3)
                    striker.bat_run_counts["4"] += adjustment * (1.15 / 3)
                    striker.bat_run_counts["0"] += adjustment * (0.1 / 3)
                    striker.bat_run_counts["1"] -= adjustment * (1 / 3)
                    striker.bat_run_counts["2"] -= adjustment * (1 / 3)
                    out_probability += 0.015

                else:
                    adjustment = random.uniform(0.04, 0.08)
                    striker.bat_run_counts["6"] += adjustment * (0.95 / 3)
                    striker.bat_run_counts["4"] += adjustment * (1.12 / 3)
                    striker.bat_run_counts["0"] += adjustment * (0.2 / 3)
                    striker.bat_run_counts["1"] -= adjustment * (0.9 / 3)
                    striker.bat_run_counts["2"] -= adjustment * (0.7 / 3)
                    out_probability += 0.01

            elif required_run_rate < 2:
                if wickets_fallen < 3:
                    adjustment = random.uniform(0.075, 0.1)
                    striker.bat_run_counts["6"] += adjustment * (1.5 / 3)
                    striker.bat_run_counts["4"] += adjustment * (1.5 / 3)
                    striker.bat_run_counts["0"] += adjustment * (0.5 / 3)
                    striker.bat_run_counts["1"] -= adjustment * (1.5 / 3)
                    striker.bat_run_counts["2"] -= adjustment * (1.5 / 3)
                    out_probability += 0.025
                else:
                    adjustment = random.uniform(0.06, 0.1)
                    striker.bat_run_counts["6"] += adjustment * (1.4 / 3)
                    striker.bat_run_counts["4"] += adjustment * (1 / 3)
                    striker.bat_run_counts["0"] += adjustment * (0.6 / 3)
                    striker.bat_run_counts["1"] -= adjustment * (1.1 / 3)
                    striker.bat_run_counts["2"] -= adjustment * (1.1 / 3)
                    out_probability += 0.035
                striker.bat_run_counts["3"] -= adjustment * (0.7 / 3)

            elif required_run_rate <= 15 / 6:
                if balls_bowled > 85:
                    if wickets_fallen < 3:
                        adjustment = random.uniform(0.065, 0.115)
                        striker.bat_run_counts["6"] += adjustment * (1.5 / 3)
                        striker.bat_run_counts["4"] += adjustment * (1.2 / 3)
                        striker.bat_run_counts["0"] += adjustment * (1.4 / 3)
                        striker.bat_run_counts["1"] -= adjustment * (1.2 / 3)
                        striker.bat_run_counts["2"] -= adjustment * (1.7 / 3)
                        out_probability += 0.04
                    else:
                        adjustment = random.uniform(0.05, 0.1)
                        striker.bat_run_counts["6"] += adjustment * (1.2 / 3)
                        striker.bat_run_counts["4"] += adjustment * (0.8 / 3)
                        striker.bat_run_counts["0"] += adjustment * (1.2 / 3)
                        striker.bat_run_counts["1"] -= adjustment * (1.2 / 3)
                        striker.bat_run_counts["2"] -= adjustment * (1.6 / 3)
                        out_probability += 0.05
                else:
                    adjustment = random.uniform(0.05, 0.1)
                    striker.bat_run_counts["6"] += adjustment * (1.3 / 3)
                    striker.bat_run_counts["4"] += adjustment * (1 / 3)
                    striker.bat_run_counts["0"] += adjustment * (1.2 / 3)
                    striker.bat_run_counts["1"] -= adjustment * (1.2 / 3)
                    striker.bat_run_counts["2"] -= adjustment * (1.6 / 3)
                    out_probability += 0.03
                striker.bat_run_counts["3"] -= adjustment * (0.9 / 3)

            else:
                if wickets_fallen < 3:
                    adjustment = random.uniform(0.075, 0.125)
                    striker.bat_run_counts["6"] += adjustment * (2 / 3)
                    striker.bat_run_counts["4"] += adjustment * (1.5 / 3)
                    striker.bat_run_counts["0"] += adjustment * (1.8 / 3)
                    striker.bat_run_counts["1"] -= adjustment * (1.2 / 3)
                    striker.bat_run_counts["2"] -= adjustment * (1.6 / 3)
                    out_probability += 0.05
                else:
                    adjustment = random.uniform(0.07, 0.12)
                    striker.bat_run_counts["6"] += adjustment * (1.8 / 3)
                    striker.bat_run_counts["4"] += adjustment * (1.5 / 3)
                    striker.bat_run_counts["0"] += adjustment * (1.8 / 3)
                    striker.bat_run_counts["1"] -= adjustment * (1.6 / 3)
                    striker.bat_run_counts["2"] -= adjustment * (1.7 / 3)
                    out_probability += 0.04
                striker.bat_run_counts["3"] -= adjustment * (0.9 / 3)

        elif wickets_fallen < 7 or required_run_rate > 2:
            defense_and_single_adjustment = random.uniform(0.07, 0.1)
            striker.bat_run_counts["0"] += defense_and_single_adjustment * (1.8 / 3)
            striker.bat_run_counts["1"] -= defense_and_single_adjustment * (1 / 3)
            striker.bat_run_counts["4"] += defense_and_single_adjustment * (1.45 / 3)
            striker.bat_run_counts["6"] += defense_and_single_adjustment * (1.85 / 3)
            out_probability += 0.032

        else:
            defense_and_single_adjustment = random.uniform(0.07, 0.09)
            striker.bat_run_counts["0"] -= defense_and_single_adjustment * (1.2 / 3)
            striker.bat_run_counts["1"] -= defense_and_single_adjustment * (1.8 / 3)
            striker.bat_run_counts["4"] += defense_and_single_adjustment * (1.5 / 3)
            striker.bat_run_counts["6"] += defense_and_single_adjustment * (1.5 / 3)
            out_probability += 0.028

    def adjust_batsman_settings(
        self,
        batter: Tracker,
        striker: Player,
        wickets_fallen,
        balls_bowled,
        score,
        out_probability,
        target=None,
    ):  # sourcery skip: low-code-quality
        # Tweeting the Probabilities of Boundaries if Wickets are available in last 15 balls
        if balls_bowled < 105:
            adjustment = random.uniform(0.02, 0.04)
            if wickets_fallen < 2:
                striker.bat_run_counts["0"] -= adjustment * (1 / 2)
                striker.bat_run_counts["1"] -= adjustment * (1 / 2)
                striker.bat_run_counts["2"] += adjustment * (1 / 2)
                striker.bat_run_counts["4"] += adjustment * (1 / 2)
            else:
                adjustment += 0.018
                striker.bat_run_counts["0"] += adjustment * (1.1 / 2)
                striker.bat_run_counts["1"] += adjustment * (0.9 / 2)
                striker.bat_run_counts["4"] -= adjustment * (1 / 2)
                striker.bat_run_counts["6"] -= adjustment * (1 / 2)
                out_probability -= 0.02

        # Opening Batsmen Settings
        if batter.balls_faced < 8 and balls_bowled < 80:
            adjustment = random.uniform(-0.01, 0.03)
            out_probability -= 0.015
            striker.bat_run_counts["0"] += adjustment * (1.5 / 3)
            striker.bat_run_counts["1"] += adjustment * (1 / 3)
            striker.bat_run_counts["2"] += adjustment * (0.5 / 3)
            striker.bat_run_counts["4"] -= adjustment * (0.5 / 3)
            striker.bat_run_counts["6"] -= adjustment * (1.5 / 3)

        # Batsmen Played between 15-30 Balls
        if batter.balls_faced > 15 and batter.balls_faced < 30:
            adjustment = random.uniform(0.03, 0.07)
            striker.bat_run_counts["0"] -= adjustment * (1 / 3)
            striker.bat_run_counts["4"] += adjustment * (1 / 3)

        if batter.balls_faced > 20 and (batter.runs_scored / batter.balls_faced) < 110:
            adjustment = random.uniform(0.05, 0.08)
            striker.bat_run_counts["0"] += adjustment * (1.5 / 3)
            striker.bat_run_counts["1"] += adjustment * (0.5 / 3)
            striker.bat_run_counts["6"] += adjustment * (2 / 3)
            out_probability += 0.05

        if batter.balls_faced > 40 and (batter.runs_scored / batter.balls_faced) < 120:
            adjustment = random.uniform(0.06, 0.09)
            striker.bat_run_counts["0"] += adjustment * (1.2 / 3)
            striker.bat_run_counts["1"] += adjustment * (0.7 / 3)
            striker.bat_run_counts["6"] += adjustment * (1.8 / 3)
            out_probability += 0.04

        if (
            batter.balls_faced > 30
            and (batter.runs_scored / batter.balls_faced) > 145
            and (wickets_fallen < 5)
            or balls_bowled > 102
        ):
            adjustment = random.uniform(0.06, 0.09)
            striker.bat_run_counts["0"] -= adjustment * (1 / 3)
            striker.bat_run_counts["1"] -= adjustment * (1.5 / 3)
            striker.bat_run_counts["4"] += adjustment * (1.6 / 3)
            striker.bat_run_counts["6"] += adjustment * (1.9 / 3)
            if target is not None:
                out_probability += 0.02

        if target is None:
            if balls_bowled > 105 and (score / balls_bowled) < 1.17:
                adjustment = random.uniform(0.06, 0.09)
                striker.bat_run_counts["0"] += adjustment * (1.2 / 3)
                striker.bat_run_counts["1"] -= adjustment * (1.6 / 3)
                striker.bat_run_counts["4"] += adjustment * (1.4 / 3)
                striker.bat_run_counts["6"] += adjustment * (2.1 / 3)
                out_probability += 0.03

            elif balls_bowled > 60 and (score / balls_bowled) < 1.1:
                adjustment = random.uniform(0.06, 0.09)
                striker.bat_run_counts["0"] -= adjustment * (1.2 / 3)
                striker.bat_run_counts["1"] -= adjustment * (0.8 / 3)
                striker.bat_run_counts["4"] += adjustment * (1 / 3)
                striker.bat_run_counts["6"] += adjustment * (1 / 3)
                out_probability += 0.02

    def adjust_bowler_settings(self, bowler: Player, spin_factor, pace_factor):
        # sourcery skip: remove-redundant-if
        if "break" or "spin" in bowler.bowling_style:
            effect = (1.0 - spin_factor) / 2
            bowler.bowl_out_rate += effect * 0.25
            bowler.bowl_run_probabilities["0"] += effect * 0.25
            bowler.bowl_run_probabilities["1"] += effect * 0.25
            bowler.bowl_run_probabilities["4"] -= effect * 0.38
            bowler.bowl_run_probabilities["6"] -= effect * 0.3

        elif "medium" or "fast" in bowler["bowlStyle"]:
            effect = (1.0 - pace_factor) / 2
            bowler.bowl_out_rate += effect * 0.22
            bowler.bowl_run_probabilities["0"] += effect * 0.18
            bowler.bowl_run_probabilities["1"] += effect * 0.22
            bowler.bowl_run_probabilities["4"] -= effect * 0.4
            bowler.bowl_run_probabilities["6"] -= effect * 0.3

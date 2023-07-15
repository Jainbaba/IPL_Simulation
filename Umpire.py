import random
from Commentator import Commentator
from Settings import Setting
from Summary import MatchSummary
from Teams import Team
from Players import Player
from Tracking import Tracker
from Utils import Utils


class Umpire:
    """
    Umpire class to conduct match innings.

    Parameters:
      - spin_factor (float): Spin pitch factor
      - pace_factor (float): Pace pitch factor
      - batting_team (Team): Batting team
      - bowling_team (Team): Bowling team
      - commentator (Commentator): Commentator object
      - target (int, optional): Target score for 2nd innings

    Attributes:

      - batting_order (list): Batting team batting order
      - bowling_order (list): Bowling team bowling order
      - batting_team (Team): Batting team
      - bowling_team (Team): Bowling team
      - spin_factor (float): Spin pitch factor
      - pace_factor (float): Pace pitch factor
      - target (int): Target score
      - wickets_fallen (int): Wickets fallen
      - runs_scored (int): Runs scored
      - balls_bowled (int): Balls bowled
      - overs (str): Current over
      - striker (Player): Striker batter
      - non_striker (Player): Non-striker batter
      - current_bowler (Player): Current bowler
      - previous_bowler (Player): Previous bowler
      - commentator (Commentator): Commentator object
      - utils (Utils): Utils object
      - settings (Settings): Settings object

    Methods:

      __init__():
        Initializes Umpire object

      change_strike():
        Swaps striker and non-striker batters

      match_result():
        Prints match result summary

      dismiss_batsman():
        Dismisses batsman and brings in new batsman

      wicketType():
        Handles wicket based on dismissal type

      calculate_batter_bowler_probabilities():
        Calculates batting/bowling probabilities

      deliver_ball():
        Delivers a ball for the current over by the specified bowler.
        Updates overs, bowler stats, batter stats, match situation etc.

      predict_ball_outcome():
        Predicts run/wicket outcome for a delivery based on probabilities.

      update_runs():
        Updates runs scored, batter/bowler stats after a delivery.

      is_death_bowler():
        Checks if a bowler is a designated death bowler.

      select_powerplay_bowler():
        Selects powerplay bowler based on current match stats.

      select_middle_overs_bowler():
        Selects bowler for middle overs based on current match stats.
        Checks if current bowler stats indicate they should be replaced.
        Prioritizes bowlers who haven't bowled yet.
        Favors bowlers with better economy rates.

      select_death_overs_bowler():
        Selects bowler for death overs based on current match stats.
        Checks if current death bowler should be replaced.
        Prioritizes bowlers who haven't bowled yet.
        Favors bowlers with better economy rates.

      play_innings():
        Simulates an innings by delivering balls over-by-over.
        Selects opening, middle overs, and death overs bowlers based on stats.
        Alternates deliveries between previous and current bowler.
        Selects new bowlers when needed based on overs.
        Updates match situation after each ball - runs, wickets, etc.
    """

    def __init__(
        self,
        spin_factor,
        pace_factor,
        batting_team: Team,
        bowling_team: Team,
        commentator: Team,
        target=None,
    ):
        self.batting_order: list(Player) = batting_team.batting_order()
        self.bowling_order: list(Player) = bowling_team.bowling_order()
        self.batting_team = batting_team
        self.bowling_team = bowling_team
        self.spin_factor = spin_factor
        self.pace_factor = pace_factor
        self.target = target
        self.wickets_fallen = 0
        self.runs_scored = 0
        self.balls_bowled = 0
        self.overs = ""
        self.striker: Player = self.batting_order[0]
        self.non_striker: Player = self.batting_order[1]
        self.current_bowler: Player = None
        self.previous_bowler: Player = None
        self.commentator: Commentator = commentator
        self.utils = Utils()
        self.settings = Setting()

    def get_tracker(self, team: Team, player: Player):
        return team.match_trackers.get(player.name)

    def change_strike(self):
        self.striker, self.non_striker = self.non_striker, self.striker

    def match_result(self):
        if self.runs_scored == (self.target - 1) and (
            self.balls_bowled == 120 or self.wickets_fallen == 10
        ):
            self.commentator.tie_message(
                f"{self.runs_scored}/{self.wickets_fallen}",
                self.batting_team,
                self.bowling_team,
                self.overs,
            )
        elif self.runs_scored >= self.target:
            self.commentator.winner_message(
                f"{self.runs_scored}/{self.wickets_fallen}",
                self.batting_team,
                self.bowling_team,
                self.overs,
                True,
                10 - self.wickets_fallen,
            )
        elif self.balls_bowled == 120 or self.wickets_fallen == 10:
            self.commentator.winner_message(
                f"{self.runs_scored}/{self.wickets_fallen}",
                self.batting_team,
                self.bowling_team,
                self.overs,
                False,
                (self.target - 1) - self.runs_scored,
            )
        return

    def find_batsman(self, players_tracker: Tracker):
        for player in players_tracker:
            if player.balls_faced == 0:
                for batsman in self.batting_team:
                    if batsman.name == player.name:
                        return batsman

    def dismiss_batsman(self, player):
        if self.wickets_fallen < 10:
            if self.striker == player:
                self.striker = self.batting_order[self.wickets_fallen + 1]
            else:
                self.non_striker = self.batting_order[self.wickets_fallen + 1]
        self.commentator.new_batsman_message(
            f"{self.runs_scored}/{self.wickets_fallen}",
            self.batting_team,
            self.bowling_team,
            self.overs,
            self.striker,
            self.current_bowler,
        )

    def wicketType(self, dismissal_type):
        if dismissal_type == "runOut":
            run_out_runs = random.randint(0, 2)
            self.runs_scored += run_out_runs
            self.utils.update_batter_tracker(
                self.get_tracker(self.batting_team, self.striker),
                run_out_runs,
                1,
                f"W(Run out):{self.current_bowler.name}:{self.balls_bowled}:{run_out_runs}",
            )
            self.utils.update_bowler_tracker(
                self.get_tracker(self.bowling_team, self.current_bowler),
                run_out_runs,
                1,
                False,
                True,
                False,
                f"{self.balls_bowled}:W(Run out):{run_out_runs}",
            )
            self.commentator.wicket_message(
                f"{self.runs_scored}/{self.wickets_fallen}",
                self.batting_team,
                self.bowling_team,
                self.striker,
                self.current_bowler,
                None,
                "Run out",
                run_out_runs,
                self.overs,
            )
            self.dismiss_batsman(self.striker)
            return
        elif dismissal_type == "caught":
            feilder: Player = self.bowling_team.determine_catcher()
            self.utils.update_batter_tracker(
                self.get_tracker(self.batting_team, self.striker),
                0,
                1,
                f"W(Caught By {feilder.name}):{self.current_bowler.name}:{self.balls_bowled}:0",
            )
            self.utils.update_bowler_tracker(
                self.get_tracker(self.bowling_team, self.current_bowler),
                0,
                1,
                False,
                True,
                False,
                f"{self.balls_bowled}:W(CaughtBy {feilder.name})",
            )
            self.utils.update_bowler_tracker(
                self.get_tracker(self.bowling_team, feilder),
                0,
                0,
                False,
                False,
                True,
                f"{self.balls_bowled}:Catch({self.striker})",
            )
            self.commentator.wicket_message(
                f"{self.runs_scored}/{self.wickets_fallen}",
                self.batting_team,
                self.bowling_team,
                self.striker,
                self.current_bowler,
                feilder,
                "Caught",
                0,
                self.overs,
            )
            self.dismiss_batsman(self.striker)
            return
        elif dismissal_type in ["bowled", "lbw", "hitwicket", "stumped"]:
            self.utils.update_batter_tracker(
                self.get_tracker(self.batting_team, self.striker),
                0,
                1,
                f"W({dismissal_type}):{self.current_bowler.name}:{self.balls_bowled}:0",
            )
            self.utils.update_bowler_tracker(
                self.get_tracker(self.bowling_team, self.current_bowler),
                0,
                1,
                False,
                True,
                False,
                f"{self.balls_bowled}:W({dismissal_type})",
            )
            self.commentator.wicket_message(
                f"{self.runs_scored}/{self.wickets_fallen}",
                self.batting_team,
                self.bowling_team,
                self.striker,
                self.current_bowler,
                None,
                dismissal_type,
                0,
                self.overs,
            )
            self.dismiss_batsman(self.striker)
            return

    def calculate_batter_bowler_probabilities(self):
        self.out_probability = (
            self.striker.bat_out_rate + self.current_bowler.bowl_out_rate
        ) / 2
        self.run_probabilities = {
            str(run): (
                (
                    self.striker.bat_run_probabilities[str(run)]
                    + self.current_bowler.bowl_run_probabilities[str(run)]
                )
                / 2
            )
            for run in range(7)
        }
        self.dismissal_probabilities = {
            _: (
                self.striker.bat_out_probabilities[_]
                + self.current_bowler.bowl_out_probabilities[_]
            )
            / 2
            for _ in ["caught", "bowled", "lbw", "hitwicket", "stumped"]
        }
        self.dismissal_probabilities["runOut"] = self.striker.run_out_probability

    def deliver_ball(self, over, bowler):
        # self.previous_bowler = self.current_bowler
        self.current_bowler = bowler
        self.settings.adjust_bowler_settings(
            self.current_bowler, self.spin_factor, self.pace_factor
        )
        balls_in_over = 0
        if self.target is not None:
            while self.balls_bowled < (over + 1) * 6 and (
                self.wickets_fallen < 10 or self.runs_scored < self.target
            ):
                balls_in_over += 1
                self.overs = f"{over}.{balls_in_over}"
                self.settings.adjust_batsman_settings(
                    self.batting_team.match_trackers.get(self.striker.name),
                    self.striker,
                    self.wickets_fallen,
                    self.balls_bowled,
                    self.runs_scored,
                    self.striker.bat_out_rate,
                )
                self.settings.second_innings_settings(
                    self.striker,
                    self.balls_bowled,
                    self.wickets_fallen,
                    self.striker.bat_out_rate,
                    self.runs_scored,
                    self.target,
                )
                self.calculate_batter_bowler_probabilities()
                self.predict_ball_outcome(self.run_probabilities)
        else:
            while self.balls_bowled < (over + 1) * 6 and self.wickets_fallen < 10:
                balls_in_over += 1
                self.overs = f"{over}.{balls_in_over}"
                self.settings.adjust_batsman_settings(
                    self.batting_team.match_trackers.get(self.striker.name),
                    self.striker,
                    self.wickets_fallen,
                    self.balls_bowled,
                    self.runs_scored,
                    self.striker.bat_out_rate,
                )
                self.settings.first_innings_settings(
                    self.striker,
                    self.balls_bowled,
                    self.wickets_fallen,
                    self.striker.bat_out_rate,
                )
                self.calculate_batter_bowler_probabilities()
                self.predict_ball_outcome(self.run_probabilities)

    def predict_ball_outcome(self, run_probabilities):
        if self.current_bowler.bowl_wide_rate > random.uniform(0, 1):
            self.runs_scored += 1
            self.utils.update_bowler_tracker(
                self.get_tracker(self.bowling_team, self.current_bowler),
                1,
                0,
                False,
                False,
                False,
                f"{self.balls_bowled}:Wide",
            )
            self.commentator.wide_message(
                f"{self.runs_scored}/{self.wickets_fallen}",
                self.batting_team,
                self.bowling_team,
                self.striker,
                self.current_bowler,
                self.overs,
            )
            return

        total_probability = sum(run_probabilities[val] for val in run_probabilities)
        last_end = 0
        run_ranges = []
        for denom in run_probabilities:
            run_range = {
                "run": denom,
                "start": last_end,
                "end": last_end + run_probabilities[denom],
            }
            run_ranges.append(run_range)
            last_end += run_probabilities[denom]
        self.balls_bowled += 1
        random_num = random.uniform(0, total_probability)

        for run_range in run_ranges:
            if run_range["start"] <= random_num < run_range["end"]:
                runs = int(run_range["run"])
                self.runs_scored += runs
                if runs != 0:
                    self.update_runs(runs)
                    if runs % 2 == 1:
                        self.change_strike()
                    return runs
                else:
                    out_probability = self.out_probability * (
                        total_probability / run_probabilities["0"]
                    )
                    out_chance = random.uniform(0, 1)
                    if out_probability > out_chance:
                        self.wickets_fallen += 1
                        total_dismissals = sum(
                            self.dismissal_probabilities[val]
                            for val in self.dismissal_probabilities
                        )
                        last_end = 0
                        dismissal_ranges = []
                        for dismissal in self.dismissal_probabilities:
                            dismissal_range = {
                                "dismissal": dismissal,
                                "start": last_end,
                                "end": last_end
                                + self.dismissal_probabilities[dismissal],
                            }
                            dismissal_ranges.append(dismissal_range)
                            last_end += self.dismissal_probabilities[dismissal]
                        random_dismissal = random.uniform(0, total_dismissals)
                        for dismissal_range in dismissal_ranges:
                            if (
                                dismissal_range["start"]
                                <= random_dismissal
                                < dismissal_range["end"]
                            ):
                                self.wicketType(dismissal_range["dismissal"])
                    else:
                        self.update_runs(runs)
                        return runs

    def update_runs(self, runs):
        self.utils.update_bowler_tracker(
            self.get_tracker(self.bowling_team, self.current_bowler),
            runs,
            1,
            False,
            False,
            False,
            f"{self.balls_bowled}:{runs}",
        )
        self.utils.update_batter_tracker(
            self.get_tracker(self.batting_team, self.striker),
            runs,
            1,
            f"{self.balls_bowled}:{runs}",
        )
        self.commentator.run_message(
            f"{self.runs_scored}/{self.wickets_fallen}",
            self.batting_team,
            self.bowling_team,
            self.striker,
            self.current_bowler,
            runs,
            self.overs,
        )

    def select_powerplay_bowler(self, over, current_bowler: Player):
        bowler_stats: Tracker = self.bowling_team.match_trackers.get(
            current_bowler.name
        )

        if (
            bowler_stats.balls_bowled > 0
            and (
                bowler_stats.balls_bowled > 11
                or bowler_stats.runs_conceded / bowler_stats.balls_bowled > 1.7
            )
            and (
                bowler_stats.balls_bowled > 11
                or bowler_stats.wickets_taken / bowler_stats.balls_bowled < 0.091
            )
        ):
            local_bowlers = [
                bowler
                for bowler in self.bowling_order
                if bowler.overs_avg[str(over + 1)] is not None
            ]
            local_bowlers.sort(key=lambda k: k.overs_avg[str(over + 1)], reverse=True)

            while True:
                bowler_pick: Player = random.choice(local_bowlers)
                bowler_pick_stats: Tracker = self.bowling_team.match_trackers.get(
                    bowler_pick.name
                )
                if (
                    bowler_pick_stats.balls_bowled < 11
                    and self.previous_bowler != bowler_pick
                ):
                    return bowler_pick
        return current_bowler

    def is_death_bowler(self, bowler: Player):
        return bowler in self.death_bowlers[:4]

    def select_middle_overs_bowler(self, current_bowler: Player, middle_bowlers):
        bowler_stats: Tracker = self.bowling_team.match_trackers.get(
            current_bowler.name
        )
        selected_bowler = current_bowler

        if (
            self.is_death_bowler(selected_bowler)
            and bowler_stats.balls_bowled > 0
            and (
                (
                    bowler_stats.balls_bowled > 17
                    or bowler_stats.runs_conceded / bowler_stats.balls_bowled > 1.5
                    or (
                        bowler_stats.runs_conceded / bowler_stats.balls_bowled
                        - self.runs_scored / self.balls_bowled
                    )
                    > 0.2
                )
                and (
                    bowler_stats.balls_bowled > 17
                    or bowler_stats.runs_conceded / bowler_stats.balls_bowled < 0.088
                )
            )
        ):
            bowlers_by_strike_rate: list(Player) = sorted(
                self.bowling_order, key=lambda k: k.bowl_balls_faced_rate, reverse=True
            )
            for bowler in bowlers_by_strike_rate:
                if not self.is_death_bowler(bowler) and (
                    self.bowling_team.match_trackers.get(bowler.name).balls_bowled < 7
                    and bowler.name != self.previous_bowler.name
                ):
                    selected_bowler = bowler
                    break

            if selected_bowler == current_bowler:
                for _ in range(7):
                    bowler_pick: Player = random.choice(middle_bowlers)
                    bowler_pick_stats: Tracker = self.bowling_team.match_trackers.get(
                        bowler_pick.name
                    )
                    if (
                        bowler_pick_stats.balls_bowled == 0
                        and not self.is_death_bowler(bowler_pick_stats)
                    ):
                        selected_bowler = bowler_pick
                        break
                    elif self.is_death_bowler(bowler_pick_stats):
                        if bowler_pick_stats.balls_bowled < 11:
                            if (
                                bowler_pick_stats.runs_conceded
                                / bowler_pick_stats.balls_bowled
                                < 1.5
                            ):
                                if bowler_pick_stats.name != self.previous_bowler.name:
                                    selected_bowler = bowler_pick
                                    break
                            elif (
                                bowler_pick_stats.runs_conceded
                                / bowler_pick_stats.balls_bowled
                                > 0.088
                            ):
                                if bowler_pick_stats.name != self.previous_bowler.name:
                                    selected_bowler = bowler_pick
                                    break
                    elif (
                        0 < bowler_pick_stats.balls_bowled < 24
                        and bowler_pick_stats.runs_conceded
                        / bowler_pick_stats.balls_bowled
                        < 1.5
                    ):
                        if bowler_pick_stats.name != self.previous_bowler.name:
                            selected_bowler = bowler_pick
                            break
                    elif (
                        0 < bowler_pick_stats.balls_bowled < 11
                        and bowler_pick_stats.runs_conceded
                        / bowler_pick_stats.balls_bowled
                        > 0.088
                    ):
                        if bowler_pick_stats.name != self.previous_bowler.name:
                            selected_bowler = bowler_pick
                            break

        elif bowler_stats.balls_bowled != 0 and (
            (
                bowler_stats.balls_bowled > 19
                or bowler_stats.runs_conceded / bowler_stats.balls_bowled > 1.6
                or (
                    bowler_stats.runs_conceded / bowler_stats.balls_bowled
                    - self.balls_bowled / self.runs_scored
                )
                > 0.2
            )
            and (
                bowler_stats.balls_bowled > 19
                or bowler_stats.runs_conceded / bowler_stats.balls_bowled < 0.095
            )
        ):
            bowlers_by_strike_rate = sorted(
                self.bowling_order, key=lambda k: k.bowl_balls_faced_rate, reverse=True
            )
            for bowler in bowlers_by_strike_rate:
                if not self.is_death_bowler(bowler) and (
                    self.bowling_team.match_trackers.get(bowler.name).balls_bowled < 7
                    and bowler.name != self.previous_bowler.name
                ):
                    selected_bowler = bowler
                    break

            if selected_bowler == current_bowler:
                for _ in range(7):
                    bowler_pick = random.choice(middle_bowlers)
                    bowler_pick_stats = self.bowling_team.match_trackers.get(
                        bowler_pick.name
                    )
                    if (
                        bowler_pick_stats.balls_bowled == 0
                        and not self.is_death_bowler(bowler_pick_stats)
                    ):
                        selected_bowler = bowler_pick
                        break
                    elif self.is_death_bowler(bowler_pick_stats):
                        if (
                            0 < bowler_pick_stats.balls_bowled < 11
                            and (
                                bowler_pick_stats.runs_conceded
                                / bowler_pick_stats.balls_bowled
                                < 1.7
                                or bowler_pick_stats.runs_conceded
                                / bowler_pick_stats.balls_bowled
                                > 0.088
                            )
                            and bowler_pick_stats.name != self.previous_bowler.name
                        ):
                            selected_bowler = bowler_pick
                            break
                    elif (
                        0 < bowler_pick_stats.balls_bowled < 24
                        and (
                            bowler_pick_stats.runs_conceded
                            / bowler_pick_stats.balls_bowled
                            < 1.6
                            or bowler_pick_stats.runs_conceded
                            / bowler_pick_stats.balls_bowled
                            < 0.1
                        )
                        and bowler_pick_stats.name != self.previous_bowler.name
                    ):
                        selected_bowler = bowler_pick
                        break

        return selected_bowler

    def select_death_overs_bowler(self, current_bowler: Player, death_bowlers):
        current_bowler_stats: Tracker = self.bowling_team.match_trackers.get(
            current_bowler.name
        )
        selected_bowler = current_bowler

        if (
            not self.is_death_bowler(selected_bowler)
            or 0 < current_bowler_stats.balls_bowled > 23
        ):
            for bowler in death_bowlers:
                bowler_stats: Tracker = self.bowling_team.match_trackers.get(
                    bowler.name
                )
                if bowler_stats.balls_bowled == 0:
                    selected_bowler = bowler
                    break
                elif (
                    bowler_stats.balls_bowled < 19
                    and bowler_stats.name != self.previous_bowler.name
                    and any(
                        tracker.balls_bowled != 0
                        and tracker.balls_bowled < 23
                        and (
                            tracker.runs_conceded == 0
                            or (tracker.balls_bowled / tracker.runs_conceded) < 1.2
                            or (tracker.wickets_taken / tracker.balls_bowled) > 0.16
                        )
                        for track, tracker in self.bowling_team.match_trackers.items()
                        if self.previous_bowler.name != track
                    )
                ):
                    selected_bowler = bowler
                    break

        return selected_bowler

    def play_innings(self):
        self.opening_bowlers = self.utils._extracted_from_blowers(
            self.bowling_order, "overs_avg", "1"
        )
        self.middle_bowlers = self.utils._extracted_from_blowers(
            self.bowling_order, "overs_avg", "10"
        )
        self.death_bowlers = self.utils._extracted_from_blowers(
            self.bowling_order, "overs_avg", "19"
        )

        for i in range(20):
            if self.wickets_fallen >= 10 or (
                self.target is not None and self.target <= self.runs_scored
            ):
                break
            if i != 0:
                self.change_strike()
                self.commentator.change_in_overs_message(
                    self.runs_scored,
                    self.batting_team,
                    self.bowling_team,
                    self.overs,
                    self.previous_bowler,
                    self.current_bowler,
                )
            
            if i < 2:
                if i % 2 == 0:
                     if i == 0:
                        self.commentator.opening_batsmen_message(
                            self.batting_team,
                            self.bowling_team,
                            self.striker,
                            self.non_striker,
                            self.opening_bowlers[0],
                            self.target,
                        )
                     self.deliver_ball(
                    i, self.opening_bowlers[0]
                )
                else:
                    if i == 0:
                        self.commentator.opening_batsmen_message(
                            self.batting_team,
                            self.bowling_team,
                            self.striker,
                            self.non_striker,
                            self.opening_bowlers[1],
                            self.target,
                        ) 
                    self.deliver_ball(i, self.opening_bowlers[1])
                self.previous_bowler = (
                    self.opening_bowlers[0] if i % 2 != 1 else self.opening_bowlers[1]
                )     
            if i < 6:
                self.deliver_ball(
                    i, self.select_powerplay_bowler(i, self.current_bowler)
                ) if i % 2 == 1 else self.deliver_ball(
                    i, self.select_powerplay_bowler(i, self.previous_bowler)
                )
            if i < 15:
                self.deliver_ball(
                    i,
                    self.select_middle_overs_bowler(
                        self.current_bowler, self.middle_bowlers
                    ),
                ) if i % 2 == 1 else self.deliver_ball(
                    i,
                    self.select_middle_overs_bowler(
                        self.previous_bowler, self.middle_bowlers
                    ),
                )
            else:
                self.deliver_ball(
                    i,
                    self.select_death_overs_bowler(
                        self.current_bowler, self.death_bowlers
                    ),
                ) if i % 2 == 1 else self.deliver_ball(
                    i,
                    self.select_death_overs_bowler(
                        self.previous_bowler, self.death_bowlers
                    ),
                )
        summary = MatchSummary()
        summary.get_summary(
            self.batting_team.match_trackers.values(),
            self.bowling_team.match_trackers.values(),
        )
        return self.runs_scored if self.target is None else self.match_result()

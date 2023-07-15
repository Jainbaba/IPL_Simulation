import random
from Feild import Feild
from Teams import Team
from Umpire import Umpire
from Commentator import Commentator
from Summary import MatchSummary
class Match:
    """
    Match class to simulate an IPL cricket match.

    Parameters:
    - None

    Attributes:
    - fields: Feild object to handle field conditions
    - team_a: First Team object selected by user
    - team_b: Second Team object selected by user
    - dew: Boolean indicating if dew is present
    - pitch_deterioration: Boolean indicating pitch deterioration
    - pitch_type: String indicating pitch type - "dead", "green", "dusty"
    - commentator: Commentator object to generate match commentary
    - batting_team: Team object for team batting first
    - bowling_team: Team object for team bowling first
    - pace_factor: Float pace bowling pitch factor
    - spin_factor: Float spin bowling pitch factor
    - first_innings: Umpire object to conduct first innings
    - target: Integer target score for second innings
    - second_innings: Umpire object to conduct second innings

    Methods:

    intro():
      - Prints match intro and prompts user to select 2 teams
      - Returns selected Team objects as team_a and team_b

    conduct_toss():
      - Simulates coin toss using randomness
      - Determines team decision to bat or bowl first
      - Returns batting_team, bowling_team order based on toss
      - Uses commentator to print toss result
    """

    def __init__(self):
        fields = Feild()
        team_a, team_b = self.intro()
        dew, pitch_deterioration, pitch_type = fields.get_field_status()
        commentator = Commentator(team_a, team_b)
        batting_team, bowling_team = self.conduct_toss(
            dew, pitch_deterioration, pitch_type, team_a, team_b, commentator
        )
        pace_factor, spin_factor = fields.pitch_info(pitch_type)
        first_innings = Umpire(
            spin_factor, pace_factor, batting_team, bowling_team, commentator
        )
        target = first_innings.play_innings() + 1
        second_innings = Umpire(
            spin_factor, pace_factor, bowling_team, batting_team, commentator, target
        )
        second_innings.play_innings()

    def intro(self):
        teams = [
            "Chennai Super Kings",
            "Delhi Capitals",
            "Kolkata Knight Riders",
            "Mumbai Indians",
            "Punjab Kings",
            "Royal Challengers Bangalore",
            "Rajasthan Royals",
            "Sunrisers Hyderabad",
        ]

        print("Welcome to the IPL simulation!")
        print("Please select two teams to compete from the following list:")
        print()

        for i, team in enumerate(teams, 1):
            print(f"{i}. {team}")

        while True:
            team1_choice = input("Enter the number for the first team: ")
            team2_choice = input("Enter the number for the second team: ")

            if (
                team1_choice.isdigit()
                and team2_choice.isdigit()
                and 1 <= int(team1_choice) <= len(teams)
                and 1 <= int(team2_choice) <= len(teams)
                and team1_choice != team2_choice
            ):
                team1_choice = int(team1_choice)
                team2_choice = int(team2_choice)
                break

            print("Invalid input. Please try again.")

        team1 = Team(teams[team1_choice - 1])
        team2 = Team(teams[team2_choice - 1])

        print()
        print(
            f"Great! The {team1.name} will be competing against the {team2.name} in this simulation."
        )
        return team1, team2

    def conduct_toss(
        self,
        dew,
        pitchDetoriate,
        typeOfPitch,
        team_a: Team,
        team_b: Team,
        commentator: Commentator,
    ):
        batting_chance = 0.45
        if dew:
            batting_chance -= random.uniform(0.09, 0.2)
        if pitchDetoriate:
            batting_chance += random.uniform(0.09, 0.2)
        if typeOfPitch == "dead":
            batting_chance -= random.uniform(0.05, 0.15)
        elif typeOfPitch == "green":
            batting_chance += random.uniform(0.05, 0.15)
        elif typeOfPitch == "dusty":
            batting_chance += random.uniform(0.04, 0.1)

        toss = random.randint(0, 1)
        outcome = random.uniform(0, 1)
        if toss == 0:
            if outcome > batting_chance:
                commentator.toss_message(team_a, "Bat")
                return [team_a, team_b]
            commentator.toss_message(team_a, "Bowl")
            return [team_b, team_a]
        if outcome > batting_chance:
            commentator.toss_message(team_b, "Bat")
            return [team_b, team_a]
        else:
            commentator.toss_message(team_b, "Bowl")
            return [team_a, team_b]


import logging
from Players import Player
from Teams import Team


class Commentator:
    """
    Commentator class to generate match commentary.

    Parameters:
    - team_a: First Team object
    - team_b: Second Team object

    Methods:

    __init__():
    - Generates introductory commentary with team names and players

    toss_message():
    - Generates commentary for toss result
    - Parameters:
        - toss_winner: Winning Team object
        - decision: Decision to bat or bowl first

    wicket_message():
    - Generates commentary for a wicket
    - Parameters:
        - score: Current score
        - batting_team: Batting Team object
        - bowling_team: Bowling Team object
        - batsmen: Batsman Player object
        - bowler: Bowler Player object
        - catcher: Catcher Player object (if caught out)
        - wicket_type: Type of wicket
        - runs: Runs scored on that delivery
        - over: Current over number

    run_message():
    - Generates commentary for runs scored
    - Parameters:
        - score: Current score
        - batting_team: Batting Team object
        - bowling_team: Bowling Team object
        - batsmen: Batsman Player object
        - bowler: Bowler Player object
        - runs: Runs scored
        - over: Current over number

    wide_message():
    - Generates commentary for a wide delivery
    - Parameters:
        - score: Current score
        - batting_team: Batting Team object
        - bowling_team: Bowling Team object
        - batsmen: Batsman Player object
        - bowler: Bowler Player object
        - over: Current over number

    winner_message():
    - Generates match result commentary
    - Parameters:
        - score: Final score
        - battingTeam: Batting Team object
        - bowling_team: Bowling Team object
        - over: Final over
        - target_chased: Boolean if target was chased
        - remaining: Remaining wickets or runs

    generate_reply():
    - Prints generated commentary to console

    """

    def __init__(self, team_a: Team, team_b: Team) -> None:
        messages = {
            "Team A Name": team_a.name.capitalize(),
            "Team A Players": team_a.__str__(),
            "Team B Name": team_b.name.capitalize(),
            "Team B Players": team_b.__str__(),
        }
        commentary = f"Welcome to the cricket match between {messages['Team A Name']} and {messages['Team B Name']}."
        commentary += f"\n{messages['Team A Name']} has sent their top players onto the field: {messages['Team A Players']}."
        commentary += f"\nIn response, {messages['Team B Name']} is ready to showcase their skills with their talented players: {messages['Team B Players']}."
        self.generate_reply(commentary)

    def toss_message(self, toss_winner: Team, decision):
        messages = {"TossWonby": toss_winner.name.capitalize(), "Selected": decision}
        commentary = f"{messages['TossWonby']} has won the toss and elected to {messages['Selected']} first."
        self.generate_reply(commentary)

    def wicket_message(
        self,
        score,
        batting_team: Team,
        bowling_team: Team,
        batsmen: Player,
        bowler: Player,
        catcher: Player,
        wicket_type: str,
        runs,
        over,
    ):
        messages = {
            "Batting Team": batting_team.name.capitalize(),
            "Bowling Team": bowling_team.name.capitalize(),
            "Batsmen": batsmen.name.capitalize(),
            "Bowler": bowler.name.capitalize(),
            "Over": over,
            "Run scored": runs,
            "Score": score,
            "WicketType": wicket_type.capitalize(),
            "Catcher": catcher.name.capitalize()
            if wicket_type == "Caught"
            else "No Catcher Involved",
        }
        commentary = f"{messages['Batsmen']} is at the crease, facing {messages['Bowler']} from the {messages['Bowling Team']}."
        if messages["WicketType"] == "Caught":
            commentary += f"\nOh, what a catch! {messages['Batsmen']} is caught by {messages['Catcher']}."
        elif messages["WicketType"] == "RunOut":
            commentary += f"\nMiscommunication between the batsmen! {messages['Batsmen']} is run out."
        else:
            commentary += f"\n{messages['Batsmen']} {messages['WicketType']}! The {messages['Bowling Team']} strikes."
        commentary += f"\n{messages['Batting Team']} scores {messages['Run scored']} run(s) in the {messages['Over']} over(s). Total score: {messages['Score']}."
        self.generate_reply(commentary)

    def run_message(
        self,
        score,
        batting_team: Team,
        bowling_team: Team,
        batsmen: Player,
        bowler: Player,
        runs,
        over,
    ):
        messages = {
            "Batting Team": batting_team.name.capitalize(),
            "Bowling Team": bowling_team.name.capitalize(),
            "Batsmen": batsmen.name.capitalize(),
            "Bowler": bowler.name.capitalize(),
            "Over": over,
            "Run scored": runs,
            "Score": score,
        }
        commentary = f"{messages['Batsmen']} is at the crease, facing {messages['Bowler']} from {messages['Bowling Team']}."

        if runs == 4:
            commentary += f"\nThat's a fantastic shot! {messages['Batsmen']} smashes it for a FOUR!"

        elif runs == 6:
            commentary += f"\nIt's a maximum! {messages['Batsmen']} launches the ball into the stands for a SIX!"

        commentary += f"\n{messages['Batsmen']} scores {messages['Run scored']} run(s) in the {messages['Over']} over(s)."

        commentary += (
            f" {messages['Batting Team']} has a total score of {messages['Score']}."
        )
        self.generate_reply(commentary)

    def wide_message(
        self,
        score,
        batting_team: Team,
        bowling_team: Team,
        batsmen: Player,
        bowler: Player,
        over,
    ):
        messages = {
            "Batting Team": batting_team.name.capitalize(),
            "Bowling Team": bowling_team.name.capitalize(),
            "Batsmen": batsmen.name.capitalize(),
            "Bowler": bowler.name.capitalize(),
            "Over": over,
            "Run scored": "Wide",
            "Score": score,
        }
        commentary = f"{messages['Bowler']} bowls a wide delivery to {messages['Batsmen']} of {messages['Batting Team']}."
        commentary += f"\nWide ball! The umpire signals an extra run for {messages['Batting Team']}. Score: {messages['Score']}."
        self.generate_reply(commentary)

    def winner_message(
        self,
        score,
        battingTeam: Team,
        bowling_team: Team,
        over,
        target_chased,
        remaining,
    ):
        messages = {
            "Batting Team": battingTeam.name.capitalize(),
            "Bowling Team": bowling_team.name.capitalize(),
            "Over": f"{int(over.split('.')[0]) + 1}.0",
            "Score": score,
            "Result": f"Won By {abs(remaining)} wickets"
            if target_chased
            else f"Won By {abs(remaining)} runs",
            "Winner": battingTeam.name.capitalize()
            if target_chased
            else bowling_team.name.capitalize(),
        }
        if target_chased:
            commentary = f"{messages['Batting Team']} successfully chases down the target set by {messages['Bowling Team']}."
        else:
            commentary = f"{messages['Bowling Team']} defends their total against {messages['Batting Team']}."

        commentary += f"\n{messages['Winner']} emerges victorious! {messages['Winner']} {messages['Result']} in the {messages['Over']} over(s)."

        commentary += f"\nFinal score: {messages['Score']}."
        self.generate_reply(commentary)

    def tie_message(self, score, battingTeam: Team, bowling_team: Team, over):
        messages = {
            "Batting Team": battingTeam.name.capitalize(),
            "Bowling Team": bowling_team.name.capitalize(),
            "Over": f"{int(over.split('.')[0]) + 1}.0",
            "Score": score,
            "Result": "Tie",
            "Winner": None,
        }
        commentary = f"The match between {messages['Batting Team']} and {messages['Bowling Team']} ends in a tie."
        commentary += (
            f"\nFinal score: {messages['Score']} in the {messages['Over']} over(s)."
        )
        self.generate_reply(commentary)

    def new_batsman_message(
        self,
        score,
        batting_team: Team,
        bowling_team: Team,
        over,
        new_batsman: Player,
        bowler: Player,
    ):
        messages = {
            "Batting Team": batting_team.name.capitalize(),
            "Bowling Team": bowling_team.name.capitalize(),
            "New Batsman": new_batsman.name.capitalize(),
            "Bowler": bowler.name.capitalize(),
            "Over": over,
            "Score": score,
        }
        commentary = f"We have a new batsman coming in for {messages['Batting Team']}. {messages['New Batsman']} strides to the crease."
        commentary += f"\n{messages['Bowler']} is ready to bowl the over for {messages['Bowling Team']}."
        commentary += f"\nThe current score is {messages['Score']} in the {messages['Over']} over(s)."
        self.generate_reply(commentary)

    def change_in_overs_message(
        self,
        score,
        batting_team: Team,
        bowling_team: Team,
        over,
        previous_bowler: Player,
        new_bowler: Player,
    ):
        messages = {
            "Batting Team": batting_team.name.capitalize(),
            "Bowling Team": bowling_team.name.capitalize(),
            "Previous Bowler": previous_bowler.name.capitalize(),
            "New Bowler": new_bowler.name.capitalize(),
            "Over": f"{int(over.split('.')[0]) + 1}.0",
            "Score": score,
        }
        if previous_bowler == new_bowler:
            commentary = f"The current over is being bowled by {messages['Previous Bowler']} for {messages['Bowling Team']}."
            commentary += f"\nIt's a change of ends for {messages['Previous Bowler']} as they continue their spell."
        else:
            commentary = f"We have a change in bowling as {messages['Previous Bowler']}'s spell comes to an end."
            commentary += f"\n{messages['New Bowler']} takes over the bowling duties for {messages['Bowling Team']}."
        commentary += f"\nThe current score is {messages['Score']} in the {messages['Over']} over(s)."
        self.generate_reply(commentary)

    def opening_batsmen_message(
        self,
        batting_team: Team,
        bowling_team: Team,
        striker: Player,
        non_striker: Player,
        opening_bowler: Player,
        target=None,
    ):
        messages = {
            "Batting Team": batting_team.name.capitalize(),
            "Bowling Team": bowling_team.name.capitalize(),
            "Striker": striker.name.capitalize(),
            "Non-striker": non_striker.name.capitalize(),
            "Opening Bowler": opening_bowler.name.capitalize(),
            "Target": target if target is not None else None,
        }
        commentary = f"We have a great innings between {messages['Batting Team']} and {messages['Bowling Team']}."
        commentary += f"\nThe opening batsmen, {messages['Striker']} and {messages['Non-striker']}, are at the crease."
        commentary += f"\n{messages['Opening Bowler']} is ready to bowl the first over for {messages['Bowling Team']}."
        if messages["Target"] is not None:
            commentary += f"\n{messages['Batting Team']} is chasing a target of {messages['Target']} runs."
        self.generate_reply(commentary)

    def generate_reply(self, messages):
        print(f"**Commentator**:\n{messages}")
        print(
            "--------------------------------------------------------------------------"
        )


# class AiCommentator:
#     def __init__(self, team_a:Team, team_b:Team, feild) -> None:
#         self.team_a = team_a
#         self.team_b = team_b
#         self.feild = feild
#         messages = {
#             "Team A Name": self.team_a.name,
#             "Team A Players": self.team_a.__str__(),
#             "Team B Name": self.team_b.name,
#             "Team B Players": self.team_b.__str__(),
#             "Feild": self.feild,
#         }
#         self.generate_reply(messages)

#     def toss_message(self, toss_winner:Team, decision):
#         messages = {"TossWonby": toss_winner.name, "Selected": decision}
#         self.generate_reply(messages)

#     def wicket_message(
#         self,
#         score,
#         batting_team:Team,
#         bowling_team:Team,
#         batsmen,
#         bowler,
#         catcher,
#         wicket_type,
#         runs,
#         over,
#     ):
#         messages = {
#             "Batting Team": batting_team.name,
#             "Bowling Team": bowling_team.name,
#             "Batsmen": batsmen.__str__(),
#             "Bowler": bowler.__str__(),
#             "Over": over,
#             "Run scored": runs,
#             "Score": score,
#             "WicketType": wicket_type,
#             "Catcher": catcher.__str__()
#             if wicket_type == "caught"
#             else "No Catcher Involved",
#         }
#         self.generate_reply(messages)

#     def run_message(self, score, batting_team, bowling_team, batsmen, bowler, runs, over):
#         messages = {
#             "Batting Team": batting_team.name,
#             "Bowling Team": bowling_team.name,
#             "Batsmen": batsmen.__str__(),
#             "Bowler": bowler.__str__(),
#             "Over": over,
#             "Run scored": runs,
#             "Score": score,
#         }
#         self.generate_reply(messages)

#     def generate_reply(self, messages):
#         pattern = r"\[(.*?)\]"
#         prompt = f"{messages} Give me a One Line Comment acting as a IPL Commentator for this Match. Reply the Comment in this Format '[comment]' "
#         bard = Bard(token="")
#         reply = bard.get_answer(prompt)["content"]
#         matches = re.findall(pattern, reply)
#         print(matches[0])

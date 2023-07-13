from collections import Counter
from Tracking import Tracker


class Player:
    def calulateBattingPoints(self):
        self.BatrunProbilities = {
            run: self.batRunDenominations[run] / self.batBallsTotal
            for run in self.batRunDenominations
        }
        self.BatoutProbilities = {
            out: self.batOutTypes[out] / self.batBallsTotal for out in self.batOutTypes
        }
        self.BatoutRates = self.batOutsTotal / self.batBallsTotal
        self.runOutProbilities = self.runnedOut / self.batBallsTotal if self.BatoutRates != 1 else 0.01

        posTotal = 0
        count = 0
        self.posAvgsAll = None
        for pos, value in Counter(self.position).items():
            if pos != "null":
                self.posAvgsAll = {pos: value / self.matches}
                posTotal += pos * value
                count += value

        self.posAvg = posTotal / self.matches if count != 0 else 9.0

    def calulateBowlingPoints(self):
        self.bowlBallsTotalRate = self.bowlBallsTotal / self.matches
        self.catchRate = self.catches / self.matches
        self.bowlWideRate = self.bowlWides / self.bowlBallsTotal
        self.bowlNoballRate = self.bowlNoballs / self.bowlBallsTotal
        self.bowlrunProbilities = {
            run: self.bowlRunDenominations[run] / self.bowlBallsTotal
            for run in self.bowlRunDenominations
        }
        self.bowloutProbilities = {
            out: self.bowlOutTypes[out] / self.bowlBallsTotal
            for out in self.bowlOutTypes
        }
        self.bowlOutRates = self.bowlOutsTotal / self.bowlBallsTotal

        self.oversAvg = {
            "20": 0,
            "1": 0,
            "2": 0,
            "3": 0,
            "4": 0,
            "5": 0,
            "6": 0,
            "7": 0,
            "8": 0,
            "9": 0,
            "10": 0,
            "11": 0,
            "12": 0,
            "13": 0,
            "14": 0,
            "15": 0,
            "16": 0,
            "17": 0,
            "18": 0,
            "19": 0,
        }

        for over, value in Counter(self.overNumbers).items():
            self.oversAvg[over] = value / self.matches if self.matches != 0 else -1

    def __init__(self, player_data):
        self._id = player_data["_id"]
        self.playerInitials = player_data["playerInitials"]
        self.displayName = player_data["displayName"]
        self.batStyle = player_data["batStyle"]
        self.bowlStyle = player_data["bowlStyle"]
        self.batRunsTotal = player_data["batRunsTotal"]
        self.batBallsTotal = (
            player_data["batBallsTotal"] if player_data["batBallsTotal"] != 0 else 1
        )
        self.bowlRunsTotal = player_data["bowlRunsTotal"]
        self.bowlBallsTotal = (
            player_data["bowlBallsTotal"] if player_data["bowlBallsTotal"] != 0 else 1
        )
        self.batOutsTotal = player_data["batOutsTotal"]
        self.bowlOutsTotal = player_data["bowlOutsTotal"]
        self.bowlNoballs = player_data["bowlNoballs"]
        self.bowlWides = player_data["bowlWides"]
        self.catches = player_data["catches"]
        self.batOutTypes = player_data["batOutTypes"]
        self.bowlOutTypes = player_data["bowlOutTypes"]
        self.batRunDenominations = player_data["batRunDenominations"]
        self.bowlRunDenominations = player_data["bowlRunDenominations"]
        self.overNumbers = player_data["overNumbers"]
        self.runnedOut = player_data["runnedOut"]
        self.position = player_data["position"]
        self.byBatsman = player_data["byBatsman"]
        self.byBowler = player_data["byBowler"]
        self.captained = player_data["captained"]
        self.wicketkeeper = player_data["wicketkeeper"]
        self.matches = player_data["matches"]
        self.Tracker = Tracker(self.displayName)
        self.calulateBattingPoints()
        self.calulateBowlingPoints()

    
    def __str__(self):
        return (
            f"Player Information:\n"
            f"ID: {self._id}\n"
            f"Player Initials: {self.playerInitials}\n"
            f"Display Name: {self.displayName}\n"
            f"Batting Style: {self.batStyle}\n"
            f"Bowling Style: {self.bowlStyle}\n"
            f"Bat Runs Total: {self.batRunsTotal}\n"
            f"Bat Balls Total: {self.batBallsTotal}\n"
            f"Bowl Runs Total: {self.bowlRunsTotal}\n"
            f"Bowl Balls Total: {self.bowlBallsTotal}\n"
            f"Bat Outs Total: {self.batOutsTotal}\n"
            f"Bowl Outs Total: {self.bowlOutsTotal}\n"
            f"Bowl No Balls: {self.bowlNoballs}\n"
            f"Bowl Wides: {self.bowlWides}\n"
            f"Catches: {self.catches}\n"
            f"Bat Out Types: {self.batOutTypes}\n"
            f"Bowl Out Types: {self.bowlOutTypes}\n"
            f"Bat Run Denominations: {self.batRunDenominations}\n"
            f"Bowl Run Denominations: {self.bowlRunDenominations}\n"
            f"Over Numbers: {self.overNumbers}\n"
            f"Runned Out: {self.runnedOut}\n"
            f"Position: {self.position}\n"
            f"By Batsman: {self.byBatsman}\n"
            f"By Bowler: {self.byBowler}\n"
            f"Captained: {self.captained}\n"
            f"Wicketkeeper: {self.wicketkeeper}\n"
            f"Matches: {self.matches}\n"
            f"Batting Run Probabilities: {self.BatrunProbilities}\n"
            f"Batting Out Probabilities: {self.BatoutProbilities}\n"
            f"Batting Out Rates: {self.BatoutRates}\n"
            f"Run Out Probilities: {self.runOutProbilities}\n"
            f"Position Average: {self.posAvgsAll}\n"
            f"Position Overall Average: {self.posAvg}\n"
            f"Bowling Run Probabilities: {self.bowlrunProbilities}\n"
            f"Bowling Out Probabilities: {self.bowloutProbilities}\n"
            f"Bowling Out Rates: {self.bowlOutRates}\n"
            f"bowlBallsTotalRate: {self.bowlBallsTotalRate}\n"
            f"catchRate: {self.catchRate}\n"
            f"bowlWideRate: {self.bowlWideRate}\n"
            f"bowlNoballRate: {self.bowlNoballRate}\n"
            f"Overs Average: {self.oversAvg}\n"
        )

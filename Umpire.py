import logging
import random

from Utils import Utils


class Umpire:
    def __init__(self, spinFactor, paceFactor, battingTeam, bowlingTeam, commentator):
        logging.basicConfig(
            filename="app.log",
            filemode="w",
            format="%(levelname)s - %(message)s",
            level=logging.INFO,
        )
        self.BattingOrder = battingTeam.battingOrder()
        self.bowlingOrder = bowlingTeam.bowlingOrder()
        self.battingTeam = battingTeam
        self.bowlingTeam = bowlingTeam
        self.spinFactor = spinFactor
        self.paceFactor = paceFactor
        self.wickets = 0
        self.score = 0
        self.balls = 0
        self.overs = ""
        self.runRate = 0
        self.onStrike = self.BattingOrder[0]
        self.offStrike = self.BattingOrder[1]
        self.CurrentBowler = None
        self.PreviousBowler = None
        self.commentator = commentator
        self.utils = Utils()
        self.overTracker()

    def MatchSettings(self):
        # sourcery skip: merge-else-if-into-elif, min-max-identity
        if self.balls < 12:
            sixAdjustment = random.uniform(0.02, 0.05)
            self.outAvg = 0 if (self.outAvg < 0.07) else self.outAvg - 0.07
            sixAdjustment = (
                self.onStrike.batRunDenominations["6"]
                if sixAdjustment > self.onStrike.batRunDenominations["6"]
                else sixAdjustment
            )
            self.onStrike.batRunDenominations["6"] -= sixAdjustment
            self.onStrike.batRunDenominations["0"] += sixAdjustment * (1 / 3)
            self.onStrike.batRunDenominations["1"] += sixAdjustment * (2 / 3)
        elif 12 <= self.balls < 36:
            if self.wickets == 0:
                defenseAndOneAdjustment = random.uniform(0.05, 0.11)
                self.onStrike.batRunDenominations["0"] -= defenseAndOneAdjustment * (
                    2 / 3
                )
                self.onStrike.batRunDenominations["1"] -= defenseAndOneAdjustment * (
                    1 / 3
                )
                self.onStrike.batRunDenominations["4"] += defenseAndOneAdjustment * (
                    2 / 3
                )
                self.onStrike.batRunDenominations["6"] += defenseAndOneAdjustment * (
                    1 / 3
                )
            else:
                defenseAndOneAdjustment = random.uniform(0.02, 0.08)
                self.onStrike.batRunDenominations["0"] -= defenseAndOneAdjustment * (
                    2 / 3
                )
                self.onStrike.batRunDenominations["1"] -= defenseAndOneAdjustment * (
                    1 / 3
                )
                self.onStrike.batRunDenominations["4"] += defenseAndOneAdjustment * (
                    2.5 / 3
                )
                self.onStrike.batRunDenominations["6"] += defenseAndOneAdjustment * (
                    0.5 / 3
                )
                self.outAvg -= 0.03
        elif 36 <= self.balls < 102:
            if self.wickets < 3:
                defenseAndOneAdjustment = random.uniform(0.05, 0.11)
                self.onStrike.batRunDenominations["0"] -= defenseAndOneAdjustment * (
                    1.5 / 3
                )
                self.onStrike.batRunDenominations["1"] -= defenseAndOneAdjustment * (
                    1 / 3
                )
                self.onStrike.batRunDenominations["4"] += defenseAndOneAdjustment * (
                    1.5 / 3
                )
                self.onStrike.batRunDenominations["6"] += defenseAndOneAdjustment * (
                    1 / 3
                )
            else:
                defenseAndOneAdjustment = random.uniform(0.02, 0.07)
                self.onStrike.batRunDenominations["0"] -= defenseAndOneAdjustment * (
                    1.6 / 3
                )
                self.onStrike.batRunDenominations["1"] -= defenseAndOneAdjustment * (
                    1.2 / 3
                )
                self.onStrike.batRunDenominations["4"] += defenseAndOneAdjustment * (
                    2.1 / 3
                )
                self.onStrike.batRunDenominations["6"] += defenseAndOneAdjustment * (
                    0.9 / 3
                )
                self.outAvg -= 0.03
        else:
            if self.wickets < 7:
                defenseAndOneAdjustment = random.uniform(0.07, 0.1)
                self.onStrike.batRunDenominations["0"] -= defenseAndOneAdjustment * (
                    0.4 / 3
                )
                self.onStrike.batRunDenominations["1"] -= defenseAndOneAdjustment * (
                    1 / 3
                )
                self.onStrike.batRunDenominations["4"] += defenseAndOneAdjustment * (
                    1.4 / 3
                )
                self.onStrike.batRunDenominations["6"] += defenseAndOneAdjustment * (
                    1.8 / 3
                )
            else:
                defenseAndOneAdjustment = random.uniform(0.07, 0.09)
                self.onStrike.batRunDenominations["0"] -= defenseAndOneAdjustment * (
                    0.4 / 3
                )
                self.onStrike.batRunDenominations["1"] -= defenseAndOneAdjustment * (
                    1.8 / 3
                )
                self.onStrike.batRunDenominations["4"] += defenseAndOneAdjustment * (
                    1.5 / 3
                )
                self.onStrike.batRunDenominations["6"] += defenseAndOneAdjustment * (
                    1.5 / 3
                )
            self.outAvg += 0.01

    def FirstInningsProbabilitySettings(self):  # sourcery skip: low-code-quality
        batter = self.battingTeam.MatchTracker.get(self.onStrike.displayName)
        outsLast10 = self.wickets

        # Tweeting the Probabilities of Boundaries if Wickets are available in last 15 balls
        if self.balls < 105:
            adjust_last10 = random.uniform(0.02, 0.04)
            if outsLast10 < 2:
                self.onStrike.batRunDenominations["0"] -= adjust_last10 * (1 / 2)
                self.onStrike.batRunDenominations["1"] -= adjust_last10 * (1 / 2)
                self.onStrike.batRunDenominations["2"] += adjust_last10 * (1 / 2)
                self.onStrike.batRunDenominations["4"] += adjust_last10 * (1 / 2)
            else:
                adjust_last10 += 0.018
                self.onStrike.batRunDenominations["0"] += adjust_last10 * (1.1 / 2)
                self.onStrike.batRunDenominations["1"] += adjust_last10 * (0.9 / 2)
                self.onStrike.batRunDenominations["4"] -= adjust_last10 * (1 / 2)
                self.onStrike.batRunDenominations["6"] -= adjust_last10 * (1 / 2)
                self.outAvg -= 0.02

        # Opening Batsmen Settings
        if batter.ballsFaced < 8 and self.balls < 80:
            adjust = random.uniform(-0.01, 0.03)
            self.outAvg -= 0.015
            self.onStrike.batRunDenominations["0"] += adjust * (1.5 / 3)
            self.onStrike.batRunDenominations["1"] += adjust * (1 / 3)
            self.onStrike.batRunDenominations["2"] += adjust * (0.5 / 3)
            self.onStrike.batRunDenominations["4"] -= adjust * (0.5 / 3)
            self.onStrike.batRunDenominations["6"] -= adjust * (1.5 / 3)

        # Batsmen Played between 15-30 Balls
        if batter.ballsFaced > 15 and batter.ballsFaced < 30:
            adjust = random.uniform(0.03, 0.07)
            self.onStrike.batRunDenominations["0"] -= adjust * (1 / 3)
            self.onStrike.batRunDenominations["4"] += adjust * (1 / 3)

        if batter.ballsFaced > 20 and (batter.runsScored / batter.ballsFaced) < 110:
            adjust = random.uniform(0.05, 0.08)
            self.onStrike.batRunDenominations["0"] += adjust * (1.5 / 3)
            self.onStrike.batRunDenominations["1"] += adjust * (0.5 / 3)
            self.onStrike.batRunDenominations["6"] += adjust * (2 / 3)
            self.outAvg += 0.05

        if batter.ballsFaced > 40 and (batter.runsScored / batter.ballsFaced) < 120:
            adjust = random.uniform(0.06, 0.09)
            self.onStrike.batRunDenominations["0"] += adjust * (1.2 / 3)
            self.onStrike.batRunDenominations["1"] += adjust * (0.7 / 3)
            self.onStrike.batRunDenominations["6"] += adjust * (1.8 / 3)
            self.outAvg += 0.04

        if (
            batter.ballsFaced > 30
            and (batter.runsScored / batter.ballsFaced) > 145
            and (self.wickets < 5)
            or self.balls > 102
        ):
            adjust = random.uniform(0.06, 0.09)
            self.onStrike.batRunDenominations["0"] -= adjust * (1 / 3)
            self.onStrike.batRunDenominations["1"] -= adjust * (1.5 / 3)
            self.onStrike.batRunDenominations["4"] += adjust * (1.6 / 3)
            self.onStrike.batRunDenominations["6"] += adjust * (1.9 / 3)

        if self.balls > 105 and (self.score / self.balls) < 1.17:
            adjust = random.uniform(0.06, 0.09)
            self.onStrike.batRunDenominations["0"] += adjust * (1.2 / 3)
            self.onStrike.batRunDenominations["1"] -= adjust * (1.6 / 3)
            self.onStrike.batRunDenominations["4"] += adjust * (1.4 / 3)
            self.onStrike.batRunDenominations["6"] += adjust * (2.1 / 3)
            self.outAvg += 0.03

        elif self.balls > 60 and (self.score / self.balls) < 1.1:
            adjust = random.uniform(0.06, 0.09)
            self.onStrike.batRunDenominations["0"] -= adjust * (1.2 / 3)
            self.onStrike.batRunDenominations["1"] -= adjust * (0.8 / 3)
            self.onStrike.batRunDenominations["4"] += adjust * (1 / 3)
            self.onStrike.batRunDenominations["6"] += adjust * (1 / 3)
            self.outAvg += 0.02

    def UpdateBatterTracker(self, player, runsScored, ballsFaced, battingLog):
        batter = self.battingTeam.MatchTracker.get(player.displayName)
        batter.runsScored += runsScored
        batter.ballsFaced += ballsFaced
        batter.battingLog.append(battingLog)

    def UpdateBowlerTracker(
        self,
        player,
        runsGiven,
        ballsDelivered,
        oversCompleted,
        wicketsTaken,
        catches,
        bowlingLog,
    ):
        bowler = self.bowlingTeam.MatchTracker.get(player.displayName)
        bowler.runsGiven += runsGiven
        bowler.ballsDelivered += ballsDelivered
        bowler.oversCompleted += 1 if oversCompleted else 0
        bowler.wicketsTaken += 1 if wicketsTaken else 0
        bowler.catches += 1 if catches else 0
        bowler.bowlingLog.append(bowlingLog)

    def changeStrike(self):
        self.onStrike, self.offStrike = self.offStrike, self.onStrike

    def playerDismissed(self, player):
        if self.wickets == 10:
            print("ALL OUT")
            return "All Out"
        else:
            if self.onStrike == player:
                self.onStrike = self.BattingOrder[self.wickets + 1]
            else:
                self.offStrike = self.BattingOrder[self.wickets + 1]

    def wicketType(self, out_type):  # sourcery skip: extract-method
        if out_type == "runOut":
            runOutRuns = random.randint(0, 2)
            self.score += runOutRuns
            self.UpdateBatterTracker(
                self.onStrike,
                runOutRuns,
                1,
                f"W(Run out):{self.CurrentBowler.displayName}:{self.balls}:{runOutRuns}",
            )
            self.UpdateBowlerTracker(
                self.CurrentBowler,
                runOutRuns,
                1,
                False,
                True,
                False,
                f"{self.balls}:W(Run out):{runOutRuns}",
            )
            self.commentator.WicketMessage(
                f"{self.score}/{self.wickets}",
                self.battingTeam,
                self.bowlingTeam,
                self.onStrike,
                self.CurrentBowler,
                None,
                "Run out",
                runOutRuns,
                self.balls,
            )
            self.playerDismissed(self.onStrike)
            return
        elif out_type == "caught":
            feilder = self.bowlingTeam.catcherProbilities()
            self.UpdateBatterTracker(
                self.onStrike,
                0,
                1,
                f"W(CaughtBy {feilder.displayName}):{self.CurrentBowler.displayName}:{self.balls}:0",
            )
            self.UpdateBowlerTracker(
                self.CurrentBowler,
                0,
                1,
                False,
                True,
                False,
                f"{self.balls}:W(CaughtBy {feilder.displayName})",
            )
            self.UpdateBowlerTracker(
                feilder,
                0,
                0,
                False,
                False,
                True,
                f"{self.balls}:Catch({self.onStrike})",
            )
            self.commentator.WicketMessage(
                f"{self.score}/{self.wickets}",
                self.battingTeam,
                self.bowlingTeam,
                self.onStrike,
                self.CurrentBowler,
                feilder,
                "Caught",
                0,
                self.balls,
            )
            self.playerDismissed(self.onStrike)
            return
        elif out_type in ["bowled", "lbw", "hitwicket", "stumped"]:
            self.UpdateBatterTracker(
                self.onStrike,
                0,
                1,
                f"W({out_type}):{self.CurrentBowler.displayName}:{self.balls}:0",
            )
            self.UpdateBowlerTracker(
                self.CurrentBowler,
                0,
                1,
                False,
                True,
                False,
                f"{self.balls}:W({out_type})",
            )
            self.commentator.WicketMessage(
                f"{self.score}/{self.wickets}",
                self.battingTeam,
                self.bowlingTeam,
                self.onStrike,
                self.CurrentBowler,
                None,
                out_type,
                0,
                self.balls,
            )
            self.playerDismissed(self.onStrike)
            return

    def calculateFieldEffectsOnBowler(self, bowler):
        # sourcery skip: remove-redundant-if
        if "break" or "spin" in bowler.bowlStyle:
            effect = (1.0 - self.spinFactor) / 2
            bowler.bowlOutRates += effect * 0.25
            bowler.bowlrunProbilities["0"] += effect * 0.25
            bowler.bowlrunProbilities["1"] += effect * 0.25
            bowler.bowlrunProbilities["4"] -= effect * 0.38
            bowler.bowlrunProbilities["6"] -= effect * 0.3
        elif "medium" or "fast" in bowler["bowlStyle"]:
            effect = (1.0 - self.paceFactor) / 2
            bowler.bowlOutRates += effect * 0.22
            bowler.bowlrunProbilities["0"] += effect * 0.18
            bowler.bowlrunProbilities["1"] += effect * 0.22
            bowler.bowlrunProbilities["4"] -= effect * 0.4
            bowler.bowlrunProbilities["6"] -= effect * 0.3

    def calculateHeadToHeadPoints(self, bowler, batsmen):
        self.outAvg = (batsmen.BatoutRates + bowler.bowlOutRates) / 2
        logging.info(
            f"bastmen: {batsmen.displayName} | bowler: {bowler.displayName} | {self.outAvg}"
        )
        self.deliveryRunAvg = {
            str(run): (
                batsmen.BatrunProbilities[str(run)]
                + bowler.bowlrunProbilities[str(run)]
            )
            for run in range(7)
        }
        self.outTypeAvg = {
            _: (batsmen.BatoutProbilities[_] + bowler.bowloutProbilities[_]) / 2
            for _ in ["caught", "bowled", "lbw", "hitwicket", "stumped"]
        }
        self.outTypeAvg["runOut"] = batsmen.runOutProbilities

    def ballDelivery(self, over, bowler):
        self.PreviousBowler = self.CurrentBowler
        self.CurrentBowler = bowler
        self.calculateFieldEffectsOnBowler(self.CurrentBowler)
        eachBallInOver = 0
        while self.balls < (over + 1) * 6 and self.wickets != 10:
            eachBallInOver += 1
            self.overs = f"{over}.{eachBallInOver}"
            print(self.overs)
            self.calculateHeadToHeadPoints(self.CurrentBowler, self.onStrike)
            self.FirstInningsProbabilitySettings()
            self.MatchSettings()
            self.ballPrediction(self.onStrike.BatrunProbilities)

    def ballPrediction(
        self, den
    ):  # sourcery skip: low-code-quality, remove-redundant-if
        if self.CurrentBowler.bowlWideRate > random.uniform(0, 1):
            self.score += 1
            self.UpdateBowlerTracker(
                self.CurrentBowler, 1, 0, False, False, False, f"{self.balls}:Wide"
            )
            self.commentator.WideMessage(
                f"{self.score}/{self.wickets}",
                self.battingTeam,
                self.bowlingTeam,
                self.onStrike,
                self.CurrentBowler,
                self.balls,
            )
            return
        else:
            total = sum(den[val] for val in den)
            denominationProbabilties = []
            last = 0
            for denom in den:
                denomObj = {
                    "denomination": denom,
                    "start": last,
                    "end": last + den[denom],
                }
                denominationProbabilties.append(denomObj)
                last += den[denom]
            self.balls += 1
            decider = random.uniform(0, total)
            for prob in denominationProbabilties:
                if prob["start"] <= decider < prob["end"]:
                    run = int(prob["denomination"])
                    self.score += run
                    if run != 0:
                        self.updateRun(run)
                        if run % 2 == 1:
                            self.changeStrike()
                        return run
                    elif run == 0:
                        probOut = self.outAvg * (total / den["0"])
                        outDecider = random.uniform(0, 1)
                        logging.info("probOut: %f, outDecider: %f", probOut, outDecider)
                        if probOut > outDecider:
                            self.wickets += 1
                            total_o = 0
                            last_o = 0
                            total_o = sum(
                                self.outTypeAvg[val] for val in self.outTypeAvg
                            )
                            probs_o = []
                            for out_k in self.outTypeAvg:
                                outobj = {
                                    "type": out_k,
                                    "start": last_o,
                                    "end": last_o + self.outTypeAvg[out_k],
                                }
                                probs_o.append(outobj)
                                last_o += self.outTypeAvg[out_k]
                            typeDeterminer = random.uniform(0, total_o)
                            for type_ in probs_o:
                                if (
                                    type_["start"] <= typeDeterminer
                                    and type_["end"] > typeDeterminer
                                ):
                                    self.wicketType(type_["type"])
                        else:
                            self.updateRun(run)
                            return run

    def updateRun(self, run):
        self.UpdateBowlerTracker(
            self.CurrentBowler,
            run,
            1,
            False,
            False,
            False,
            f"{self.balls}:{run}",
        )
        self.UpdateBatterTracker(self.onStrike, run, 1, f"{self.balls}:{run}")
        self.commentator.RunMessage(
            f"{self.score}/{self.wickets}",
            self.battingTeam,
            self.bowlingTeam,
            self.onStrike,
            self.CurrentBowler,
            run,
            self.balls,
        )

    def powerplayPick(self, over, bowlerInp):
        bowlerDict = self.bowlingTeam.MatchTracker.get(bowlerInp.displayName)
        bowlerToReturn = bowlerInp
        if bowlerDict.ballsDelivered > 0 and (
            (
                bowlerDict.ballsDelivered > 11
                or (bowlerDict.runsGiven / bowlerDict.ballsDelivered) > 1.7
            )
            and (
                bowlerDict.ballsDelivered > 11
                or (bowlerDict.wicketsTaken / bowlerDict.ballsDelivered) < 0.091
            )
        ):
            valid = False  # continue this
            localBowling = sorted(
                self.bowlingOrder, key=lambda k: k.oversAvg[str(over + 1)]
            )
            localBowling.reverse()
            while not valid:
                pick = localBowling[random.randint(0, 3)]
                pickInfo = self.bowlingTeam.MatchTracker.get(pick.displayName)
                if pickInfo.ballsDelivered < 11 and self.PreviousBowler != pick:
                    bowlerToReturn = pick
                    valid = True
        return bowlerToReturn

    def inDeathBowlers(self, bowler):
        return bowler.displayName in [
            self.death_bowlers[0].displayName,
            self.death_bowlers[1].displayName,
            self.death_bowlers[2].displayName,
        ]

    def middleOversPick(self, bowler, middle_bowlers):
        # sourcery skip: low-code-quality
        bowlerDict = self.bowlingTeam.MatchTracker.get(bowler.displayName)
        bowlerToReturn = bowler
        if self.inDeathBowlers(bowlerToReturn) and bowlerDict.ballsDelivered > 0:
            if (
                (bowlerDict.ballsDelivered > 17)
                or (bowlerDict.runsGiven / bowlerDict.ballsDelivered) > 1.5
                or (
                    (bowlerDict.runsGiven / bowlerDict.ballsDelivered)
                    - (self.balls / self.score)
                )
                > 0.2
            ) and (
                bowlerDict.ballsDelivered > 17
                or (bowlerDict.runsGiven / bowlerDict.ballsDelivered < 0.088)
            ):
                loopIndex = 3
                playersExp = sorted(
                    self.bowlingOrder, key=lambda k: k.bowlBallsTotalRate
                )
                playersExp.reverse()
                valid = False
                expIndex = 0
                for pexp in playersExp:
                    if expIndex >= 4:
                        break
                    if not self.inDeathBowlers(pexp) and (
                        self.bowlingTeam.MatchTracker.get(
                            pexp.displayName
                        ).ballsDelivered
                        < 7
                        and pexp.displayName != self.PreviousBowler.displayName
                    ):
                        bowlerToReturn = pexp
                        valid = True
                    expIndex += 1

                while not valid:
                    pick = middle_bowlers[random.randint(0, loopIndex)]
                    pickInfo = self.bowlingTeam.MatchTracker.get(pick.displayName)
                    if pickInfo.ballsDelivered == 0:
                        bowlerToReturn = pick
                        valid = True
                    elif self.inDeathBowlers(pickInfo):
                        if pickInfo.ballsDelivered < 11:
                            if pickInfo.runsGiven / pickInfo.ballsDelivered < 1.5:
                                if (
                                    pickInfo.displayName
                                    != self.PreviousBowler.displayName
                                ):
                                    bowlerToReturn = pick.ballsDelivered
                                    valid = True
                            elif pickInfo.runsGiven / pickInfo > 0.088:
                                if (
                                    pickInfo.displayName
                                    != self.PreviousBowler.displayName
                                ):
                                    bowlerToReturn = pick
                                    valid = True
                    elif (
                        pickInfo.ballsDelivered < 24
                        and (pickInfo.runsGiven / pickInfo.ballsDelivered) < 1.5
                    ):
                        if pickInfo.displayName != self.PreviousBowler.displayName:
                            bowlerToReturn = pick
                            valid = True
                    elif (
                        pickInfo.ballsDelivered < 11
                        and pickInfo.runsGiven / pickInfo.ballsDelivered > 0.088
                    ):
                        if pickInfo.displayName != self.PreviousBowler.displayName:
                            bowlerToReturn = pick
                            valid = True
                    loopIndex += 1
                    if loopIndex >= 6:
                        for i2 in range(7):
                            picked_ = middle_bowlers[i2]
                            if (
                                not self.inDeathBowlers(picked_)
                                and picked_.displayName
                                != self.PreviousBowler.displayName
                            ):
                                bowlerToReturn = picked_
                                valid = True

        elif (bowlerDict.ballsDelivered) != 0 and (
            (
                (bowlerDict.ballsDelivered > 19)
                or (bowlerDict.runsGiven / bowlerDict.ballsDelivered) > 1.6
                or (
                    (bowlerDict.runsGiven / bowlerDict.ballsDelivered)
                    - (self.balls / self.score)
                )
                > 0.2
            )
            and (
                bowlerDict.ballsDelivered > 19
                or (bowlerDict.runsGiven / bowlerDict.ballsDelivered < 0.095)
            )
        ):
            valid = False
            loopIndex = 3
            playersExp = sorted(self.bowlingOrder, key=lambda k: k.bowlBallsTotalRate)
            playersExp.reverse()
            expIndex = 0
            for pexp in playersExp:
                if expIndex >= 4:
                    break
                if not self.inDeathBowlers(pexp) and (
                    self.bowlingTeam.MatchTracker.get(pexp.displayName).ballsDelivered
                    < 7
                    and pexp.displayName != self.PreviousBowler.displayName
                ):
                    bowlerToReturn = pexp
                    valid = True
                expIndex += 1
            while not valid:
                pick = middle_bowlers[random.randint(0, loopIndex)]
                pickInfo = self.bowlingTeam.MatchTracker.get(pick.displayName)
                if pickInfo.ballsDelivered == 0:
                    bowlerToReturn = pick
                    valid = True
                elif self.inDeathBowlers(pickInfo):
                    if (
                        0 < pickInfo.ballsDelivered < 11
                        and ((pickInfo.runsGiven / pickInfo.ballsDelivered) < 1.7)
                        or (pickInfo.runsGiven / pickInfo.ballsDelivered) > 0.088
                    ) and pickInfo.displayName != self.PreviousBowler.displayName:
                        bowlerToReturn = pick
                        valid = True
                elif (
                    0 < pickInfo.ballsDelivered < 24
                    and ((pickInfo.runsGiven / pickInfo.ballsDelivered) < 1.6)
                    or (pickInfo.runsGiven / pickInfo.ballsDelivered < 0.1)
                ) and pickInfo.displayName != self.PreviousBowler.displayName:
                    bowlerToReturn = pick
                    valid = True
                loopIndex += 1
                if loopIndex >= 6:
                    for i2 in range(7):
                        picked_ = middle_bowlers[i2]
                        if (
                            not self.inDeathBowlers(picked_)
                            and picked_.displayName != self.PreviousBowler.displayName
                        ):
                            bowlerToReturn = picked_
                            valid = True
        return bowlerToReturn

    def deathOversPick(self, bowlerInp, death_bowlers):
        # sourcery skip: low-code-quality
        bowlerDict = self.bowlingTeam.MatchTracker.get(bowlerInp.displayName)
        bowlerToReturn = bowlerInp
        if (
            not self.inDeathBowlers(bowlerToReturn)
            or 0 < bowlerDict.ballsDelivered > 23
        ):
            valid = False
            pickerIndex = 0
            while not valid:
                pick = death_bowlers[pickerIndex]
                pickInfo = self.bowlingTeam.MatchTracker.get(pick.displayName)
                if pickInfo.ballsDelivered == 0:
                    bowlerToReturn = pick
                    valid = True
                elif (
                    pickInfo.ballsDelivered < 19
                    and pickInfo.displayName != self.PreviousBowler.displayName
                ):
                    for track in self.bowlingTeam.MatchTracker:
                        tracker = self.bowlingTeam.MatchTracker.get(track)
                        if self.PreviousBowler.displayName != track and (
                            tracker.ballsDelivered != 0 and tracker.ballsDelivered < 23
                        ):
                            if tracker.runsGiven == 0:
                                bowlerToReturn = pick
                                valid = True

                            elif (
                                (tracker.ballsDelivered / tracker.runsGiven) < 1.2
                            ) or (tracker.wicketsTaken / tracker.ballsDelivered) > 0.16:
                                bowlerToReturn = pick
                                valid = True
                    bowlerToReturn = pick
                    valid = True
                pickerIndex += 1
        return bowlerToReturn

    def overTracker(self):
        self.opening_bowlers = self.utils._extracted_from_blowers(
            self.bowlingOrder, "oversAvg", "1"
        )
        self.middle_bowlers = self.utils._extracted_from_blowers(
            self.bowlingOrder, "oversAvg", "10"
        )
        self.death_bowlers = self.utils._extracted_from_blowers(
            self.bowlingOrder, "oversAvg", "19"
        )
        for i in range(20):
            if i != 0:
                self.changeStrike()
            if i < 2:
                self.ballDelivery(
                    i, self.opening_bowlers[0]
                ) if i % 2 == 0 else self.ballDelivery(i, self.opening_bowlers[1])
                self.PreviousBowler = (
                    self.opening_bowlers[0] if i % 2 != 1 else self.opening_bowlers[1]
                )
            if i < 6:
                self.ballDelivery(
                    i, self.powerplayPick(i, self.CurrentBowler)
                ) if i % 2 == 1 else self.ballDelivery(
                    i, self.powerplayPick(i, self.PreviousBowler)
                )
            if i < 15:
                self.ballDelivery(
                    i, self.middleOversPick(self.CurrentBowler, self.middle_bowlers)
                ) if i % 2 == 1 else self.ballDelivery(
                    i, self.middleOversPick(self.PreviousBowler, self.middle_bowlers)
                )
            else:
                self.ballDelivery(
                    i, self.deathOversPick(self.CurrentBowler, self.death_bowlers)
                ) if i % 2 == 1 else self.ballDelivery(
                    i, self.deathOversPick(self.PreviousBowler, self.death_bowlers)
                )

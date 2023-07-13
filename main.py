import json
import logging
import random
import time
from Feild import feild
logging.basicConfig(filename='app.log', filemode='w', format='%(levelname)s - %(message)s',level=logging.INFO)
from Teams import Team
from Umpire import Umpire
from Commentator import Commentator
with open('teams.json') as fl:
    dataFile = json.load(fl)
    
def doToss(secondInnDew, pitchDetoriate, typeOfPitch,teamA,teamB,commentator):
        battingLikely = 0.45
        if secondInnDew:
            battingLikely -= random.uniform(0.09, 0.2)
        if pitchDetoriate:
            battingLikely += random.uniform(0.09, 0.2)
        if typeOfPitch == "dead":
            battingLikely -= random.uniform(0.05, 0.15)
        if typeOfPitch == "green":
            battingLikely += random.uniform(0.05, 0.15)
        if typeOfPitch == "dusty":
            battingLikely += random.uniform(0.04, 0.1)

        toss = random.randint(0, 1)
        outcome = random.uniform(0, 1)
        if toss == 0:
            if outcome > battingLikely:
                commentator.tossMessage(teamA, "BAT FIRST")
                return [teamA,teamB]
            commentator.tossMessage(teamA, "BOWL FIRST")
            return [teamB,teamA]
        if outcome > battingLikely:
            commentator.tossMessage(teamB, "BAT FIRST")
            return [teamB,teamA]
        else:
            commentator.tossMessage(teamB, "BOWL FIRST")
            return [teamA,teamB]
            
teamA = Team("csk",dataFile["csk"])
teamB = Team("dc",dataFile["dc"])
fields = feild()
secondInnDew = False
dew = False
pitchDetoriate = True
detoriate = False
paceFactor = None
spinFactor = None
outfield = None
typeOfPitch = "dusty"
paceFactor, spinFactor, outfield = fields.pitchInfo(typeOfPitch)
commentator = Commentator(teamA,teamB,typeOfPitch)
battingTeam,bowlingTeam = doToss(secondInnDew,pitchDetoriate,typeOfPitch,teamA,teamB,commentator)
matchUmpire = Umpire(spinFactor,paceFactor,battingTeam,bowlingTeam,commentator)






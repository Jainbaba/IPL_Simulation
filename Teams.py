import json
import random
from Players import Player
from Tracking import Tracker
from Utils import Utils


class Team:
    def __init__(self, name, players):
        self.name = name
        self.players = []
        self.MatchTracker = {}
        self.catcherTracker = {}
        with open("playerInfo.json") as f:
            data = json.load(f)
            
        self.utils = Utils()

        for i in players:
            playerData = data[i]
            player = Player(playerData)
            self.players.append(player)
            self.MatchTracker[player.displayName] = (Tracker(player))

    def battingOrder(self):
        return sorted(self.players, key=lambda k: k.posAvg)

    def bowlingOrder(self):
        return self.utils._extracted_from_blowers(self.players, "bowlOutRates")

    
    
    def catcherProbilities(self):
        Total = sum(catcher.catchRate for catcher in self.players)
        catcherDetermine = random.uniform(0, Total)
        start = 0
        for p in self.players:
            if start <= catcherDetermine < (start + p.catchRate):
                return p
            start += p.catchRate
            
    def __str__(self) -> str:
        return [p.displayName for p in self.players]
            
        

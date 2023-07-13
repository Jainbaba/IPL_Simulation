class Tracker:
    def __init__(self,player):
        self.displayName = player
        self.runsScored = 0
        self.runsGiven = 0
        self.ballsFaced = 0
        self.ballsDelivered = 0
        self.oversCompleted = 0
        self.wicketsTaken = 0
        self.catches = 0
        self.battingLog = []
        self.bowlingLog = []
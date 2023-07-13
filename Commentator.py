from bardapi import Bard
import re
class AiCommentator:
    def __init__(self,teamA,teamB,feild) -> None:
        self.teamA = teamA
        self.teamB = teamB
        self.feild = feild
        messages = {
            "Team A Name" : self.teamA.name,
            "Team A Players" : self.teamA.__str__(),
            "Team B Name" : self.teamB.name,
            "Team B Players" : self.teamB.__str__(),
            "Feild" : self.feild,
        }
        self.replyGenerate(messages)
        
    def tossMessage(self,TossWonby,Selected):
        messages = {
            "TossWonby" : TossWonby.name,
            "Selected" : Selected
        }
        self.replyGenerate(messages)
        
    def WicketMessage(self,score, battingTeam,bowlingTeam,batsmen,bowler,catcher,wicketType,run, over):
        messages = {
            "Batting Team": battingTeam,
            "Bowling Team": bowlingTeam,
            "Batsmen": batsmen.__str__(),
            "Bowler" : bowler.__str__(),
            "Over" : over,
            "Run scored" : run,
            "Score" : score,
            "WicketType" : wicketType,
            "Catcher": catcher.__str__() if wicketType == "caught" else "No Catcher Involved"
        }
        self.replyGenerate(messages)
        
    def RunMessage(self, score, battingTeam,bowlingTeam,batsmen, bowler,run, over):
        messages = {
            "Batting Team": battingTeam.name,
            "Bowling Team": bowlingTeam.name,
            "Batsmen": batsmen.__str__(),
            "Bowler" : bowler.__str__(),
            "Over" : over,
            "Run scored" : run,
            "Score" : score
        }
        self.replyGenerate(messages)
        
    def replyGenerate(self,messages):
        pattern = r'\[(.*?)\]'
        Prompt = F"{messages} Give me a One Line Comment acting as a IPL Commentator for this Match. Reply the Comment in this Format '[comment]' "
        token = 'Xwg3T-YMh0SjAgHShZVkn3mvhu6J4Z8e4VzoPncaCgelDUJk-jjBj3G7rAOEuQwndgXAyA.'
        bard = Bard(token=token)
        reply = bard.get_answer(Prompt)['content']
        matches = re.findall(pattern, reply)
        print(matches[0])
        
class Commentator:
    def __init__(self,teamA,teamB,feild) -> None:
        self.teamA = teamA
        self.teamB = teamB
        self.feild = feild
        messages = {
            "Team A Name" : self.teamA.name,
            "Team A Players" : self.teamA.__str__(),
            "Team B Name" : self.teamB.name,
            "Team B Players" : self.teamB.__str__(),
            "Feild" : self.feild,
        }
        self.replyGenerate(messages)
        
    def tossMessage(self,TossWonby,Selected):
        messages = {
            "TossWonby" : TossWonby.name,
            "Selected" : Selected
        }
        self.replyGenerate(messages)
        
    def WicketMessage(self,score,battingTeam,bowlingTeam,batsmen,bowler,catcher,wicketType,run, over):
        messages = {
            "Batting Team": battingTeam.name,
            "Bowling Team": bowlingTeam.name,
            "Batsmen": batsmen.displayName,
            "Bowler" : bowler.displayName,
            "Over" : over,
            "Run scored" : run,
            "Score" : score,
            "WicketType" : wicketType,
            "Catcher": catcher.displayName if wicketType == "Caught" else "No Catcher Involved"
        }
        self.replyGenerate(messages)
        
    def RunMessage(self, score, battingTeam,bowlingTeam,batsmen, bowler,run, over):
        messages = {
            "Batting Team": battingTeam.name,
            "Bowling Team": bowlingTeam.name,
            "Batsmen": batsmen.displayName,
            "Bowler" : bowler.displayName,
            "Over" : over,
            "Run scored" : run,
            "Score" : score
        }
        self.replyGenerate(messages)
    
    def WideMessage(self, score, battingTeam,bowlingTeam,batsmen, bowler, over):
        messages = {
            "Batting Team": battingTeam.name,
            "Bowling Team": bowlingTeam.name,
            "Batsmen": batsmen.displayName,
            "Bowler" : bowler.displayName,
            "Over" : over,
            "Run scored" : "Wide",
            "Score" : score
        }
        self.replyGenerate(messages)
        
    def replyGenerate(self,messages):
        print(f"{messages}\n")    
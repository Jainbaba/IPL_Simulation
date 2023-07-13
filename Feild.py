import random

class feild:
    def pitchInfo(self,typeOfPitch):
        if typeOfPitch == "dusty":
            pace = 1 + 0.5 * (random.random() * 0.0)
            spin = 1 + 0.5 * (random.random() * 0.0)
            spin = spin - random.uniform(0.1, 0.16)
            outfield = (1 + (0.5 * ((random.random() * 0.0))))
        elif typeOfPitch == "green":
            pace = 1 + 0.5 * (random.random() * 0.0)
            pace = pace - random.uniform(0.1, 0.16)
            spin = 1 + 0.5 * (random.random() * 0.0)
            outfield = (1 + (0.5 * ((random.random() * 0.0))))
        elif typeOfPitch == "dead":
            pace = 1 + 0.5 * (random.random() * 0.0)
            spin = 1 + 0.5 * (random.random() * 0.0)
            outfield = (1 + (0.5 * ((random.random() * 0.0))))

        return pace, spin, outfield
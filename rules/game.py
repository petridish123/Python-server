
"""
Player:

name
points
scores
cur round

"""


class player:
    def __init__(self,label, points = 0):
        self.points = points
        self.label = label
        self.scores = {0:{}}
        self.cur_round = 0

    def update_points(self,points):
        self.points = points
        self.label.text = str(points)

    def set_score_from_player(self, id :int, score : int):
        def _helper():
            self.scores[self.cur_round][id] = score
            print(self.scores)
        return  _helper

    def set_next_round(self):
        self.cur_round += 1
        self.scores[self.cur_round] = {}
    
    def get_average_from_round(self, round: int):
        if round in self.scores:
            new_scores = list(self.scores[round].values())
            total = 0
            n = 0 
            for score in new_scores:
                n+=1
                total += score
            average = total / n
            return average
        else:
            print("There is no such round logged")
            return 0

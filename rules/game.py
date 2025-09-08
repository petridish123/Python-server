
"""
Player:

name
points
scores
cur round

"""


class player:
    def __init__(self,label,name, points = 0):
        self.points = points
        self.label = label
        self.name = name
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


"""
Game is the rules that is going to be on the server side

Game holds the collection of players and modifies them correctly
This is the data object


"""

class game:

    def __init__(self,):
        self.players = {}
        self.num_players = 0
    
    def add_player(self, player_name : str, PLAYER : player):
        self.players[player_name]  = PLAYER
        self.num_players += 1

    def start_game(self) -> int:
        
        return self.num_players
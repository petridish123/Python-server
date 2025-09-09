
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
        if self.label:
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
        self.id_players = {}
        self.players_id = {}
        self.num_players = 0
    
    def add_player(self, player_name : str, PLAYER : player):
        self.id_players[player_name]  = PLAYER
        self.players_id[PLAYER] = player_name
        self.num_players += 1

    def make_ID(self,):
        if self.num_players in self.id_players or self.num_players == 0:
            new_id = self.num_players
            while new_id in self.id_players or new_id == 0:
                new_id += 1
            return new_id
        else: return self.num_players

    def start_game(self) -> int:
        
        return self.num_players
    
    def remove_player(self, player_name = None, player:player |None = None):
        if player_name and player_name in self.id_players:
            temp_player = self.id_players[player_name]
            self.id_players.pop(player_name)
            self.players_id.pop(temp_player)
            self.num_players -= 1
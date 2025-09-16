
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
    
    def add_player(self, player_name : str|None = None, PLAYER : player|None = None) -> int:
        if not player_name:
            player_name = self.make_ID()
        if not PLAYER:
            PLAYER = player(None, player_name)
        self.id_players[player_name]  = PLAYER
        self.players_id[PLAYER] = player_name
        self.num_players += 1

        return player_name

    def make_ID(self,) -> int:
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


from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QLineEdit, QVBoxLayout, QGridLayout
)

class sub_player:

    def __init__(self, ID, layout : QGridLayout|QVBoxLayout, row : int) -> None:
        self.current_allocation : int = 0 
        self.scores : dict = {0:0} # for each round, append a score
        self.layout : QGridLayout|QVBoxLayout= layout
        self.cur_row : int= row
        self.ID = ID
        self.cur_round : int = 0
        self.widgets  = []

    def add_player(self) -> None:
        
        label1 = QLabel("Player: " + str(self.ID))
        self.layout.addWidget(label1, self.cur_row, 0)
        self.widgets.append(label1)

        new_label = QLabel("Points: " + str(0))
        self.layout.addWidget(new_label, self.cur_row, 6)
        self.widgets.append(new_label)


        button = QPushButton("Very Negative")
        button.setFixedWidth(100)
        button.clicked.connect(self.set_score( -2))
        self.layout.addWidget(button,self.cur_row,1)
        self.widgets.append(button)

        button = QPushButton("Negative")
        button.setFixedWidth(100)
        button.clicked.connect(self.set_score(-1))
        self.layout.addWidget(button,self.cur_row,2)
        self.widgets.append(button)

        button = QPushButton("Neutral")
        button.setFixedWidth(100)
        button.clicked.connect(self.set_score(0))
        self.layout.addWidget(button,self.cur_row,3)
        self.widgets.append(button)

        button = QPushButton("Positive")
        button.setFixedWidth(100)
        button.clicked.connect(self.set_score(1))
        self.layout.addWidget(button,self.cur_row,4)
        self.widgets.append(button)

        button = QPushButton("Very Positive")
        button.setFixedWidth(100)
        button.clicked.connect(self.set_score(2))
        self.layout.addWidget(button,self.cur_row,5)
        self.widgets.append(button)
    
    def change_row(self, new_row):
        self.cur_row  = new_row
        for widget in self.widgets:
            column = self.get_widget_column(widget)
            self.layout.removeWidget(widget)
            self.layout.addWidget(widget,self.cur_row, column)
    
    def off_yerself(self):
        for widget in self.widgets:
            self.layout.removeWidget(widget)
            widget.hide()
            widget.deleteLater()

    def get_widget_column(self, widget):
        for i in range(self.layout.count()):
            item = self.layout.itemAt(i)
            if item.widget() == widget:
                row, column, row_span, col_span = self.layout.getItemPosition(i)
                return column
        return None

    def set_score(self, amount : int):
        def _():
            self.current_allocation = amount
            self.scores[self.cur_round] = amount
        return _
    
    def set_round(self, round_num) -> None:
        self.cur_round = round_num
    
    def increment_round(self) -> None:
        self.set_round(self.cur_round + 1)
    
    def get_score(self) -> tuple:
        return self.ID, self.current_allocation
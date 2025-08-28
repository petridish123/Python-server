
"""
This is going to implement the PyQt6 stuff and add a new set of buttons and label for text



"""

class game:

    def __init__(self, player_count):
        self.player_count : int = player_count

    

    def add_players(self):
        for player in self.player_count:
            print("Adding a new player")
import numpy as np
import math
from Shared import game, player_matrix
import pandas as pd

class equation:
    def __init__(self, Ids): #ID matrix is a dict that maps ids to their matrix
        self.t = 0 # This is time 0
        self.matrices = {self.t: {id:player_matrix(id,Ids)} for id in Ids} # This will keep track of the times
        self.allocations = {self.t: {Id:[0 for i in range(len(Ids))] for Id in Ids}}
        self.ids = [Id for Id in Ids]
        self.reputations = {self.t:[10 for i in self.ids]}
        
    def U_bar(self, k , i , j, t = None):
        if t == None: t = self.t
        if  t<0:t=0
        """
        The rating of player i by player j as observed by player k at time t
        """

    def u_underscore(self, k, i ,j, t = None):
        if t == None: t = self.t
        if t < 0: t = 0
        """
        used in U_bar, the rating for this round based on events and the scores given

        """
    def R(self, k, i, t = None):
        if t == None: t = self.t
        if t < 0: t = 0
        """
        Player i's reputation as observed by player k
        """
        total = 0
        for n in range(len(self.ids)):
            j = self.ids[n]
            if i == j:
                continue
            total += self.U_bar(k,j, i, t) * self.reputations[0 if t<1 else t-1][j]
        
        return total
    
    def total_events(self, k,i,j,events):
        if type(events) != pd.DataFrame:
            new_events = pd.DataFrame(events)
        new_events = new_events[k in new_events["Watcher"]] 



"""
TODO:
- get events in here
- finish the calculation
"""

"""
Questions:
- what should the starting popularity be?

"""

"""
Remember that the allocations are formatted as
{time: {Id:{allocations}... for all IDs} ... for each round}

"""
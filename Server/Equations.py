import numpy as np
import math
from Shared import game, player_matrix
import pandas as pd

class equation:
    LAMBDA = .9
    ALPHA = .5

    def __init__(self, Ids): #ID matrix is a dict that maps ids to their matrix
        self.t = 0 # This is time 0
        self.matrices = {self.t: {id:player_matrix(id,Ids) for id in Ids}} # This will keep track of the times
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

    def update_matrices(self, allocations, events, cur_time): # These are the events for this round
        self.t = cur_time # Cur_time is the new round, so I need to calculate everyting wrt t-1
        self.matrices[self.t] = {}
        print(f"time : {self.t}")
        # print(allocations)
        # print(events)
        # print(pd.DataFrame(events))
        events = pd.DataFrame(events)
        # print(self.matrices)
        for k in self.ids:
            
            prev = self.t - 1
            
            self.matrices[self.t][k] = self.matrices[prev][k] # updating where the matrix is and storing a snapshot in the dictionary
            self.matrices[prev][k] = self.matrices[prev][k].save_copy()
            
            for i in self.ids:
                for j in self.ids:
                    if i == j:
                        continue
                    # print("attempt")
                    # print(allocations)
                    s_i_j = allocations[self.t][i][str(j)] # How player i thinks about player j. Since all allocations are observable for now, it is as observed by k
                    average_event = None
                    e_score = self.ALPHA * self.calc_events(events,k,i,j)
                    score = self.LAMBDA * (s_i_j + e_score) + (1-self.LAMBDA) * (self.matrices[prev][k][i, j])
                    # print(self.matrices[prev][k])
                    print(f"score of {i} to {j} as observed by {k}: {score}")
                    self.matrices[self.t][k].matrix[i-1, j-1] = score
            print(f"Diff from prev and current: \nprev for {k}\n{str(self.matrices[prev][k])} \ncur for {k}\n{str(self.matrices[self.t][k])}")
            
    
    def calc_events(self, events : pd.DataFrame, k, i, j):
        mask = events.apply(
            lambda row: (j in row["To"]) and (i in row["From"]) and (k in row["Watcher"]),
            axis=1
        )
        filtered_events = events[mask]
        # print(filtered_events)
        if len(filtered_events) == 0:
            return 0
        total = 0
        for _, row in filtered_events.iterrows():
            total += self.score(row["TYPE"])
        total /= len(filtered_events)
        return total
             
        

    def score(self, type: str):
        if type == "HUNT": return 1
        else: return -1
    
        



"""
TODO:
- get events in here :check:
- finish the calculation
- 

I have all the data being passed in: allocations and events. Use the equations given by Jake to do the thing
"""

"""
Questions:
- what should the starting popularity be?

"""

"""
Remember that the allocations are formatted as
{time: {Id:{allocations}... for all IDs} ... for each round}


Ui_j ^ k (t) = lambda * [ (allocation i_j ^ k ) + alpha * (average event i_j I(k))] + (1-lambda) Ui_j ^ k (t-1)


"""
import numpy as np
import math
from Shared import game, player_matrix
from Shared import plot_directional_graph, plot_matrix_with_labels
import pandas as pd

class equation:
    LAMBDA = .55
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
                    cur_allocations = allocations[self.t]
                    t_score = 0
                    if not (cur_allocations[i]["CAMP"] != cur_allocations[k]["CAMP"] or cur_allocations[k]["CAMP"] is None) or k == i:
                        s_i_j = cur_allocations[i][str(j)]
                        
                        e_score = self.ALPHA * self.calc_events(events,k,i,j)
                        t_score = self.LAMBDA * (s_i_j + e_score)
                    

                    score = t_score + (1-self.LAMBDA) * (self.matrices[prev][k][i-1, j-1])
                    self.matrices[self.t][k].matrix[i-1, j-1] = score
            plot_matrix_with_labels(self.matrices[self.t][k].matrix,t= self.t,k=k)
            
    
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
             
    def reputation(self,k, i, t=0):
        """
        This is the reputation of player i as observed by player k

        it is equal to the sum of all the ideas of the sentiments from player j => i as observed by k where i!=j multiplied by the reputation of player j as observed by player k in t-1
        """
        if t ==0: t = self.t
        total = 0
        for j in self.ids:
            if i == j: continue
            total += self.matrices[t][k].matrix[j-1,i-1] * self.matrices[t][k].reputations[t-1][j] # U bar from j to i as observed by k times the believed reputation of j at t-1
        
        return total

    def true_reputation(self,i,t = 0):
        t = t if t != 0 else self.t
        N = len(self.ids) if len(self.ids) > 0 else 1
        total = 0        
        for k in self.ids:
            if k == i: continue # player i cannot give itself a boost in reputation
            total += self.matrices[t][k].reputations[t][i] # this takes the reputation of i as observed by player k

        return total / N

    def all_reputations(self,t=0):
        t= t if t!= 0 else self.t
        """
        For every player i, update player k's belief about their reputation for each k
        """
        reputations = {}
        for i in self.ids:
            for k in self.ids:
                if k == i: continue
                pmatrix = self.matrices[t][k]
                if not t in pmatrix.reputations: # if there is no reputation for time t, create one
                    pmatrix.create_new_t_reputation(t)
                reputation_ = self.reputation(k,i) # Supposed to be the reputation of player i as observed by player k
                # print(f"reputation of player {i} as observed by player {k} : {reputation_}") # I think this needs to be normalized
                pmatrix.reputations[t][i] = reputation_#self.reputation(k,i) # update the reputation belief of player k about player i

            

        for i in self.ids: # this normalizes all the beliefs, thus cannot be combined with previous loop
            pmatrix = self.matrices[t][i]
            # print(pmatrix.reputations)
            self.normalize_reputations(pmatrix.reputations[t]) # normalize them jauns  # pmatrix.reputations = 

        for i in self.ids: # Since this depends on the the beliefs being normallized, this cannot be combined but must happen afterwards
            reputations[i] = self.true_reputation(i,t)
        # print(f"before: {reputations}")


        """
        Normalizing below        
        """

        self.normalize_reputations(reputations)

        
        print(f"true reputations: {reputations}")
        return reputations

        # This will calculate the believed reputation of all players about all other players and then calculate the true reputation.
        # This function needs to create the new reputation slots in the player matrix
    def normalize_reputations(self, reputations): # Currently has the issue where the player whos matrix this is will also be normalized.... is that bad?
        # print(np.array(list(reputations.values())).flatten())
        reputations_sum = np.sum(np.abs(np.array(list(reputations.values())).flatten())) # Gets the total of the reputations


        for x in reputations: # This loop puts the values [-0.5,0.5]
            new_x = reputations[ x ] / ( reputations_sum + 1e-9) #2*
            # print(f"new_x : {new_x}")
            reputations[x] = new_x

        rep_mean = np.mean(np.array(list(reputations.values())).flatten())
        # print(f"rep mean {rep_mean}")
        adjustment = 0.5 - rep_mean

        for x in reputations: # This loop makes sure that the values are [0,1]
            reputations[x] = reputations[x] + adjustment


    def score(self, type: str):
        if type == "HUNT": return 1
        else: return -1
    
        





"""
Remember that the allocations are formatted as
{time: {Id:{allocations}... for all IDs, "CAMP":camp_int} ... for each round}


Ui_j ^ k (t) = lambda * [ (allocation i_j ^ k ) + alpha * (average event i_j I(k))] + (1-lambda) Ui_j ^ k (t-1)


"""
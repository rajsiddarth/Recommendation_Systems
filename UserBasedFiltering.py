
import math

from operator import itemgetter

#################################################
# recommender class does user-based filtering and recommends items 
class UserBasedFilteringRecommender:
    
    # class variables:    
    # none
    
    ##################################
    # class instantiation method - initializes instance variables
    #
    # usersItemRatings:
    # users item ratings data is in the form of a nested dictionary:
    # at the top level, we have User Names as keys, and their Item Ratings as values;
    # and Item Ratings are themselves dictionaries with Item Names as keys, and Ratings as values
    # Example: 
    #     {"Angelica":{"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
    #      "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}}
    #
    # k:
    # the number of nearest neighbors
    # defaults to 1
    #
    # m:
    # the number of recommedations to return
    # defaults to 10
    #
    def __init__(self, usersItemRatings, metric='pearson', k=1, m=10):
        
        # set self.usersItemRatings
        self.usersItemRatings = usersItemRatings
            
        # set self.k
        if k > 0:   
            self.k = k
        else:
            print ("    (FYI - invalid value of k (must be > 0) - defaulting to 1)")
            self.k = 1
         
        # set self.m
        if m > 0:   
            self.m = m
        else:
            print ("    (FYI - invalid value of m (must be > 0) - defaulting to 10)")
            self.m = 10
            

    #################################################
    # pearson correlation similarity
    # notation: if UserX is Angelica and UserY is Bill, then:
    # userXItemRatings = {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0}
    # userYItemRatings = {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}
    def pearsonFn(self, userXItemRatings, userYItemRatings):
        
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        
        n = len(userXItemRatings.keys() & userYItemRatings.keys())
        
        for item in userXItemRatings.keys() & userYItemRatings.keys():
            x = userXItemRatings[item]
            y = userYItemRatings[item]
            sum_xy += x * y
            sum_x += x
            sum_y += y
            sum_x2 += pow(x, 2)
            sum_y2 += pow(y, 2)
       
        if n == 0:
            print ("    (FYI - personFn n==0; returning -2)")
            return -2
        
        denominator = math.sqrt(sum_x2 - pow(sum_x, 2) / n) * math.sqrt(sum_y2 - pow(sum_y, 2) / n)
        if denominator == 0:
            print ("    (FYI - personFn denominator==0; returning -2)")
            return -2
        else:
            return round((sum_xy - (sum_x * sum_y) / n) / denominator, 2)
            

    #################################################
    # make recommendations for userX from the most similar k nearest neigibors (NNs)
    def recommendKNN(self, userX):
             #Initializing a list to capture nearest neighbours and their distances to userX
        distance=[]
        
        for user in self.usersItemRatings.keys():
            
            if(user!=userX):
                
               similarity= self.pearsonFn(self.usersItemRatings[userX],self.usersItemRatings[user])
               distance.append([user,similarity])
               
               #Distance list containing the nearest user name and the pearson correlation dist in sorted order
               distance=list(reversed(sorted(distance,key=itemgetter(1))))
        
        #Function for nearest neighbor
        #Dividing it into two parts if k=1 and if k greater than 1
        
        if(self.k==1):
            
            #Initializing an empty dictionary to store the output 
            #temp contains the ratings of the movies given by nearest neighbour but not by userX
            temp={}
            
            #Taking the items which are rated by nearest neighbour but not user X
            #This is obtained by removing the movies which are rated by nearest neighbour but not by userX
            
            nearest_neighbour=distance[0][0]
            
            for item in self.usersItemRatings[nearest_neighbour].keys()-self.usersItemRatings[userX].keys():
                    
                    temp[item]=self.usersItemRatings[nearest_neighbour][item]
                    
            output=list(reversed(sorted(temp.items(),key=itemgetter(1))))
                        
        #For k nearest neighbours
        
        else:
            
            #Taking the distance list calculated above between al the users
            #We subset the list only to give us the K nearest neighbours
            distance=distance[:self.k]
            
            sum_ratios=0
            wt_Average={}
            
            for i in range(len(distance)):
                
                #Transforming pearson correlation distances by adding 1 and dividing by 2
                distance[i][1]=(distance[i][1]+1)/2
                
                #sum_ratios.Calculating the sum of distances of the nearest neighbours
                sum_ratios=distance[i][1]+sum_ratios
            
            #Creating weighted averages
            #wt_Average is a dictionary containing the nearest users and their weighted ratios
            
            for i in range(len(distance)):
               
                wt_Average[distance[i][0]]=distance[i][1]/sum_ratios

            output={}
            
            #Taking nearest neighbors from wt_Average
            
            for user in wt_Average.keys():
                
                for item in self.usersItemRatings[user].keys():
                    
                    if item not in self.usersItemRatings[userX].keys():
                        
                        if item not in output.keys():
                            output[item]=round(self.usersItemRatings[user][item]*wt_Average[user],2)
                        else:
                            output[item]=round(self.usersItemRatings[user][item]*wt_Average[user]+output[item],2)
                      
            output=list(reversed(sorted(output.items(),key=itemgetter(1))))
              
        return output    


print ()

##################################
# data set for collaborative filtering 
##################################
     
songData = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
         "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
         "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0, "Deadmau5": 1.0, "Norah Jones": 3.0, "Phoenix": 5, "Slightly Stoopid": 1.0},
         "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0, "Deadmau5": 4.5, "Phoenix": 3.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 2.0},
         "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0, "Norah Jones": 4.0, "The Strokes": 4.0, "Vampire Weekend": 1.0},
         "Jordyn":  {"Broken Bells": 4.5, "Deadmau5": 4.0, "Norah Jones": 5.0, "Phoenix": 5.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 4.0},
         "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0, "Norah Jones": 3.0, "Phoenix": 5.0, "Slightly Stoopid": 4.0, "The Strokes": 5.0},
         "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0, "Phoenix": 4.0, "Slightly Stoopid": 2.5, "The Strokes": 3.0}
        }

###################################
## User Based filtering 
###################################

# import UserBasedFiltering module
from UserBasedFiltering import UserBasedFilteringRecommender

print ()

ubf = UserBasedFilteringRecommender(songData)
print ("------------------------------")
print ("UBF NN Pearson Recommendations")
print ("------------------------------")
for user in songData.keys():
    print(user, ":", ubf.recommendKNN(user))

print ()

# pearson KNN with k=3

ubf = UserBasedFilteringRecommender(songData, k=3)
print ("-------------------------------------")
print ("UBF KNN (k=3) Pearson Recommendations")
print ("-------------------------------------")
for user in songData.keys():
    print(user, ":", ubf.recommendKNN(user))

print()
        

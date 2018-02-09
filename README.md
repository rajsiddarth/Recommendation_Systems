# Recommendation_Systems
Building a model for recommendation systems using K nearest neighbour based on Pearson correlation.

  The model calculates the distance between users based on the Pearson correlation distance. The recommendations can be based on one nearest neighbour(k=1) or more than one nearest neighbour(k>1). For k>1 the model first normalizes the pearson correlation distance by adding 1 and dividing by 2.Later it uses the weighted average of the distance to calculate the ratings of the user.
  
  To run the model for your own data set ,change the data set given in the code and the parameter k for k>1.

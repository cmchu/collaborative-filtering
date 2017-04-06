# Description

Implementation of a memory-based collaborative filtering system without using any machine learning libraries. This code was originally used to predict movie ratings using a dataset of Netflix ratings. 

# Quick Review

Collaborative filtering is a type of recommendation system that recommends items by matching users who have similar interests, as opposed to recommending by matching attributes of a user with the attributes of an item (content-based system). Two subgroups of collaborative filtering are memory-based methods and model-based methods. Memory-based methods memorize the utility matrix (matrix delineating the degree of preference each user has for each item) in order to make recommendations. They base the recommendations on the relationship between a user and the rest of the utility matrix. On the other hand, model-based methods fit a parmeterized model to the utility matrix and, thus, make recommendations using this model. An example of this would be matrix factorization.

In order to compute the similarity between users, we can use Pearson's Correlation Coefficient. However, in this example, I am going to use a related metric that accounts for the fact that users are rating a subset of the items.

# Execution

The training and testing files should have the following format: ItemId,UserId,Rating

The code can be run as follows:
python cf.py --train path/to/train_set --test path/to/test_set

The code will output the RMSE and MAE on the test set, as well as a predictions.txt file. The predictions.txt file will have 4 columns, with the 4th column being the prediction for the test set.


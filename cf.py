import argparse
import re
import os
import csv
import math
import collections as coll

def parse_argument():
    """
    Code for parsing arguments
    """
    parser = argparse.ArgumentParser(description='Parsing a file.')
    parser.add_argument('--train', nargs=1, required=True)
    parser.add_argument('--test', nargs=1, required=True)
    args = vars(parser.parse_args())
    return args


def parse_file(filename):
    """
    Given a filename outputs user_ratings and movie_ratings dictionaries

    Input: filename

    Output: user_ratings, movie_ratings
        where:
            user_ratings[user_id] = {movie_id: rating}
            movie_ratings[movie_id] = {user_id: rating}
    """
    user_ratings = {}
    movie_ratings = {}
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            movie_id = int(row[0])
            user_id = int(row[1])
            rating = float(row[2])
            if user_id in user_ratings:
                user_temp_dict = user_ratings[user_id]
                user_temp_dict[movie_id] = rating
                user_ratings[user_id] = user_temp_dict
            else:
                user_ratings[user_id] = {movie_id: rating}
            if movie_id in movie_ratings:
                movie_temp_dict = movie_ratings[movie_id]
                movie_temp_dict[user_id] = rating
                movie_ratings[movie_id] = movie_temp_dict
            else:
                movie_ratings[movie_id] = {user_id: rating}
    return user_ratings, movie_ratings


def compute_average_user_ratings(user_ratings):
    """ Given a the user_rating dict compute average user ratings

    Input: user_ratings (dictionary of user, movies, ratings)
    Output: ave_ratings (dictionary of user and ave_ratings)
    """
    ave_ratings = {}
    for user in user_ratings:
        user_dict = user_ratings[user]
        values = user_dict.values()
        ave_ratings[user] = sum(values)/float(len(values))
    return ave_ratings


def compute_user_similarity(d1, d2, ave_rat1, ave_rat2):
    """ Computes similarity between two users

        Input: d1, d2, (dictionary of user ratings per user) 
            ave_rat1, ave_rat2 average rating per user (float)
        Ouput: user similarity (float)
    """
    movie_id_intersect = set(d1.keys()) & set(d2.keys())
    if len(movie_id_intersect) == 0:
        return 0.0
    numer = 0.0
    denom1 = 0.0
    denom2 = 0.0
    for movie_id in movie_id_intersect:
        numer += (d1[movie_id]-ave_rat1)*(d2[movie_id]-ave_rat2)
        denom1 += (d1[movie_id]-ave_rat1)**2
        denom2 += (d2[movie_id]-ave_rat2)**2
    if numer == 0:
        return 0.0
    w_ij = numer/math.sqrt(denom1*denom2)
    return w_ij


def main():
    """
    This function is called from the command line via
    
    python cf.py --train [path to filename] --test [path to filename]
    """
    args = parse_argument()
    train_file = args['train'][0]
    test_file = args['test'][0]
    train_user_ratings, train_movie_ratings = parse_file(train_file)
    test_user_ratings, test_movie_ratings = parse_file(test_file)
    train_ave_user_ratings = compute_average_user_ratings(train_user_ratings)
    f = open('predictions.txt', 'wt')
    writer = csv.writer(f)
    AE = 0.0
    SE = 0.0
    n = 0
    similarity_dict = {}
    for user_id in test_user_ratings:
        d1 = train_user_ratings[user_id]
        ave_rat1 = train_ave_user_ratings[user_id]
        for movie_id in test_user_ratings[user_id]:
            denom = 0.0
            numer = 0.0
            true_rating = test_user_ratings[user_id][movie_id]
            for movie_user_id in train_movie_ratings[movie_id]:
                if (user_id, movie_user_id) in similarity_dict or (movie_user_id, user_id) in similarity_dict:
                    ave_rat2 = train_ave_user_ratings[movie_user_id]
                    try:
                        similarity = similarity_dict[(user_id, movie_user_id)]
                    except:
                        similarity = similarity_dict[(movie_user_id, user_id)]
                    denom += abs(similarity)
                    numer += similarity*(train_movie_ratings[movie_id][movie_user_id] - ave_rat2)
                else:
                    d2 = train_user_ratings[movie_user_id]
                    ave_rat2 = train_ave_user_ratings[movie_user_id]
                    similarity = compute_user_similarity(d1, d2, ave_rat1, ave_rat2)
                    similarity_dict[(user_id, movie_user_id)] = similarity
                    denom += abs(similarity)
                    numer += similarity*(train_movie_ratings[movie_id][movie_user_id] - ave_rat2)
            if denom == 0:
                rating_prediction = ave_rat1
            else:
                rating_prediction = ave_rat1 + numer/denom
            writer.writerow((movie_id, user_id, true_rating, rating_prediction))
            AE += abs(rating_prediction - true_rating)
            SE += (rating_prediction - true_rating)**2
            n += 1
    f.close()
    MAE = AE/n
    RMSE = math.sqrt(SE/n)
    print "RMSE %0.4f" % RMSE
    print "MAE %0.4f" % MAE


if __name__ == '__main__':
    main()
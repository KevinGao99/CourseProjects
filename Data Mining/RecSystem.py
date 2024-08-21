#-*- coding: utf-8 -*-
'''
@author cleartear

@thanks Lockvictor
'''
import pandas as pd
import numpy as np
import sys
import random
import math
import os
from operator import itemgetter
from usercf import UserBasedCF
from itemcf import ItemBasedCF

class RecSystem(object):
    '''the main part of the Recommendation System'''

    def __init__(self, user):
        self.user = user
        self.watched_movies = {}
        self.recommend_movies = {}

        print ('We would like to recommend movie to %d' % int(self.user),file=sys.stderr)

    def get_movie(self):
        '''to get movies which the user have seen. '''
        watched_movies = dict()
        self.watched_movies = watched_movies

    def itemcf_rec_movie(self):
        print("Begin to recommend 10 movies by item-cf.", file=sys.stderr)
        ratingfile = os.path.join('src', 'ratings.csv')
        itemcf = ItemBasedCF()
        itemcf.generate_dataset(ratingfile)
        itemcf.calc_movie_sim()
        item_rec_movies=itemcf.evaluate()
        self.recommend_movies.extend(item_rec_movies)
        print("the item-cf recommend movie is:")
        for movie, rank in item_rec_movies:
            print("recommend No. %s movie." % movie)

    def usercf_rec_movie(self):
        print("Begin to recommend 10 movies by item-cf.", file=sys.stderr)
        ratingfile = os.path.join('src', 'ratings.csv')
        usercf = UserBasedCF()
        usercf.generate_dataset(ratingfile)
        usercf.calc_user_sim()
        self.recommend_movies = usercf.evaluate()
        print("The user-cf recommend movie is:")
        for movie, rank in self.recommend_movies:
            print("recommend No. %s movie." % movie)

    def NLP_rec_movie(self):
        self.recommend_movies.add(NLP.recommend(self.user))
        print("the NLP recommend movie is:")

    def Reload_rec_movie(self):

        print("the final recommend movie is:")


if __name__ == '__main__':
    recsystem = RecSystem('1')
    recsystem.usercf_rec_movie()
    recsystem.itemcf_rec_movie()

#-*- coding: utf-8 -*-
import sys
import random
import pandas as pd
import numpy as np

genre = pd.read_excel('movie_genres.xls')
reload_table = pd.read_csv('reload.csv')
# movie_list是推荐系统的被推荐用户看过的电影

def cosine_similarity(a):
    sum_similarity = 0
    n = len(movie_list)
    for movieIndex in movie_list:
        similarity = sum(genre.loc[genre['movieId'] == movieIndex].iloc[0, 4:22].values*genre.loc[genre['movieId'] == a].iloc[0, 4:22].values)/np.sqrt(sum(genre.loc[genre['movieId'] == movieIndex].iloc[0, 4:22].values)*sum(genre.loc[genre['movieId'] == a].iloc[0, 4:22].values))
        sum_similarity += similarity
    return sum_similarity/n
# to_select是之前多路召回生成的电影列表
similarity = []
for m in to_select:
    similarity.append(cosine_similarity(m))
dict_rec = {'movieId':to_select.values, 'similarity':similarity}
rec = pd.DataFrame(dict_rec)
for mId in rec['movieId']:
    rec.loc[rec['movieId'] == mId, 'score'] = 0 - rec.loc[rec['movieId'] == mId, 'similarity'].values[0] + reload_table.loc[reload_table['movieId'] == mId, 'wilson_lb'].values[0]
rec = rec.sort_values('score', ascending = False)
# recommanded 是最后降序输出的推荐电影列表
recommanded = rec.head(5)['movieId'].tolist()

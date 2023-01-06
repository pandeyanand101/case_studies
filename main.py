#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 19:52:46 2022

@author: anandshankerpandey
"""


import pandas as pd
import numpy as np
from flask import Flask, request
print("new changes")
#read all the trained SVD components
svd_U = np.genfromtxt('./data/svd_U.csv', delimiter=",")
svd_sigma = np.genfromtxt('./data/svd_sigma.csv', delimiter=",")
svd_VT = np.genfromtxt('./data/svd_VT.csv', delimiter=",")
train_df = pd.read_pickle("./data/train_df.pkl")
pivot_data = pd.read_pickle("./data/pivot_data.pkl",compression='xz')
#pred_data = pd.read_pickle("./data/pred_data.pkl")

# Get the predicted ratings for all the restaurants
all_predicted_ratings_df = np.dot(np.dot(svd_U,svd_sigma), svd_VT)

#Predicted ratings
pred_data = pd.DataFrame(all_predicted_ratings_df, columns = pivot_data.columns)
pred_data.set_index(pivot_data.index,inplace = True)


def recommend_non_visited(userID, num_recommendations, pivot_data=pivot_data, pred_data=pred_data):
    user_index  = userID

    sorted_user_ratings = pivot_data.loc[user_index].sort_values(ascending = False) #sort user ratings

    sorted_user_predictions = pred_data.loc[user_index].sort_values(ascending = False)#sorted_user_predictions
    
    temp = pd.concat([sorted_user_ratings, sorted_user_predictions], axis = 1)
    temp.index.name = 'RecommendedRes'
    temp.columns = ['user_ratings', 'user_predictions']
    
    temp = temp.loc[temp.user_ratings == 0]
    temp = temp.sort_values('user_predictions', ascending = False)
    return list(temp.head(num_recommendations).index)


exist_cust = list(train_df['hashed_email'].unique())
res_rank_df = train_df[['RestaurantUID','res_overall_rating']].drop_duplicates().sort_values(['res_overall_rating'],ascending=False)

app = Flask(__name__)


@app.route('/recommend')
def recommend_res():
    custid = request.args.get('hashed_email')
    if custid in exist_cust:
        print('existing customer')
        cust_hist = train_df[train_df['hashed_email']==custid][['hashed_email','RestaurantUID','cat_count','popularity','cust_freq','res_overall_rating']].drop_duplicates()
        res_hist = cust_hist.sort_values(['cust_freq','cat_count','popularity'],ascending=False)
        if len(res_hist)>=3:
            res_hist = res_hist[:3]
            recommended = list(res_hist['RestaurantUID'])
        else:
            recommended = list(res_hist['RestaurantUID'])
            n = 3 - len(recommended)
            res_rank = recommend_non_visited(custid, n)
            recommended = recommended + res_rank
    else:
        print('non existing customer')
        res_rank = res_rank_df[:3]
        recommended = list(res_rank['RestaurantUID'])
    print("results:",recommended)
    return "results: "+str(recommended)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

print("second change")

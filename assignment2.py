#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: donger
"""

import pandas as pd
import lightgbm as lgb
import matplotlib.pyplot as plt
train_feature = pd.read_csv('./data/trainFeatures.csv')
test_feature = pd.read_csv('./data/testFeatures.csv')
train_labels = pd.read_csv('./data/trainLabels.csv',header = None)
train_labels.rename({0:'over50k'}, axis='columns', inplace=True) 
# merge train_feature and train_labels
train_data = pd.merge(train_feature,train_labels,left_index=True,right_index=True,how='outer')
train_data.head()

# merge capital-gain and capital loss to one col
# capital = capital-gain;capital = -capital-loss
train_data['capital-gain'] = train_data['capital-gain']-train_data['capital-loss']
train_data.rename({'capital-gain':'capital'}, axis='columns', inplace=True)
#drop capital loss
train_data.drop(columns = 'capital-loss',inplace=True)
test_feature['capital-gain'] = test_feature['capital-gain']-test_feature['capital-loss']
test_feature.rename({'capital-gain':'capital'}, axis='columns', inplace=True)
#drop capital loss
test_feature.drop(columns = 'capital-loss',inplace=True) 

# drop the repeated data
train_data.drop_duplicates(inplace=True)

#drop fnlwgt
train_data.drop(columns='fnlwgt',inplace=True)
test_feature.drop(columns='fnlwgt',inplace=True)
#drop education-num, beacause education and education are repeated
train_data.drop(columns='education-num',inplace=True)
test_feature.drop(columns='education-num',inplace=True)
#only in training data has these two values,in testing data no these values, so drop them 
train_data = train_data[(train_data['workclass'] != ' Never-worked')]
train_data = train_data[(train_data['native-country'] != ' Holand-Netherlands')]


#do one hot encoder
train_data = pd.get_dummies(train_data)
test_feature= pd.get_dummies(test_feature)

train_Y = train_data['over50k']
train_data.drop(columns='over50k',inplace=True)
train_X = train_data
from sklearn.model_selection import GridSearchCV
model_lgb = lgb.LGBMClassifier(objective='binary',
                              num_leaves=25,
                              learning_rate=0.05,    
                              bagging_seed=2018,
                              verbosity= -1,
                              bagging_frequency= 5,
                              metric='binary_logloss,auc', 
                              bagging_fraction = 0.7,
                              feature_fraction = 0.5)

#params_test1={'num_leaves':range(25, 35, 1),'max_depth':range(20, 22, 1)}
params_test1={'num_leaves':range(32, 35, 1)}

gsearch1 = GridSearchCV(estimator=model_lgb, param_grid=params_test1, scoring='accuracy', cv=5, verbose=1, n_jobs=4)

gsearch1.fit(train_X, train_Y)
print(gsearch1.grid_scores_, gsearch1.best_params_, gsearch1.best_score_)
best_model = gsearch1.best_estimator_
pred_test = best_model.predict(test_feature)
fig, ax = plt.subplots(figsize=(12,18))
lgb.plot_importance(best_model, max_num_features=50, height=0.8, ax=ax)
ax.grid(False)
plt.title("LightGBM - Feature Importance", fontsize=15)
plt.show()
sub_df = pd.DataFrame(pred_test)
sub_df[sub_df < 0.5] = 0
sub_df[sub_df >= 0.5] = 1
sub_df.to_csv("./A2_dchenay_20551304_prediction.csv", index=False,header=False)
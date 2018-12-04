#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: donger
"""
import time
import os, os.path
import cv2
import keras
import matplotlib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

from sklearn.metrics import silhouette_score

import pandas as pd
import numpy as np
DIR = "/Users/donger/Downloads/images"


def pre_processing(path):
    # arrays to store our images and filenames of images
    images = []
    filenames = []
    for filename in os.listdir(path):
        if '.jpg' in filename:
            imgpath = os.path.join(path, filename)
            # Use imread in opencv to read the image
            image = cv2.imread(imgpath)

            # Resize it to 224 x 224
            image = cv2.resize(image, (224, 224))

            # Convert it from BGR to RGB so we can plot them later (because openCV reads images as BGR)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Now we add it to our array
            images.append(image)
            
            filenames.append(filename)
            
    # Convert to numpy arrays
    images = np.array(images, dtype=np.float32)
    filenames = np.array(filenames)

    # Normalise the images
    images /= 255
           
    # shuffle the data, we don't split the test dataset here, just want to shuffle data
    images, X_test, filenames, y_test = train_test_split(images, filenames, test_size=0, random_state=43)

    return images, filenames


def feature_extraction(covnet_model, raw_images):
    # Pass our training data through the network
    pred = covnet_model.predict(raw_images)

    # Flatten the array
    flat = pred.reshape(raw_images.shape[0], -1)

    return flat

def create_fit_PCA(data, n_components=None):
    p = PCA(n_components=n_components, random_state=728)
    p.fit(data)

    return p

'''
def create_train_kmeans(data, number_of_clusters=21):
    # n_jobs is set to -1 to use all available CPU cores. 

    k = KMeans(n_clusters=number_of_clusters, n_jobs=-1, random_state=4)

    k.fit(data)


    return k

'''

images, filenames = pre_processing(DIR)

# Load the vgg16_model use trainned vgg16 model to get feature of images

vgg16_model = keras.applications.vgg16.VGG16(include_top=False, weights="imagenet",pooling='max', input_shape=(224,224,3))

vgg16_output = feature_extraction(vgg16_model, images)


# Create PCA instances for each covnet output
vgg16_pca = create_fit_PCA(vgg16_output)

vgg16_output_pca = vgg16_pca.transform(vgg16_output)

#K_vgg16_pca = create_train_kmeans(vgg16_output_pca)
number_of_clusters = 11

K_means_cluster = KMeans(n_clusters=number_of_clusters, n_jobs=-1, random_state=4)

K_means_cluster.fit(vgg16_output_pca)

#Use Silhouette Coefficient and sse to find how many clusters
'''
data = vgg16_output_pca

Scores = [] 
SSE = [] 
for k in range(2,30):
    estimator = KMeans(n_clusters=k,n_jobs=-1, random_state=43)  
    estimator.fit(data)
    Scores.append(silhouette_score(data,estimator.labels_,metric='euclidean'))
    SSE.append(estimator.inertia_)
X = range(2,30)
plt.xlabel('k')
plt.ylabel('Silhouette Coefficient')
plt.plot(X,Scores,'o-')
plt.show()


X = range(2,30)
plt.xlabel('k')
plt.ylabel('SSE')
plt.plot(X,SSE,'o-')
plt.show()  
  
'''
K_means_prediction = K_means_cluster.predict(vgg16_output_pca)

#save the filename of images from same culster together in a list
clusterlist = []
for i in range(11):
    clusterlist.append([])
for i in range(len(K_means_prediction)):
    clusterlist[K_means_prediction[i]].append(filenames[i])

#save the images in same cluster to one file, so we can take of look at our result
'''
import shutil
for i in range(11):
    images = []
    clusterpath = os.path.join('/Users/donger/cluster11','cluster'+str(i))
    if not os.path.exists(clusterpath):
        os.mkdir(clusterpath)
    for filename in clusterlist[i]:
        if 'jpg' in filename:
            imgpath =os.path.join(DIR,filename)
            dstfile = os.path.join(clusterpath,filename)
            shutil.copyfile(imgpath,dstfile)
'''
          
#delete the .jpg in filename
for i in range(11):
    for j in range(len(clusterlist[i])):
        if('.jpg' in clusterlist[i][j]):
            clusterlist[i][j] = clusterlist[i][j].replace('.jpg','')
        

#store the result to dataframe then save to csv file
result = pd.DataFrame(columns = ['Cluster 1','Cluster 2','Cluster 3','Cluster 4','Cluster 5','Cluster 6','Cluster 7','Cluster 8','Cluster 9','Cluster 10','Cluster 11'])
maxlen = 0
for i in range(len(clusterlist)):
    if len(clusterlist[i]) >= maxlen:
        maxlen = len(clusterlist[i])
        max = i

result['Cluster '+str(max+1)] = clusterlist[max]
for i in range(len(clusterlist)):
  for j in range(len(clusterlist[i])):
     result['Cluster '+str(i+1)][j] = str('\'')+ str(clusterlist[i][j])+str('\'')

result.to_csv('result.csv',quoting = 0, index=False)
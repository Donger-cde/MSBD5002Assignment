# MSBD5002
## Homework1
hashtree.py
fptree.py
## Homework2（5002hw2.py）
### Task Description
The dataset come from 1994 Census database. Prediction task is to determine whether a person makes over 50K a year.
### Data Description
#### 1. Feature 
#### age: 
The age of the individual; this attribute is continuous.
#### work-class: 
The type of the employer that the individual has; this attribute is nominal.
#### fnlwgt: 
Final weight, this is the number of people the census believes the entry represents; this attribute is continuous.
#### education: 
The highest level of education achieved for that individuals; This attribute is nominal.
#### education-num: 
Highest level of education in numerical form; this attribute is continuous.
#### marital-status: 
Marital status of the individual; This attribute is nominal.
#### occupation: 
The occupation of the individual;This attribute is nominal. 
#### relationship: 
The family relationship of the individual; This attribute is nominal. 
#### race: 
The race of the individual; This attribute is nominal.
#### education-num: 
Highest level of education in numerical form; this attribute is continuous.
#### sex: 
Female, Male; This attribute is nominal.
#### capital-gain: 
capital gains recorded; This attribute is continuous.
#### capital-loss: 
capital losses recorded; This attribute is continuous. 
#### hours-per-week: 
Hours worked per week; This attribute is continuous. 
#### native-country: 
label person’s country.
####  2. Labels：
#### 0: 
means a person makes no more than 50K a year, i.e. <=50k 
#### 1: 
means a person makes over 50K a year, i.e. >50K

## Homework3（5002hw3.py）
### Task Description
Cluster 5011 jpg images
### My solution
1. Pass our 5011 images through trained VGG-16 to obtain bottleneck features.
2. Cluster the images by K-means(Use silhouette coefficient and SSE to help us to select K)




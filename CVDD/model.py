##IMPORTING THE LIBRARIES USED IN OUR MODEL

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv("heart.csv")
#print(df.head)
#print(df.info)
print(df.shape)

heart_data = df.drop_duplicates()
print(heart_data.shape)
#print(heart_data.describe())
print(heart_data['target'].value_counts())

sns.heatmap(heart_data.corr())
#plt.show()
print(heart_data.columns)
X = heart_data.drop(columns='target',axis=1)
Y = heart_data['target']
#print(X)
#print(Y)

#Continues and Categorical Variables
cate_val = []
cont_val = []

for columns in heart_data.columns:
  if heart_data[columns].nunique()<=10:
    cate_val.append(columns)
  else:
    cont_val.append(columns)
#print(cate_val)
#print(cont_val)

#splitting dataset
from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test = train_test_split(X,Y, test_size=0.2,stratify=Y,random_state=2)

#print(X.shape,X_train.shape,X_test.shape)

#model training
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
#model = LogisticRegression()
model= RandomForestClassifier()
model.fit(X_train,Y_train)
X_train_prediction = model.predict(X_train)
training_data_accuracy = accuracy_score(X_train_prediction, Y_train)
print("Accuracy on Training Data:", training_data_accuracy)

#testing
X_test_prediction1 = model.predict(X_test)
testing_data_accuracy= accuracy_score(X_test_prediction1, Y_test)
print("Accuracy on Testing Data:", testing_data_accuracy)

#evaluation



#pickle file for model
import pickle
pickle.dump(model, open("model.pkl",'ab'))
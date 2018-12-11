import pandas as pd
import csv
import sklearn as sk
from sklearn import linear_model, metrics

train =pd.read_csv('train.csv')
#print(train)

nw=pd.get_dummies(train, columns =['Crop','Crop_variety','Crop_disease'])
traindata =nw
Y_train = nw['Occurance']
del traindata['Occurance']
X_train =traindata
reglm = linear_model.LogisticRegression()


train, test = train_test_split(df, test_size=0.2)
train = pd.get_dummies(train)
trainf = train
trainf.index =range(1244)
Y_train =train['Occurance']
del trainf['Occurance']
import sklearn as sk
from sklearn import linear_model, metrics
reglm = linear_model.LogisticRegression()
reglm.fit(trainf, Y_train)


LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
          intercept_scaling=1, max_iter=100, multi_class='ovr', n_jobs=1,
          penalty='l2', random_state=None, solver='liblinear', tol=0.0001,
          verbose=0, warm_start=False)
trainf.to_csv('ftrain.csv')
Y_train.to_csv('fytrain.csv')
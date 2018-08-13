#cropdiseaseforecasting
import pandas as pd
import sklearn as sk
from sklearn import linear_model, metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import BayesianRidge, LinearRegression
from sklearn.ensemble import RandomForestClassifier



data =pd.read_csv('sdtrain.csv',sep =';') 
testdata =pd.read_csv('sdtest.csv',sep =';') #
tdata =data                             
y_train =data['Occurance']              
y_test =testdata['Occurance']           
del testdata['Occurance']              
del tdata['Occurance']                  
del tdata['SMC']                        
del testdata['SMC']

X_train=pd.get_dummies(tdata,columns =['Crop','Crop_variety','Crop_disease']) ########getdummies for crop,and crop varieties

reglm = linear_model.LogisticRegression()           ##################logistic regression#####################
reglm.fit(X_train,y_train)
clf=RandomForestClassifier(n_estimators=26)         #######################random classifier##############
clf.fit(X_train,y_train)

X_test=pd.get_dummies(testdata,columns =['Crop','Crop_variety','Crop_disease'])

y_predict1 =clf.predict(X_test)                   ##################y predicted by random classfier ##############
y_predict2 = reglm.predict(X_test)                ####################y predicted by logistic regressor######################


aclf =metrics.accuracy_score(y_test, y_predict1)*100 ########accuracy  level of random classifier
alm =metrics.accuracy_score(y_test, y_predict2)*100  ##########accuracy level of logistic model
                           

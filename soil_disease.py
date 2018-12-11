import pandas as pd
import statsmodels.formula.api as smf
soil_data=[[0.31,138,14.14,328,0.03,1.43,0.04436],[0.55,113,19.13,565,0.12,1.26,0.4857],[0.13,94,6.38,123,0.08,1.55,0.3922],[0.26,100,10.81,363,0.07,1.45,0.4082],[0.44,107,19.4,304,0.1,1.47,0.4096],[0.31,100,26.62,0.1,1.44,0.4050],[0.78,138,68.47,964,0.18,1.25,0.4856],[0.24,88,44.91,260,0.08,1.57,0.4207]]
df= pd.DataFrame(soil_data, columns =['OC','N','P','K','EC','BD','Porosity'])
rs =smf.ols('BD ~ OC + N + P + K + EC', data =df).fit()

df= pd.read_csv('finaldata.csv')
#use rsbd.params['OC'] to get coeff of reg
import numpy as np
BD =[]
for i in range(len(df)):
    BD.append(df.N[i] * rs.params['N'] + df.P[i] * rs.params['P'] + df.P[i] * rs.params['K'] + df.OC[i] * rs.params['OC'] +df.EC[i] * rs.params['EC'] + rs.params['Intercept'])

BD  =pd.DataFrame(BD, columns =['BD'])
for i in range(len(BD)):
    if BD.BD[i] >=1.65:
        BD.BD[i] =1.65
    elif BD.BD[i]<=1:
        BD.BD[i] =1
    else:
        continue
df =df.join(BD)
porosity =[]
par_den =2.65
for i in range(len(df)):
    porosity.append(1 - (df.BD[i] / par_den))

porosity =pd.DataFrame(porosity, columns =['porosity'])
df =df.join(porosity)

SMC =[]
for i in range(len(df)):
    c = ((df.Precipitaion[i] + df.Irrigation[i] - df.BD[i] * df.porosity[i]) / df.porosity[i])
    if c >= 1:
        SMC.append(float(1))
    else:
        SMC.append(c)
SMC =pd.Series(SMC)
SMC =pd.DataFrame(SMC , columns =['SMC'])

for i in range(len(df)):
    if (df.Crop_disease[i] == str('Dampingoff') and df.SMC[i] >= 0.75 and df.Soil_temperature[i] <= 24 and df.BD[i] <= 1.2):
        Disease.append(1.0)
    elif (df.Crop_disease[i] == str('septorialeafspot') and df.SMC[i] >= 0.75 and df.N[i] <= 230 and df.P[i] <= 32 and df.K[i] <= 250):
        Disease.append(1.0)
    elif (df.Crop_disease[i] == str('bacterialstemcanker') and df.Soil_temperature[i] >= 27 and df.Soil_temperature[i] <= 30 and df.SMC[i] >= 0.75):
        Disease.append(1.0)
    elif (df.Crop_disease[i] == str('fussiramwilt') and df.Soil_temperature[i] >= 35 and df.SMC[i]>= 0.65):
        Disease.append(1.0)
    else:
        Disease.append(0)


####################project elctricity energy housing consumption#######
import pandas as pd
import math
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.graphics.factorplots import interaction_plot
from scipy import stats

datafile = "ecdata.csv"
data =pd.read_csv(datafile)
print(data)

def effect_estimate(k,v,p,t,data):
    s1 =0
    s2=0
    for i in range(len(data)):
        if (data[str(v)][i] == p):
            s1 = s1 + data[t][i]
        else:
            s2 = s2 + data[t][i]
        estimate =(s1-s2)*(1/(math.pow(2,(k-1))))
    mean_data= sum(data[t])/len(data)
    for
    return (estimate)
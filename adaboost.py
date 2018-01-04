import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import cross_validation, metrics
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
rcParams['figure.figsize']=12,4
train=pd.read_csv("H:\\xgboostdata\\Dataset\\Dataset\\Train_nyOWmfK.csv");
target='Disbursed'


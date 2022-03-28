from cProfile import label
from ntpath import join
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from random import randrange
import datetime
from sklearn.ensemble import IsolationForest
from sklearn.metrics import precision_recall_curve
def random_date(start,l):
    dates = []
    current = start
    while l > 0:
        current = current + datetime.timedelta(minutes=randrange(300))
        while current in dates:
            current = current + datetime.timedelta(minutes=randrange(300))
        dates.append(current)
        l-=1
    return dates

#pre-processing speed data
speed_df = pd.read_csv('speed.csv')
speed_df = speed_df.drop(['id', 'vehicle_id','sensor'], axis=1)
speed_df = speed_df.rename(columns={"data" : "speed"})

#pre-processing rpm data
rpm_df = pd.read_csv('rpm.csv')
rpm_df = rpm_df.drop(['id', 'vehicle_id','sensor'], axis=1)
rpm_df = rpm_df.rename(columns={"data" : "rpm"})

#joining rpm and speed dataframe on timestamp
columns_names = ["timestamp","speed","rpm"]
joined_df = pd.merge(rpm_df,speed_df,on="timestamp")
joined_df = joined_df.reindex(columns=columns_names)
label_df = pd.DataFrame({"anomaly" : [-1]*joined_df.shape[0]})
joined_df = pd.concat([joined_df,label_df],axis=1)
print(joined_df.tail(2))
# with open("rpm.csv","r") as f:
#     with open("rpmAnomaly.csv","w") as d:
#         i = 0
#         for line in f:
#             if i == 0:
#                 d.write(line.strip() + ",anomaly\n")
#             else:
#                 d.write(line.strip() + ",0\n")
#             i+=1
from cProfile import label
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from random import randrange
import random
import datetime
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split

seed = 3

random.seed(seed)
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
speed_df = pd.read_csv('speedAnomaly.csv')
speed_df = speed_df.drop(['id', 'vehicle_id','sensor'], axis=1)
speed_df = speed_df.rename(columns={"data" : "speed"})
print(speed_df.head())
#pre-processing rpm data
rpm_df = pd.read_csv('rpmAnomaly.csv')
rpm_df = rpm_df.drop(['id', 'vehicle_id','sensor'], axis=1)
rpm_df = rpm_df.rename(columns={"data" : "rpm"})
print(rpm_df.head())

timestamp = rpm_df["timestamp"]
print(timestamp.head())

low_rpm_high_speed = []
high_rpm_low_speed = []

i = 0
i1 = 0
while i < 75:
    index = random.randint(0,timestamp.shape[0] - 1)
    while index in low_rpm_high_speed:
        index = random.randint(0,timestamp.shape[0] - 1)
    low_rpm_high_speed.append(index)
    i+=1
while i1 < 75:
    index = random.randint(0,timestamp.shape[0] - 1)
    while index in high_rpm_low_speed or index in low_rpm_high_speed:
        index = random.randint(0,timestamp.shape[0] - 1)
    high_rpm_low_speed.append(index)
    i1+=1
print(len(high_rpm_low_speed))
print(len(low_rpm_high_speed))

print(rpm_df.iloc[high_rpm_low_speed[0]], high_rpm_low_speed[0])
for i in high_rpm_low_speed:
    rpm_df.loc[i,"rpm"] = random.randint(2500,4000)
    speed_df.loc[i,"speed"] = random.randint(0,40)
    rpm_df.loc[i,"anomaly"] = 1
    speed_df.loc[i,"anomaly"] = 1
for i in low_rpm_high_speed:
    rpm_df.loc[i,"rpm"] = random.randint(0,1000)
    speed_df.loc[i,"speed"] = random.randint(80,150)
    rpm_df.loc[i,"anomaly"] = 1
    speed_df.loc[i,"anomaly"] = 1

rpm_df.to_csv("rpmAn.csv")
speed_df.to_csv("speedAn.csv")


#joining rpm and speed dataframe on timestamp
#columns_names = ["timestamp","speed","rpm"]
#labels = []
#for i in range(rpm_df.shape[0]):
    #labels.append(rpm_df["anomaly"][i] or speed_df["anomaly"][i])
#rpm_speed_df = pd.merge(rpm_df,speed_df,on="timestamp")
#rpm_speed_df = rpm_speed_df.reindex(columns=columns_names)
#rpm_speed_df = pd.concat([rpm_speed_df,pd.DataFrame({"is_anomalous":labels})],axis=1)
#print(rpm_speed_df.head())
#print(rpm_speed_df.head(5))
# label_df = pd.DataFrame({"anomaly" : [-1]*rpm_speed_df.shape[0]})
# rpm_speed_df = pd.concat([rpm_speed_df,label_df],axis=1)
#ax = plt.gca()
#ax.set_xlim([-100, 4500])
#plt.scatter(rpm_speed_df["rpm"],rpm_speed_df["speed"],c=rpm_speed_df["anomaly"],cmap="coolwarm")
#plt.savefig("rpm_speed_scatter.png")
#plt.clf()
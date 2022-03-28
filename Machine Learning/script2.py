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


#inserting anomalies
rng = np.random.default_rng()
low_speed_df = pd.DataFrame(rng.integers(0, 40, size=(75, 1)), columns=['speed']) #low speed values
high_speed_df = pd.DataFrame(rng.integers(80, 150, size=(75, 1)), columns=['speed']) #high speed values

low_rpm_df = pd.DataFrame(rng.integers(0, 1000, size=(75, 1)), columns=['rpm']) #low rpm values
high_rpm_df = pd.DataFrame(rng.integers(3000, 5000, size=(75, 1)), columns=['rpm']) #high rpm values

today_date = datetime.datetime.now()
first_random_date_df = []
second_random_date_df = []

for x in random_date(today_date,75):
    first_random_date_df.append(x.strftime("%Y-%m-%d %H:%M:%S"))
for x in random_date(today_date + datetime.timedelta(days=15),75):
    second_random_date_df.append(x.strftime("%Y-%m-%d %H:%M:%S"))

first_anomalies_df = pd.DataFrame({"timestamp": first_random_date_df,"speed": low_speed_df["speed"],"rpm":high_rpm_df["rpm"],"anomaly":[1]*75})
second_anomalies_df = pd.DataFrame({"timestamp": second_random_date_df,"speed": high_speed_df["speed"],"rpm":low_rpm_df["rpm"],"anomaly":[1]*75})
joined_df = pd.concat([joined_df,first_anomalies_df,second_anomalies_df],ignore_index=True)
joined_df = joined_df.sample(frac=1) #returns a shuffled dataframe
plt.scatter(joined_df["rpm"],joined_df["speed"])
plt.savefig("rpm_speed_anomaly_scatter.png")

#Creating final dataframe
complete_dataframe = joined_df.drop(["timestamp","anomaly"],axis=1)
complete_np_dataframe = complete_dataframe.to_numpy()
#machine learning model: Isolation Forest
model = IsolationForest(n_estimators=100,contamination=0.04, max_features=complete_dataframe.shape[1])
model.fit(complete_np_dataframe)
# Get Anomaly Scores and Predictions
anomaly_score = model.decision_function(complete_np_dataframe)
predictions = model.predict(complete_np_dataframe)
res = np.add(predictions,joined_df["anomaly"])

#Visualizing result
anomaly_plot = plt.scatter(complete_dataframe['rpm'], complete_dataframe['speed'], c = anomaly_score, cmap = 'coolwarm')
plt.colorbar(anomaly_plot,label = 'More Negative = More Anomalous')
plt.xlabel('RPM', fontsize = 12)
plt.ylabel('Speed', fontsize = 12)
plt.grid()
plt.savefig("heatmap.png")

prediction_plot = plt.scatter(complete_dataframe['rpm'], complete_dataframe['speed'], c = predictions, cmap = 'coolwarm')
plt.xlabel('RPM', fontsize = 14)
plt.ylabel('Speed', fontsize = 14)
plt.grid()
plt.title(f'Contamination = 0.04, Accuracy ={round(list(res).count(0)/len(res),3)}', weight = 'bold')
plt.savefig("prediction.png")

print(f"anomalies = {list(predictions).count(-1)}")
print(f"accuracy = {list(res).count(0)/len(res)}")

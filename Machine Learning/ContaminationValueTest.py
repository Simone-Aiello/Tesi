import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from random import  randrange
import datetime
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split

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
rpm_speed_df = pd.merge(rpm_df,speed_df,on="timestamp")
rpm_speed_df = rpm_speed_df.reindex(columns=columns_names)
label_df = pd.DataFrame({"anomaly" : [-1]*rpm_speed_df.shape[0]})
rpm_speed_df = pd.concat([rpm_speed_df,label_df],axis=1)
ax = plt.gca()
ax.set_xlim([-100, 4500])
plt.scatter(rpm_speed_df["rpm"],rpm_speed_df["speed"],c=rpm_speed_df["anomaly"],cmap="coolwarm")
plt.savefig("rpm_speed_scatter_1.png")
plt.clf()

#inserting anomalies
rng = np.random.default_rng()
low_speed_df = pd.DataFrame(rng.integers(0, 40, size=(75, 1)), columns=['speed']) #low speed values
high_speed_df = pd.DataFrame(rng.integers(80, 150, size=(75, 1)), columns=['speed']) #high speed values

low_rpm_df = pd.DataFrame(rng.integers(0, 1000, size=(75, 1)), columns=['rpm']) #low rpm values
high_rpm_df = pd.DataFrame(rng.integers(2500, 4000, size=(75, 1)), columns=['rpm']) #high rpm values

today_date = datetime.datetime.now()
first_random_date_df = []
second_random_date_df = []

for x in random_date(today_date,75):
    first_random_date_df.append(x.strftime("%Y-%m-%d %H:%M:%S"))
for x in random_date(today_date + datetime.timedelta(days=15),75):
    second_random_date_df.append(x.strftime("%Y-%m-%d %H:%M:%S"))

first_anomalies_df = pd.DataFrame({"timestamp": first_random_date_df,"speed": low_speed_df["speed"],"rpm":high_rpm_df["rpm"],"anomaly":[1]*75})
second_anomalies_df = pd.DataFrame({"timestamp": second_random_date_df,"speed": high_speed_df["speed"],"rpm":low_rpm_df["rpm"],"anomaly":[1]*75})
rpm_speed_df = pd.concat([rpm_speed_df,first_anomalies_df,second_anomalies_df],ignore_index=True)
plt.scatter(rpm_speed_df["rpm"],rpm_speed_df["speed"],c=rpm_speed_df["anomaly"],cmap='coolwarm')
plt.savefig("rpm_speed_anomaly_scatter_1.png")
plt.clf()

#Creating dataframe for training and testing
labels = rpm_speed_df["anomaly"]
complete_dataframe = rpm_speed_df.drop(["timestamp","anomaly"],axis=1)
x_train, x_test, y_train, y_test = train_test_split(complete_dataframe,labels,test_size=0.3,stratify=labels)

#Plotting training data
plt.scatter(x_train["rpm"],x_train["speed"],c=y_train,cmap='coolwarm')
plt.savefig("train_scatter")
plt.clf()

#Plotting testing data
plt.scatter(x_test["rpm"],x_test["speed"],c=y_test,cmap='coolwarm')
plt.savefig("test_scatter")
plt.clf()

#Machine learning model: Isolation Forest
contaminations = np.arange(0.01,0.07,0.01)
print(contaminations)
for contamination in contaminations:
    if contamination > 0.06:
        contamination = 0.06
    model = IsolationForest(contamination=contamination, max_features=x_train.shape[1])

    #Training the model with train data
    model.fit(x_train.to_numpy())
    anomaly_score_training = model.decision_function(x_train.to_numpy())
    training_prediction = model.predict(x_train.to_numpy())
    training_result = np.add(training_prediction,y_train)


    #Plotting training heatmap
    anomaly_train_plot = plt.scatter(x_train['rpm'], x_train['speed'], c = -1*anomaly_score_training, cmap = 'coolwarm')
    plt.colorbar(anomaly_train_plot,label = 'More Red = More Anomalous')
    plt.xlabel('RPM', fontsize = 12)
    plt.ylabel('Speed', fontsize = 12)
    plt.grid()
    plt.savefig(f"Contamination_{contamination}/heatmap_train_contamination_{contamination}.png")
    plt.clf()

    #Plotting training prediction
    prediction_plot = plt.scatter(x_train['rpm'], x_train['speed'], c = -1*training_prediction, cmap = 'coolwarm')
    plt.colorbar(prediction_plot,label = 'More Red = More Anomalous')
    plt.xlabel('RPM', fontsize = 14)
    plt.ylabel('Speed', fontsize = 14)
    plt.grid()
    plt.title(f'Contamination = {contamination}, Accuracy ={round(list(training_result).count(0)/len(training_result),3)}', weight = 'bold')
    plt.savefig(f"Contamination_{contamination}/prediction_train_contamination_{contamination}.png")
    plt.clf()

    #Testing the accuracy of the model on data unseen before
    anomaly_score_test = model.decision_function(x_test.to_numpy())
    test_prediction = model.predict(x_test.to_numpy())
    test_result = np.add(test_prediction,y_test)

    #Plotting test heatmap
    anomaly_test_plot = plt.scatter(x_test['rpm'], x_test['speed'], c = -1*anomaly_score_test, cmap = 'coolwarm')
    plt.colorbar(anomaly_test_plot,label = 'More Red = More Anomalous')
    plt.xlabel('RPM', fontsize = 12)
    plt.ylabel('Speed', fontsize = 12)
    plt.grid()
    plt.savefig(f"Contamination_{contamination}/heatmap_test_contamination_{contamination}.png")
    plt.clf()

    #Plotting test prediction
    test_prediction_plot = plt.scatter(x_test['rpm'], x_test['speed'], c = -1*test_prediction, cmap = 'coolwarm')
    plt.colorbar(test_prediction_plot,label = 'More Red = More Anomalous')
    plt.xlabel('RPM', fontsize = 14)
    plt.ylabel('Speed', fontsize = 14)
    plt.grid()
    plt.title(f'Contamination = {contamination}, Accuracy ={round(list(test_result).count(0)/len(test_result),3)}', weight = 'bold')
    plt.savefig(f"Contamination_{contamination}/prediction_test_contamination_{contamination}.png")
    plt.clf()


# Get Anomaly Scores and Predictions
#anomaly_score = model.decision_function(complete_np_dataframe)
#predictions = model.predict(complete_np_dataframe)
#res = np.add(predictions,rpm_speed_df["anomaly"])

# #Plotting result
# anomaly_score = -1*anomaly_score
# anomaly_plot = plt.scatter(complete_dataframe['rpm'], complete_dataframe['speed'], c = anomaly_score, cmap = 'coolwarm')
# plt.colorbar(anomaly_plot,label = 'More Red = More Anomalous')
# plt.xlabel('RPM', fontsize = 12)
# plt.ylabel('Speed', fontsize = 12)
# plt.grid()
# plt.savefig("heatmap.png")

# prediction_plot = plt.scatter(complete_dataframe['rpm'], complete_dataframe['speed'], c = predictions, cmap = 'coolwarm')
# plt.xlabel('RPM', fontsize = 14)
# plt.ylabel('Speed', fontsize = 14)
# plt.grid()
# plt.title(f'Contamination = {contamination}, Accuracy ={round(list(res).count(0)/len(res),3)}', weight = 'bold')
# plt.savefig("prediction.png")

# print(f"anomalies = {list(predictions).count(-1)}")
# print(f"accuracy = {list(res).count(0)/len(res)}")

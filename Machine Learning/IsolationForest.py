from math import gamma
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import numpy as np
import datetime
from sklearn.ensemble import IsolationForest
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from mlxtend.plotting import plot_decision_regions
import seaborn as sns
def train_isolation_forest(x_train,x_test,y_train,y_test):
    contamination = 0.06
    model = IsolationForest(contamination=contamination, max_features=x_train.shape[1])

    #Training the model with train data
    model.fit(x_train.to_numpy())
    anomaly_score_training = model.decision_function(x_train.to_numpy())
    training_prediction = model.predict(x_train.to_numpy())


    #Plotting training heatmap
    anomaly_train_plot = plt.scatter(x_train['rpm'], x_train['speed'], c = -1*anomaly_score_training, cmap = 'coolwarm')
    plt.colorbar(anomaly_train_plot,label = 'More Red = More Anomalous')
    plt.xlabel('RPM', fontsize = 12)
    plt.ylabel('Speed', fontsize = 12)
    plt.grid()
    plt.savefig(f"heatmap_train_contamination_{contamination}.png")
    plt.clf()

    #Plotting training prediction
    prediction_plot = plt.scatter(x_train['rpm'], x_train['speed'], c = -1*training_prediction, cmap = 'coolwarm')
    plt.colorbar(prediction_plot,label = 'More Red = More Anomalous')
    plt.xlabel('RPM', fontsize = 14)
    plt.ylabel('Speed', fontsize = 14)
    plt.grid()
    plt.title(f'Contamination = {contamination}', weight = 'bold')
    plt.savefig(f"prediction_train_contamination_{contamination}.png")
    plt.clf()

    #Testing the accuracy of the model on data unseen before
    anomaly_score_test = model.decision_function(x_test.to_numpy())
    test_prediction = model.predict(x_test.to_numpy())

    #Plotting test heatmap
    anomaly_test_plot = plt.scatter(x_test['rpm'], x_test['speed'], c = -1*anomaly_score_test, cmap = 'coolwarm')
    plt.colorbar(anomaly_test_plot,label = 'More Red = More Anomalous')
    plt.xlabel('RPM', fontsize = 12)
    plt.ylabel('Speed', fontsize = 12)
    plt.grid()
    plt.savefig(f"heatmap_test_contamination_{contamination}.png")
    plt.clf()

    #Plotting test prediction
    test_prediction_plot = plt.scatter(x_test['rpm'], x_test['speed'], c = -1*test_prediction, cmap = 'coolwarm')
    plt.colorbar(test_prediction_plot,label = 'More Red = More Anomalous')
    plt.xlabel('RPM', fontsize = 14)
    plt.ylabel('Speed', fontsize = 14)
    plt.grid()
    plt.title(f'Contamination = {contamination}', weight = 'bold')
    plt.savefig(f"prediction_test_contamination_{contamination}.png")
    plt.clf()

    #Evaluating accuracy of the model

    #In isolation forest -1 is anomalous and 1 is not anomalous
    training_prediction = [0 if i == 1 else 1 for i in training_prediction]
    test_prediction = [0 if i == 1 else 1 for i in test_prediction]


    #Plotting the result
    columns = ["Predicted not anomalous","Predicted anomalous"]
    rows = ["Actual not anomalous","Actual anomalous"]
    training_confusion_matrix = pd.DataFrame(confusion_matrix(y_true=y_train,y_pred=training_prediction),columns=columns,index=rows)
    sns.heatmap(training_confusion_matrix,annot=True,fmt='d',cmap="gist_gray_r",cbar=False).set(title="Training result")
    plt.savefig(f"training_confusion_matrix_{contamination}.png")
    plt.clf()
    testing_confusion_matrix = pd.DataFrame(confusion_matrix(y_true=y_test,y_pred=test_prediction),columns=columns,index=rows)
    sns.heatmap(testing_confusion_matrix,annot=True,fmt='d',cmap="gist_gray_r",cbar=False).set(title="Testing result")
    plt.savefig(f"testing_confusion_matrix_{contamination}.png")
def train_svc(x_train,x_test,y_train,y_test):
    gamma = 0.00001 #0.001 o questo sono quelli che vanno meglio, capire perché magari facendo il plot della regione che prendono
    svm = SVC(kernel="rbf",gamma=gamma,random_state=3)
    svm.fit(x_train,y_train)
    hyperplane_distance = svm.decision_function(x_test)
    prediction = svm.predict(x_test)
    hyperplane_distance_plot = plt.scatter(x_test['rpm'], x_test['speed'], c = hyperplane_distance, cmap = 'coolwarm')
    plt.colorbar(hyperplane_distance_plot,label = 'Distance from the hyperplane')
    plt.xlabel('RPM', fontsize = 12)
    plt.ylabel('Speed', fontsize = 12)
    plt.grid()
    plt.savefig(f"heatmap_train_gamma_{gamma}.png")
    plt.clf()
    
    hyperplane_prediction_plot = plt.scatter(x_test['rpm'], x_test['speed'], c = prediction, cmap = 'coolwarm')
    plt.colorbar(hyperplane_prediction_plot,label = 'Predictions')
    plt.xlabel('RPM', fontsize = 12)
    plt.ylabel('Speed', fontsize = 12)
    plt.grid()
    plt.savefig(f"prediction_train_gamma_{gamma}.png")
    plt.clf()

    plot_decision_regions(x_train.to_numpy(), y_train.to_numpy(), clf=svm, legend=2)
    plt.savefig("decision_regions.png")

#Plotting starting dataset
starting_speed = pd.read_csv("speed.csv")
starting_rpm = pd.read_csv("rpm.csv")
ax = plt.gca()
ax.set_xlim([-100, 4000])
plt.xlabel('RPM', fontsize = 12)
plt.ylabel('Speed', fontsize = 12)
plt.scatter(starting_rpm["data"],starting_speed["data"],c=[0]*starting_speed.shape[0],cmap="coolwarm")
plt.savefig("starting_rpm_speed_scatter.png")
plt.clf()

#pre-processing speed data containing anomalies
speed_df = pd.read_csv("speedAn.csv")
speed_df = speed_df.drop(["id"], axis=1)

#pre-processing rpm dataset containing anomalies
rpm_df = pd.read_csv("rpmAn.csv")
rpm_df = rpm_df.drop(["id","anomaly"], axis=1)

#joining rpm and speed dataframe on timestamp
columns_names = ["timestamp","speed","rpm","is_anomalous"]
rpm_speed_df = pd.merge(rpm_df,speed_df,on="timestamp")
rpm_speed_df = rpm_speed_df.rename(columns={"anomaly" : "is_anomalous"})
rpm_speed_df = rpm_speed_df.reindex(columns=columns_names)
#ax.set_xlim([-100, 4000])

#Plotting dataset containing anomalies
plt.xlabel('RPM', fontsize = 12)
plt.ylabel('Speed', fontsize = 12)
plt.scatter(rpm_speed_df["rpm"],rpm_speed_df["speed"],c=rpm_speed_df["is_anomalous"],cmap="coolwarm")
plt.savefig("rpm_speed_scatter.png")
plt.clf()


#Splitting dataframe for training and testing
labels = rpm_speed_df["is_anomalous"]
complete_dataframe = rpm_speed_df.drop(["timestamp","is_anomalous"],axis=1)
x_train, x_test, y_train, y_test = train_test_split(complete_dataframe,labels,test_size=0.3,stratify=labels,random_state=3)

#Plotting training data
plt.xlabel('RPM', fontsize = 12)
plt.ylabel('Speed', fontsize = 12)
plt.scatter(x_train["rpm"],x_train["speed"],c=y_train,cmap='coolwarm')
plt.savefig("train_scatter")
plt.clf()

#Plotting testing data
plt.xlabel('RPM', fontsize = 12)
plt.ylabel('Speed', fontsize = 12)
plt.scatter(x_test["rpm"],x_test["speed"],c=y_test,cmap='coolwarm')
plt.savefig("test_scatter")
plt.clf()

#train_isolation_forest(x_train,x_test,y_train,y_test)
train_svc(x_train,x_test,y_train,y_test)
#Machine learning model: Isolation Forest
# contamination = 0.06
# model = IsolationForest(contamination=contamination, max_features=x_train.shape[1])

# #Training the model with train data
# model.fit(x_train.to_numpy())
# anomaly_score_training = model.decision_function(x_train.to_numpy())
# training_prediction = model.predict(x_train.to_numpy())


# #Plotting training heatmap
# anomaly_train_plot = plt.scatter(x_train['rpm'], x_train['speed'], c = -1*anomaly_score_training, cmap = 'coolwarm')
# plt.colorbar(anomaly_train_plot,label = 'More Red = More Anomalous')
# plt.xlabel('RPM', fontsize = 12)
# plt.ylabel('Speed', fontsize = 12)
# plt.grid()
# plt.savefig(f"heatmap_train_contamination_{contamination}.png")
# plt.clf()

# #Plotting training prediction
# prediction_plot = plt.scatter(x_train['rpm'], x_train['speed'], c = -1*training_prediction, cmap = 'coolwarm')
# plt.colorbar(prediction_plot,label = 'More Red = More Anomalous')
# plt.xlabel('RPM', fontsize = 14)
# plt.ylabel('Speed', fontsize = 14)
# plt.grid()
# plt.title(f'Contamination = {contamination}', weight = 'bold')
# plt.savefig(f"prediction_train_contamination_{contamination}.png")
# plt.clf()

# #Testing the accuracy of the model on data unseen before
# anomaly_score_test = model.decision_function(x_test.to_numpy())
# test_prediction = model.predict(x_test.to_numpy())

# #Plotting test heatmap
# anomaly_test_plot = plt.scatter(x_test['rpm'], x_test['speed'], c = -1*anomaly_score_test, cmap = 'coolwarm')
# plt.colorbar(anomaly_test_plot,label = 'More Red = More Anomalous')
# plt.xlabel('RPM', fontsize = 12)
# plt.ylabel('Speed', fontsize = 12)
# plt.grid()
# plt.savefig(f"heatmap_test_contamination_{contamination}.png")
# plt.clf()

# #Plotting test prediction
# test_prediction_plot = plt.scatter(x_test['rpm'], x_test['speed'], c = -1*test_prediction, cmap = 'coolwarm')
# plt.colorbar(test_prediction_plot,label = 'More Red = More Anomalous')
# plt.xlabel('RPM', fontsize = 14)
# plt.ylabel('Speed', fontsize = 14)
# plt.grid()
# plt.title(f'Contamination = {contamination}', weight = 'bold')
# plt.savefig(f"prediction_test_contamination_{contamination}.png")
# plt.clf()

# #Evaluating accuracy of the model

# #In isolation forest -1 is anomalous and 1 is not anomalous
# training_prediction = [0 if i == 1 else 1 for i in training_prediction]
# test_prediction = [0 if i == 1 else 1 for i in test_prediction]


# #Plotting the result
# columns = ["Predicted not anomalous","Predicted anomalous"]
# rows = ["Actual not anomalous","Actual anomalous"]
# training_confusion_matrix = pd.DataFrame(confusion_matrix(y_true=y_train,y_pred=training_prediction),columns=columns,index=rows)
# sns.heatmap(training_confusion_matrix,annot=True,fmt='d',cmap="gist_gray_r",cbar=False).set(title="Training result")
# plt.savefig(f"training_confusion_matrix_{contamination}.png")
# plt.clf()
# testing_confusion_matrix = pd.DataFrame(confusion_matrix(y_true=y_test,y_pred=test_prediction),columns=columns,index=rows)
# sns.heatmap(testing_confusion_matrix,annot=True,fmt='d',cmap="gist_gray_r",cbar=False).set(title="Testing result")
# plt.savefig(f"testing_confusion_matrix_{contamination}.png")








"""
https://github.com/facebookresearch/Kats
"""
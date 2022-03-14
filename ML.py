# Training the model by simple Machine Learning
import pandas
dataSet = pandas.read_csv("dialect_dataset_cleaned.csv",encoding ='utf-16')

from sklearn.preprocessing import LabelEncoder
dataSet['text']    = list(map(str, dataSet['text']) ) # to string array
dataSet['text']    = LabelEncoder().fit_transform (dataSet['text'   ])
dataSet['dialect'] = LabelEncoder().fit_transform (dataSet['dialect'])

x = dataSet .drop('id',1) .drop('dialect',1) # text
y = dataSet['dialect']

from sklearn.model_selection import train_test_split as split
xTrain , xTest , yTrain , yTest = split (x , y ,test_size=.3)

from sklearn.ensemble import RandomForestClassifier as tree
model = tree()
model.fit(xTrain , yTrain)

from sklearn.metrics import accuracy_score
print("accuracy = "+ str(accuracy_score (yTest , model.predict(xTest) )))
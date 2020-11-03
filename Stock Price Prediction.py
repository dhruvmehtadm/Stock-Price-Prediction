# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1k9bCKB6EhN55PMABMB93oiKGfPAc5jnS
"""

#importing libraries
import math
import pandas_datareader as web
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
plt.style.use('fivethirtyeight')

#get the stock quote
df = web.DataReader('AAPL', data_source='yahoo', start='2012-01-01', end='2020-10-31')
#show data
df

#get the no. of rows and columns
df.shape

#visualise closing price history
plt.figure(figsize=(16,8))
plt.title('Close Price History')
plt.plot(df['Close'])
plt.xlabel('Date')
plt.ylabel('Close Price USD')
plt.show()

#create new dataframe with only close column
data = df.filter(['Close'])
#convert dataframe to numpy array
dataset = data.values
#get the number pf rows to train the LSTM model
training_data_len = math.ceil(len(dataset)*0.8)
training_data_len

#scale data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)
scaled_data

#create training dataset
#create scaled training dataset
train_data = scaled_data[0:training_data_len, :]
#split data into xtrain and ytrain
x_train = []
y_train = []

for i in range(60, len(train_data)):
  x_train.append(train_data[i-60:i, 0])
  y_train.append(train_data[i, 0])
  if i<=60:
    print(x_train)
    print(y_train)

#convert x_train, y_train to numpy arrays so we can use them for training LSTM model
x_train, y_train = np.array(x_train), np.array(y_train)

#reshape xtrain dataset
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
x_train.shape

#building LSTM model
model = Sequential()
model.add(LSTM(50, return_sequences = True, input_shape = (x_train.shape[1], 1)))
model.add(LSTM(50, return_sequences = False))
model.add(Dense(25))
model.add(Dense(1))

#compile the model
model.compile(optimizer='adam', loss = 'mean_squared_error')

#training model
model.fit(x_train, y_train, batch_size = 1, epochs = 1)

#create testing dataset
#create new array containing scaled values from index 1719 to 2223
test_data = scaled_data[training_data_len-60:, :]
#create xtest and ytest datasets
x_test = []
y_test = dataset[training_data_len:, :]
for i in range(60, len(test_data)):
  x_test.append(test_data[i-60:i, 0])

#convert data into numpy array
x_test = np.array(x_test)

#reshape the data
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
x_test.shape

#get model's predicted price for xtest
pred = model.predict(x_test)
pred = scaler.inverse_transform(pred)

#getting root mean square error
rmse = np.sqrt(np.mean(pred - y_test)**2)
rmse

#plot data
train = data[:training_data_len]
valid = data[training_data_len:]
valid['Predictions'] = pred
#visualise model
plt.figure(figsize = (16,8))
plt.title('Model')
plt.xlabel('Date')
plt.ylabel('Close Price USD')
plt.plot(train['Close'])
plt.plot(valid[['Close', 'Predictions']])
plt.legend(['Train', 'Valid', 'Predictions'], loc = 'lower right')
plt.show()

#show actual and predicted price
valid

#get quote
apple_quote = web.DataReader('AAPL', data_source='yahoo', start='2012-01-01', end='2020-10-31')
new_df = apple_quote.filter(['Close'])
last_60_days = new_df[-60:].values
last_60_days_scaled = scaler.transform(last_60_days)
X_test = []
X_test.append(last_60_days_scaled)
X_test  = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
pred_price = model.predict(X_test)
pred_price = scaler.inverse_transform(pred_price)
print(pred_price)

#get quote
apple_quote2 = web.DataReader('AAPL', data_source='yahoo', start='2012-01-01', end='2020-11-02')
print(apple_quote2['Close'])


import pandas as pd
import numpy as np
import time
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras import optimizers
from keras.callbacks import ModelCheckpoint
from keras.models import Sequential, Model
from keras.layers import LSTM, Dense, Dropout

LOOKBACK = 7
PREDICTION = 1

df_train = pd.read_csv('trainDATA.csv')
df_train = df_train.drop('date', axis=1)
df_train = df_train.drop('store', axis=1)
df_train = df_train.loc[df_train['item'] == 1]
df_train = df_train.drop('item', axis=1)
def createLaggedFrame(data, window=1, lag=1, dropnan=True):
    cols, names = list(), list()
    for i in range(window, 0, -1):
        cols.append(data.shift(i))
        names += [('%s(t-%d)' % (col, i)) for col in data.columns]
    cols.append(data)
    names += [('%s(t)' % (col)) for col in data.columns]
    cols.append(data.shift(-lag))
    names += [('%s(t+%d)' % (col, lag)) for col in data.columns]
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    if dropnan:
        agg.dropna(inplace=True)
    return agg
series = createLaggedFrame(df_train,LOOKBACK,PREDICTION)
last_item = 'item(t-%d)' % LOOKBACK
last_store = 'store(t-%d)' % LOOKBACK
columns_to_drop = [('%s(t+%d)' % (col, PREDICTION)) for col in ['item', 'store']]
labels_col = 'sales(t+%d)' % PREDICTION
labels = series[labels_col]
series = series.drop(labels_col, axis=1)
X_train, X_valid, Y_train, Y_valid = train_test_split(series, labels.values, test_size=0.4,shuffle=False)
X_train_vals = X_train.values.reshape((X_train.shape[0], 1, X_train.shape[1]))
X_valid_vals = X_valid.values.reshape((X_valid.shape[0], 1, X_valid.shape[1]))
def build_model():
    lr = 0.0003
    adam = optimizers.adam(lr)
    model_lstm = Sequential()
    model_lstm.add(LSTM(50, activation='tanh', input_shape=(X_train_vals.shape[1], X_train_vals.shape[2]), dropout=0.2, recurrent_dropout=0.2, return_sequences=True))
    model_lstm.add(LSTM(50, activation='tanh', input_shape=(X_train_vals.shape[1], X_train_vals.shape[2]), dropout=0.2, recurrent_dropout=0.2))
    model_lstm.add(Dense(1, activation='linear'))
    model_lstm.compile(loss='mse', optimizer=adam, metrics=['mape'])
    return model_lstm

model = build_model()
filepath = "Product-{epoch:02d}-{val_loss:.3f}" 
checkpoint = ModelCheckpoint("models/{}.model".format(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='max')) # saves only the best ones
history = model.fit(
    X_train_vals, 
    Y_train, 
    epochs=3, 
    batch_size=70,
    validation_data=(X_valid_vals, Y_valid),
    verbose=2,
    callbacks=[checkpoint]
)
def forecast(fit_model, previous_data, data_length, steps=1):
    previous_data = np.array(previous_data).reshape(1,1,data_length+1)
    return fit_model.predict(previous_data,steps=steps)

print(forecast(model,[3,6,7,8,3,2,4,12],LOOKBACK))
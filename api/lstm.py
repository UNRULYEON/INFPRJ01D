import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras import optimizers
from keras.callbacks import ModelCheckpoint
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout


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

def cleanUpDataframe(data, PREDICTION):
    labels_col = 'stock(t+%d)' % PREDICTION
    labels = data[labels_col]
    series = data.drop(labels_col, axis=1)
    X_train, X_valid, Y_train, Y_valid = train_test_split(series, labels.values, test_size=0.4, shuffle=False)
    X_train_vals = X_train.values.reshape((X_train.shape[0], 1, X_train.shape[1]))
    X_valid_vals = X_valid.values.reshape((X_valid.shape[0], 1, X_valid.shape[1]))
    return X_train_vals, X_valid_vals, Y_train, Y_valid

def build_model(X_vals):
    lr = 0.0003
    adam = optimizers.adam(lr)
    model_lstm = Sequential()
    model_lstm.add(LSTM(50, activation='tanh', input_shape=(X_vals.shape[1], X_vals.shape[2]), dropout=0.2, recurrent_dropout=0.2, return_sequences=True))
    model_lstm.add(LSTM(50, activation='tanh', input_shape=(X_vals.shape[1], X_vals.shape[2]), dropout=0.2, recurrent_dropout=0.2))
    model_lstm.add(Dense(1, activation='linear'))
    model_lstm.compile(loss='mse', optimizer=adam, metrics=['mape'])
    return model_lstm

def model_fit(xT, yT, xV, yV, productId):
    model = None
    filepath = (f"./models/Product-{productId}.model")
    if(os.path.exists(filepath)):
        model = load_model(filepath)
        print("found model")
    else:
        model = build_model(xT)
    checkpoint = ModelCheckpoint(filepath, monitor='val_mean_absolute_percentage_error', verbose=1, save_best_only=True, mode='min')
    model.fit(
        xT,
        xV,
        epochs=100,
        batch_size=70,
        validation_data=(yT, yV),
        verbose=2,
        callbacks=[checkpoint]
    )
def model_loader(productId):
    return load_model(f"./api/models/Product-{productId}.model")


def forecast(fit_model, previous_data, data_length, steps=1):
    previous_data = np.array(previous_data).reshape(1, 1, data_length+1)
    return fit_model.predict(previous_data, steps=steps)

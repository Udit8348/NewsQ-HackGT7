#!./venv/bin/python3

import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from typing import Tuple, List
import json

#import matplotlib.pyplot as plt

def getModel(X:np.array, Y:np.array) -> tf.keras.Sequential:
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(units = 1, input_shape=(X.shape[1],), activation='sigmoid'),
    ])
    model.compile(optimizer='sgd', loss='mse')
    train_history = model.fit(X, Y, epochs=100000)
    """
    W_tf, b_tf = [x.numpy() for x in model.weights]
    print(W_tf, b_tf)
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.plot(np.arange(500), train_history.history['loss'], 'b-', label='loss')
    xlab, ylab = ax.set_xlabel('epochs'), ax.set_ylabel('loss')
    plt.show()
    """
    return model

def parseCSVFile(filename:str) -> Tuple[Tuple[str, str], List[List[float]], List[float]]:
    ARTICLES = []
    Y = []
    X = []
    try:
        with open(filename, "r") as f:
            #f.readline()
            while True:
                data = f.readline().rstrip("\n").split(",")
                if len(data) < 3: break
                ARTICLES.append((data[0], data[1]))
                Y.append(float(data[2]))
                X.append(list(map(lambda x: float(x), data[3:])))
    except IOError:
        pass
    return ARTICLES, np.array(X), np.array(Y)

def parseJSONFile(filename:str) -> Tuple[Tuple[str, str], List[List[float]], List[float]]:
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            return list(map(lambda x: tuple(x), data["ARTICLES"])), np.array(data["X"]), np.array(data["Y"]) 
    except IOError:
        pass
    return [], np.zeros(0), np.zeros(0)

def main() -> None:
    ARTICLES, X, Y = parseJSONFile("json_training_data.json")
    print(ARTICLES)
    print(X)
    print(Y)
    #X = np.ones((100,3)) * 500
    #Y = np.zeros(100)
    scaler = MinMaxScaler()
    scaler.fit(X)
    normalizedX = scaler.transform(X)
    model = getModel(normalizedX, Y)
    print(model.predict(normalizedX))

if __name__ == "__main__":
    main()

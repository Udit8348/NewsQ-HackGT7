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
    train_history = model.fit(X, Y, epochs=20000)
    """
    W_tf, b_tf = [x.numpy() for x in model.weights]
    print(W_tf, b_tf)
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.plot(np.arange(500), train_history.history['loss'], 'b-', label='loss')
    xlab, ylab = ax.set_xlabel('epochs'), ax.set_ylabel('loss')
    plt.show()
    """
    return model

def parseCSVFile(filename:str) -> Tuple[Tuple[str, str, str], List[List[float]], List[float]]:
    ARTICLES = []
    Y = []
    X = []
    try:
        with open(filename, "r") as f:
            #f.readline()
            while True:
                data = f.readline().rstrip("\n").split(",")
                if len(data) < 4: break
                ARTICLES.append((data[0], data[1], data[2]))
                Y.append(float(data[3]))
                X.append(list(map(lambda x: float(x), data[4:])))
    except IOError:
        pass
    return ARTICLES, np.array(X), np.array(Y)

def parseJSONFile(filename:str) -> Tuple[Tuple[str, str, str], List[List[float]], List[float]]:
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            return data["ARTICLES"], np.array(data["X"]), np.array(data["Y"]) 
    except IOError:
        pass
    return [], np.zeros(0), np.zeros(0)

def parseJSONFileNoY(filename:str) -> Tuple[Tuple[str, str, str], List[List[float]], List[float]]:
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            return data["ARTICLES"], np.array(data["X"])
    except IOError:
        pass
    return [], np.zeros(0), np.zeros(0)

def main() -> None:
    ARTICLES, X, Y = parseJSONFile("json_training_data_2.json")
    print(ARTICLES)
    print(X)
    print(Y)
    #X = np.ones((100,3)) * 500
    #Y = np.zeros(100)
    scaler = MinMaxScaler()
    scaler.fit(X)
    normalizedX = scaler.transform(X)
    model = getModel(normalizedX, Y)
    NEW_ARTICLES, NEW_X = parseJSONFileNoY("json_output_data_2.json")
    scaler.fit(NEW_X)
    normalizedNEW_X = scaler.transform(NEW_X)
    predictions = model.predict(normalizedNEW_X)
    print(predictions)
    result = []
    for i in range(len(NEW_ARTICLES)):
        result.append([NEW_ARTICLES[i][0], NEW_ARTICLES[i][1], NEW_ARTICLES[i][2], float(predictions[i][0])])
    result.sort(key = lambda x: x[3], reverse = True)
    with open("final2.json", "w") as f:
        json.dump(result, f)
    print(*result, sep = "\n")

if __name__ == "__main__":
    main()

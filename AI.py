import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

class AI:
    def __init__(self, noofInputs, outputs):
        self.noofInputs = noofInputs
        self.outputs = outputs
        self.model = None
        self.weightsShapes = []

    def createNeuralNet(self, hiddenLayers):
        self.model = Sequential()
        self.model.add(Dense(hiddenLayers[0], input_dim=self.noofInputs, activation='relu'))
        for layer in hiddenLayers[1:]:
            self.model.add(Dense(layer, activation='relu'))
        self.model.add(Dense(self.outputs, activation='linear'))
        self.model.compile(loss='mean_squared_error', optimizer='adam')

    def predict(self, inputs):
        return self.model.predict(np.array([inputs]))

    def getWeightsVector(self):
        weights = self.model.get_weights()
        self.weightsShapes = [w.shape for w in weights]
        flattened_weights = np.concatenate([w.flatten() for w in weights])
        return flattened_weights

    def setWeightsFromVector(self, weightsVector):
        weightsVector = np.array(weightsVector)  # Convert to NumPy array
        weights = []
        start = 0
        for shape in self.weightsShapes:
            size = np.prod(shape)
            weights.append(weightsVector[start:start + size].reshape(shape))
            start += size
        self.model.set_weights(weights)

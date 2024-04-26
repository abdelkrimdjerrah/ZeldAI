import numpy as np


class Perceptron:
    def __init__(self, learning_rate, num_inputs):
        self.learning_rate = learning_rate
        self.weights = np.random.rand(num_inputs + 1)  
        self.bias = self.weights[-1]

    def predict(self, inputs):
        inputs_with_bias = np.append(inputs, 1)  
        activation = np.dot(inputs_with_bias, self.weights)
        return self.activation_function(activation)

    def activation_function(self, x):
        return 1 / (1 + np.exp(-x))

    def train(self, inputs, target):
        inputs_with_bias = np.append(inputs, 1)  
        prediction = self.predict(inputs)
        error = target - prediction

        self.weights += self.learning_rate * error * inputs_with_bias

        return error
    
    def get_action(self, inputs):
        prediction = self.predict(inputs)
        print(prediction)
        
        if prediction >= 0.6:
            return "shoot"
        elif prediction >= 0.4:
            return "follow"
        else:
            return "random"





# import the necessary modules for your ANN below:
# For instance: import numpy as np
import numpy as np
import p3.config as c

class ANN(object):
    def __init__(self, num_inputs, num_hidden_nodes, num_outputs, weights):
        self.weights = weights # this is an individual which is actually a list of weights (genome)
        # You need to extract the list of weights and put each weight into correct place in your ANN.
        # Therefore ANN topology should be fixed through all generations.
        num_hidden_weights = (num_inputs+1) * num_hidden_nodes
        # Let's assume that you have one hidden layer, then you would end up with two matrices of weights:
        # 1) Between the input layer and the hidden layer
        # 2) Between the hidden layer and the output layer
        # Hence, place them in the following hidden and output weights variables, respectively.
        self.hidden_weights = np.array(weights[:num_hidden_weights]).reshape(num_hidden_nodes,num_inputs+1)
        self.output_weights = np.array(weights[num_hidden_weights:]).reshape(num_outputs,num_hidden_nodes+1)

    def activation(self, x):
        # x is the net input to the neuron (previously represented as "z" during the class)
        # a is the activation value ( a = activation(z) )
        # activation function could be sigmoid function: 1/(1+exp(-x))
        a = 1/(1+np.exp(-x))
        return a

    def evaluate(self, inputs):
        # Compute outputs from the fully connected feed-forward ANN:
        # So basically, you will perform the operations that you did on HW4:
        # Let's assume that you have one hidden layer with 2 hidden nodes. Then you would have
        # a matrix of weights (first layer of weights beetween the input and hidden layers) of
        # size: 2 x (3+1) = 8, and another matrix of weights (second layer between the hidden
        # layer and the output layer) of size: 2 x (2+1) = 6, resulting in total of 14 weights.
        inputs.append(1) # Bias
        z2 = np.dot(self.hidden_weights, inputs)

        hidden_nodes = []
        hidden_nodes.append(1) # Bias
        for i in range(c.nnet['n_h_neurons']):
            hidden_nodes.append(self.activation(z2[i]))

        z3 = np.dot(self.output_weights, hidden_nodes)

        outputs = []
        for i in range(c.nnet['n_outputs']):
            outputs.append(self.activation(z3[i]))
        
        return outputs
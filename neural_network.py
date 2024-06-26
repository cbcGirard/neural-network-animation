import matplotlib.pyplot as plt
# matplotlib.use("Agg")
from math import fabs
from formulae import sigmoid, sigmoid_derivative, random_weight, get_synapse_colour, adjust_line_to_perimeter_of_circle, layer_y_margin
import parameters


class Synapse():
    def __init__(self, input_neuron_index, x1, x2, y1, y2):
        self.input_neuron_index = input_neuron_index
        self.weight = random_weight()
        self.signal = 0
        x1, x2, y1, y2 = adjust_line_to_perimeter_of_circle(x1, x2, y1, y2)
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def draw(self, ax):
        line = plt.Line2D((self.x1, self.x2), 
                          (self.y1, self.y2), 
                          lw=fabs(self.weight*parameters.synapse_width_scale), 
                          color=get_synapse_colour(self.weight), zorder=1)
        outer_glow = plt.Line2D((self.x1, self.x2), 
                                (self.y1, self.y2), 
                                lw=(fabs(self.weight) * 2), 
                                color=get_synapse_colour(self.weight), 
                                zorder=2, alpha=self.signal * 0.4)
        ax.add_line(line)
        ax.add_line(outer_glow)


class Neuron():
    def __init__(self, x, y, previous_layer):
        self.x = x
        self.y = y
        self.output = 0
        self.synapses = []
        self.error = 0
        index = 0
        if previous_layer:
            for input_neuron in previous_layer.neurons:
                synapse = Synapse(index, x, input_neuron.x, y, input_neuron.y)
                self.synapses.append(synapse)
                index += 1

    def train(self, previous_layer):
        for synapse in self.synapses:
            # Propagate the error back down the synapse to the neuron in the layer below
            previous_layer.neurons[synapse.input_neuron_index].error += self.error * sigmoid_derivative(self.output) * synapse.weight
            # Adjust the synapse weight
            synapse.weight += synapse.signal * self.error * sigmoid_derivative(self.output)
        return previous_layer

    def think(self, previous_layer):
        activity = 0
        for synapse in self.synapses:
            synapse.signal = previous_layer.neurons[synapse.input_neuron_index].output
            activity += synapse.weight * synapse.signal
        self.output = sigmoid(activity)

    def draw(self, ax):
        circle = plt.Circle((self.x, self.y), 
                               radius=parameters.neuron_radius, 
                               fill=True, color=(0.2, 0.2, 0), 
                               zorder=3)
        outer_glow = plt.Circle((self.x, self.y), 
                                   radius=parameters.neuron_radius * 1.5, 
                                   fill=True, 
                                   color=(self.output, self.output, 0), zorder=4, alpha=self.output * 0.5)
        

        ax.add_patch(circle)
        ax.add_patch(outer_glow)
        if parameters.annotate:
            ax.text(self.x + 0.8, self.y, round(self.output, 2))

        for synapse in self.synapses:
            synapse.draw(ax)


class Layer():
    def __init__(self, network, number_of_neurons):
        if len(network.layers) > 0:
            self.is_input_layer = False
            self.previous_layer = network.layers[-1]
            self.y = self.previous_layer.y + parameters.distance_between_layers
        else:
            self.is_input_layer = True
            self.previous_layer = None
            self.y = parameters.x_margin
        self.neurons = []
        x = layer_y_margin(number_of_neurons)
        # x = parameters.y_margin
        for iteration in range(number_of_neurons):
            # neuron = Neuron(x, self.y, self.previous_layer)
            neuron = Neuron(self.y, x, self.previous_layer)
            self.neurons.append(neuron)
            x += parameters.distance_within_layer

    def think(self):
        for neuron in self.neurons:
            neuron.think(self.previous_layer)

    def draw(self,ax):
        for neuron in self.neurons:
            neuron.draw(ax)


class NeuralNetwork():
    def __init__(self, requested_layers):
        self.layers = []
        for number_of_neurons in requested_layers:
            self.layers.append(Layer(self, number_of_neurons))

    def train(self, example):
        error = example.output - self.think(example.inputs)
        self.reset_errors()
        self.layers[-1].neurons[0].error = error
        for l in range(len(self.layers) - 1, 0, -1):
            for neuron in self.layers[l].neurons:
                self.layers[l - 1] = neuron.train(self.layers[l - 1])
        return fabs(error)

    def do_not_think(self):
        for layer in self.layers:
            for neuron in layer.neurons:
                neuron.output = 0
                for synapse in neuron.synapses:
                    synapse.signal = 0

    def think(self, inputs):
        for layer in self.layers:
            if layer.is_input_layer:
                for index, value in enumerate(inputs):
                    self.layers[0].neurons[index].output = value
            else:
                layer.think()
        return self.layers[-1].neurons[0].output

    def draw(self,ax):
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        plt.cla()
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        for layer in self.layers:
            layer.draw(ax)
        # plt.show()

    def reset_errors(self):
        for layer in self.layers:
            for neuron in layer.neurons:
                neuron.error = 0
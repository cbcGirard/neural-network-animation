from tkinter import NE
from numpy import exp, random, pi, arctan2
from math import atan, sin, cos
import parameters
from matplotlib.colors import hex2color

POS_SYNAPSE_COLOR = hex2color("#00966c")
NEG_SYNAPSE_COLOR = hex2color("#a50034")

def sigmoid(x):
    return 1 / (1 + exp(-x))


def sigmoid_derivative(x):
    return x * (1 - x)


def seed_random_number_generator():
    random.seed(1)


def random_weight():
    return 2 * random.random() - 1


def get_synapse_colour(weight):
    if weight > 0:
        return POS_SYNAPSE_COLOR
        # return 0, 1, 0
    else:
        # return 1, 0, 0
        return NEG_SYNAPSE_COLOR


def adjust_line_to_perimeter_of_circle(x1, x2, y1, y2):
    # angle = atan((x2 - x1) / float(y2 - y1))
    # angle = atan(float(y2 - y1)/(x2 - x1) )
    angle = arctan2(x2 - x1, y2 - y1)

    x_adjustment = -parameters.neuron_radius * sin(angle)
    y_adjustment = -parameters.neuron_radius * cos(angle)

    return x1 - x_adjustment, x2 + x_adjustment, y1 - y_adjustment, y2 + y_adjustment


def layer_y_margin(number_of_neurons):
    return parameters.y_margin + parameters.distance_within_layer * (parameters.number_of_neurons_in_widest_layer - number_of_neurons) / 2


def calculate_average_error(cumulative_error, number_of_examples):
    if cumulative_error:
        return round(cumulative_error * 100 / number_of_examples, 2)
    else:
        return None
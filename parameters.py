from numpy import geomspace, linspace
# Parameters for drawing the network
distance_between_layers = 5
distance_within_layer = 3
neuron_radius = 0.5
number_of_neurons_in_widest_layer = 4

# Display parameters
synapse_width_scale = 2
font_size = 20


y_margin = 3
x_margin = 2
error_bar_x_position = 14
output_y_position = 15

width = 25
height = 20

def calc_area(layer_counts):
    global width
    global height
    global error_bar_x_position
    global number_of_neurons_in_widest_layer

    max_layer = max(layer_counts)

    width = (len(layer_counts)-1) * distance_between_layers + x_margin*2
    height = (max_layer-1) * distance_within_layer + y_margin*2

    # print(f"Initial dimensions: {width} x {height}")

    if width/height > 16/9:
        height = width * 9/16
    else:
        width = height * 16/9

    error_bar_x_position = width - 10 - x_margin
    number_of_neurons_in_widest_layer = max_layer

    # print("width: ", width)
    # print("height: ", height)


# Parameters for the video
frames_per_second = 30
nframes = 60
# show_iterations = [2, 10, 20, 50, 100, 200, 300, 400, 500, 1000, 2500, 12500, 60000]
video_file_name = "neural_network.mp4"
metadata = dict(artist="CBC Girard", title="Neural Network")

# Parameters for training the network
# training_iterations = 60000
training_iterations = 5000

show_iterations = geomspace(2, training_iterations, num=nframes, dtype=int)
# show_iterations = linspace(2, training_iterations, num=50, dtype=int)
annotate = False

training_timeline = True
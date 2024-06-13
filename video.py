import parameters
import matplotlib
# matplotlib.use("macosx")
from matplotlib import pyplot, animation, rcParams
from matplotlib.animation import FFMpegWriter

OFFWHITE = "#f7f2e8"

def generate_writer(fig, axis, layer_counts):
    # FFMpegWriter = animation.writers['ffmpeg']
    # fig = pyplot.figure()
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)

    width = parameters.width
    height = parameters.height


    pyplot.xlim(0, width)
    pyplot.ylim(0, height)
    writer = FFMpegWriter(fps=parameters.frames_per_second, metadata=parameters.metadata)
    # axis = pyplot.gca()
    # axis.set_axis_bgcolor('black')
    axis.set_facecolor('#231F20')
    axis.axes.get_xaxis().set_visible(False)
    axis.axes.get_yaxis().set_visible(False)
    rcParams['font.size'] = parameters.font_size
    rcParams['text.color'] = OFFWHITE
    rcParams['font.sans-serif'].insert(0, 'Futura')

    return fig, axis, writer


def annotate_frame(i, e, average_error, example):
    if parameters.annotate:
        pyplot.text(1, parameters.height - 1, "Iteration #" + str(i))
        pyplot.text(1, parameters.height - 2, "Training example #" + str(e + 1))
        pyplot.text(1, parameters.output_y_position, "Desired output:")
        pyplot.text(1, parameters.output_y_position - 1, str(example.output))
        pyplot.text(1, parameters.x_margin + 1, "Inputs:")
        pyplot.text(1, parameters.x_margin, str(example.inputs))
    if average_error:
        error_bar(average_error,i)


def error_bar(average_error,i):
    err_string = "Average Error " 
    if parameters.annotate:
        err_string += str(average_error) + "%"
    pyplot.text(parameters.error_bar_x_position, parameters.height - 1, err_string)
    border = pyplot.Rectangle((parameters.error_bar_x_position, parameters.height - 3), 10, 1, color='white', fill=False)
    pyplot.gca().add_patch(border)
    rectangle = pyplot.Rectangle((parameters.error_bar_x_position, parameters.height - 3), 10 * average_error / 100, 1, color='red')
    pyplot.gca().add_patch(rectangle)

    if parameters.training_timeline:
        time_border = pyplot.Rectangle((parameters.error_bar_x_position, parameters.height - 5), 10, 1, color='white', fill=False)
        pyplot.gca().add_patch(time_border)
        time_rectangle = pyplot.Rectangle((parameters.error_bar_x_position, parameters.height - 5), 10 * i / parameters.training_iterations, 1, color='blue')
        pyplot.gca().add_patch(time_rectangle)
        pyplot.text(parameters.error_bar_x_position, parameters.height - 6, "Training iterations")


def take_still(image_file_name):
    pyplot.savefig(image_file_name)

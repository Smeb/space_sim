import matplotlib.pyplot as plt

def compare_two_vectors(vector_1_results, vector_2_results, xs, labels, context, vector1_name, vector2_name):
    """Side by side comparison of the elements of two vectors, producing six graphs
    Input:
        vector1_results - A list of numpy.arrays with three elements
        vector2_results - A list of numpy.arrays with three elements
        xs - the x values to plot against (typically a time series)
        labels - (x_label, y_label, [3 element labels]),
        vector1_name - The string name for vector1
        vector2_name - The string name for vector2
    Output:
        Six graphs, saved as ./docs/media/{context}{vector1_name}{vector2_name}.png directory as well as shown to the user
    """
    import itertools
    plot_title = "Comparison of the {} vectors for a {} and {} propogated orbit".format(context, vector1_name, vector2_name)
    figs = []

    f, axes = plt.subplots(3, 2, sharex=True, sharey=False, figsize=(12, 8), dpi=80)
    min_max_arr = list(itertools.chain(*(vector_1_results + vector_2_results)))
    min_y = min(min_max_arr) * 1.15
    max_y = max(min_max_arr) * 1.15

    for pair, ys_1, ys_2, l in zip(axes, zip(*vector_1_results), zip(*vector_2_results), labels[2]):
        for axis, ys, vname in zip(pair, [ys_1, ys_2], [vector1_name, vector2_name]):
            axis.set_ylim([min_y, max_y])
            axis.set_title("{} {}".format(vname, l))
            axis.plot(xs, ys)

    f.text(0.50, 0.04, labels[0],  ha='center', fontsize=14)
    f.text(0.04, 0.5, labels[1], va='center', rotation='vertical', fontsize=14)
    plt.savefig("./docs/media/{}{}{}_comparison.png".format(context, vector1_name, vector2_name))
    plt.show()

def superimpose_two_vectors(vector_1_results, vector_2_results, xs, labels, context, vector1_name, vector2_name):
    """Superimposes the elements of two vectors onto one another, producing three graphs
    Input:
        vector1_results - A list of numpy.arrays with three elements
        vector2_results - A list of numpy.arrays with three elements
        xs - the x values to plot against (typically a time series)
        labels - (x_label, y_label, [3 element labels]),
        vector1_name - The string name for vector1
        vector2_name - The string name for vector2
    Output:
        Three graphs, saved as ./docs/media/{context}{vector1_name}{vector2_name}.png directory as well as shown to the user
    """
    import itertools
    plot_title = "Comparison of the {} vectors for a {} and {} propogated orbit".format(context, vector1_name, vector2_name)
    figs = []

    f, axes = plt.subplots(3, sharex=True, sharey=False, figsize=(12, 8), dpi=80)
    min_max_arr = list(itertools.chain(*(vector_1_results + vector_2_results)))
    min_y = min(min_max_arr) * 1.15
    max_y = max(min_max_arr) * 1.15

    for axis, ys_1, ys_2, l in zip(axes, zip(*vector_1_results), zip(*vector_2_results), labels[2]):
        axis.set_ylim([min_y, max_y])
        print(sum([a - b for a, b in zip(ys_1, ys_2)]))
        axis.set_title("{} vs {} for {}".format(vector1_name, vector2_name, l))
        axis.plot(xs, ys_1, color='b')
        axis.plot(xs, ys_1, color='r')

    f.text(0.50, 0.04, labels[0],  ha='center', fontsize=14)
    f.text(0.04, 0.5, labels[1], va='center', rotation='vertical', fontsize=14)
    plt.savefig("./docs/media/{}{}{}_superimposed.png".format(context, vector1_name, vector2_name))
    plt.show()

def plot_gs_vis_2d(ground_stations_visibilities, name):
    """Plots a 2-dimensional grid of ground stations as red points, where the size of the point
    is scaled according to the size of the visibility index. Saves the result to
    './docs/media/<fname>.png'

    Input:
        ground_stations_visibilities - a list of tuples (GroundStation, int)
        name - the name to save the file as
    """
    from basis_converters.from_radians import degrees
    from operator import itemgetter
    # Get the maximum size for scaling
    maximum = max(ground_stations_visibilities, key=itemgetter(1))[1]
    plt.xlim([-180, 180])
    plt.ylim([-90, 90])
    for gs, density in ground_stations_visibilities:
        gsy, gsx = gs.lat_long
        gs_m_y, gs_m_x = list(map(degrees, gs.lat_long))
        plt.plot(gs_m_x, gs_m_y, 'bo', markersize=density / maximum * 10.0, color='r')
    plt.xlabel('longitude(degrees)')
    plt.ylabel('latitude(degrees)')
    plt.savefig('./docs/media/{}.png'.format(name))
    plt.show()

import matplotlib.pyplot as plt

def time_plot(data_series, time_delta, name):
    import itertools
    xs = [x * 10 for x in  range(len(data_series[0]))]
    handles = []

    min_max_arr = list(itertools.chain(*(data_series)))
    min_y = min(min_max_arr) * 1.15
    max_y = max(min_max_arr) * 1.15

    f = plt.figure(figsize=(12, 8))
    plt.ylim([min_y, max_y])
    for series, color, l in zip(data_series, ['r', 'g', 'b'], ['e', 'n', 'u']):
        handles.append(plt.scatter(xs, series, s=1, c=color, label=l).get_label())
    plt.legend(handles)
    plt.xlabel('time(s)')
    plt.ylabel('difference (km)')
    plt.grid()
    plt.savefig('./docs/media/{}.png'.format(name))
    plt.show()

def timelines(y, xstart, xstop, color):
    plt.hlines(y, xstart, xstop, color, lw=4)
    plt.vlines(xstart, y+0.03, y-0.03, color, lw=2)
    plt.vlines(xstop, y+0.03, y-0.03, color, lw=2)

def time_series_plot(ground_stations_passes):
    from matplotlib.dates import DateFormatter, MinuteLocator
    from operator import itemgetter
    starts = []
    stops = []

    for index, ((gs, passes), color) in enumerate(zip(ground_stations_passes, ['r', 'b', 'k', 'g'])):
        for (start, _, _), (_, _, stop) in passes:
            starts.append(start)
            stops.append(stop)
            timelines(index, start, stop, color)


    fmt = DateFormatter('%H:%M:%S')

    ax = plt.gca()
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(fmt)
    ax.xaxis.set_major_locator(MinuteLocator(interval=10))

    plt.xlim(min(starts), max(stops))
    plt.xlabel('Time')
    plt.show()

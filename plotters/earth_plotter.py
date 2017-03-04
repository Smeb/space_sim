from mpl_toolkits.basemap import Basemap, cm
import matplotlib.pyplot as plt
import numpy

def ground_tracks_3(orbits):
    """Plots data from a number or Results instances onto maps, organised by row
    Input:
        orbits - an arbitrary length list of Results
    Output:
        A visualisation, which is shown to the user
    """
    from basis_converters.from_eci import eci_to_kep
    from basis_converters.from_radians import degrees
    fig = plt.figure()
    for i, orbit in enumerate(orbits):
        sp = fig.add_subplot(1, len(orbits), i + 1)
        m = init_projection()
        lists = list(zip(*orbit.lat_long_h))
        latitudes = list(map(degrees, lists[0]))
        longitudes = list(map(degrees, lists[1]))
        xs, ys = m(longitudes, latitudes)
        sp.set_title(orbit.pname)
        m.plot(xs, ys)
    plt.subplots_adjust(hspace=0.3)
    plt.show()

def plot_ground_tracks_vs_vis(results, ground_stations, name):
    """Superimposes visible points onto ground tracks
    Input:
        results - an instance of a Result object
        ground_stations - a list of ground_stations with which to filter the results
        name - the name for the output file
    Output:
        A visualisation, which is saved to './docs/media/{name}.png'
    """
    from basis_converters.from_ecef import ecef_to_lat_long_h
    from basis_converters.from_radians import degrees

    # Unwrap values and convert to degrees for basemap
    latitudes, longitudes, _ = list(zip(*results.lat_long_h))

    latitudes = list(map(degrees, latitudes))
    longitudes = list(map(degrees, longitudes))

    m = init_projection()

    xs, ys = m(longitudes, latitudes)
    m.plot(xs, ys, 'bo', markersize=1, color='k')
    handles = []
    for gs, c in zip(ground_stations, ['r', 'g', 'b', 'sienna']):
        gsy, gsx = gs.lat_long
        gs_m_x, gs_m_y = m(degrees(gsx), degrees(gsy))
        m.plot(gs_m_x, gs_m_y, 'bo', markersize=10, color=c, label=gs.name)
        points = [ecef_to_lat_long_h(point) for point in results.ecef_r if gs.visible(point)]
        lats, longs = zip(*[(degrees(lats), degrees(longs)) for lats, longs, _ in points])
        lats_m, longs_m = m(lats, longs)
        m.plot(longs_m, lats_m, 'bo', markersize=1, color=c)
    plt.legend()
    plt.tight_layout()
    plt.savefig('./docs/media/{}.png'.format(name), dpi=1000)
    plt.show()

def plot_gs_vis(search_data, name):
    """Takes an input list of GroundStations with visibility lengths and color annotations and
    plots them onto a basemap projection. Data processing must be done before this function receives the list

    Input:
        search_data - annotated results of a grid search
        name - the name of the output file
    Output:
        (side effect) - saves a map to ./docs/media/{name}.png
    """
    from operator import itemgetter
    from basis_converters.from_radians import degrees
    plt.figure(figsize=(8, 14), dpi=200)
    m = init_projection()
    _, max_density, _ = max(search_data, key=itemgetter(1))
    for gs, density, color in search_data:
        gsy, gsx = gs.lat_long
        gs_m_x, gs_m_y = m(degrees(gsx), degrees(gsy))

        m.plot(gs_m_x, gs_m_y, 'bo', markersize=density / max_density * 10, color=color)
    plt.savefig("./docs/media/{}.png".format(name))
    plt.show()

def plot_polar(ground_station, results, name):
    """Takes a GroundStation with a Visibility list and draws a map using a
    polar projection

    Input:
        ground_station - A GroundStation instance
        results - a Results instance
    Output:
        (side effect) - saves a map to ./docs/media/{name}_stereo.png
    """
    import altair
    from basis_converters.from_ecef import ecef_to_lat_long_h
    from basis_converters.from_radians import degrees
    pass_times = ground_station.divide_passes(results)



    lat, long = map(degrees, ground_station.lat_long)

    m = Basemap(projection='stere', width=9000000, height=9000000, lat_0=lat, lon_0=long, lat_ts=10)
    m.drawcoastlines(linewidth=0.25)
    m.drawcountries(linewidth=0.25)
    m.fillcontinents(color='ghostwhite', lake_color='skyblue')
    m.drawmapboundary(fill_color='skyblue')

    long_m, lat_m = m(long, lat)
    plt.plot(long_m, lat_m, markersize=10)
    for passes in pass_times:
        lats = []
        longs = []
        for item in passes:
            lat, long, _ = ecef_to_lat_long_h(item)
            lats.append(degrees(lat))
            longs.append(degrees(long))
        longs_m, lats_m = m(longs, lats)
        plt.plot(longs_m, lats_m)
    plt.savefig("./docs/media/{}_passes.png".format(name))
    plt.show()

def init_projection():
    """Initialises the map object which is used for all the earth_plotter tasks
    Input:
        None
    Output:
        None
    """
    m = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90,\
              llcrnrlon=-180, urcrnrlon=180, resolution='c')
    m.drawcoastlines(linewidth=0.25)
    m.drawcountries(linewidth=0.25)
    m.fillcontinents(color='ghostwhite', lake_color='skyblue')
    m.drawmapboundary(fill_color='skyblue')

    m.drawmeridians(numpy.arange(0, 360, 60), labels=[False, False, False, True])
    m.drawparallels(numpy.arange(-90, 90, 60), labels=[True, False, False, False])
    return m

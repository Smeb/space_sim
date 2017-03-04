def ground_station_gs(increment):
    """Generates candidate ground stations in the range
        latitude  = (-90, 90)
        longitude = (-180, 180)
        Where values are separated by the value of increment.
    """
    from models.ground_station import GroundStation
    from numpy import arange, pi
    from basis_converters.from_topo import lat_long_to_ecef
    index = 0
    ground_stations = []
    for longitude in arange(-pi + increment, pi, increment):
        for latitude in arange(-pi / 2 + increment, pi / 2, increment):
            ground_stations.append(GroundStation(lat_long_to_ecef([latitude,
              longitude]), str(index)))
            index += 1
    return ground_stations

def grid_search(increment, data):
    """Generates candidates using ground_station_gs then from generated candidates
    the input data is filtered for visibility.

        Returns a list of [GroundStation, Visibility], where Visibility is in the
        ECEF_R basis
    """
    from basis_converters.from_ecef import ecef_to_lat_long_h
    from basis_converters.from_radians import degrees
    from utils.save_load import save, load

    results = load(['grid_search', increment, data])
    if results is not None:
        return results

    ground_stations = ground_station_gs(increment)
    results = []
    for gs in ground_stations:
        visible = [x for x in data.ecef_r if gs.visible(x)]
        lat, long = gs.lat_long
        print("{}, {}".format(degrees(lat), degrees(long)))
        results.append((gs, visible))

    save(['grid_search', increment, data], results)
    return results

def filter_candidates(candidates):
    """Looks up each candidate based on longitude and latitude using Nominatim
    and filters out candidates which aren't over land (returns None for the address)

    Returns a list of [(GroundStation, Visibility, Color)], where color='r', in
    preparation for grid_search_long
    """
    import time
    from geopy.geocoders import Nominatim
    from basis_converters.from_radians import degrees
    geolocator = Nominatim()

    filtered_candidates = []
    for index, (gs, visible) in enumerate(candidates):
        lat, long = gs.lat_long
        try:
            time.sleep(1)
            lookup = geolocator.reverse("{}, {}".format(degrees(lat), degrees(long)))
            if lookup.address is not None:
                print("{}, {} - {}".format(degrees(lat), degrees(long), lookup.address))
                filtered_candidates.append((gs, visible))
            else:
                print("{}, {} - Not Found".format(degrees(lat), degrees(long)))
        except Exception as e:
            print(e)
    # Also sets all points to 'r' in preparation for Grid Search
    northern_hemisphere = [(gs, visible, 'r') for gs, visible in filtered_candidates if gs.lat_long[0] > 0]
    southern_hemisphere = [(gs, visible, 'r') for gs, visible in filtered_candidates if gs.lat_long[0] <= 0]
    return northern_hemisphere, southern_hemisphere

def grid_search_long(increment, data):
    """Conducts a two phase grid search, generating candidates using grid_search,
    and then filtering out candidates over water. The candidates are divided into
    Northern and Souther hemispheres.

    In the first phase the candidate ground station with the greatest visibility in
    each hemisphere is chosen. In the second phase the search space is reduced by
    removing points visible from the candidates chosen in the first phase, and then
    two further ground stations are selected based on the number of points visible.

    Returns a list of [(GroundStation, Visibility, Color)], where for chosen candidates
    Color='g' (Green), and all other candidates Color='r'
    """
    from basis_converters.from_topo import lat_long_to_ecef
    from utils.save_load import save, load
    from operator import itemgetter
    hemispheres = load(['filtered_grid_search', increment, data])
    if hemispheres is None:
        candidates = grid_search(increment, data)
        hemispheres = filter_candidates(candidates)
        save(['filtered_grid_search', increment, data], hemispheres)
    # Find the best candidate in both the Northern and Southern hemisphere
    maximums = [[], []]
    for hemisphere_index, hemisphere in enumerate(hemispheres):
        items = [len(visible) for _, visible, _ in hemisphere]
        index, _ = max(enumerate(items), key=itemgetter(1))
        maximums[hemisphere_index].append(index)

    # Find the second best ground station in each hemisphere after filtering out points
    # visible to the first station
    for hemisphere_index, hemisphere in enumerate(hemispheres):
        reduced_hemisphere = []
        best_gs, _, _ = hemisphere[maximums[hemisphere_index][0]]
        for item_index, (_, visibility, _) in enumerate(hemisphere):
            # Don't add the previous best candidate
            if item_index == maximums[hemisphere_index][0]:
                continue
            filtered_visiblity = [point for point in visibility if best_gs.visible(point) is False]
            reduced_hemisphere.append(len(filtered_visiblity))

        index, _ = max(enumerate(reduced_hemisphere), key=itemgetter(1))
        if index >= maximums[hemisphere_index][0]:
            # Adjust for the removed list element (the best candidate)
            index += 1
        maximums[hemisphere_index].append(index)

    for hemisphere_index, hemisphere in enumerate(maximums):
        for maximum in hemisphere:
            gs, visibility, _ = hemispheres[hemisphere_index][maximum]
            hemispheres[hemisphere_index][maximum] = (gs, visibility, 'g')
            print(len(visibility))

    # Flatten hemispheres since there's no further need to divide the search
    hemispheres = [item for sublist in hemispheres for item in sublist]
    for gs, visibility, c in hemispheres:
        from basis_converters.from_radians import degrees
        if c=='g':
            lat, long = map(degrees, gs.lat_long)
            print(lat, long, len(visibility))


    return hemispheres




    save(['filtered_grid_search', increment, data], hemispheres)

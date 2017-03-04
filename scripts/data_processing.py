def compute_passes(ground_stations, orbit_results):
    from basis_converters.from_radians import degrees
    """Given ground stations and an orbit, computes passes for the orbit and saves them to a file in ./docs/media/<fname>.tex
    with a file name derived from the latitude, longitude coordinates, in tex table format

    Input:
        ground_stations - a list of GroundStation instances
        orbit_results - a Result instance

    Output:
        .tex tables for each GroundStation's passes
        results - a list of
                    (ground station, (start time, start elevation, start
                        azimuth, end time, end elevation, end azimuth))
                  tuples

    """
    results = []
    for gs in ground_stations:
        passes = gs.pass_times(orbit_results)
        lat, long = map(degrees, gs.lat_long)
        results.append((gs, passes))
        continue
        with open('./docs/media/{}_gs.tex'.format(gs.name), 'w') as f:
            print(lat, long, file=f)
            for (start_t, start_e, start_a), (end_t, end_e, end_a) in passes:
                print(start_t, start_e, start_a, end_t, end_e, end_a, end_t - start_t, sep=" & ", end="\\\\ \n", file=f)
    return results

def compare_orbits_rv(orbit1_results, orbit2_results):
    """Compares the R and V vectors from two orbits in the ECI basis
    Input:
        orbit1_results - An instance of a Results object
        orbit2_results - An instance of a Results object
    Output:
        Twelve graphs, saved in the ./docs/media directory as well as shown to the user
    """
    from plotters.plotter2d import compare_two_vectors
    orbit1_r, orbit1_v = zip(*orbit1_results.eci)

    orbit2_r, orbit2_v = zip(*orbit2_results.eci)
    time = [10 * i for i in range(len(orbit1_r))]
    compare_two_vectors(orbit1_r, orbit2_r, time, ('eci position (km)', 'time (s)', ['x', 'y', 'z']), 'position',
                        orbit1_results.pname,
                        orbit2_results.pname)
    compare_two_vectors(orbit1_v, orbit2_v, time, ('velocity (km/s)', 'time (s)', ['u', 'v', 'w']), 'velocity',
                        orbit1_results.pname,
                        orbit2_results.pname)

def compare_orbits_superimposed(orbit1_results, orbit2_results):
    """Superimposes orbit R and V vectors onto one another.
    Input:
        orbit1_results - An instance of a Results object
        orbit2_results - An instance of a Results object
    Output:
        Six graphs, saved in the ./docs/media directory as well as shown to the user
    """
    from plotters.plotter2d import superimpose_two_vectors
    orbit1_r, orbit1_v = zip(*orbit1_results.eci)

    orbit2_r, orbit2_v = zip(*orbit2_results.eci)
    time = [10 * i for i in range(len(orbit1_r))]
    superimpose_two_vectors(orbit1_r, orbit2_r, time, ('eci position (km)', 'time (s)', ['x', 'y', 'z']), 'position',
                        orbit1_results.pname,
                        orbit2_results.pname)
    superimpose_two_vectors(orbit1_v, orbit2_v, time, ('velocity (km/s)', 'time (s)', ['u', 'v', 'w']), 'velocity',
                        orbit1_results.pname,
                        orbit2_results.pname)

def compare_orbits_hcl(results_a, results_b, name):
    """Compares orbits in the hcl basis and plots them using time_plot
    Output:
        results_a - A Results instance
        results_b - A Results instance
        name - a string
    """
    from validation_tools.orbit_comparison import orbit_difference_hcl
    from plotters.time_plotter import time_plot
    plot_points = orbit_difference_hcl(results_a, results_b)
    time_plot(plot_points, 10, name)

def plotting_task():
    """All purpose plotting task for miscellaneous plotting functions uncomment desired line to plot
    """
    from scripts.generate_data import propogate_kep_rk4
    kep_vectors, rk4_mono_vectors, rk4_j2_vectors = propogate_kep_rk4('./data/jason2.json', 10, 8640)
    # compare_orbit_eci(kep_vectors, rk4_mono_vectors)
    # plot_ground_tracks_vs_vis(rk4_j2_vectors, gs, 'rk4_j2_ideal_super')
    # ground_tracks_3([kep_vectors, rk4_mono_vectors, rk4_j2_vectors])

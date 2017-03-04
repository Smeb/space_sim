def grid_search_lats(results):
    """Performs a grid search using the input results
    Inputs:
        results: Any Results instance, but ideally the Results generated using the most comprehensive model
    Outputs:
        This is a script, so it has no output but hooks into application functionality
    """
    from optimisation_tools.grid_search import grid_search
    from plotters.plotter2d import plot_gs_vis_2d
    from numpy import pi
    search = grid_search(pi / 20, results)
    plottable_results = [(gs, len(visibility)) for gs, visibility in search]
    plot_gs_vis_2d(plottable_results, 'latitude_based_gs')

def grid_search_task(results):
    """Finds four candidate ground stations based on a grid search and returns the
    results
    Inputs:
        results: Any Results instance, but ideally the Results generated using the most comprehensive model
    Outputs:
        plottable_results - an annotated list of [(GroundStation, [ECEF], color)] tuples
    """
    from numpy import pi
    from plotters.earth_plotter import plot_gs_vis
    from optimisation_tools.grid_search import grid_search_long
    search_results = grid_search_long(pi / 20, results)
    plottable_results = [(gs, len(visibility), color) for gs, visibility, color in search_results]
    plot_gs_vis(plottable_results, 'ideal_gs')
    return plottable_results

def find_candidate_gs(results):
    """Finds four candidate ground stations based on a grid search, computes pass
    data, and then creates visualisations using a stereo projection
    Inputs:
        results: Any Results instance, but ideally the Results generated using the most comprehensive model
    Outputs:
        This is a script, so it has no output but hooks into application functionality
    """
    candidates = [ground_station for ground_station, _, c in grid_search_task(results) if c='g']

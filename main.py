"""Program entry point - import a script from scripts to run a specific task
"""
from scripts.generate_data import propogate_kep_rk4
from models.ground_station import GroundStation
from scripts.data_processing import compute_passes
from basis_converters.from_radians import degrees
from basis_converters.from_degrees import radians
from plotters.earth_plotter import plot_polar

from validation_tools.orbit_comparison import orbit_difference_topo
from plotters.time_plotter import time_plot

from plotters.time_plotter import time_series_plot
kep_vectors, rk4_mono_vectors, rk4_j2_vectors = propogate_kep_rk4('./data/jason2.json', 10, 8640)
from basis_converters.from_topo import lat_long_to_ecef
ground_stations = [GroundStation(lat_long_to_ecef([radians(52.45), radians(0.81)]), 'England'),
 GroundStation(lat_long_to_ecef([radians(52.56), radians(117.00)]), 'Russia'),
 GroundStation(lat_long_to_ecef([radians(-64.86), radians(-63.41)]), 'Antartica'),
 GroundStation(lat_long_to_ecef([radians(-45.0), radians(171.0)]), 'New Zealand')]

for gs in ground_stations:
    differences = orbit_difference_topo(kep_vectors.ecef_r, rk4_mono_vectors.ecef_r, gs)
    time_plot(differences, 10, "{}_{}_enu".format(kep_vectors.pname, rk4_mono_vectors.pname))

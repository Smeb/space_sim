"""Contains various global definitions that should be immediately visible to
anyone not familiar with the codebase, and so which are stored in the root folder"""

import os

mu = 398600.4415

r_equatorial = 6378
r_polar = 6356
r_earth = (r_equatorial + r_polar) / 2

root_path = os.path.abspath(os.getcwd())
pickle_path = root_path + '/data/pickle'

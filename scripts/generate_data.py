from models.simulator import Simulator
from models.spacecraft_state import SpacecraftState
from propogators.kepler import propogate_kepler
from propogators.rk4_monopole import propogate_rk4 as monopole_rk4
from propogators.rk4_monopole_j2 import propogate_rk4 as j2_rk4

def propogate_kep_rk4(fname, delta, n_iterations):
    """Loads the file specified at fname into a SpacecraftState instance, and then
    propogates for time difference delta and the specified n_iterations for the
    propogate_kepler, rk4_monopole, and j2_rk4 algorithms

    Input:
        fname - the file on disk to load
        delta - the time delta with which to propogate
        n_iterations - the number of steps to propogate forwards by
    Output:
        (Results, Results, Results) - where Results is a result of one of the algorithms
    """
    import pickle
    import os
    from utils.save_load import save, load

    with open(fname) as f:
      spacecraft = SpacecraftState.fromData(f)

    kep_sim = Simulator(spacecraft.copy(), propogate_kepler, 'kep')
    rk4_sim = Simulator(spacecraft.copy(), monopole_rk4, 'kep2')
    rk4_j2_sim = Simulator(spacecraft.copy(), j2_rk4, 'rk4j2')

    kep_vectors = kep_sim.propogate_in_period(n_iterations, delta)
    rk4_vectors = rk4_sim.propogate_in_period(n_iterations, delta)
    rk4_j2_vectors = rk4_j2_sim.propogate_in_period(n_iterations, delta)

    return kep_vectors, rk4_vectors, rk4_j2_vectors

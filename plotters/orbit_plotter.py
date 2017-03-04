import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from numpy import matrix

def compare_3_orbits_2d(orbita, orbitb, orbitc):
    from basis_converters.rotation import rotate_x
    from basis_converters.from_eci import eci_to_kep
    fig, axes = plt.subplots(1,3, sharey=True)
    plt.style.use('seaborn-dark')

    R, V = orbita.eci[0]
    _, _, incl, _, _, _ = eci_to_kep(R, V)
    axes[0].set_ylabel('y (km)')
    for orbit, axis, c in zip([orbita, orbitb, orbitc], axes, ['r', 'g', 'b']):#
        axis.set_xlabel('x (km)')


        xs, ys, _ = zip(*[rotate_x(-incl, point) for point in orbit.eci_r])
        axis.plot(xs, ys, label=orbit.pname, color=c)
        axis.set_xlim([-8000, 8000])
        axis.set_ylim([-8000, 8000])
        axis.set_title(orbit.pname)

    plt.show()

def compare_orbit_eci_3d(results):
    from mpl_toolkits.mplot3d import Axes3D
    from basis_converters.from_eci import eci_to_kep
    fig = plt.figure()

    ax = fig.gca(projection='3d')
    plt.style.use('seaborn-dark')

    ax.set_xlabel('x (km)')
    ax.set_ylabel('y (km)')
    ax.set_zlabel('z (km)')

    xs, ys, zs = zip(*results.eci_r)
    plt.plot(xs, ys, zs, label=results.pname)
    plt.legend()

    plt.show()

def compare_orbit_eci(orbita, orbitb):
    import numpy as np
    from basis_converters.from_eci import eci_to_kep
    from basis_converters.rotation import rotate_x
    import matplotlib.cm as mplcm
    import matplotlib.colors as colors
    R, V = orbita.eci[0]
    _, _, incl, _, _, _ = eci_to_kep(R, V)

    fig = plt.figure()
    ax = fig.gca()
    plt.style.use('seaborn-dark')

    ax.set_xlabel('x (km)')
    ax.set_ylabel('y (km)')

    rotated_orbita = [rotate_x(-incl, point) for point in orbita.eci_r]
    rotated_orbitb = [rotate_x(-incl, point) for point in orbitb.eci_r]
    for orbit, name in [(rotated_orbita, orbita.pname), (rotated_orbitb, orbitb.pname)]:
        xs, ys, _ = zip(*orbit)
        plt.scatter(xs, ys, marker=None, label=name)
    plt.legend()
    plt.show()

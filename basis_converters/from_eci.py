def eci_to_ecef_r(R, date):
    """
    Inputs:
        R - vector of position (km)
        date - timedate

    Outputs:
        x - km
        y - km
        z - km
    """
    from numpy import array, cos, dot, sin
    from basis_converters.rotation import rotate_z

    theta_g = 4.8949608921 + 6.3003880989677574 * calc_d(date)
    return rotate_z(theta_g, R)

def calc_d(date):
    """
    Calculates the difference in days between a given date and 1st January 12:00, 2000,
    Input:
        data - a datetime object
    Output:
        time_difference - float
    """
    from datetime import datetime

    base_time = datetime(2000, 1, 1, 12)
    diff = date - base_time
    return diff.total_seconds() / (86400)

def eci_to_hcl_basis(eci):
    """
    Computes hcl basis vectors for a spacecraft from a given eci position

    Input
    eci - A tuple of R, V vectors

    Output
    h, c, l - basis vectors in the height, cross-track, and along-track
    directions
    """
    from numpy import cross
    from numpy.linalg import norm
    R, V = eci
    h = R / norm(R)
    c = cross(R, V) / norm(cross(R, V))
    l = cross(h, c)
    return h, c, l

def eci_to_kep(position, velocity):
    """
    Input:
            position - [x, y, z] (km)
            velocity - [u, v, w] (km/s)
    Output:
        kep - a set of Keplerian elements
            semi-major-axis (km),
            eccentricity (should be in the range (0, 1)),
            inclination (radians),
            argument of periapsis (radians),
            Right Ascension of Ascending Node (radians),
            True Anomaly (radians)
    """
    from numpy import arccos, cross, dot, inner, pi
    from numpy.linalg import norm
    from config import mu
    # The acceptable error bound
    eps = 1.e-10

    r = norm(position)
    v = norm(velocity)
    vr = inner(position, velocity) / r

    H = cross(position, velocity)
    h = norm(H)

    incl = arccos(H[2] / h)

    N = cross([0, 0, 1], H)
    n = norm(N)

    if n != 0:
        RA = arccos(N[0] / n)
        if N[1] < 0:
            RA = 2 * pi - RA
    else:
        RA = 0

    E = calc_eccentricity_vec(position, velocity, v, r, vr)
    e = norm(E)

    if n != 0:
        if e > eps:
            w = arccos(dot(N, E) / n / e)
            if E[2] < 0:
                w = 2 * pi - w
        else:
            w = 0
    else:
        w = 0


    if e > eps:
        TA = arccos(dot(E, position) / e / r)
        if vr < 0:
            TA = 2 * pi - TA
    else:
        cp = cross(N, position)
        if cp[2] >= 0:
            TA = arccos(dot(N, position) / n / r)
        else:
            TA = 2 * pi - arccos(dot(N, position) / n / r)

    a = h**2 / mu / (1 - e**2)
    return a, e, incl, w, RA, TA

def calc_eccentricity_vec(position, velocity, v, r, vr):
    from config import mu
    p1 = 1 / mu
    p2 = (v**2 - mu / r) * position
    p3 = r * vr * velocity
    p4 = p2 - p3
    return p1 * p4

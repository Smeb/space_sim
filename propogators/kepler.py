def propogate_kepler(R, V, delta):
    """Calculates Rdt, Vdt vectors of a satellite delta seconds from a given
    initial state R, V does so for a single time step

    Input:
    R - an array of x, y, z in the ECI basis in Km
    V - an array of u, v, w in the ECI basis in Km/s
    delta - the time from zero (computed by the calling function) in s

    Output:
        Rdt - The propogation of R stepped forwards delta seconds in Km
        Vdt - The propogation of V stepped forwards delta seconds in Km/s
    """
    from numpy import arctan2, cos, pi, sin
    from numpy.linalg import norm
    from basis_converters.from_eci import eci_to_kep
    from config import mu
    kep = eci_to_kep(R, V)
    a, e, _, _, _, RA = kep
    r = norm(R)

    n = (mu / a**3)**0.5
    cosE0 = r * cos(RA) / a + e
    sinE0 = r * sin(RA) / (a * (1 - e**2)**0.5)

    # calculates eccentric anomaly E0 in the range 0, 2pi, normalising it if less than 0
    E0 = arctan2(sinE0, cosE0)
    E0 = E0 if E0 >  0 else E0 + 2*pi
    M0 = E0 - e * sin(E0)
    Mi = M0 + n * delta
    Ei = solve_kepler(e, Mi)

    Rdt = update_position(Ei, kep)
    Vdt = update_velocity(Ei, kep)
    return Rdt, Vdt

def update_position(Ei, kep):
    """Calculates Rdt based on Ei and a set of Keplerian elements
    Input:
        Ei - Eccentricity at i
        kep - a set of Keplerian elements
            (semi-major-axis (km),
            eccentricity (should be in the range (0, 1)),
            inclination (radians),
            argument of periapsis (radians),
            Right Ascension of Ascending Node (radians),
            True Anomaly (radians) )
    Output:
        Rdt - the values of vector R for the time step delta (based on Ei) in Km
    """
    from numpy import cos, dot, sin
    from basis_converters.from_kep import gaussian_vectors
    a, e, incl, w, RA, _ = kep
    x = a * (cos(Ei) - e)
    y = a * (1 - e**2)**0.5 * sin(Ei)

    P, Q = gaussian_vectors(incl, w, RA)
    return dot(x, P) + dot(y, Q)


def update_velocity(Ei, kep):
    """Calculates Vdt based on Ei and a set of Keplerian elements
    Input:
        Ei - Eccentricity at i
        kep - a set of Keplerian elements
            (semi-major-axis (km),
            eccentricity (should be in the range (0, 1)),
            inclination (radians),
            argument of periapsis (radians),
            Right Ascension of Ascending Node (radians),
            True Anomaly (radians) )
    Output:
        Vdt - the values of vector V for the time step delta (based on Ei) in Km/s
    """
    from numpy import cos, dot, sin
    from basis_converters.from_kep import gaussian_vectors
    from config import mu
    a, e, incl, w, RA, _ = kep
    r = a * (1- e * cos(Ei))
    x_dot = - (a * mu)**0.5 * sin(Ei) / r
    y_dot = (a * mu)**0.5 * (1 - e**2)**0.5 * cos(Ei) / r

    P, Q = gaussian_vectors(incl, w, RA)
    return dot(x_dot, P) + dot(y_dot, Q)

def kepler(E, Mi, e):
    """Solves the Keplerian equation rearranged to equal zero
    Input:
        E - the Eccentric Anomaly (radians)
        Mi - the Mean Anomaly (radians) at the next time step
        e - the eccentricity (should be in the range (0, 1))
    """
    from numpy import sin
    return E - e*sin(E) - Mi

def solve_kepler(e, Mi):
    """Solves the Keplerian equation rearranged to equal zero
    Input:
        Mi - the Mean Anomaly (radians) at the next time step
        e - the eccentricity (should be in the range (0, 1))
    Output:
        E - the Eccentric anomaly (radians) at the next time step
    """
    from numpy import cos, pi, sin
    E = pi if e > 0.8 else Mi
    while abs(kepler(E, Mi, e)) > 1e-10:
        E = E - (E - e*sin(E) - Mi) / (1 - e*cos(E))
    return E

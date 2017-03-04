def kep_to_eci(kepler):
    """
    Input:
        kepler - a set of Keplerian elements
            (semi-major-axis (km),
            eccentricity (should be in the range (0, 1)),
            inclination (radians),
            argument of periapsis (radians),
            Right Ascension of Ascending Node (radians),
            True Anomaly (radians) )
    Output:
        eci - [R, V] position and velocity (km, km/s)
    """
    from numpy import add, cos, multiply, sin
    a, e, incl, w, RA, TA = tuple(kepler)

    P, Q = gaussian_vectors(incl, w, RA)

    p = a * (1 - e**2)
    r = p / (1 + e * cos(TA))

    x = r * cos(TA)
    y = r * sin(TA)

    cartesian_position = add(multiply(x, P), multiply(y, Q))

    cosE = x / a + e
    sinE = y / (a * (1 - e**2)**0.5)

    f = (a * mu)**0.5 / r
    g = (1 - e**2)**0.5

    cartesian_velocity = add(multiply(-f * sinE, P), multiply(f * g * cosE, Q))
    return cartesian_position, cartesian_velocity

def gaussian_vectors(incl, w, RA):
    from numpy import cos, sin
    P = [
    cos(RA) * cos(w) - sin(RA) * cos(incl) * sin(w),
    sin(RA) * cos(w) + cos(RA) * cos(incl) * sin(w),
    sin(incl) * sin(w)
    ]

    Q = [
    -cos(RA) * sin(w) - sin(RA) * cos(incl) * cos(w),
    cos(RA) * cos(incl) * cos(w) - sin(RA) * sin(w),
    sin(incl) * cos(w)
    ]

    return P, Q

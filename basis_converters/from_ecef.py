def ecef_to_lat_long_h(ecef):
    """
    Inputs:
        ECEF - vector of position (km)

    Outputs:
        latitude - radians
        longitude - radians
        h - km
    """
    from numpy import arctan, arctan2, dot
    from numpy.linalg import norm
    from config import r_earth

    x, y, z = ecef

    longitude = arctan2(y, x)
    latitude = arctan(z / norm([x, y]))
    h = norm(ecef) - r_earth

    return latitude, longitude, h

def project_ecef_enu(ecef, enu):
    """Projects an ECEF vector onto a given enu basis
    """
    from numpy import dot
    e, n, u = enu
    x_e = dot(ecef, e)
    x_n = dot(ecef, n)
    x_u = dot(ecef, u)
    return x_e, x_n, x_u

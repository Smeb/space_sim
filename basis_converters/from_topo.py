def lat_long_to_enu(lat, long, ecef):
  """Returns the unit vectors in  East, North and Up directions
  for the topocentric basis centred on latitude, longitude
  Input:
    lat - radians
    long - radians
    ecef - [x, y, z] (km)
  """
  from numpy import array, cos, sin

  e = array([-sin(long), cos(long), 0])
  n = array([-cos(long) * sin(lat), -sin(long) * sin(lat), cos(lat)])
  u = array([ cos(long) * cos(lat),  sin(long) * cos(lat), sin(lat)])

  return e, n, u

def lat_long_to_ecef(latitude_longitude):
    """Returns the ecef position vector for the given longitude and
    latitude (assumes a height of zero)

    Input:
        latitude_longitude - (latitude, longitude) (radians)
    Output:
        ecef - [x, y, z] (km)
    """
    from config import r_earth
    from numpy import array, cos, pi, sin, arctan2, arctan
    from numpy.linalg import norm
    latitude, longitude, *_ = latitude_longitude

    x = r_earth * cos(latitude) * cos(longitude)
    y = r_earth * cos(latitude) * sin(longitude)
    z = r_earth * sin(latitude)

    return array([x, y, z])

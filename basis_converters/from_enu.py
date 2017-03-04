def enu_to_ecef(latitude, longitude):
    """
    Inputs:
        latitude - radians
        longitude - radians

    Outputs:
        x - km
        y - km
        z - km
    """
    from numpy import array, cos, sin
    from numpy.linalg import norm
    x = array[-sin(lat), -cos(lat) * sin(long), cos(lat) * cos(long)]
    y = array[ cos(lat), -sin(lat) * sin(long), sin(lat) * cos(long)]
    z = array[      0,           cos(long), sin(long)]

    return x, y, z

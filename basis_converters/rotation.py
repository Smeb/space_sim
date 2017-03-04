def rotate_x(angle, vector):
    from numpy import array, cos, dot, sin
    R3_x = array([
      [1,          0,           0],
      [0,  cos(angle), sin(angle)],
      [0, -sin(angle), cos(angle)]
    ])
    return dot(R3_x, vector)


def rotate_z(angle, vector):
    from numpy import array, cos, dot, sin
    R3_z = array([
      [ cos(angle), sin(angle),  0],
      [-sin(angle),  cos(angle), 0],
      [            0,             0, 1]
    ])
    return dot(R3_z, vector)

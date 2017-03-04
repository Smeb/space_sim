GM = 398600.4418
a = 6378.1363
c_2_0 = ((1/5)**0.5)**-1 * -0.0004841653711736

def propogate_rk4(R, V, h):
    """Propgates forwards one step using the rk4 monopole gravity model
    Input:
        R - a vector of eci elements in Km
        V - a vector of eci elements in Km/s
        h - the time step (s)
    Output:
        Rdt - R propogated forwards by h
        Vdt - V propogated forwards by h
    """
    from numpy import array
    from numpy.linalg import norm
    r = norm(R)
    x0, y0, z0 = R

    k1_x = k_xy(h, x0, r, z0)
    k1_y = k_xy(h, y0, r, z0)
    k1_z = k_z(h, z0, r)

    # Calculates the RK2 terms
    xyz_2 = [f(p, v, h, k) for p, v, k in zip(R, V, [k1_x, k1_y, k1_z])]
    rk2 = norm(xyz_2)

    x_2, y_2, z_2 = xyz_2

    k2_x = k_xy(h, x_2, rk2, z_2)
    k2_y = k_xy(h, y_2, rk2, z_2)
    k2_z = k_z(h, z_2, rk2)

    # Calculates the RK3 terms
    x_3, y_3, z_3 = [f(p, v, h, k) for p, v, k in zip(R, V, [k2_x, k2_y, k2_z])]
    rk3 = rk2

    k3_x = k_xy(h, x_3, rk3, z_3)
    k3_y = k_xy(h, y_3, rk3, z_3)
    k3_z = k_z(h, z_3, rk3)

    # Calculates the RK4 terms
    xyz_4 = [f1(p, v, h, k) for p, v, k in zip(R, V, [k3_x, k3_y, k3_z])]
    rk4 = norm(xyz_4)

    x_4, y_4, z_4 = xyz_4

    k4_x = k_xy(h, x_4, rk4, z_4)
    k4_y = k_xy(h, y_4, rk4, z_4)
    k4_z = k_z(h, z_4, rk4)

    k1_xyz = [k1_x, k1_y, k1_z]
    k2_xyz = [k2_x, k2_y, k2_z]
    k3_xyz = [k3_x, k3_y, k3_z]
    k4_xyz = [k4_x, k4_y, k4_z]

    # Calculates the updated position using the k1_xyz, k2_xyz, k3_xyz, 4k_xyz elements
    P = [1/3 * (k1 + k2 + k3) for k1, k2, k3 in zip(k1_xyz, k2_xyz, k3_xyz)]
    Q = [1/3 * (k1 + 2 * k2 + 2 * k3 + k4) for k1, k2, k3, k4 in zip(k1_xyz, k2_xyz, k3_xyz, k4_xyz)]
    R1 = [f1(r0, h, v0, pk) for r0, v0, pk in zip(R, V, P)]
    V1 = [v0 + vk / h for v0, vk in zip(V, Q)]
    return array(R1), array(V1)

def k_xy(h, p, r, z):
    """calculates k_x or k_y including the J2 perturbation for x and y only
    Globals:
        c_2_0 - the denormalised c_2_0 coefficient
        GM - the standard gravitational parameter (km^3 / s^2)
    Input:
        p - a position parameter, x, y, z (km)
        v - a velocityparameter, u, v, w (km/s)
        h - the time step (s)
        k - the previous k term (km)
    Output:
        k_x/k_y - (km)
    """
    return (1/2 * h**2 * (
        ((-GM * p) / r**3) +
        ((3/2 * GM * a**2) / r**5) * c_2_0 * p * (1 - 5 * z**2 / r**2)))

def k_z(h, p, r):
    """k_z calculation including the J2 perturbation for z only
    Globals:
        c_2_0 - the denormalised c_2_0 coefficient
        GM - the standard gravitational parameter (km^3 / s^2)
    Input:
        p - a position parameter, x, y, z (km)
        v - a velocityparameter, u, v, w (km/s)
        h - the time step (s)
        k - the previous k term (km)
    Output:
        k_z - (km)
    """
    return (1/2 * h**2 * (((-GM * p) / r**3) +
        3/2 * GM * a**2 / r**5 * c_2_0 * p * (3 - 5 * p**2 / r**2)))

def f(p, v, h, k):
    """Calculates the RK2 and RK3 terms
    Input:
        p - a position parameter, x, y, z (km)
        v - a velocityparameter, u, v, w (km/s)
        h - the time step (s)
        k - the previous k term (km)
    Output:
        k2/k3 - (km)
    """
    return p + h/2 * v + k / 4

def f1(p, v, h, k):
    """Calculates the RK4 terms
    Input:
        p - a position parameter, x, y, z (km)
        v - a velocityparameter, u, v, w (km/s)
        h - the time step (s)
        k - the previous k term (km)
    Output:
        k4 - (km)
    """
    return p + h * v + k

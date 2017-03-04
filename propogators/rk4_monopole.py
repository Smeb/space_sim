from config import mu

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
    k1_xyz = [k(h, p, r) for p in R]

    # Calculates the RK2 terms
    xyz_2 = [f(p, v, h, k) for p, v, k in zip(R, V, k1_xyz)]
    rk2 = norm(xyz_2)
    k2_xyz = [k(h, p, rk2) for p in xyz_2]

    # Calculates the RK3 terms
    xyz_3 = xyz_2
    rk3 = rk2
    k3_xyz = [k(h, p, rk3) for p in xyz_3]

    # Calculates the RK4 terms
    xyz_4 = [f1(p, v, h, k) for p, v, k in zip(R, V, k3_xyz)]
    rk4 = norm(xyz_4)
    k4_xyz = [k(h, p, rk4) for p in xyz_4]

    P = [1/3 * (k1 + k2 + k3) for k1, k2, k3 in zip(k1_xyz, k2_xyz, k3_xyz)]
    Q = [1/3 * (k1 + 2 * k2 + 2 * k3 + k4) for k1, k2, k3, k4 in zip(k1_xyz, k2_xyz, k3_xyz, k4_xyz)]
    R1 = [r0 + h * v0 + pk for r0, v0, pk in zip(R, V, P)]
    V1 = [v0 + vk / h for v0, vk in zip(V, Q)]
    return array(R1), array(V1)

def k(h, p, r):
    """The k function for a monopole gravity model
    Input:
        h - the time step (s)
        p - a parameter from a list comprehension (Km)
        r - the normal (km)
    Output:
    """
    return 1/2 * h**2 * (-mu * p / r**3)

def f(p, v, h, k):
  return p + 1/2 * h * v + k / 4

def f1(p, v, h, k):
  return p + h * v + k

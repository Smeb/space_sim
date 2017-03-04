"""
Module which implements comparison between different orbital trajectories
"""

def orbit_differences(seriesA, seriesB):
  """
  Returns a list composed from two input lists where each element at
  index i is the difference of the elements at i for seriesA, and
  seriesB

  Input
  seriesA - input list of values
  seriesB - input list of values

  Output
  List of element differences of seriesA - seriesB
  """
  return [a - b for a, b in zip(seriesA, seriesB)]

def orbit_differences_rv(seriesA, seriesB):
  """
  Decorator function which takes two lists of tuples of (R, V) and
  extracts the R values into separate lists to be passed to
  orbit_differences

  Input
  seriesA - input list of (R, V) vectors
  seriesB - input list of (R, V) vectors

  Output
  List of element differences of seriesA - seriesB for the R vectors
  only
  """
  return orbit_differences(extract_r(seriesA), extract_r(seriesB))


def orbit_difference_hcl(orbita, orbitb):
  """
  Calculates orbit differences in the hcl basis between two orbits,
  given two orbits in the eci basis. The difference is calculated with
  respect to orbita.

  Inputs:
  orbita - A list of (R, V) tuples describing an orbit in the eci basis
  orbitb - A list of (R, V) tuples describing an orbit in the eci basis

  Outputs:
  x_h - A list of differences in the height direction
  x_c - A list of differences in the cross-track direction
  x_l - A list of differences in the along-track direction

  All output lists are in order (that is if the eci orbits given are a
  time series, then the outputs will be in the same time series)
  """
  from basis_converters.from_eci import eci_to_hcl_basis
  from numpy import dot
  x_h = []
  x_c = []
  x_l = []
  for base, difference in zip(orbita.eci, orbit_differences_rv(orbita.eci, orbitb.eci)):
    h, c, l = eci_to_hcl_basis(base)
    x_h.append(dot(difference, h))
    x_c.append(dot(difference, c))
    x_l.append(dot(difference, l))
  return (x_h, x_c, x_l)



def orbit_difference_topo(orbita, orbitb, gs):
  """
  Calculates orbit differences in terms of an observer in the
  topocentric basis

  Inputs:
  orbita - A list of R vectors describing an orbit in the ecef basis
  orbitb - A list of R vectors describing an orbit in the ecef basis
  gs - A GroundStation object from which enu vectors can be obtained
  """
  from numpy import dot
  e, n, u = gs.enu
  x_e = [dot(x, e) for x in orbit_differences(orbita, orbitb)]
  x_n = [dot(x, n) for x in orbit_differences(orbita, orbitb)]
  x_u = [dot(x, u) for x in orbit_differences(orbita, orbitb)]
  return (x_e, x_n, x_u)

def extract_r(eci):
  return [r for r, _ in eci]

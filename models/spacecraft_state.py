import json
import pprint
import numpy
import datetime


class SpacecraftState:
  @classmethod
  def fromData(cls, file):
    state = json.load(file)
    return cls(state['name'], state['cart'], state['t'])

  def __init__(self, name, cart, t):
    self._name = name
    self._position = numpy.array(cart[0])
    self._velocity = numpy.array(cart[1])
    if isinstance(t, str):
      self._t = datetime.datetime.strptime(t, '%d/%m/%Y, %H:%M:%S.184000')
    else:
      self._t = t

  def copy(self):
    return SpacecraftState(self._name, [self._position, self._velocity], self._t)

  @property
  def position(self):
    return self._position

  @property
  def velocity(self):
    return self._velocity

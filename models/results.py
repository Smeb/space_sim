class Results:
    """Encapsulates a set of results, provided access methods for transforming
    data safely"""
    def __init__(self, vectors, delta, epoch, pname):
        self._vectors = vectors
        self._delta = delta
        self._epoch = epoch
        self._pname = pname

    @property
    def pname(self):
        return self._pname

    @property
    def epoch(self):
        return self._epoch


    @property
    def eci(self):
        return self._vectors

    @property
    def eci_r(self):
        return [r for r, _ in self.eci]

    @property
    def ecef_r(self):
        """Returns a copy of the primary data list, mapped to the ecef bases (km)"""
        from datetime import datetime, timedelta
        from basis_converters.from_eci import eci_to_ecef_r
        times = [self._epoch + timedelta(0, self._delta * i) for i in range(len(self.eci_r))]
        return [eci_to_ecef_r(vector, time) for vector, time in zip(self.eci_r, times)]

    @property
    def delta(self):
        return self._delta

    @property
    def lat_long_h(self):
        """Returns a copy of the primary data list, mapped to latitudes and longitudes (radians)"""
        from basis_converters.from_ecef import ecef_to_lat_long_h
        return list(map(ecef_to_lat_long_h, self.ecef_r))

    def __str__(self):
        """Important for saving and loading functionality, uses md5"""
        import hashlib
        print(str(self._pname) +
        str(len(self._vectors) - 1) +
        str(self._delta) +
        str(self._vectors[0][0]) +
        str(self._vectors[0][1]))
        key = (
            str(self._pname) +
            str(len(self._vectors) - 1) +
            str(self._delta) +
            str(self._vectors[0][0]) +
            str(self._vectors[0][1]))
        return hashlib.md5(key.encode()).hexdigest()

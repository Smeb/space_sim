class GroundStation():
    """Encapsulates a ground station, provided access methods as well as a visibility
    function for parsing ECEF entries to check for visibility"""
    def __init__(self, ecef, name):
        from numpy import array
        from basis_converters.from_ecef import ecef_to_lat_long_h
        from basis_converters.from_topo import lat_long_to_enu

        self._name = name
        self._ecef = array(ecef)
        self._latitude, self._longitude, _ = ecef_to_lat_long_h(self._ecef)
        self._position = ecef
        self._e, self._n, self._u = lat_long_to_enu(self._latitude, self._longitude, ecef)

    @property
    def name(self):
          return self._name

    @property
    def position(self):
        return self._position

    @property
    def enu(self):
        return self._e, self._n, self._u

    @property
    def lat_long(self):
        return self._latitude, self._longitude

    def angle_and_azimuth(self, satellite_ecef):
        """Calculates the angle and azimuth of the satellite from the
        ground station
        Input:
            satellite_ecef - position vector in ecef (km)
        Output:
            angle - radians
            azimuth - radians
        """
        from numpy import arcsin, arctan2, dot
        from numpy.linalg import norm

        r_ss = satellite_ecef - self.position
        r_ss_norm = r_ss / norm(r_ss)

        r_sse = dot(r_ss_norm, self._e)
        r_ssn = dot(r_ss_norm, self._n)
        r_ssu = dot(r_ss_norm, self._u)

        angle = arcsin(r_ssu)
        azimuth = arctan2(r_sse, r_ssn)
        return angle, azimuth


    def pass_times(self, results):
        """Calculates pass times, as well as azimuth and elevation for the given pass times from a given
        set of orbital results

        Input:
            results - an instance of results

        Output:
            passes - a list of tuples with the following structure: ((pass_begin), (pass_end))
            pass_start - a tuple (time, elevation, azimuth) recording the start of the pass
            pass_end - a tuple (time, elevation, azimuth) recording the end of the pass
        """
        from datetime import datetime, timedelta
        ecef_data = results.ecef_r
        passes = []
        start = 0
        end = 0
        run = False
        for index, point in enumerate(ecef_data):
            if self.visible(point) and run is False:
                start = results.epoch + timedelta(0, results.delta * index)
                start_elevation, start_azimuth = self.angle_and_azimuth(point)
                run = True
            if self.visible(point) is not True and run is True:
                end = results.epoch + timedelta(0, results.delta * index)
                end_elevation, end_azimuth = self.angle_and_azimuth(point)
                passes.append(((start, start_elevation, start_azimuth), (end, end_elevation, end_azimuth)))
                run = False
        return(passes)

    def divide_passes(self, results):
        ecef_data = results.ecef_r
        passes = []
        run = False
        for index, point in enumerate(ecef_data):
            if self.visible(point) and run is False:
                cur_list = [point]
                run = True
            if self.visible(point) and run is True:
                cur_list.append(point)
            if self.visible(point) is not True and run is True:
                passes.append(cur_list)
                run = False
        return passes

    def visible(self, satellite_ecef):
        """Checks if an ecef position is visible
        """
        angle, _ = self.angle_and_azimuth(satellite_ecef)
        if angle - 0.0872665 > 0:
            return True
        return False

class Simulator:
    """Wrapper class to run orbital propogator against a given spacecraft for
    a defined step
    """
    def __init__(self, spacecraft, propogator, pname):
        self._spacecraft = spacecraft
        self._pname = pname
        self._propogator = propogator

    def propogate_in_period(self, n, dt):
        """Checks to see if results exist, otherwise propogates the requested
        number of times
        """
        from models.results import Results
        from utils.save_load import save, load
        key = self.save_key(n, dt)
        data = load(['propogate_in_period', key])
        if data is not None:
            return data

        vectors = [(self._spacecraft.position, self._spacecraft.velocity)]
        position = self._spacecraft.position
        velocity = self._spacecraft.velocity
        for i in range(1, n + 1):
            # Generates the base propogation series and freezes the values
            vector = self._propogator(vectors[i - 1][0], vectors[i - 1][1], dt)
            for item in vector:
                item.flags.writeable = False
            vectors.append(vector)
        data = Results(vectors, dt, self._spacecraft._t, self._pname)
        save(['propogate_in_period', key], data)
        return data

    def save_key(self, n, dt):
        import hashlib
        key = (
            str(self._pname) +
            str(n) +
            str(dt) +
            str(self._spacecraft.position) +
            str(self._spacecraft.velocity))
        return hashlib.md5(key.encode()).hexdigest()

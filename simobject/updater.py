import numpy as np


class Updater:
    """
    An update object that updates the field that it is given.

    Parameters
    ----------

    func : callable
        the owner (e.g. simulation) that this Updater is attached to.

    """

    def __init__(self, func=None):
        self.func = func

    def update(self, obj):
        self.func(obj)


class DataUpdater(Updater):
    """
    Special Updater that keeps track of the changing quantities by
    appending them to a numpy array.

    Parameters:
    -----------
    keys : list
        a list of strings, each one is the name of a simulation attribute to store

    string : str, optional, defaults to None
        if it is a string, it will be written out at every snapshot and formatted
        with passing the string object. For example

            string = 'time = {0.time}'

        will access simulation.time.
    """
    keys = []

    def __init__(self, keys, *args, string=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.keys = list(keys)
        self.string = string

    def print(self, sim):
        if self.string is not None:
            print(self.string.format(sim), end='', flush=True)

    def update(self, sim, string=None):
        if string is not None:
            self.string = string

        self.print(sim)

        for key in self.keys:
            if key in sim.data:
                sim.data[key] = np.vstack(
                    (sim.data[key], getattr(sim, key))
                )
            else:
                sim.data[key] = np.array(getattr(sim, key)[None, ...])

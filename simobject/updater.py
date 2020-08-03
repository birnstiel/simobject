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
    Special updater that keeps track of the changing quantities by
    appending them to a numpy array.
    """
    keys = []

    def __init__(self, keys, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keys = list(keys)

    def update(self, sim):
        print('updating data')
        for key in self.keys:
            if key in sim.data:
                sim.data[key] = np.vstack(
                    (sim.data[key], getattr(sim, key))
                )
            else:
                sim.data[key] = np.array(getattr(sim, key)[None, ...])

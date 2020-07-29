class Updater:
    """
    An update object that updates the field that it is given.

    Keywords:
    ---------

    func : callable
        the owner (e.g. simulation) that this Updater is attached to.

    """

    def __init__(self, func=None):
        self.func = func

    def update(self, obj):
        self.func(obj)

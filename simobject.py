import numpy as np


class Updater:
    """
    An update object that updates the field that it is attached to.

    Keywords:
    ---------

    owner : object
        the owner (e.g. simulation) that this Updater is attached to.

    """

    def __init__(self, owner=None, func=None):
        self.func = func
        self.owner = owner

    def update(self):
        self.func(self.owner)


class Quantity(np.ndarray):
    """numpy.ndarray that also stores its owner and a info string.

    The input_array and extra keywords are passed to np.asarray.

    WARNING: it has the same tricky boolean behavior as numpy arrays:

    >>> s = Quantity(True)
    >>> if s is True:
    >>>     print('True')
    >>> else:
    >>>     print('False')
    'False'

    But the other ways work:

    >>> if s == True: print('True')
    True
    >>> if s: print('True')
    True


    Arguments:
    ----------

    input_array : scalar | list | array
        anything accepted by `np.asarray`

    info : str
        will be setting self.info and used in the string representation

    owner : obj
        any object to refer to as owner that could be accessed within methods,
        e.g. a parent simulation object whose values might be needed inside
        update.

    updater : obj
        Updater object

    systoler : obj
        Updater object that will be used in the systole (before all updates)

    diastoler : obj
        Updater object that will be used in the diastole (after all updates)
    """

    def __new__(
        cls,
        input_array,
        info=None,
        owner=None,
        updater=None,
        systoler=None,
        diastoler=None,
        **kwargs,
    ):

        # We first cast to be our class type

        obj = np.asarray(input_array, **kwargs).view(cls)

        # we copy extra-attributes from our input array

        if isinstance(input_array, Quantity):
            obj.info = input_array.info
            obj.owner = input_array.owner

            # here we call the setter in order to link them to self

            obj.updater = input_array._updater
            obj.systoler = input_array._systoler
            obj.diastoler = input_array._diastoler

        # if arguments were passed, those override the values
        # from the input array

        obj.info = info or obj.info
        obj.owner = owner or obj.owner
        obj.updater = updater or obj.updater
        obj.systoler = systoler or obj.systoler
        obj.diastoler = diastoler or obj._diastoler

        # Finally, we return the newly created object:

        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return

        self.info = getattr(obj, "info", None)
        self.owner = getattr(obj, "owner", None)
        self._updater = getattr(obj, "_updater", None)
        self._systoler = getattr(obj, "_systoler", None)
        self._diastoler = getattr(obj, "_diastoler", None)

    def __repr__(self):
        rep = super().__repr__()
        if self.info is not None:
            rep = rep.replace(__class__.__name__, f"{self.info}\n")
        return rep

    def setvalue(self, value):
        "sets this array to the new value, but keeps its info and owner"
        self.setfield(value, self.dtype)

    def update(self):
        "call the Updater to do the update"
        if self._updater is not None:
            self.updater.update()

    def _constructupdater(self, value):
        """create an Updater object from `value` and link to self.

        `value` can be:

        - `None`, then `None` is returned
        - an `Updater`, then it is returned, but its owner is updated
        - a function, then a new Updater is created and returned
        """
        if isinstance(value, Updater):
            value.owner = self
            return value
        elif hasattr(value, "__call__"):
            return Updater(func=value, owner=self)
        elif value is None:
            return None
        else:
            raise TypeError(
                "<value> must be None, a function, or an Updater instance")

    @property
    def updater(self):
        return self._updater

    @property
    def systoler(self):
        return self._systoler

    @property
    def diastoler(self):
        return self._diastoler

    @updater.setter
    def updater(self, value):
        updtr = self._constructupdater(value)
        self._updater = updtr

    @systoler.setter
    def systoler(self, value):
        updtr = self._constructupdater(value)
        self._systoler = updtr

    @diastoler.setter
    def diastoler(self, value):
        updtr = self._constructupdater(value)
        self._diastoler = updtr


class Simulation(object):

    # we want to only store quantities in _data

    __slots__ = ["_quantities", "_systole_order",
                 "_update_order", "_diastole_order"]

    def __init__(self):

        # we call the method from super because we overwrite the own __setattr__

        super().__setattr__("_quantities", {})
        super().__setattr__("_systole_order", [])
        super().__setattr__("_update_order", [])
        super().__setattr__("_diastole_order", [])

    # this is how one gets an attribute

    def __getattr__(self, key):
        return self._quantities[key]

    # this is how to set an 'attribute' that internally we store in _quantities

    def __setattr__(self, key, value):
        if isinstance(value, Quantity):
            self.addQuantity(key, value, info=key)
        else:
            raise TypeError(
                "attributes assigned to simulation must be of type <Quantity>"
            )

    def addQuantity(self, key, value, info=None, updater=None, systoler=None, diastoler=None):
        """
        adds `value` as apparent attribute under the name `key`.

        `value` will be casted to type Quantity and it's owner will be set to
        this simulation.

        - If `info` is None, then `key` is also set as the `info` attribute of the
          Quantity unless that one already had that attribute to begin with, else `key`
          is used instead.

        - if `value` has already updater, systoler, or diastoler, those will be inherited, but their
          owner will be changed.

        - if `updater`, `systoler`, and/or `diastoler` are given, those always override the
          ones that might already be set in `value`.

        """
        q = Quantity(value, owner=self)

        q.info = info or q.info or key

        # this actually calls the setter and getter to make sure
        # the updater is linked correctly

        q.updater = updater or q.updater
        q.systoler = systoler or q.systoler
        q.diastoler = diastoler or q.diastoler

        self._quantities[key] = q

    def getSystoleOrder(self):
        return self._systole_order

    # to make tab completion work

    def __dir__(self):
        return sorted(set(super().__dir__() + list(self._quantities.keys())))

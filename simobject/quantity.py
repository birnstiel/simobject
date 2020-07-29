import numpy as np

from .updater import Updater


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

    constant : bool
        if constant, then the value cannot be changed
    """

    def __new__(
        cls,
        input_array,
        info=None,
        owner=None,
        updater=None,
        systoler=None,
        diastoler=None,
        constant=None,
        **kwargs,
    ):

        # We first cast to be our class type

        obj = np.asarray(input_array, **kwargs).view(cls)

        # we copy extra-attributes from our input array

        if isinstance(input_array, Quantity):
            obj.info = input_array.info
            obj.owner = input_array.owner
            obj._constant = input_array._constant

            # here we call the setter in order to link them to self

            obj.updater = input_array._updater
            obj.systoler = input_array._systoler
            obj.diastoler = input_array._diastoler

        # if arguments were passed, those override the values
        # from the input array

        obj.info = info or obj.info
        obj.owner = owner or obj.owner

        if constant is not None:
            obj._constant = constant

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
        self._constant = getattr(obj, "_constant", False)
        self._updater = getattr(obj, "_updater", None)
        self._systoler = getattr(obj, "_systoler", None)
        self._diastoler = getattr(obj, "_diastoler", None)

    def __repr__(self):
        rep = super().__repr__()
        if self.info is not None:
            rep = ("Constant " if self._constant else "") + \
                rep.replace(__class__.__name__, f"{self.info}\n")
        return rep

    def setvalue(self, value):
        "sets this array to the new value, but keeps its info and owner"
        if self._constant:
            raise TypeError("This Quantity is constant.")
        self.setfield(value, self.dtype)

    def systole(self):
        "call the Systole updater"
        if self._systoler is not None:
            self._systoler.update(self)

    def update(self):
        "call the Updater to do the update"
        if self._updater is not None:
            self.updater.update(self)

    def diastole(self):
        "call the Diastole updater"
        if self._diastoler is not None:
            self._diastoler.update(self)

    def _constructupdater(self, value):
        """create an Updater object from `value`.

        `value` can be:

        - `None`, then `None` is returned
        - an `Updater`, then `value` is just returned
        - a function, then a new Updater is created and returned
        """
        if isinstance(value, Updater):
            return value
        elif hasattr(value, "__call__"):
            return Updater(func=value)
        elif value is None:
            return None
        else:
            raise TypeError(
                "<value> must be None, a function, or an Updater instance")

    @property
    def constant(self):
        return self._constant

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

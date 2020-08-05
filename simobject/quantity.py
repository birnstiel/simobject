from .heartbeat_object import HeartbeatObject

import numpy as np


class Quantity(np.ndarray, HeartbeatObject):
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


    Parameters
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
        copy=False,
        **kwargs,
    ):

        # We first cast to be our class type

        obj = np.array(input_array, copy=copy, **kwargs).view(cls)

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

        self.info = getattr(obj, "info", None)
        self.owner = getattr(obj, "owner", None)
        self._constant = getattr(obj, "_constant", False)
        self._updater = getattr(obj, "_updater", None)
        self._systoler = getattr(obj, "_systoler", None)
        self._diastoler = getattr(obj, "_diastoler", None)

    def __repr__(self):
        rep = super().__repr__()
        if self._constant:
            rep = "Constant " + rep
        if self.info is not None:
            rep = rep.replace(__class__.__name__, f"{self.info}\n")
        return rep

    def setvalue(self, value):
        """sets this array to the new value, but keeps its info and owner"""
        if self._constant:
            raise TypeError("This Quantity is constant.")
        self.setfield(value, self.dtype)

    @property
    def constant(self):
        return self._constant

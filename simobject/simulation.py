from collections import OrderedDict

from .quantity import Quantity
from .heartbeat_object import HeartbeatObject


class Simulation(HeartbeatObject):
    """Simulation object with updatable quantities

    This object ...
    - ... stores `Quantities` in _quantities that can be set with `addQuantity`
    - ... keeps track of the update order in systole, update, diastole
    - ... has itself a systole, and a diastole that can be set
    - ... overrides `update` which in this case calls all `systole`, `update`, and `diastoles`
    - ... provides a `data` dictionary to store other data (parameters, ...).

    the lists `systole_order`, `update_order`, and `diastole_order` can be set, but if they are empty
    they return the order in which the Quantities were added.
    """

    __slots__ = ["_quantities", "_systole_order",
                 "_update_order", "_diastole_order", "_data"]

    def __init__(self):

        # we call the method from super because we overwrite the own __setattr__

        super().__setattr__("_quantities", OrderedDict())
        super().__setattr__("_systole_order", [])
        super().__setattr__("_update_order", [])
        super().__setattr__("_diastole_order", [])
        super().__setattr__("_data", {})

    # this is how one gets an attribute

    def __getattribute__(self, key):
        _quantities = super().__getattribute__("_quantities")
        if key in _quantities:
            return _quantities[key]
        else:
            return super().__getattribute__(key)

    # this is how to set an 'attribute' that internally we store in _quantities

    def __setattr__(self, key, value):
        _quantities = super().__getattribute__("_quantities")

        if isinstance(value, Quantity):
            self.addQuantity(key, value, info=value.info or key)
        elif key in _quantities:
            _quantities[key].setvalue(value)
        else:
            super().__setattr__(key, value)

    def addQuantity(self, key, value, info=None, updater=None, systoler=None, diastoler=None, constant=None, copy=True):
        """
        adds `value` as apparent attribute under the name `key`.

        `value` will be casted to type Quantity. If a numpy ndarray is
        passed, a new memory buffer will be created.

        If a quantity is passed,

        - ... a new Quantity object will be created with the same attributes.
        - ... and if `value` has already updater, systoler, or diastoler, those will be inherited
        - ... and if `updater`, `systoler`, and/or `diastoler` are given, those always override the
          ones that might already be set in `value`.
        - ... and `info` is None, then `key` is also set as the `info` attribute of the
          Quantity unless that one already had that attribute to begin with, else `key`
          is used instead.

        Parameters:
        -----------

        copy : bool, optional, defaults to True
            by default a copy of the input value is created. If set to
            False, the same memory (for ndarrays) or object (for Quantities)
            are used.

        """
        if isinstance(value, Quantity) and copy is False:
            q = value
        else:
            q = Quantity(value, owner=self, copy=copy)

        q.info = info or q.info or key

        if constant is not None:
            q._constant = constant

        # this actually calls the setter and getter to make sure
        # the updater is linked correctly

        q.updater = updater or q.updater
        q.systoler = systoler or q.systoler
        q.diastoler = diastoler or q.diastoler

        self._quantities[key] = q

    def update(self):
        """updates everything:

        it calls:
        - the systole of the simulation object itself
        - the systole of all quantities in `self.systole_order`, then
        - the update of all quantities in `self.update_order`, then
        - the diastole of all quantities in `self.diastole_order`, then
        - the diastole of the simulation object itself
        """
        self.systole()

        for key in self.systole_order:
            getattr(self, key).systole()

        for key in self.update_order:
            getattr(self, key).update()

        for key in self.diastole_order:
            getattr(self, key).diastole()

        self.diastole()

    @property
    def update_order(self):
        "the order in which the quantity-updates are called"
        if len(self._update_order) == 0:
            return list(self._quantities.keys())
        else:
            return self._update_order

    @update_order.setter
    def update_order(self, value):
        "value is a list of strings: names of the quantities to update"
        self._check_list(value)
        self._update_order = value

    @property
    def systole_order(self):
        "the order in which the quantity-systoles are called"
        if len(self._systole_order) == 0:
            return list(self._quantities.keys())
        else:
            return self._systole_order

    @systole_order.setter
    def systole_order(self, value):
        "value is a list of strings: names of the quantities to update in the systole"
        self._check_list(value)
        self._systole_order = value

    @property
    def diastole_order(self):
        if len(self._diastole_order) == 0:
            return list(self._quantities.keys())
        else:
            return self._diastole_order

    @diastole_order.setter
    def diastole_order(self, value):
        "value is a list of strings: names of the quantities to update in the diastole"
        self._check_list(value)
        self._diastole_order = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        raise AttributeError(
            'cannot reassign data dictionary, use its methods like pop, update, ... instead')

    @staticmethod
    def _check_list(value):
        "checks if `value` is a list of strings"
        if not isinstance(value, list):
            raise TypeError('input must be  a list')
        for val in value:
            if not isinstance(val, str):
                raise TypeError('not a str: ' + str(val))

    # to make tab completion work

    def __dir__(self):
        return sorted(set(super().__dir__() + list(self._quantities.keys())))

    def __repr__(self):
        s = "Simulation\n\n"

        for key in sorted(self._quantities.keys(), key=str.casefold):

            val = self._quantities[key]

            if key.startswith("_"):
                continue

            if len(key) > 12:
                name = key[:9] + "..."
            else:
                name = key

            if type(val) is Quantity:
                s += "{:11s}{:7s}: {:12s} {}\n".format("    Const. " if val._constant else "",
                                                       "Quantity", name, "(" + val.info + ")" if val.info else "")
            else:
                s += "{:11s}{:7s}: {:12s}\n".format("",
                                                    type(val).__name__, name)

        return s

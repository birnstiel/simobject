from .updater import Updater
from .quantity import Quantity


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

    def addQuantity(self, key, value, info=None, updater=None, systoler=None, diastoler=None, constant=False):
        """
        adds `value` as apparent attribute under the name `key`.

        `value` will be casted to type Quantity and it's owner will be updated to
        this simulation.

        - If `info` is None, then `key` is also set as the `info` attribute of the
          Quantity unless that one already had that attribute to begin with, else `key`
          is used instead.

        - if `value` has already updater, systoler, or diastoler, those will be inherited

        - if `updater`, `systoler`, and/or `diastoler` are given, those always override the
          ones that might already be set in `value`.

        """
        q = Quantity(value, owner=self)

        q.info = info or q.info or key
        q._constant = constant or q._constant

        # this actually calls the setter and getter to make sure
        # the updater is linked correctly

        q.updater = updater or q.updater
        q.systoler = systoler or q.systoler
        q.diastoler = diastoler or q.diastoler

        self._quantities[key] = q

    @property
    def systole_order(self):
        return self._systole_order

    @systole_order.setter
    def systole_order(self, value):
        self._systole_order = value

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

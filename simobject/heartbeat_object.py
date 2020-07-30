from .updater import Updater


class HeartbeatObject(object):
    """Object with systole, update, and diastole

    systoler, updater, and diastoler are properties that can be
    set with a function or an Updater object.

    systole, update, diastole are calling the respective
    updater.
    """
    _systoler = None
    _updater = None
    _diastoler = None

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

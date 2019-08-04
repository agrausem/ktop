from typing import List

import inspect
from functools import partial, wraps
from json import JSONEncoder


class JsonSerializable(JSONEncoder):

    _klasses: List[type] = []

    def __init__(self, kls):
        super().__init__()
        self.__kls = kls
        self._klasses.append(kls)

    def get_json_members(self):
        return inspect.getmembers(
            self.__kls, lambda o: isinstance(o, JsonProperty)
        )

    def scan_properties(self, o):
        for name, property in self.get_json_members():
            value = getattr(o, name)
            if value.__class__ in self._klasses:
                value = value.default()
            elif isinstance(value, (list, tuple)):
                value = [
                    v.default() if v.__class__ in self._klasses else v
                    for v in value
                ]
            yield name, value

    def default(self, o):
        if isinstance(o, self.__kls):
            return dict(self.scan_properties(o))
        return super().default(o)

    def __call__(self, *args, **kwargs):

        @wraps(self.__kls)
        def wrapped(cls):
            cls.__json__ = True
            instance = cls(*args, **kwargs)
            # setattr(inspect, 'default', partial(self.default, instance))
            setattr(instance, 'default', partial(self.default, instance))
            return instance

        return wrapped(self.__kls)


class JsonProperty(property):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


json_property = JsonProperty

from abc import ABC
import inspect


class Base(ABC):
    """Abstract base class for all classes."""

    def _class_name(self) -> str:
        return f'{self.__class__.__name__} Class'

    @classmethod
    def _method_name(cls) -> str:
        return f'{inspect.currentframe().f_back.f_code.co_name} Method'

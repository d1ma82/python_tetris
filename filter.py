from abc import ABC, abstractmethod

class Filter(ABC):

    @abstractmethod
    def frame()->bytes: pass

    @abstractmethod
    def apply()->None: pass
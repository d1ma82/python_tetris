from numpy import ndarray
from abc import ABC, abstractmethod

class Filter(ABC):

    @abstractmethod
    def frame()->ndarray: pass

    @abstractmethod
    def apply()->None: pass
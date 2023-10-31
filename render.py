from abc import ABC, abstractmethod
from filter import Filter

class Render(ABC):

    @abstractmethod
    def attach_filterlist(filter:list[Filter])->None: pass

    @abstractmethod
    def render()->None: pass

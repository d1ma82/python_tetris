import scene as sc
from filter import Filter
from render import Render


class GL_Render(Render):

    def __init__(self, viewport:tuple) -> None:    

        self.__viewport = viewport           
        self.__scene = sc.Scene(self.__viewport, './shader/out.frag', './shader/out.vert')
        self.__filters:list[Filter] = None
        pass
    
    def attach_filterlist(self, filter:list[Filter]): self.__filters = filter

    def render(self):

        for f in self.__filters: f.apply()
        self.__scene.build(self.__filters[0].frame())
        pass
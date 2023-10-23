
class Source:

    def __init__(self, file):

        try:
            self.__afile = open(file)
            self.__isopen = True
        except OSError as err:
            self.__isopen = False
            print("OSError. ", err)
        pass

    def is_opened(self)->bool: return self.__isopen

    def __del__(self):

        if self.__isopen: self.__afile.close()
        pass

    
    
    def read(self): return self.__afile.read()
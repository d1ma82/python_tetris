

class Source:

    def open(self, file):

        try:
            self.__afile = open(file)

        except FileExistsError as err:
            print("File not exists. ", err)
        pass


    
    def __del__(self):

        self.__afile.close()
        pass

    
    
    def read(self):

        return self.__afile.read()
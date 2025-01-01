from abc import ABC, abstractmethod

class ExtensionHandler(ABC):
    
    def __init__(self, *ext_type):
       self.ext_types = ext_type 

    def get_file(self, file_name, extension, *data):
        if extension not in self.ext_types:
            return
        self.process(file_name, extension, *data)
    
    @abstractmethod
    def process(self, file_name, extension, *data):
        pass

import os

class Copier:
    
    def __init__(self):
        self.number_of_copies = 0

        # source
        self.file_path = ""
        self.split_path = []
        self.name = ""
        self.extension = ""
        
        # destination
        self.destination = ""
        self.same_dir = True

        # file number
        self.incr = False
        self.start_num = 0

        # modificators
        self.modify = False
        self.handlers = []

    def copy(self):
        self.copy_files()
        if self.modify:
            self.modify_files()
        self.clear()

    def copy_files(self):
        if self.incr:
            prompt = f'for /l %f in ({self.start_num + 1},1,{self.start_num + self.number_of_copies}) do (copy "{self.file_path}" "{self.destination}\\{self.name}%f.{self.extension}")'
        else:
            prompt = f'for /l %f in ({self.start_num + 1},1,{self.start_num + self.number_of_copies}) do (copy "{self.file_path}" "{self.destination}\\{self.name} (%f).{self.extension}")'
        os.system(prompt)
        
    def modify_files(self):
        for i in range(self.start_num + 1, self.start_num + self.number_of_copies + 1):
            if self.incr:
                dest = f'{self.destination}\\{self.name}{i}.{self.extension}'
            else:
                dest = f'{self.destination}\\{self.name} ({i}).{self.extension}'
            self.modify_file(dest, i)
                
    def modify_file(self, file_dest, *info):
        for handler in self.handlers:
            handler.get_file(file_dest, self.extension, *info)


    def set_data(self, number_of_copies, source, dest, same_dir, incr, modify):
        
        self.number_of_copies = number_of_copies
        self.process_number_of_copies()
            
        self.file_path = source
        self.process_file_path()

        self.same_dir = same_dir
        self.destination = dest
        self.process_dest_path()

        self.incr = incr
        if incr:
            self.process_numeric_name()

        self.modify = modify
        

    def process_number_of_copies(self):
        if self.number_of_copies is None:
            raise ValueError("Enter a number of copies!")
        else:
            try:
                self.number_of_copies = int(self.number_of_copies)
            except ValueError:
                raise ValueError("Enter an integer number!")
            if self.number_of_copies <= 0 or self.number_of_copies > 512:
                raise ValueError("Enter a number from 1 to 512")

    def process_file_path(self):
        if self.file_path == "":
            raise ValueError("File wasn't chosen!")
        else:
            self.split_path = self.file_path.split('/')
            name_with_ext = self.split_path[-1]
            self.name = name_with_ext.split('.')[0]
            self.extension = name_with_ext.split('.')[1]
            self.file_path = self.file_path.replace('/', '\\')

    def process_dest_path(self):
        if self.same_dir:
            self.destination = '\\'.join(self.split_path[:-1])
        else:
            self.destination = self.destination.replace('/', '\\')
            
        if self.destination == "":
            raise ValueError("Destination directory wasn't chosen!\nIf you want to copy to the same directory, mark the checkbox")


    def process_numeric_name(self):
        index = -1
        while abs(index) <= len(self.name):
            if not self.name[index].isnumeric():
                break
            index -= 1
        if index != -1:
            self.start_num = int(self.name[index+1:])
            self.name = self.name[:index+1]

    def add_handler(self, handler):
        self.handlers.append(handler)

    def clear(self):
        self.number_of_copies = 0

        self.file_path = ""
        self.split_path = []
        self.name = ""
        self.extension = ""
        
        self.destination = ""
        self.same_dir = True

        self.incr = False
        self.start_num = 0

        self.modify = False
        #self.handlers = []
        
 

    

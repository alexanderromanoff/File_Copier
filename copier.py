import shutil

class Copier:
    
    def __init__(self):
        self.number_of_copies = 0
        self.file_path = ""
        self.split_path = []
        self.destination = ""
        self.same_dir = True
        self.cur = 0
        self.name = ""
        self.extension = ""
        self.start_num = "0"

        self.handlers = []


    def copy_file(self, modify, progress_callback=None):
        if self.cur < self.number_of_copies:
            i = int(self.start_num) + 1 + self.cur
            dest = f"{self.destination}/{self.name}{str(i).zfill(len(self.start_num))}.{self.extension}"
            self.cur += 1

            shutil.copy2(self.file_path, dest, follow_symlinks=True)
            for handler in self.handlers:
                handler.get_file(dest, self.extension, i)

            if progress_callback:
                progress_callback(self.cur)         
            return True
        self.clear()
        return False

    def set_data(self, number_of_copies, source, dest, same_dir, incr):
        
        self.number_of_copies = number_of_copies
        self.process_number_of_copies()
            
        self.file_path = source
        self.process_file_path()
        if incr:
            self.process_numeric_name()

        self.same_dir = same_dir
        self.destination = dest
        self.process_dest_path()
        

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

    def process_dest_path(self):
        if self.same_dir:
            self.destination = '/'.join(self.split_path[:-1])
        
        elif self.destination == "":
            raise ValueError("Destination directory wasn't chosen!\nIf you want to copy to the same directory, mark the checkbox")


    def process_numeric_name(self):
        index = -1
        while abs(index) <= len(self.name):
            if not self.name[index].isnumeric():
                break
            index -= 1
        if index != -1:
            self.start_num = self.name[index+1:]
            self.name = self.name[:index+1]

    def add_handler(self, handler):
        self.handlers.append(handler)

    def clear(self):
        self.number_of_copies = 0
        self.file_path = ""
        self.split_path = []
        self.destination = ""
        self.same_dir = True
        self.cur = 0
        self.name = ""
        self.extension = ""
        self.start_num = "0"
 

    

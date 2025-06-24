import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showerror, showinfo
import copier as cpr


TITLE_ROW = 0

FILE_CHOICE_ROW = 1
FILE_CHOICE_AUX_ROW = 2

DEST_CHOICE_ROW = 3
DEST_CHOICE_AUX_ROW = 4

NUMBER_ENTRY_ROW = 5

OVERDRIVE_ROW = 6

EXPAND = "EW"
OFFSET = 10


class Application:
    def __init__(self, copier, *files_specifications):

        self.copier = copier
        self.file_specs = [("All files", "*.*")]
        self.file_specs.append(*files_specifications)
        
        self.master = tk.Tk()
        self.master.geometry("570x180")
        self.master.title("Copying Files")
        self.master.resizable(False, False)
                
        self.incr_num = tk.BooleanVar(value=True)
        self.same_dir = tk.BooleanVar(value=True)
        self.use_ext = tk.BooleanVar(value=True)
        
        self.init_master()
        

    def init_master(self):
        # greetings phrase
        infoLabel = tk.Label(text="Select a file for copying")
        infoLabel.grid(row=TITLE_ROW, column=0, padx=OFFSET*3, columnspan=3)

        # file chhosing interface
        fileLabel = tk.Label(text=f"Chosen file: ")
        fileLabel.grid(row=FILE_CHOICE_ROW, column=0, sticky="e")

        self.fileText = tk.Text(height=1,width=15, wrap="none", state="disabled")
        self.fileText.grid(row=FILE_CHOICE_ROW, column=1)

        self.fileSelectorButton = tk.Button(text="Select a file", command=self.open_file)
        self.fileSelectorButton.grid(row=FILE_CHOICE_ROW, column=2, sticky=EXPAND, padx=OFFSET)

        self.increaseNumericNames = tk.Checkbutton(text="Increase number in the name of file", variable=self.incr_num, command=self.process_incr_num)
        self.increaseNumericNames.grid(row=FILE_CHOICE_ROW, column=3, sticky="w")
        self.increaseNumericNames.select()

        self.fileScroller = tk.Scrollbar(orient="horizontal", command=self.fileText.xview)
        self.fileText["xscrollcommand"] = self.fileScroller.set
        self.fileScroller.grid(row=FILE_CHOICE_AUX_ROW,column=1, sticky=EXPAND, padx=OFFSET)

        # destination choosing interface
        destLabel = tk.Label(text="Chosen directory: ")
        destLabel.grid(row=DEST_CHOICE_ROW, column=0, sticky="e")

        self.destText = tk.Text(height=1,width=15, wrap="none", state="disabled")
        self.destText.grid(row=DEST_CHOICE_ROW, column=1)

        self.destSelectorButton = tk.Button(text="Select a directory", command=self.open_directory, state="disabled")
        self.destSelectorButton.grid(row=DEST_CHOICE_ROW, column=2, sticky=EXPAND, padx=OFFSET)

        self.onlyDirCheckBox = tk.Checkbutton(text="Copy to the same directory", variable=self.same_dir, command=self.process_only_dir)
        self.onlyDirCheckBox.grid(row=DEST_CHOICE_ROW, column=3, sticky="w")
        self.onlyDirCheckBox.select()

        self.destScroller = tk.Scrollbar(orient="horizontal", command=self.destText.xview)
        self.destText["xscrollcommand"] = self.destScroller.set
        self.destScroller.grid(row=DEST_CHOICE_AUX_ROW, column=1, sticky=EXPAND)
        
        # number getting interface
        self.numbersLabel = tk.Label(text="Number of copies: ")
        self.numbersLabel.grid(row=NUMBER_ENTRY_ROW, column=0, sticky="e")

        self.numbersText = tk.Text(height=1, width=15, wrap="none")
        self.numbersText.grid(row=NUMBER_ENTRY_ROW, column=1)

        self.useExtCheckBox = tk.Checkbutton(text="Modify the files", variable=self.use_ext, command=self.process_use_ext)
        self.useExtCheckBox.grid(row=NUMBER_ENTRY_ROW, column=3, sticky="w")
        self.useExtCheckBox.select()

        self.okButton = tk.Button(text="Copy", command=self.copy)
        self.okButton.grid(row=NUMBER_ENTRY_ROW, column=2, sticky=EXPAND, padx=OFFSET)

        # progress bar
##        self.progressBar = ttk.Progressbar(self.master, orient="horizontal", mode="determinate")
##        self.progressBar.grid(row=PROGRESS_BAR_ROW, column=0, columnspan=4, sticky="ew", padx=OFFSET, pady=OFFSET)
##        self.progressBar["maximum"] = 0

        # overdrive
        self.exitButton = tk.Button(text="Exit", command=self.exit)
        self.exitButton.grid(row=OVERDRIVE_ROW, column=3, sticky=EXPAND, padx=OFFSET*2, pady=OFFSET)

        self.master.mainloop()

    def write(self, textbox, info, disable=True):
        textbox.config(state="normal")
        textbox.delete("1.0", "end")
        textbox.insert("1.0", info)
        if disable:
            textbox.config(state="disabled")

    def open_file(self):
        source_path = fd.askopenfilename(filetypes=self.file_specs)
        self.write(self.fileText, source_path)

    def open_directory(self):
        destination_path = fd.askdirectory()
        self.write(self.destText, destination_path)

    def process_only_dir(self):
        if self.same_dir:
            self.same_dir = False
            self.destSelectorButton.config(state="normal")
        else:
            self.same_dir = True
            self.write(self.destText, "")
            self.destSelectorButton.config(state="disabled")
            
    def process_incr_num(self):
        self.incr_num = not (self.incr_num)

    def process_use_ext(self):
        self.use_ext = not (self.use_ext)

    def copy(self):
        success = False
        try:
            print(bool(self.use_ext))
            self.copier.set_data(
                self.numbersText.get("1.0", "end")[:-1],
                self.fileText.get("1.0", "end")[:-1],
                self.destText.get("1.0", "end")[:-1],
                bool(self.same_dir),
                bool(self.incr_num),
                bool(self.use_ext))

            self.copier.copy()
            success = True

        except Exception as ex:
            showerror(title="Error!", message=ex)

        self.clear(success)
        

    def clear(self, success):
        if success:
            showinfo(title="Success!", message="Files were successfully copied")
        self.write(self.fileText, "")
        self.write(self.destText, "")
        self.write(self.numbersText, "", False)
        
        
    def exit(self):
        self.master.destroy()



            

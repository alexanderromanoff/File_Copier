import sys
import os
sys.path.append("..")

import ext_modules as em
import openpyxl
from openpyxl import load_workbook

class xlsExtHandler(em.ExtensionHandler):

    def __init__(self):
        super().__init__("xlsx")
    
    def process(self, file_name, extension, *data):
        workbook = openpyxl.load_workbook(file_name)
        sheet = workbook.active
        sheet['B4'] = data[0]
        workbook.save(file_name)
        workbook.close()

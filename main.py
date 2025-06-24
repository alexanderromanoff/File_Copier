import viz
import copier as cpr
from extensions import excel_ext as xl_ex

if __name__ == "__main__":
    copier = cpr.Copier()
    copier.add_handler(xl_ex.xlsExtHandler())
    app = viz.Application(copier, ("Excel files (only .xlsx)", ".xlsx"))


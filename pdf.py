from fpdf import FPDF
import csv
from fpdf.fonts import FontFace
from fpdf.enums import TableCellFillMode


CELL_PADDING = 2
KAUFWERT = 2035.07
PROVISION = 0.15
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (34, 139, 34)

# Loads data from aktuell.csv
def get_csv_data():
    with open("aktuell.csv", encoding="utf8") as aktuell:
        data = list(csv.reader(aktuell, delimiter=","))
    return data

# Formats currency values into a x,xx format
def format_currency(value):
    return f"{value:.02f}".replace('.', ',')

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', size=12)
        self.cell(0, 20, "Wertentwicklung", ln=True, align="C")

    # creates a table based on the data from akutell.csv
    def case_table(self):
        csv_data = get_csv_data()

        # print Headders
        self.set_font('Arial', 'B', 10)
        for header in csv_data[0]:
            self.cell(31, 10, header, border=1, align="C")
        self.ln()

        # print rows
        self.set_font('Arial', '', 10)
        for row in csv_data[1:]:
            for cell in row:
                self.cell(31, 5, cell, border=1, align="C")
            self.ln()  # Move to the next line

    # gets the sum of all values and calculates the profit
    def calculate_profit(self, gesammt):

        self.set_font('Arial', 'B', 10)
        self.ln(10)

        self.cell(50, 5, f"Umsatz:", align="R")
        self.cell(50, 5, format_currency(gesammt), align="L")
        self.ln()

        self.cell(50, 5, f"Abzüglich 15 % Provision:", align="R")
        self.cell(50, 5, f"- {format_currency(gesammt * 0.15)}", align="L")
        self.ln()

        self.cell(50, 5, f"Abzüglich Kaufwert:" , align="R")
        self.cell(50, 5, f"- {format_currency(KAUFWERT)}", align="L")
        self.ln()
        
        # prints the total profit (red or green)
        if gesammt < KAUFWERT:
            self.set_text_color(COLOR_RED)
        else:
            self.set_text_color(COLOR_GREEN)
        self.cell(50, 10, f"Gewinn:", align="R")
        self.cell(50, 10, format_currency(gesammt * 0.85 - KAUFWERT), align="L")


        



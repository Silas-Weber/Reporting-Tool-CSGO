from fpdf import FPDF
import csv
from fpdf.fonts import FontFace
from fpdf.enums import TableCellFillMode

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', size=12)
        self.cell(0, 20, "Wertentwicklung", ln=True, align="C")


    # creates a table based on the data from akutell.csv
    def case_table(self):
        with open("aktuell.csv", encoding="utf8") as aktuell:
            data = list(csv.reader(aktuell, delimiter=","))

        # first collum in the table (Headders)
        self.set_font('Arial', 'B', 10)
        for header in data[0]:
            self.cell(31, 10, header, border=1, align="C")
        self.ln()

        # Create the data rows
        self.set_font('Arial', '', 10)
        for row in data[1:]:
            for cell in row:
                self.cell(31, 5, cell, border=1, align="C")
            self.ln()  # Move to the next line

    # gets the sum of all values and calculates the profit
    def end_value(self, gesammt):
        gesammt_kaufwert=2035.07
        provision=0.15
        self.set_font('Arial', 'B', 10)

        self.ln(10)
       # self.set_xy(105, 100)

        self.cell(50, 5, f"Umsatz:", align="R")
        self.cell(50, 5, f"{gesammt:.02f}".replace('.', ','), align="L")
        self.ln()
        self.cell(50, 5, f"Abzüglich 15 % Provision:", align="R")
        self.cell(50, 5, f"- {gesammt * 0.15:.02f}".replace('.', ','), align="L")
        self.ln()
        self.cell(50, 5, f"Abzüglich Kaufwert:" , align="R")
        self.cell(50, 5, f"- {gesammt_kaufwert:.02f}".replace('.', ','), align="L")
        self.ln()
        if gesammt < gesammt_kaufwert:
            self.set_text_color(r=255, g=0, b=0)
        else:
            self.set_text_color(r=34, g=139, b=34)
        self.cell(50, 10, f"Gewinn:", align="R")
        self.cell(50, 10, f"{(gesammt * 0.85) - gesammt_kaufwert:.02f}".replace('.', ','), align="L")


        



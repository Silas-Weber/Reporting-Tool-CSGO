from pdf import PDF
import csv
import requests
import datetime
from decimal import Decimal

headers = {
    "Accept-Encoding": "br"
}
ITEMS = "Shadow Case,Chroma 2 Case,Chroma 3 Case,Prisma 2 Case,Prisma Case,Spectrum 2 Case,CS20 Case,Danger Zone Case,Snakebite Case"
ANZAHL = [2000, 3900, 5951, 4000, 1400, 3447, 869, 1000, 2000]
KAUFWERT = [0.11, 0.07, 0.12, 0.07, 0.06, 0.04, 0.03, 0.10, 0.10 ]


params = {
    "app_id": 730, # CS:GO
    "currency": "EUR",               
    "market_hash_name": ITEMS
    }

# 
def get_item_data():
    response = requests.get("https://api.skinport.com/v1/sales/history", params=params, headers=headers )
    return response.json()

def calculate_sum():
    with open('aktuell.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        gesamt = 0
        for row in reader:
            kiste_wert = row['Preis (Aktuell)'].replace(',', '.')
            anzahl = row['Anzahl']
            gesamt += float(kiste_wert) * int(anzahl)
    return gesamt

# macht eine API-Anfrage an Skinport, und gibt die letzten 24 Stunden Durchschnittspreise der angegebenen Items aus.
def create_data_csv():

    with open('aktuell.csv', 'w', newline='') as aktuell:
        fieldnames = ['Name', 'Preis (Kauf)', 'Preis (Aktuell)', 'Anzahl', 'Wert (Aktuell)', 'Prozent']
        writer = csv.DictWriter(aktuell, fieldnames=fieldnames)
        writer.writeheader()
        
        for i, infos in enumerate(get_item_data()):
            writer.writerow(
                {'Name': infos['market_hash_name'],
                 'Preis (Kauf)': f"{KAUFWERT[i]:,.02f}".replace('.', ','),
                'Preis (Aktuell)': f"{infos['last_24_hours']['avg']}".replace('.', ','),
                'Anzahl': ANZAHL[i],
                'Wert (Aktuell)': f"{infos['last_24_hours']['avg'] * ANZAHL[i]:.02f}".replace('.', ','),
                'Prozent': f"{(infos['last_24_hours']['avg'] - KAUFWERT[i]) / KAUFWERT[i] * 100:.2f} %"
                }
            )

def main():

    create_data_csv()
    summe = calculate_sum()
    print(summe)
    pdf = PDF()
    pdf.add_page(orientation='portrait', format="a4")
    pdf.case_table()
    pdf.calculate_profit(summe)

    date = datetime.datetime.now().strftime("%d.%m.%Y")
    print(date)
    pdf.output(f"Report/{date}.pdf")
    

if __name__ == "__main__":
    main()
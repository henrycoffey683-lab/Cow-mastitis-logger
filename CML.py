import csv
from datetime import date


def add_record():
    cow_id = input("Cow ID: ")
    quarter = input("Quarter: ")
    symtoms = input("Symtoms: ")
    severity = input("Severtity: (1-5): ")
    notes = input("any additional notes: " )
    today =  date.today()

    with open("mastitis_log.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            today,
            cow_id,
            quarter,
            symtoms,
            severity,
            notes
        ])
    print ("Record saved successfully!")


print("cow health logger")
add_record()

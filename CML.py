import csv
from datetime import date
import os



FILENAME = "mastitis_log.csv"

HEADERS = ["Date", "Cow_ID", "Quarter", "Symtoms", "Severity", "Notes"]

def setup_file():
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w", newline="") as file:
            writer= csv.writer(file)
            writer.writerow(HEADERS)
            
        


def get_input(prompt):
    value = input(prompt)

    if value.lower() == "cancel":
        return None
    return value


def add_record():
    print("\n--- Add Cow Record ---")
    print ("type 'cancel' at any time to return to main menu\n")


    cow_id = get_input("Cow ID: ")
    if cow_id is None:
        print("adding record cancelled\n ")
        return
    
    quarter = get_input("Quarter: ")
    if quarter is None:
        print("adding record cancelled \n")
        return
    
    symptoms = get_input("Symtoms: ")
    if symptoms is None:
        print("adding record cancelled\n ")
        return
    
    severity = get_input("Severtity: (1-5): ")
    if severity is None:
        print("adding record cancelled \n")
        return
    notes = get_input("any additional notes: " )
    if notes is None:
        print("adding notes cancelled\n ")
        return

    with open("mastitis_log.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            date.today(),
            cow_id,
            quarter,
            symptoms,
            severity,
            notes
        ])
    print ("Record saved successfully!\n")

def view_records():
    print("\n --- All Cow Records ---")

    with open(FILENAME, "r", newline="") as file:
        reader = csv.reader(file)
        records = list(reader)

        if len(records) <=1:
            print("No Records have been added yet.")
        

        else:
            print(" | ".join(HEADERS))
            print("-" * 100)

            for number, row in enumerate(records[1:], start=1):
                print(f"{number}. " + " | ".join(row))


            input("\nPress enter to return to the main menu.")
    

def search_records():
    print("\n--- Search Cow Records ---")
    print("type cancel to return to main menu")

    cow_id = input("Enter Cow ID to search: ")

    if cow_id.lower() == "cancel":
        print()
        return
    
    found = False 

    with open(FILENAME,"r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["Cow ID"].lower() ==cow_id.lower():
                print("\nRecord found:")
                for key, value in row.items():
                    print(f"{key}: {value}")
                    found = True

    if not found:
        print("No records found for that Cow ID.")

    input("\nPress enter to return to the main menu.")
def edit_record():
    print("\n--- Edit cow record---")
    print("type cancel to return to main menu")

    cow_id = input("Enter Cow ID to edit: ")

    if cow_id.lower() =="cancel":
        print()
        return

    #read all records from the file 
    with open(FILENAME, "r", newline="") as file:
        reader = csv.DictReader(file)
        records = list(reader)
    # find record belonging to this cow
    matching_indexes = [
        index for index, record in enumerate(records)
        if record["cow ID"].lower() == cow_id.lower()
    ]

    if not matching_indexes:
        print("no records with that cow ID")
        input("\npress enter to return to main menu")
        return
    print("\nwatching records:")
    for number, index in enumerate(matching_indexes, start=1):
        record = records[index]
        print(
            f"\n{number}. Date: {record['Date']} | "
            f" quarter: {record['quarter']} | "
            f"symptoms: {record['symptoms']} | "
        )
    choice = input("\n enter the record number to edit: ")
    if choice.lower() == "cancel":
        return
    try:
        choice_number = int(choice)
        if choice_number < 1 or choice_number > len(matching_indexes):
            print("invalid record number.")
            input("\nPress Enter to return to main menu")
            return
    except ValueError:
        print("please enter a valid number")
        input("\npress enter to return to main menu")
        return
    record_index = matching_indexes[choice_number - 1]
    record = records[record_index]
    print("\n leave a field blank to keep its original value")
    print("type cancel to stop editing without saving\n")
    for field in HEADERS:
        current_value = record[field]
        new_value = input(f"{field}[{current_value}]: ")

        if new_value.lower() == "cancel":
            print("editing cancelled. no changes were saved.\n")
            return
        if new_value.strip():
            record[field] = new_value
    #save all records back to the csv file
    with open(FILENAME, "w", newline="") as file:
        writer =csv.DictWriter(file, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(records)

    print("\n record updated successfully!")
    input("\n press enter to return to the main menu")




def main():
    setup_file()


    while True:
        print("Cow Mastitis Logger")
        print("1.Add a record")
        print("2.View all records")
        print("3.Search by Cow ID")
        print("5.Edit cow records")
        print("5.exit")

        choice = input("\nchoose an option; type 1-5:")

        if choice == "1":
            add_record()

        elif choice == "2":
            view_records()

        elif choice == "3":
            search_records()

        elif choice == "4":
            edit_record()

        elif choice == "5":
            print("Until next timme!")
            break
        else:
            print("please enter an number between 1 and 5.\n")

if __name__ == "__main__":
    main()




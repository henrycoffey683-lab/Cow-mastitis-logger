import csv
from datetime import date
import os
from datetime import date, datetime, timedelta


FILENAME = "mastitis_log.csv"

HEADERS = [
    "Date",
    "Cow_ID",
    "Quarter",
    "Symptoms",
    "Severity",
    "Notes"
    ]

def setup_file():
    if not os.path.exists(FILENAME) or os.path.getsize(FILENAME) ==0:
        with open(FILENAME, "w", newline="") as file:
            writer= csv.writer(file)
            writer.writerow(HEADERS)
            
def mastitis_report():
    print("\n--- Mastitis Report ---")


    today = date.today()

    #work out the current reporting period.
    # the period starts on the 15th and ends on the 14 of the next month
    if today.day >= 15:
        start_date = date(today.year, today.month, 15) 
    else:
        #go back to the previous 15th of the month
        if today.month == 1:
            start_date = date(today.year - 1, 12, 15)    
        else:
            start_date = date(today.year, today.month - 1, 15)
    # calculate next months 15th then subtract one day
    if start_date.month == 12:
        next_month_15th = date(start_date.year + 1, 1, 15)
    else:
        next_month_15th = date(
            start_date.year,
            start_date.month + 1,
            15
        )

    end_date = next_month_15th - timedelta(days=1)
    found_records = []

    with open(FILENAME, "r", newline="") as file:
        reader = csv.DictReader(file)


        for row in reader:
            try:
                record_date = datetime.strptime(
                    row["Date"], "%Y-%m-%d"
                ).date()

                if start_date <= record_date <= end_date:
                    found_records.append(row)

            except ValueError:
                #skipp records with an invalid date
                pass


    print(

        f"\nReporting period: "
        f"{start_date.strftime('%d %B %Y')} to "
        f"{end_date.strftime('%d %B %Y')}"
    )

    # add the reports folder 
    os.makedirs("reports", exist_ok=True)
    report_filename = (
        f"reports/mastitis_report_"
        f"{start_date}_to_{end_date}.csv"
    )
    with open(report_filename, "w", newline="") as report_file:
        writer = csv.DictWriter(
            report_file,
            fieldnames=HEADERS
        )

        writer.writeheader()
        writer.writerows(found_records)





    if not found_records:
        print("\nNo mastitis records found for this reporting period.")
    else:
        print("\n" + " | ".join(HEADERS))
        print("-" * 100)

        for number, record in enumerate(found_records, start=1):
            print(
                f"{number}. {record['Date']} | "
                f"{record['Cow_ID']}  | "
                f"{record['Quarter']}  | "
                f"{record['Symptoms']}  | "
                f"{record['Severity']}  | "
                f"{record['Notes']}"
            )
        print(f"\nTotal records: {len(found_records)}")
    print(f"\n Report saved as: {report_filename}")

    input("\nPress Enter to returnto the main menu")



def get_input(prompt):
    value = input(prompt)

    if value.lower() == "cancel":
        return None
    return value


def add_record():
    print("\n--- Add Cow Record ---")
    print ("type 'cancel' at any time to return to main menu\n")


    cow_id = get_input("Cow_ID: ")
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
    print("\n --- All Cow Records ---\n")

    with open(FILENAME, "r", newline="") as file:
        reader = csv.DictReader(file)
        records = list(reader)

        if not records:
            print("No Records have been added yet.")
        

        else:
            print_table(records)
            print(f"\nTotal records: {len(records)}")


            input("\nPress enter to return to the main menu.")

def print_table(records):
    """display records in a neatly formatted table"""

    if not records:
        print("no records found.")
        return
    column_widths = []

    for i, header in enumerate(HEADERS):
        widest_value = max(
            len(str(row.get(header, "")))
            for row in records
        )
        column_widths.append(
            max(len(header), widest_value)
        )
    header_row =" | ".join(
        header.ljust(column_widths[i])
        for i, header in enumerate(HEADERS)
    )
    print(header_row)

    print("-+-".join(
        "-" * width for width in column_widths
    ))

    for record in records:
        row = " | ".join(
            str(record.get(header, "")).ljust(column_widths[i])
            for i, header in enumerate(HEADERS)
        )
        print(row)
    

def search_records():
    print("\n--- Search Cow Records ---")
    print("type cancel to return to main menu\n")

    cow_id = input("Enter Cow ID to search: ")

    if cow_id.lower() == "cancel":
        print()
        return
    
    found = False 

    with open(FILENAME,"r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["Cow_ID"].lower() == cow_id.lower():
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
        if record["Cow_ID"].lower() == cow_id.lower()
    ]

    if not matching_indexes:
        print("No records with that cow ID")
        input("\npress enter to return to main menu")
        return
    print("\nwatching records:")
    for number, index in enumerate(matching_indexes, start=1):
        record = records[index]
        print(
            f"\n{number}. Date: {record['Date']} | "
            f" quarter: {record['Quarter']} | "
            f"symptoms: {record['Symptoms']} | "
        )
    choice = input("\n Enter the record number to edit: ")
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

    print("\n Record updated successfully!")
    input("\n Press enter to return to the main menu")




def main():
    setup_file()


    while True:
        print("Cow Mastitis Logger")
        print("1.Add a record")
        print("2.View all records")
        print("3.Search by Cow ID")
        print("4.Edit cow records")
        print("5.Mastitis montly record")
        print("6.Exit")
        

        choice = input("\nchoose an option; type 1-6:")

        if choice == "1":
            add_record()

        elif choice == "2":
            view_records()

        elif choice == "3":
            search_records()

        elif choice == "4":
            edit_record()

        elif choice == "5":
            mastitis_report()
    

        elif choice == "6":
            print("Until next time!")
            break
        else:
            print("please enter an number between 1 and 6.\n")

if __name__ == "__main__":
    main()




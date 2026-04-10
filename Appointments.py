import json
import os

appointments = []

FILE_NAME = "appointments.json"

def get_writable_file():
    global FILE_NAME
    
    try:
        with open(FILE_NAME, "w") as f:
            pass
        return FILE_NAME
    except OSError:
        pass

    try:
        temp_file = "/tmp/appointments.json"
        with open(temp_file, "w") as f:
            pass
        FILE_NAME = temp_file
        return FILE_NAME
    except OSError:
        pass

    FILE_NAME = None
    return None

def load_appointments():
    global appointments
    if FILE_NAME and os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                appointments = json.load(file)
        except:
            appointments = []
    else:
        appointments = []

def save_appointments():
    if not FILE_NAME:
        print("Warning: Unable to save appointments in this environment.")
        return

    try:
        with open(FILE_NAME, "w") as file:
            json.dump(appointments, file, indent=4)
    except OSError:
        print("Warning: Unable to save appointments.")

def home_menu():
    print("\n--- Appointment Scheduling System ---")
    print("1. Create Appointment")
    print("2. View Appointments")
    print("3. Update Appointment")
    print("4. Delete Appointment")
    print("5. Search Appointments")
    print("6. Exit")

def get_input(prompt):
    value = input(prompt)
    if value.lower() == 'e':
        print("Exiting system. Goodbye!")
        save_appointments()
        exit()
    return value

def create_appointment():
    print("\n--- Create Appointment ---")
    
    name = input("Enter appointment name (or 'b' to go back, 'e' to exit): ")
    if name.lower() == 'b':
        return
    if name.lower() == 'e':
        save_appointments()
        exit()

    date = get_input("Enter date (MM/DD/YYYY): ")
    time = get_input("Enter time (HH:MM): ")

    appointment = {
        "name": name,
        "date": date,
        "time": time
    }

    appointments.append(appointment)
    save_appointments()
    print("Appointment created successfully.")
    input("Press Enter to return to the home menu.")

def view_appointments():
    print("\n--- View Appointments ---")
    if not appointments:
        print("No appointments scheduled.")
    else:
        for i, appt in enumerate(appointments, start=1):
            print(f"{i}. {appt['name']} on {appt['date']} at {appt['time']}")
    
    choice = input("\nEnter 'b' to go back or 'e' to exit: ")
    if choice.lower() == 'e':
        save_appointments()
        exit()

def update_appointment():
    print("\n--- Update Appointment ---")
    view_list_only()

    if not appointments:
        input("Press Enter to return to the home menu.")
        return

    choice = input("Enter appointment number to update (or 'b' to go back): ")
    if choice.lower() == 'b':
        return

    if choice.isdigit():
        choice = int(choice)
        if 1 <= choice <= len(appointments):
            name = get_input("Enter new name: ")
            date = get_input("Enter new date: ")
            time = get_input("Enter new time: ")

            appointments[choice - 1]["name"] = name
            appointments[choice - 1]["date"] = date
            appointments[choice - 1]["time"] = time

            save_appointments()
            print("Appointment updated successfully.")
        else:
            print("Invalid selection.")
    else:
        print("Invalid input.")

    input("Press Enter to return to the home menu.")

def delete_appointment():
    print("\n--- Delete Appointment ---")
    view_list_only()

    if not appointments:
        input("Press Enter to return to the home menu.")
        return

    choice = input("Enter appointment number to delete (or 'b' to go back): ")
    if choice.lower() == 'b':
        return

    if choice.isdigit():
        choice = int(choice)
        if 1 <= choice <= len(appointments):
            confirm = input("Are you sure you want to delete? (y/n): ")
            if confirm.lower() == 'y':
                removed = appointments.pop(choice - 1)
                save_appointments()
                print(f"Deleted appointment: {removed['name']}")
            else:
                print("Deletion canceled.")
        else:
            print("Invalid selection.")
    else:
        print("Invalid input.")

    input("Press Enter to return to the home menu.")

def search_appointments():
    print("\n--- Search Appointments ---")
    keyword = input("Enter name or date to search (or 'b' to go back): ")
    
    if keyword.lower() == 'b':
        return
    if keyword.lower() == 'e':
        save_appointments()
        exit()

    results = [
        appt for appt in appointments
        if keyword.lower() in appt["name"].lower() or keyword in appt["date"]
    ]

    if results:
        print("\nMatching Appointments:")
        for appt in results:
            print(f"{appt['name']} on {appt['date']} at {appt['time']}")
    else:
        print("No matching appointments found.")

    input("Press Enter to return to the home menu.")

def view_list_only():
    if not appointments:
        print("No appointments scheduled.")
    else:
        for i, appt in enumerate(appointments, start=1):
            print(f"{i}. {appt['name']} on {appt['date']} at {appt['time']}")

def main():
    get_writable_file()   
    load_appointments()

    while True:
        home_menu()
        choice = input("Select an option: ")

        if choice == "1":
            create_appointment()
        elif choice == "2":
            view_appointments()
        elif choice == "3":
            update_appointment()
        elif choice == "4":
            delete_appointment()
        elif choice == "5":
            search_appointments()
        elif choice == "6":
            save_appointments()
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()

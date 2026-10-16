# =============================================================================
# Student Record Management System
# Programming Fundamentals with Python - Week 8 Refactoring Exercise
#
# This program reads student data from a CSV file and provides a menu-driven
# interface to list all students and search for a student by ID.
#
# NOTE TO STUDENTS: This program works correctly but is written in a "top-down"
# style with no functions and uses global variables. Your task is to refactor
# this program to make it more readable and maintainable by organizing the code
# into well-named functions and eliminating the use of global variables.
# =============================================================================

import csv

# -----------------------------------------------------------------------------
# Global Variables
# -----------------------------------------------------------------------------
student_records = []        # Holds all student records loaded from the CSV
csv_filename = ""           # Stores the filename entered by the user
menu_choice = ""            # Stores the user's menu selection
csv_loaded = False          # Tracks whether a CSV file has been loaded

search_id = ""              # Stores the Student ID entered during a search
found_student = None        # Stores the matching student record, if found
search_index = 0            # Loop counter used during linear search

row_number = 0              # Loop counter used when printing student records
current_student = None      # Holds the current record during iteration

student_id = ""             # Fields parsed from each CSV row
student_name = ""
major = ""
gpa = ""
total_credits = ""

# =============================================================================
# Main Program Loop
# =============================================================================

print("=" * 60)
print("   Student Record Management System")
print("=" * 60)

while True:

    # -------------------------------------------------------------------------
    # Display Menu
    # -------------------------------------------------------------------------
    print()
    print("Please select an option:")
    print("  1. Read CSV")
    print("  2. List CSV Contents")
    print("  3. Search for Student by ID")
    print("  4. Exit")
    print()

    menu_choice = input("Enter your choice (1-4): ").strip()

    # =========================================================================
    # Option 1: Read CSV
    # =========================================================================
    if menu_choice == "1":

        csv_filename = input("Enter the CSV filename (e.g., students.csv): ").strip()

        # BUG 4 FIX: clear the list so reloading does not duplicate records
        student_records.clear()

        # BUG 1 FIX: keep the file open until iteration finishes.
        # DictReader is lazy and reads rows during the loop, not at creation.
        csv_file = open(csv_filename, newline="")
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            student_id     = row["StudentID"]
            student_name   = row["StudentName"]
            major          = row["Major"]
            gpa            = row["GPA"]
            total_credits  = row["TotalCredits"]

            student_record = {
                "StudentID"    : student_id,
                "StudentName"  : student_name,
                "Major"        : major,
                "GPA"          : gpa,
                "TotalCredits" : total_credits
            }

            student_records.append(student_record)

        csv_file.close()          # BUG 1 FIX: close after the loop, not before

        csv_loaded = True         # BUG 3 FIX: record that data is now loaded

        print()
        print(f"Success! {len(student_records)} student record(s) loaded from '{csv_filename}'.")

    # =========================================================================
    # Option 2: List CSV Contents
    # =========================================================================
    elif menu_choice == "2":

        if not csv_loaded:
            print()
            print("No data loaded. Please use Option 1 to read a CSV file first.")

        else:
            print()
            print("-" * 82)          # BUG 5 FIX: was 80, now matches the others
            print(f"{'#':<5} {'Student ID':<12} {'Student Name':<22} {'Major':<24} {'GPA':<6} {'Credits'}")
            print("-" * 82)

            row_number = 1

            for current_student in student_records:
                print(
                    f"{row_number:<5}"
                    f"{current_student['StudentID']:<12}"
                    f"{current_student['StudentName']:<22}"
                    f"{current_student['Major']:<24}"
                    f"{current_student['GPA']:<6}"
                    f"{current_student['TotalCredits']}"
                )

                row_number = row_number + 1   # BUG 6 FIX: advance the counter

            print("-" * 82)
            print(f"Total records: {len(student_records)}")

    # =========================================================================
    # Option 3: Search for Student by ID
    # =========================================================================
    elif menu_choice == "3":

        if not csv_loaded:
            print()
            print("No data loaded. Please use Option 1 to read a CSV file first.")

        else:
            search_id = input("Enter the Student ID to search for: ").strip()

            search_index = 0
            found_student = None      # BUG 8 FIX: clear any prior result

            # BUG 9 FIX: "<" not "<=" so the index never runs past the end
            while search_index < len(student_records):
                # BUG 10 FIX: uppercase BOTH sides for a true case-insensitive match
                if student_records[search_index]["StudentID"].upper() == search_id.upper():
                    found_student = student_records[search_index]
                    search_index = len(student_records)       # BUG 9 FIX: exit cleanly
                else:
                    search_index = search_index + 1

            print()

            if found_student is None:
                print(f"No student found with ID '{search_id}'.")
            else:
                print("Student found!")
                print("-" * 40)
                print(f"  Student ID    : {found_student['StudentID']}")
                print(f"  Student Name  : {found_student['StudentName']}")
                print(f"  Major         : {found_student['Major']}")
                print(f"  GPA           : {found_student['GPA']}")
                print(f"  Total Credits : {found_student['TotalCredits']}")
                print("-" * 40)

    # =========================================================================
    # Option 4: Exit
    # =========================================================================
    elif menu_choice == "4":      # BUG 7 FIX: input() returns a string, not an int
        print()
        print("Thank you for using the Student Record Management System. Goodbye!")
        break

    # =========================================================================
    # Invalid Input
    # =========================================================================
    else:
        print()
        print(f"'{menu_choice}' is not a valid option. Please enter 1, 2, 3, or 4.")

"""
Student Record Management System - Refactored
Author: Stavion Colquitt
Date:   2026-10-16
Description:
    Object-oriented redesign of student_records.py. A Student class
    represents one record, a GraduateStudent subclass extends it, and a
    StudentRoster class owns the collection and provides every menu
    action as a method. Searching uses binary search. All state lives in
    instance attributes; there are no global variables.

    External behaviour matches student_records_fixed.py exactly: the same
    menu, the same prompts, and the same output format.
"""

import csv


class Student:
    """One student record loaded from the CSV file."""

    def __init__(self, student_id, student_name, major, gpa, total_credits):
        """Store the five fields that describe a student."""
        self.student_id = student_id
        self.student_name = student_name
        self.major = major
        self.gpa = gpa
        self.total_credits = total_credits

    def __str__(self):
        """Return this student as one aligned table row."""
        return (f"{self.student_id:<12}"
                f"{self.student_name:<22}"
                f"{self.major:<24}"
                f"{self.gpa:<6}"
                f"{self.total_credits}")

    def detail_lines(self):
        """Return the multi-line detail view shown after a search."""
        return (f"  Student ID    : {self.student_id}\n"
                f"  Student Name  : {self.student_name}\n"
                f"  Major         : {self.major}\n"
                f"  GPA           : {self.gpa}\n"
                f"  Total Credits : {self.total_credits}")


class GraduateStudent(Student):
    """A student who is also working on a thesis."""

    def __init__(self, student_id, student_name, major, gpa,
                 total_credits, thesis_topic):
        """Initialize the inherited fields, then add the thesis topic."""
        super().__init__(student_id, student_name, major, gpa, total_credits)
        self.thesis_topic = thesis_topic

    def __str__(self):
        """Extend the parent row with the thesis topic."""
        return super().__str__() + f"  [Thesis: {self.thesis_topic}]"

    def detail_lines(self):
        """Extend the parent detail view with the thesis topic."""
        return (super().detail_lines() +
                f"\n  Thesis Topic  : {self.thesis_topic}")


class StudentRoster:
    """Owns the student list and provides every menu action."""

    def __init__(self):
        """Start with an empty roster and no file loaded."""
        self.students = []
        self.csv_loaded = False
        self.filename = ""

    def load_csv(self, filename):
        """Load records from a CSV file. Returns the number loaded."""
        loaded = []

        try:
            with open(filename, newline="") as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    try:
                        loaded.append(Student(
                            row["StudentID"].strip(),
                            row["StudentName"].strip(),
                            row["Major"].strip(),
                            row["GPA"].strip(),
                            row["TotalCredits"].strip()))
                    except (KeyError, AttributeError, TypeError):
                        print("  Skipping a row with an unexpected format.")
        except FileNotFoundError:
            print()
            print(f"No file named '{filename}' was found. "
                  f"Check the name and try again.")
            return 0
        except OSError as error:
            print()
            print(f"Could not read '{filename}': {error}")
            return 0

        # replace rather than extend, so reloading never duplicates records
        self.students = loaded

        # binary search requires the list to be in sorted order
        self.students.sort(key=lambda student: student.student_id.upper())

        self.csv_loaded = True
        self.filename = filename
        return len(self.students)

    def list_students(self):
        """Print every loaded record in a numbered table."""
        if not self.csv_loaded:
            print()
            print("No data loaded. Please use Option 1 to read a CSV file first.")
            return

        print()
        print("-" * 82)
        print(f"{'#':<5} {'Student ID':<12} {'Student Name':<22} "
              f"{'Major':<24} {'GPA':<6} {'Credits'}")
        print("-" * 82)

        for row_number, student in enumerate(self.students, start=1):
            print(f"{row_number:<5}{student}")

        print("-" * 82)
        print(f"Total records: {len(self.students)}")

    def binary_search(self, search_id):
        """Find a student by ID using binary search.

        Returns the matching Student, or None when no record matches.
        """
        target = search_id.strip().upper()
        low = 0
        high = len(self.students) - 1

        while low <= high:
            middle = (low + high) // 2
            current_id = self.students[middle].student_id.upper()

            if current_id == target:
                return self.students[middle]
            elif current_id < target:
                low = middle + 1       # target must be in the upper half
            else:
                high = middle - 1      # target must be in the lower half

        # low passed high, so every element was ruled out
        return None

    def search_by_id(self, search_id):
        """Search for one student ID and print the result."""
        if not self.csv_loaded:
            print()
            print("No data loaded. Please use Option 1 to read a CSV file first.")
            return

        found_student = self.binary_search(search_id)

        print()

        if found_student is None:
            print(f"No student found with ID '{search_id}'.")
        else:
            print("Student found!")
            print("-" * 40)
            print(found_student.detail_lines())
            print("-" * 40)

    def run(self):
        """Display the menu and handle selections until the user exits."""
        print("=" * 60)
        print("   Student Record Management System")
        print("=" * 60)

        while True:
            print()
            print("Please select an option:")
            print("  1. Read CSV")
            print("  2. List CSV Contents")
            print("  3. Search for Student by ID")
            print("  4. Exit")
            print()

            menu_choice = input("Enter your choice (1-4): ").strip()

            if menu_choice == "1":
                filename = input(
                    "Enter the CSV filename (e.g., students.csv): ").strip()
                record_count = self.load_csv(filename)
                if record_count:
                    print()
                    print(f"Success! {record_count} student record(s) "
                          f"loaded from '{filename}'.")

            elif menu_choice == "2":
                self.list_students()

            elif menu_choice == "3":
                search_id = input(
                    "Enter the Student ID to search for: ").strip()
                self.search_by_id(search_id)

            elif menu_choice == "4":
                print()
                print("Thank you for using the Student Record "
                      "Management System. Goodbye!")
                break

            else:
                print()
                print(f"'{menu_choice}' is not a valid option. "
                      f"Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    roster = StudentRoster()
    roster.run()

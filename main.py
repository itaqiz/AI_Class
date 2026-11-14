import json
import os
from datetime import datetime


class Student303:
    def __init__(self, student_id, name, age, department, marks):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.department = department
        self.marks = marks

    def calculate_average(self):
        if not self.marks:
            return 0

        return sum(self.marks) / len(self.marks)

    def calculate_grade(self):
        average = self.calculate_average()

        if average >= 85:
            return "A"
        elif average >= 80:
            return "A-"
        elif average >= 75:
            return "B+"
        elif average >= 71:
            return "B"
        elif average >= 68:
            return "B-"
        elif average >= 64:
            return "C+"
        elif average >= 60:
            return "C"
        elif average >= 50:
            return "D"
        else:
            return "F"

    def display_info(self):
        print("\nStudent Information")
        print("-------------------------")
        print("ID:", self.student_id)
        print("Name:", self.name)
        print("Age:", self.age)
        print("Department:", self.department)
        print("Marks:", self.marks)
        print("Average:", round(self.calculate_average(), 2))
        print("Grade:", self.calculate_grade())

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "department": self.department,
            "marks": self.marks
        }


class StudentManagementSystem:

    def __init__(self):
        self.students = {}
        self.filename = "students.json"
        self.load_data()

    def load_data(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, "r") as file:
                    data = json.load(file)

                    for student_data in data:
                        student = Student(
                            student_data["student_id"],
                            student_data["name"],
                            student_data["age"],
                            student_data["department"],
                            student_data["marks"]
                        )

                        self.students[student.student_id] = student

        except (json.JSONDecodeError, KeyError, TypeError) as error:
            print("Error loading data:", error)

    def save_data(self):
        try:
            data = []

            for student in self.students.values():
                data.append(student.to_dict())

            with open(self.filename, "w") as file:
                json.dump(data, file, indent=4)

            print("Data saved successfully!")

        except IOError as error:
            print("Error saving data:", error)

    def add_student(self):
        try:
            student_id = input("Enter student ID: ")

            if student_id in self.students:
                print("Student ID already exists!")
                return

            name = input("Enter student name: ")
            age = int(input("Enter student age: "))
            department = input("Enter department: ")

            marks = []

            number_of_subjects = int(
                input("Enter number of subjects: ")
            )

            for i in range(number_of_subjects):
                mark = float(input(f"Enter marks for subject {i + 1}: "))

                if mark < 0 or mark > 100:
                    print("Marks must be between 0 and 100.")
                    return

                marks.append(mark)

            student = Student(
                student_id,
                name,
                age,
                department,
                marks
            )

            self.students[student_id] = student

            self.save_data()

            print("Student added successfully!")

        except ValueError:
            print("Invalid input. Please enter the correct data types.")

    def view_students(self):

        if not self.students:
            print("No students found.")
            return

        for student in self.students.values():
            student.display_info()

    def search_student(self):

        student_id = input("Enter student ID to search: ")

        student = self.students.get(student_id)

        if student:
            student.display_info()
        else:
            print("Student not found!")

    def delete_student(self):

        student_id = input("Enter student ID to delete: ")

        if student_id in self.students:
            del self.students[student_id]

            self.save_data()

            print("Student deleted successfully!")

        else:
            print("Student not found!")

    def update_student(self):

        student_id = input("Enter student ID to update: ")

        student = self.students.get(student_id)

        if not student:
            print("Student not found!")
            return

        print("1. Update Name")
        print("2. Update Age")
        print("3. Update Department")
        print("4. Update Marks")

        choice = input("Choose an option: ")

        if choice == "1":
            student.name = input("Enter new name: ")

        elif choice == "2":
            student.age = int(input("Enter new age: "))

        elif choice == "3":
            student.department = input("Enter new department: ")

        elif choice == "4":
            marks = []

            count = int(input("Enter number of subjects: "))

            for i in range(count):
                mark = float(input(f"Enter marks for subject {i + 1}: "))

                if mark < 0 or mark > 100:
                    print("Invalid marks!")
                    return

                marks.append(mark)

            student.marks = marks

        else:
            print("Invalid choice!")
            return

        self.save_data()
        print("Student updated successfully!")

    def show_top_students(self):

        if not self.students:
            print("No students available.")
            return

        sorted_students = sorted(
            self.students.values(),
            key=lambda student: student.calculate_average(),
            reverse=True
        )

        print("\nTop Performing Students")
        print("-------------------------")

        for student in sorted_students[:5]:
            print(
                student.name,
                "| Average:",
                round(student.calculate_average(), 2),
                "| Grade:",
                student.calculate_grade()
            )

    def department_statistics(self):

        departments = {}

        for student in self.students.values():

            department = student.department

            if department not in departments:
                departments[department] = []

            departments[department].append(
                student.calculate_average()
            )

        print("\nDepartment Statistics")
        print("-------------------------")

        for department, averages in departments.items():

            department_average = sum(averages) / len(averages)

            print("Department:", department)
            print("Students:", len(averages))
            print("Average Performance:", round(department_average, 2))
            print()

    def search_by_grade(self):

        grade = input("Enter grade to search: ").upper()

        matching_students = [
            student
            for student in self.students.values()
            if student.calculate_grade() == grade
        ]

        if matching_students:
            for student in matching_students:
                print(
                    student.name,
                    "-",
                    student.calculate_grade()
                )
        else:
            print("No students found with this grade.")

    def show_class_report(self):

        if not self.students:
            print("No data available.")
            return

        averages = [
            student.calculate_average()
            for student in self.students.values()
        ]

        highest = max(averages)
        lowest = min(averages)
        overall = sum(averages) / len(averages)

        print("\nClass Performance Report")
        print("-------------------------")
        print("Total Students:", len(self.students))
        print("Class Average:", round(overall, 2))
        print("Highest Average:", highest)
        print("Lowest Average:", lowest)

        passed = sum(1 for average in averages if average >= 50)
        failed = len(averages) - passed

        print("Passed Students:", passed)
        print("Failed Students:", failed)

    def menu(self):

        while True:

            print("\n================================")
            print("   STUDENT MANAGEMENT SYSTEM")
            print("================================")

            print("1. Add Student")
            print("2. View All Students")
            print("3. Search Student")
            print("4. Update Student")
            print("5. Delete Student")
            print("6. Show Top Students")
            print("7. Department Statistics")
            print("8. Search Students by Grade")
            print("9. Class Performance Report")
            print("10. Save Data")
            print("0. Exit")

            choice = input("\nEnter your choice: ")

            if choice == "1":
                self.add_student()

            elif choice == "2":
                self.view_students()

            elif choice == "3":
                self.search_student()

            elif choice == "4":
                self.update_student()

            elif choice == "5":
                self.delete_student()

            elif choice == "6":
                self.show_top_students()

            elif choice == "7":
                self.department_statistics()

            elif choice == "8":
                self.search_by_grade()

            elif choice == "9":
                self.show_class_report()

            elif choice == "10":
                self.save_data()

            elif choice == "0":
                self.save_data()
                print("Exiting system...")
                break

            else:
                print("Invalid choice. Try again.")


if __name__ == "__main__":

    system = StudentManagementSystem()

    system.menu()
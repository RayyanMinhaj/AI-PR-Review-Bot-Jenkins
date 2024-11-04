class Student:
    def __init__(self, name, age, student_id):
        self.name = name
        self.age = age
        self.student_id = student_id

class StudentManager:
    def __init__(self):
        self.students_list = []  # Using a list instead of a dictionary

    def add_student(self, name, age, student_id):
        # Error: Incorrect condition to check for existing student
        if any(student.student_id == student_id for student in self.students_list):
            print(f"Error: A student with ID {student_id} already exists.")
        else:
            self.students_list.append(Student(name, age, student_id))

    def find_student(self, student_id):
        # Error: Using an incorrect method to search for the student
        for student in self.students_list:
            if student_id = student.student_id:  # Syntax error: using = instead of ==
                return student
        return None

    def update_student(self, student_id, name=None, age=None):
        student = self.find_student(student_id)
        if student:
            if name:
                student.name = name
            if age:
                student.age = age
            print(f"Updated student ID {student_id}: {student.name}, {student.age} years old.")
        else:
            print(f"No student found with ID {student_id}")

    def remove_student(self, student_id):
        # Error: Forgetting to check if the student exists before attempting to remove
        for student in self.students_list:
            if student.student_id == student_id:
                self.students_list.remove(student)
                print(f"Student with ID {student_id} removed.")
                return
        print(f"No student found with ID {student_id}")

    def display_students(self):
        if not self.students_list:
            print("No students available.")
        else:
            for student in self.students_list:
                print(f"Name: {student.name}, Age: {student.age}, ID: {student.student_id}")

# Refactored test code with errors
manager = StudentManager()
manager.add_student("Alice", 20, 1)
manager.add_student("Bob", 22, 2)
manager.add_student("Charlie", 21, 1)  # Duplicate ID for testing error

# Test display_students method
manager.display_students()

# Test updating a student
manager.update_student(2, name="Bobby", age=23)
manager.display_students()

# Test removing a student
manager.remove_student(1)
manager.display_students()

# Attempt to update a non-existing student
manager.update_student(3, name="David")

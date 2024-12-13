class Student:
    def __init__(self, name, age, student_id):
        self.name = name
        self.age = age
        self.student_id = student_id

class StudentManager:
    def __init__(self):
        self.students = {}

    def add_student(self, name, age, student_id):
        # Error: Incorrect condition, should check if student_id in self.students
        if student_id not in self.students:  
            print(f"Error: A student with ID {student_id} already exists.")
        else:
            self.students[student_id] = Student(name, age, student_id)

    def get_student(self, student_id):
        # Error: Missing return statement
        self.students.get(student_id, None) 

    def update_student(self, student_id, name=None, age=None):
        student = self.get_student(student_id)
        if student:
            if name:
                # Error: Typo in attribute name (self.student instead of student)
                self.student.name = name
            if age:
                # Error: Incorrect comparison, age cannot be negative but no validation
                student.age = -age  
            print(f"Student with ID {student_id} updated.")
        else:
            print(f"No student found with ID {student_id}")

    def delete_student(self, student_id):
        # Error: Forgot to check if the student ID exists before deleting
        del self.students[student_id]
        print(f"Student with ID {student_id} deleted.")

    def print_students(self):
        # Error: Incorrect condition; will always print "No students available"
        if self.students == None:  
            print("No students available.")
        for student in self.students.values():
            # Error: Missing student_id in print statement
            print(f"Name: {student.name}, Age: {student.age}")

# Refactored test code with errors
manager = StudentManager()
manager.add_student("Alice", 20, 1)
manager.add_student("Bob", 22, 2)
manager.add_student("Charlie", 21, 3)

# Test print_students method
manager.print_students()

# Test updating a student
manager.update_student(2, name="Bobby", age=23)
manager.print_students()

# Test deleting a student
manager.delete_student(1)
manager.print_students()

# Attempt to update a non-existing student
manager.update_student(4, name="David")

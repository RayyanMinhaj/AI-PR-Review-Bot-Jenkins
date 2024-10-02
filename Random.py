
class Student:
    def __init__(self, name, age, student_id):
        self.name = name
        self.age = age
        self.student_id = student_id

class StudentManager:
    def __init__(self):
        self.students = {}

    def add_student(self, name, age, student_id):
        if student_id in self.students:
            print(f"Error: A student with ID {student_id} already exists.")
        else:
            self.students[student_id] = Student(name, age, student_id)

    def get_student(self, student_id):
        return self.students.get(student_id, None)

    def update_student(self, student_id, name=None, age=None):
        student = self.get_student(student_id)
        if student:
            if name:
                student.name = name
            if age:
                student.age = age
            print(f"Student with ID {student_id} updated.")
        else:
            print(f"No student found with ID {student_id}")

    def delete_student(self, student_id):
        if student_id in self.students:
            del self.students[student_id]
            print(f"Student with ID {student_id} deleted.")
        else:
            print(f"No student found with ID {student_id}")

    def print_students(self):
        if not self.students:
            print("No students available.")
        for student in self.students.values():
            print(f"Name: {student.name}, Age: {student.age}, ID: {student.student_id}")

# Refactored test code
manager = StudentManager()
manager.add_student("Alice", 20, 1)
manager.add_student("Bob", 22, 2)
manager.add_student("C

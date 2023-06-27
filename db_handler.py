import sqlite3

class DBHandler():
    _instance = None
    #ensuring that the db object is singleton
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DBHandler, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    def __init__(self, db_location="data/attendance.db"):
        self.db_location = db_location
        self.db_creation_queries = [
            # Create the Students table
            '''
            CREATE TABLE IF NOT EXISTS Students (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
            ''',
            # Create the Classes table
            '''
            CREATE TABLE IF NOT EXISTS Classes (
                id INTEGER PRIMARY KEY,
                subject TEXT,
                name TEXT NOT NULL
            )
            ''',
            # Create the Lessons table
            '''
            CREATE TABLE IF NOT EXISTS Lessons (
                id INTEGER PRIMARY KEY,
                date TEXT NOT NULL,
                class_id INTEGER,
                FOREIGN KEY (class_id) REFERENCES Classes (id)
            )
            ''',
            # Create the Attendance table
            '''
            CREATE TABLE IF NOT EXISTS Attendance (
                id INTEGER PRIMARY KEY,
                student_id INTEGER,
                lesson_id INTEGER,
                attendance_status BOOL NOT NULL,
                FOREIGN KEY (student_id) REFERENCES Students (id),
                FOREIGN KEY (lesson_id) REFERENCES Lessons (id)
            )
            '''
        ]
        self.conn = self.init_db()
    def close(self):
        self.conn.close()

    def init_db(self):
        # Connect to the database or create a new one
        conn = sqlite3.connect(self.db_location)
        for query in self.db_creation_queries:
            conn.execute(query)
        # Commit the changes and return the connection
        conn.commit()
        return conn
        # conn.close()

    def add_student(self, student_id, name):
        """
        Add a new student to the Students table
        """
        try:
            sql = "INSERT INTO Students (id, name) VALUES (?, ?)"
            self.conn.execute(sql, (student_id, name))
            self.conn.commit()
            print("Student added successfully.")
            return True
        except sqlite3.IntegrityError:
            print("Error: Student ID already exists.")
            return False

    def add_class(self, subject, name):
        """
        Add a new class to the Classes table
        """
        sql = "INSERT INTO Classes (subject, name) VALUES (?, ?)"
        self.conn.execute(sql, (subject, name))
        self.conn.commit()

    def add_lesson(self, date, class_id):
        """
        Add a new lesson to the Lessons table
        """
        sql = "INSERT INTO Lessons (date, class_id) VALUES (?, ?)"
        self.conn.execute(sql, (date, class_id))
        self.conn.commit()

    def add_attendance(self, student_id, lesson_id, attendance_status):
        """
        Add a new attendance record to the Attendance table
        """
        sql = "INSERT INTO Attendance (student_id, lesson_id, attendance_status) VALUES (?, ?, ?)"
        self.conn.execute(sql, (student_id, lesson_id, attendance_status))
        self.conn.commit()
    def get_students(self):
        """
        Return the content of the Students table as a dictionary
        """
        sql = "SELECT * FROM Students"
        cursor = self.conn.execute(sql)
        columns = [column[0] for column in cursor.description]
        students = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return students

    def get_classes(self):
        """
        Return the content of the Classes table as a dictionary
        """
        sql = "SELECT * FROM Classes"
        cursor = self.conn.execute(sql)
        columns = [column[0] for column in cursor.description]
        classes = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return classes

    def get_lessons(self):
        """
        Return the content of the Lessons table as a dictionary
        """
        sql = "SELECT * FROM Lessons"
        cursor = self.conn.execute(sql)
        columns = [column[0] for column in cursor.description]
        lessons = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return lessons

    def get_attendance(self):
        """
        Return the content of the Attendance table as a dictionary
        """
        sql = "SELECT * FROM Attendance"
        cursor = self.conn.execute(sql)
        columns = [column[0] for column in cursor.description]
        attendance = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return attendance

    def remove_student(self, student_id):
        """
        Remove a student from the Students table
        """
        sql = "DELETE FROM Students WHERE id = ?"
        self.conn.execute(sql, (student_id,))
        self.conn.commit()

    def remove_class(self, class_id):
        """
        Remove a class from the Classes table
        """
        sql = "DELETE FROM Classes WHERE id = ?"
        self.conn.execute(sql, (class_id,))
        self.conn.commit()

    def remove_lesson(self, lesson_id):
        """
        Remove a lesson from the Lessons table
        """
        sql = "DELETE FROM Lessons WHERE id = ?"
        self.conn.execute(sql, (lesson_id,))
        self.conn.commit()

    def remove_attendance(self, attendance_id):
        """
        Remove an attendance record from the Attendance table
        """
        sql = "DELETE FROM Attendance WHERE id = ?"
        self.conn.execute(sql, (attendance_id,))
        self.conn.commit()
def test_addition(db_handler):

    # Add a student
    db_handler.add_student(1, "John Doe")

    # Add a class
    db_handler.add_class("Mathematics", "Math Sunday")

    # Add a lesson
    db_handler.add_lesson("2023-06-27", 1)

    # Add an attendance record
    db_handler.add_attendance(1, 1, True)

def test_removal(db_handler):

    # Remove a student
    db_handler.remove_student(1)

    # Remove a class
    db_handler.remove_class(1)

    # Remove a lesson
    db_handler.remove_lesson(1)

    # Remove an attendance record
    db_handler.remove_attendance(1)

    # Close the connection
    conn.close()
if __name__ == "__main__":
    db_handler = DBHandler()
    print("students: \n", db_handler.get_students())
    print("lessons: \n" , db_handler.get_lessons())
    print("classes: \n" , db_handler.get_classes())
    print("attendance: \n" , db_handler.get_attendance())
    # test_addition(db_handler)
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
                class_id INTEGER,
                lesson_number INT NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (class_id) REFERENCES Classes (id),
                PRIMARY KEY (class_id, lesson_number)
            );
            ''',
            # Create the Attendance table
            '''
            CREATE TABLE IF NOT EXISTS Attendance (
                id INTEGER PRIMARY KEY,
                student_id INTEGER,
                class_id INTEGER,
                lesson_number INTEGER,
                attendance_status BOOL NOT NULL,
                FOREIGN KEY (student_id) REFERENCES Students (id),
                FOREIGN KEY (class_id, lesson_number) REFERENCES Lessons (class_id, lesson_number)
            );
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
        sql = "SELECT COALESCE(MAX(lesson_number), 0) + 1 FROM Lessons WHERE class_id = ?"
        cursor = self.conn.execute(sql, (class_id,))
        lesson_number = cursor.fetchone()[0]
        print("lesson number: ",lesson_number)
        sql = "INSERT INTO Lessons (date, class_id, lesson_number) VALUES (?, ?, ?)"
        self.conn.execute(sql, (date, class_id, lesson_number))
        self.conn.commit()

    def add_attendance(self, student_id, class_id, lesson_number, attendance_status):
        """
        Add a new attendance record to the Attendance table
        """
        if(lesson_number == -1):
            lesson_number = self.get_last_lesson(class_id)

        sql = "INSERT INTO Attendance (student_id, class_id, lesson_number, attendance_status) VALUES (?, ?, ?, ?)"
        self.conn.execute(sql, (student_id, class_id, lesson_number, attendance_status))
        self.conn.commit()
    def set_attendance(self, student_id, class_id, lesson_number, attendance_status):
        print(
                student_id,
                class_id,
                lesson_number, 
                attendance_status
            )
        sql = f"""
            UPDATE Attendance
            SET attendance_status = {attendance_status}
            WHERE student_id = {student_id} AND class_id = {class_id} AND lesson_number = {lesson_number};
        """
        self.conn.execute(sql)
        self.conn.commit()
    
    def get_students(self,class_id=None):
        """
        Return the content of the Students table as a dictionary
        """
        # sql = """
        #     SELECT DISTINCT s.id AS student_id, s.name AS student_name, l.id AS lessons_id
        #     FROM Classes c
        #     JOIN Lessons l ON c.id = l.class_id
        #     JOIN Attendance a ON l.id = a.lesson_id
        #     JOIN Students s ON a.student_id = s.id
        # """
        sql = f"""SELECT s.id AS student_id, s.name AS student_name, c.id as class_id, GROUP_CONCAT(a.attendance_status) AS attendance_records
            FROM Classes c
            JOIN Lessons l ON c.id = l.class_id
            JOIN Attendance a ON l.class_id = a.class_id AND l.lesson_number = a.lesson_number
            JOIN Students s ON a.student_id = s.id
            WHERE c.id = {class_id}
            GROUP BY s.id, s.name;
            """
        # if(class_id):
        #     print(class_id)
        #     sql+= f"\nWHERE c.id = {class_id}"
        cursor = self.conn.execute(sql)
        columns = [column[0] for column in cursor.description]
        students = [dict(zip(columns, row)) for row in cursor.fetchall()]
        for student in students:
            attendance_str = student['attendance_records']
            attendance_array = [bool(int(status)) for status in attendance_str.split(',')]
            student['attendance_records'] = attendance_array
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

    def get_lessons(self,class_id):
        """
        Return the content of the Lessons table as a dictionary
        """
        sql = f"""
            SELECT lesson_number, date
            FROM Lessons
            WHERE class_id = {class_id};
        """
        cursor = self.conn.execute(sql)
        columns = [column[0] for column in cursor.description]
        lessons = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return lessons
    def get_last_lesson(self,class_id):
        """
        Return the last lesson number
        """
        sql = f"""
            SELECT MAX(lesson_number) AS last_lesson_number
            FROM Lessons
            WHERE class_id = {class_id};
        """
        cursor = self.conn.execute(sql)
        lesson_number = cursor.fetchall()[0][0]
        return lesson_number
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
    def check_exist(self, student_id, class_id):
        sql = f"""
        SELECT CASE WHEN COUNT(*) > 0 THEN 1 ELSE 0 END AS has_attendance
        FROM Attendance
        WHERE student_id = {student_id} AND class_id = {class_id};
        """
        cursor = self.conn.execute(sql)
        exist = cursor.fetchall()[0][0]
        return exist
def test_addition(db_handler):

    # Add a student
    db_handler.add_student(1, "John Doe")
    db_handler.add_student(2, "Jane Doe")

    # Add a class
    db_handler.add_class("Mathematics", "Math Sunday")
    db_handler.add_class("Physics", "Physics Monday")

    # Add a lesson
    db_handler.add_lesson("2023-06-27", 1)
    db_handler.add_lesson("2023-06-28", 1)
    db_handler.add_lesson("2023-06-29", 1)
    db_handler.add_lesson("2023-06-30", 1)
    db_handler.add_lesson("2023-06-28", 2)
    db_handler.add_lesson("2023-06-29", 2)

    # Add an attendance record
    db_handler.add_attendance(1, 1,1, True)
    db_handler.add_attendance(1, 1,2, False)
    db_handler.add_attendance(1, 1,3, True)
    db_handler.add_attendance(1, 1,4, True)
    db_handler.add_attendance(2, 1,1, False)
    db_handler.add_attendance(2, 1,2, False)
    db_handler.add_attendance(2, 1,3, True)
    # db_handler.add_attendance(2, 1,2, False)
    db_handler.add_attendance(2, 2,1, True)
    db_handler.add_attendance(2, 2,2, True)

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
    # print("students: \n", db_handler.get_students())
    # print("lessons: \n" , db_handler.get_lessons())
    # print("classes: \n" , db_handler.get_classes())
    # print("attendance: \n" , db_handler.get_attendance())

    # db_handler.add_attendance(2, 1, True)
    test_addition(db_handler)
    # db_handler.add_lesson("today",1)
    # print(db_handler.get_classes())
    # db_handler.set_attendance(2,2,3, False)
    for item in db_handler.get_students(2):
        print(item)
    # for item in db_handler.get_lessons(1):
    #     print(item)
    # print(db_handler.get_last_lesson(1))
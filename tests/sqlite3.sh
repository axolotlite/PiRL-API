#!/bin/bash
# list tables
sqlite3 data/attendance.db .tables .schema
output="Attendance  Classes     Lessons     Students  
CREATE TABLE Students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );
CREATE TABLE Classes (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );
CREATE TABLE Lessons (
        id INTEGER PRIMARY KEY,
        date TEXT NOT NULL,
        class_id INTEGER,
        FOREIGN KEY (class_id) REFERENCES Classes (id)
    );
CREATE TABLE Attendance (
        id INTEGER PRIMARY KEY,
        student_id INTEGER,
        lesson_id INTEGER,
        attendance_status TEXT NOT NULL,
        FOREIGN KEY (student_id) REFERENCES Students (id),
        FOREIGN KEY (lesson_id) REFERENCES Lessons (id)
    );"

#test adding records
for table in $(sqlite3 data/attendance.db .tables); do echo "$table: ";sqlite3 data/attendance.db "SELECT * FROM $table;"; done;
output="1|1|1|Present
1|Mathematics
1|2023-06-27|1
1|John Doe"
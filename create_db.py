import sqlite3
import os
import sys
databaseexisted = os.path.isfile('schedule.db')

dbcon = sqlite3.connect('schedule.db')


def print_table(list_of_tuples):
    for item in list_of_tuples: print(item)



with dbcon:
    cursor = dbcon.cursor()
    if not databaseexisted:  # First time creating the database. Create the tables
        cursor.execute(
            "CREATE TABLE courses(id INTEGER PRIMARY KEY, course_name TEXT NOT NULL,student TEXT NOT NULL,number_of_students INTEGER NOT NULL,class_id INTEGER REFERENCES classrooms(id),course_length INTEGER NOT NULL)")  # create table courses
        cursor.execute("CREATE TABLE students(grade TEXT PRIMARY KEY ,count INTEGER NOT NULL)")  # create table students
        cursor.execute(
            "CREATE TABLE classrooms(id INTEGER PRIMARY KEY ,location TEXT NOT NULL,current_course_id INTEGER NOT NULL,current_course_time_left INTEGER NOT NULL)")  # create table students


    def main(args):
        cursor.execute("SELECT * FROM courses")
        courses = cursor.fetchall()
        if(len(courses) is not 0):
            return
        inputfilename = args[1]
        if not os.path.isfile(inputfilename):  # check if file exists
            return

        with open(inputfilename) as input_file:  # try-with-resources
            for line in input_file:
                if line[-1] == '\n':
                    line = line[:-1]

                words = line.split(', ')
                if words[0] == "S":
                    cursor.execute("INSERT INTO students VALUES(?,?)", (words[1], words[2]))
                elif words[0] == "R":
                    cursor.execute("INSERT INTO classrooms VALUES(?,?,?,?)", (words[1], words[2], 0, 0))
                else:
                    cursor.execute("INSERT INTO courses VALUES(?,?,?,?,?,?)",
                                   (words[1], words[2], words[3], words[4], words[5], words[6]))

        cursor.execute("SELECT * FROM courses")
        courses = cursor.fetchall()
        print("courses")
        print_table(courses)
        cursor.execute("SELECT * FROM classrooms")
        classrooms_list = cursor.fetchall()
        print("classrooms")
        print_table(classrooms_list)
        cursor.execute("SELECT * FROM students")
        students_list = cursor.fetchall()
        print("students")
        print_table(students_list)
        dbcon.commit()
if __name__ == '__main__':
    main(sys.argv)

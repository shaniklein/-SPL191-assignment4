import sqlite3
import os
from sqlite3.dbapi2 import Cursor


def main():
    dbcon = sqlite3.connect('schedule.db')
    with dbcon:
        cursor = dbcon.cursor()
        cursor.execute("SELECT * FROM courses")
        courses_list = cursor.fetchall()
        if(len(courses_list) is 0 ):
            print("courses")
            print_table(courses_list)
            cursor.execute("SELECT * FROM classrooms")
            classrooms_list = cursor.fetchall()
            print("classrooms")
            print_table(classrooms_list)
            cursor.execute("SELECT * FROM students")
            students_list = cursor.fetchall()
            print("students")
            print_table(students_list)

        i = 0
        while os.path.isfile('schedule.db')and len(courses_list) is not 0:
            cursor: Cursor = dbcon.cursor()
            # cursor.execute("SELECT current_course_time_left,id,location,current_course_id,c FROM classrooms")
            cursor.execute("SELECT * FROM classrooms")
            classrooms_list = cursor.fetchall()

            for classroom in classrooms_list:
                class_id = classroom[0]
                location = classroom[1]
                current_course_id = classroom[2]
                current_course_time_left = classroom[3]

                cursor.execute("SELECT course_name FROM courses WHERE class_id=?", [class_id])
                current_course_name = cursor.fetchone()
                if current_course_name is None:
                    continue
                current_course_name=current_course_name[0]
                # if we need to update the time that left, if it will be zero we need to put new curse
                if current_course_time_left > 1:
                    print("({}) {}: occupied by {}".format(i, location, current_course_name))
                    current_course_time_left = current_course_time_left-1
                    cursor.execute("UPDATE classrooms SET current_course_time_left=? WHERE current_course_id=? ",[current_course_time_left,current_course_id])

                else:  # current_course_time_left is 0:
                    if current_course_id is not 0:
                        # if course is finish
                        print("({}) {}: {} is done".format(i, location, current_course_name))
                        cursor.execute("DELETE FROM courses WHERE id=?",[current_course_id])
                    # available class- add course
                    cursor.execute("SELECT * FROM courses WHERE class_id=?", [class_id])

                    course=cursor.fetchone()
                    if course is None:
                        cursor.execute("UPDATE classrooms SET current_course_id=?, current_course_time_left=? WHERE current_course_id=?", [0, 0, current_course_id])  # if there is no courses that want this class

                    else:
                        next_course_id = course[0]
                        next_course_length = course[5]
                        next_course_name = course[1]
                        next_class_id=course[4]
                        next_course_student_type = course[2]
                        number_of_students=course[3]

                        cursor.execute("SELECT count FROM students WHERE grade= ?" , [next_course_student_type])
                        current_count = cursor.fetchone()[0] - number_of_students
                        cursor.execute("UPDATE classrooms SET current_course_id=?, current_course_time_left=? WHERE id=?", [next_course_id,next_course_length,next_class_id])
                        print("({}) {}: {} is schedule to start".format(i, location, next_course_name))
                        # update the count of the student after opening new course
                        cursor.execute("UPDATE students SET count=? WHERE grade=?",[current_count, next_course_student_type])

                dbcon.commit()

            cursor.execute("SELECT * FROM courses")
            courses_list = cursor.fetchall()
            print("courses")
            print_table(courses_list)
            cursor.execute("SELECT * FROM classrooms")
            classrooms_list = cursor.fetchall()
            print("classrooms")
            print_table(classrooms_list)
            cursor.execute("SELECT * FROM students")
            students_list = cursor.fetchall()
            print("students")
            print_table(students_list)
            i += 1


def print_table(list_of_tuples):
    for item in list_of_tuples: print(item)


if '__main__' == __name__:
    main()

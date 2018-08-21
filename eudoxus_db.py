import sqlite3
import os.path
import re

DBNAME = 'eudoxus_db'

def find_db():
    dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir, DBNAME)

def create_db():
    print('create new db', DBNAME)
    sql = [
        'CREATE TABLE history (id INTEGER PRIMARY KEY, year TEXT, date TEXT);',
        'CREATE TABLE unis (id INTEGER PRIMARY KEY, name TEXT);',
        'CREATE TABLE programs (id INTEGER PRIMARY KEY, name TEXT, year TEXT, uni INTEGER);',
        'CREATE TABLE books (code TEXT PRIMARY KEY, title TEXT, author TEXT, publisher TEXT);',
        'CREATE TABLE books_courses (course_id INTEGER, book_id INTEGER, rank NUMERIC);',
        'CREATE TABLE courses (id INTEGER PRIMARY KEY, code TEXT, name TEXT, prog_id INTEGER, semester NUMERIC, spring_winter TEXT);',
        'CREATE INDEX books_index ON books(code ASC);',
        'CREATE INDEX courses_index ON courses(id ASC);',
        'CREATE INDEX programs_index ON programs(id ASC);']
    try:
        con = sqlite3.connect(DBNAME)
        with con:
            c = con.cursor()
            for table in sql:
                print("executing...", table)
                print(c.execute(table))  # create tables
            con.commit()
    except sqlite3.Error as e:
        print('Σφάλμα στο άνοιγμα βάσης δεδομένων', DBNAME, e)

def query(sql):
    try:
        con = sqlite3.connect(find_db())
        with con:
            c = con.cursor()
            result = c.execute(sql)  # execute sql
            con.commit()
            return result.fetchall()
    except sqlite3.Error as e:
        print('Σφάλμα στο άνοιγμα βάσης δεδομένων', DBNAME, e)
        return False

def insert_uni(name):
    try:
        con = sqlite3.connect(find_db())
        with con:
            c = con.cursor()
            result = c.execute("select * from unis where name='{}';".format(name))
            found = c.fetchall()
            print(found)
            if found:
                print(name, "already in db")
                return found[0][0]
            else:
                sql = "insert into unis (name) values ('{}');".format(name)
                c.execute(sql)
                uni_id = c.lastrowid
                con.commit()
                return uni_id
    except sqlite3.Error as e:
        print('Σφάλμα στο άνοιγμα βάσης δεδομένων', DBNAME, e)
        return False

def insert_program(name, year, uni):
    print(name, year, uni)
    try:
        con = sqlite3.connect(find_db())
        with con:
            c = con.cursor()
            result = c.execute("select * from programs where name='{}' and uni='{}' and year='{}';".format(name, uni, year))
            found = c.fetchall()
            print(found)
            if found:
                print(name, "already in db")
                return found[0][0]
            else:
                sql = "insert into programs (name, year, uni) values ('{}','{}','{}');".format(name, year, uni)
                c.execute(sql)
                prog_id = c.lastrowid
                con.commit()
                return prog_id
    except sqlite3.Error as e:
        print('Σφάλμα στο άνοιγμα βάσης δεδομένων', DBNAME, e)
        return False

def insert_course(code, name, prog_id, sem):
    if sem:
        semester = re.findall(r"ΕΞΆΜΗΝΟ (.+?) ", sem, re.I)[0]
        spring_winter = sem.split()[-1]
    else: semester, spring_winter = 0,""
    #print(code, name, prog_id, semester, spring_winter)
    try:
        con = sqlite3.connect(find_db())
        with con:
            c = con.cursor()
            result = c.execute("select * from courses where name='{}' and code='{}' and prog_id='{}';".format(name, code, prog_id))
            found = c.fetchall()
            #print(found)
            if found:
                print(name, "already in db")
                return found[0][0]
            else:
                sql = "insert into courses (code, name, prog_id, semester, spring_winter) values ('{}','{}','{}','{}','{}');"
                sql = sql.format(code, name, prog_id, semester, spring_winter)
                c.execute(sql)
                prog_id = c.lastrowid
                con.commit()
                return prog_id
    except sqlite3.Error as e:
        print('Σφάλμα στο άνοιγμα βάσης δεδομένων', DBNAME, e)
        return False

def insert_book(code, course_id, title, rank, author="", publisher=""):
    #print(code, course_id, title, rank)
    try:
        con = sqlite3.connect(find_db())
        with con:
            c = con.cursor()
            result = c.execute("select * from books where code='{}';".format(code))
            found = c.fetchall()
            #print(found)
            if found:
                print(title, "already in db")
                book_id = found[0][0]
            else:
                sql = "insert into books (code, title) values ('{}','{}');".format(code, title.strip())
                c.execute(sql)
                book_id = code
                con.commit()
            # check also books_courses table
            result = c.execute("select * from books_courses where book_id='{}' and course_id='{}';".format(code, course_id))
            found = c.fetchall()
            #print(found)
            if found:
                print(title, "already in db for course_id = ", course_id)
            else:
                sql = "insert into books_courses (course_id, book_id, rank) values ('{}','{}', {});".format(course_id, code, rank)
                c.execute(sql)
                course_book_id = c.lastrowid
                con.commit()
                return course_book_id
    except sqlite3.Error as e:
        print('Σφάλμα στο άνοιγμα βάσης δεδομένων', DBNAME, e)
        return False
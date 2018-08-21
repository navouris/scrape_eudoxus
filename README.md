# scrape_eudoxus
Python script for downloading an offline version of the eudoxus database of Programs, courses, textbooks for a set academic year 
(eudoxus.gr)
To be used for research on the Greek higher education system. (e.g. textbooks, for a specific course accross institutions).

<bold>Instructions<\bold>

It has been tested with python 3.x
Download bs4 library (instructions at https://pypi.org/project/beautifulsoup4/)
Run the script scrape_eudoxus.py
The script asks for the academic year (use any number between 2012 and current year) and downloads entries in an sqlite3 database 
for that academic year, using beautifulsoup4 for scraping the corresponding web pages.

It creates a database eudoxus_db in the same directory of the script.

The schema of the database is as follows:
'CREATE TABLE history (id INTEGER PRIMARY KEY, year TEXT, date TEXT);',
'CREATE TABLE unis (id INTEGER PRIMARY KEY, name TEXT);',
'CREATE TABLE programs (id INTEGER PRIMARY KEY, name TEXT, year TEXT, uni INTEGER);',
'CREATE TABLE books (code TEXT PRIMARY KEY, title TEXT, author TEXT, publisher TEXT);',
'CREATE TABLE books_courses (course_id INTEGER, book_id INTEGER, rank NUMERIC);',
'CREATE TABLE courses (id INTEGER PRIMARY KEY, code TEXT, name TEXT, prog_id INTEGER, semester NUMERIC, spring_winter TEXT);',
'CREATE INDEX books_index ON books(code ASC);',
'CREATE INDEX courses_index ON courses(id ASC);',
'CREATE INDEX programs_index ON programs(id ASC);'

One may use tools like DB Browser for SQLite (https://sqlitebrowser.org/) for querying the database, or build and run scripts 
for a particular project. 

An example of such script is documented in Avouris (2018), in preparation for PCI 2018, Athens, November 2018.

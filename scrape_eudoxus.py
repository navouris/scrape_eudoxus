# eudoxus scraper N.Avouris, August 2018, to move entire eudoxus data for a [year] to database
from bs4 import BeautifulSoup
import os.path
import urllib.request
import re
import time
import eudoxus_db
YEAR = '2018'
DEBUG = False

def find_courses_and_books(url2, prog_id, uni, acad_year):
    # version 1 implementation with beautiful soup
    print(prog_id, "\n", url2)
    try:
        with urllib.request.urlopen(url2) as response:
            html = response.read()
    except:
        print('unable to open', url2, prog_id)
        return False
    soup = BeautifulSoup(html, "lxml")
    for tag in soup.find_all('h2'):
        if "Μάθημα" in tag.get_text():
            c = tag.get_text()
            course = c.split(':')[1]
            course_code = re.findall(r'\[(.*?)\]', c)
            if course_code: course_code = course_code[0]
            else: course_code = ' '
            course_data = tag.find_next_siblings("h3")[0]
            course_data = course_data.get_text()
            # sem = re.findall(r"Εξάμηνο ([0-9]+) ", course_data, re.I)[0]
            # winter_spring = course_data.split()[-1]
            c_id = eudoxus_db.insert_course(course_code, upper_term(course.strip()), prog_id, course_data)
            books = tag.find_next_siblings("ol")[0]
            thebooks = books.find_all('ul')
            book_rank = 1
            for b in thebooks:
                thebook = b.get_text()
                print("thebook ...", thebook)
                book_code = re.findall(r"\[(.+?)\]", thebook, re.I)[0]
                print("book code ....", book_code)
                book_title = re.findall(r":(.+?)\bΛεπτομέρειες", thebook.replace('\n',''), re.I)[0]
                print("book title ....", book_title)
                eudoxus_db.insert_book(book_code, c_id, upper_term(book_title), book_rank)
                book_rank += 1

####### main ##################################################################

def search_in_evdoxos(acad_year):
    import time
    start = time.time()
    #url1 = input("Enter a website to extract the URL's from: ")
    url1 = r'https://service.eudoxus.gr/public/departments'
    # print(url1)

    print("Αναζήτηση στις σελίδες του eudoxus  ... {} ".format(acad_year))

    with urllib.request.urlopen(url1) as response:
        h  = response.read().decode('utf-8')
    soup = BeautifulSoup(h, "lxml" )
    #count all departmnets
    d = 0
    for tag in soup.find_all('p'): d += 1
    print (" ... all programs of study to be searched are: ", d)
    d1=0
    uni, dept = '', ''
    for tag in soup.find_all():
        if tag.name == 'h2' and tag.get_text() not in ['Λίστα Ιδρυμάτων και Τμημάτων', 'Περιεχόμενα']:
            uni_ = tag.get_text()
            if uni_ != uni:
                uni = uni_
                print(uni)
                uni_id = eudoxus_db.insert_uni(uni)
                if uni_id: print(uni, " id=", uni_id)
        if tag.name == 'p' and uni != '':
            dept_ = tag.get_text()
            if dept_ != dept:
                d1 += 1
                dept = dept_
                print('\t\t{:.1f}% {}'.format(100*d1/d, dept))
        if tag.name == 'a' and tag.get_text() == acad_year:
            url2 = tag['href']
            url2= "https://service.eudoxus.gr"+url2
            # search in url2
            prog_id = eudoxus_db.insert_program(upper_term(dept), YEAR, uni_id)
            if prog_id: print("κωδ. Προγράμματος, id=", prog_id)
            find_courses_and_books(url2, prog_id, uni_id, acad_year)

def remove_tonos(st):
    tonoi = {'ά':'α', 'έ':'ε', 'ή':'η', 'ί':'ι', 'ό':'ο', 'ύ':'υ', 'ώ':'ω'}
    atono_st = ''
    for ch in st.lower():
        if ch in tonoi: atono_st += tonoi[ch]
        elif ord(ch) == 769 : continue # remove COMBINING ACUTE ACCENT oxia character
        else : atono_st += ch
    return atono_st

def upper_term(term):
    term = remove_tonos(term.lower())
    return(term.upper())

######################################################################################
if __name__ == '__main__':
    while True:
        y = input('Επιλέξτε ακαδ. έτος [{}] - x για έξοδο - ... '.format(YEAR))
        if y.upper() == 'X' or y.upper() == 'Χ': break
        if y != '': YEAR = y
        if int(YEAR) >= 2011 and int(YEAR) <= 2030: # αποδεκτά ακαδ. έτη
            acad_year = str(int(YEAR) - 1) + " - " + str(YEAR)
            acad_year = 'Πρόγραμμα Σπουδών (' + acad_year + ")"
            print("Academic year = ", acad_year)
            if not os.path.isfile(eudoxus_db.DBNAME):
                eudoxus_db.create_db()
            if eudoxus_db.query("select * from history where year={};".format(YEAR)):
                # Η αναζήτηση αυτή υπάρχει ήδη στην βάση δεδομένων
                print("data found")
                #TODO to implement a db based search
            else:
                search_in_evdoxos(acad_year)
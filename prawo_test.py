import mysql.connector
import random
#Connecting with mysql
db = mysql.connector.connect(
          host="localhost",
          user="root",
          passwd="Ezmysql@1",
          database="producto"
)

#Adding a mysql cursor
cursor = db.cursor()

#Importing data from mysql into lists
pytanie = []
media = []
odpowiedz_a, odpowiedz_b, odpowiedz_c = [],[],[]
poprawna_odpowiedz = []
cursor.execute("SELECT Pytanie FROM pytania_egzminacyjne WHERE Kategorie LIKE '%B%' ")
for question in cursor:
          pytanie.append(question)

cursor.execute("SELECT Media FROM pytania_egzminacyjne WHERE Kategorie LIKE '%B%' ")
for m in cursor:
          media.append(m)

cursor.execute("SELECT `Odpowiedź A` FROM pytania_egzminacyjne WHERE Kategorie LIKE '%B%' ")
for a in cursor:
          odpowiedz_a.append(a)

cursor.execute("SELECT `Odpowiedź B` FROM pytania_egzminacyjne WHERE Kategorie LIKE '%B%' ")
for b in cursor:
          odpowiedz_b.append(b)

cursor.execute("SELECT `Odpowiedź C` FROM pytania_egzminacyjne WHERE Kategorie LIKE '%B%' ")
for c in cursor:
          odpowiedz_c.append(c)

cursor.execute("SELECT `Poprawna odp` FROM pytania_egzminacyjne WHERE Kategorie LIKE '%B%' ")
for po in cursor:
          poprawna_odpowiedz.append(po)

#Selecting 40 random questions
print(str(media[0]).strip("(),"))
is_changed = False
nr_pytan = []
for _ in range(40):
          i = random.randint(0,2014)
          while(not is_changed):
                    if(i not in nr_pytan):
                              is_changed = True
                    else:
                              i = random.randint(0,2014)
          nr_pytan.append(i)
print(str(media[nr_pytan[0]]).strip("(),'"))
import mariadb
import random

#Connecting with mysql
db = mariadb.connect(
          host="127.0.0.1",
          user="root",
          passwd="Ezmariadb@1",
          database="mysql",
          port=3307
)

#Adding a mysql cursor
cursor = db.cursor()

#Importing data from mysql into lists
pytanie = []
media = []
odpowiedz_a, odpowiedz_b, odpowiedz_c = [],[],[]
poprawna_odpowiedz = []
wylosowano = []
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

#Selecting 32 random questions
print(str(media[0]).strip("(),"))
is_changed = False
nr_pytan = []
for _ in range(20):
          i = random.randint(0,2017)
          is_changed = False
          while(not is_changed):
                    if(i not in nr_pytan):
                              if(str(str(poprawna_odpowiedz[i]).strip("(),'")).strip("(),'") == "Tak" or str(poprawna_odpowiedz[i]).strip("(),'") == "Nie"):
                                        is_changed = True
                              else:
                                        i = random.randint(0,2017)
                    else:
                              i = random.randint(0,2017)
          nr_pytan.append(i)

for _ in range(12):
          i = random.randint(0,2017)
          is_changed = False
          while(not is_changed):
                    if(i not in nr_pytan):
                              if(str(poprawna_odpowiedz[i]).strip("(),'") == "A" or str(poprawna_odpowiedz[i]).strip("(),'") == "B" or str(poprawna_odpowiedz[i]).strip("(),'") == "C"):
                                        is_changed = True
                              else:
                                        i = random.randint(0,2017)
                    else:
                              i = random.randint(0,2017)
          nr_pytan.append(i)

for j in range(len(nr_pytan)):
          sting = f"UPDATE pytania_egzminacyjne SET Wylosowano = Wylosowano + 1 WHERE Pytanie = {str(pytanie[nr_pytan[j]]).strip("(),")}"
          cursor.execute(sting)
          db.commit()

cursor.execute("SELECT Wylosowano FROM pytania_egzminacyjne WHERE Kategorie LIKE '%B%' ")
for los in cursor:
          wylosowano.append(los)
# db.close()
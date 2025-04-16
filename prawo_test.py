import mariadb
import random

filepath = "dbconnection.txt"
content = []

with open(filepath, "r") as file:
          for line in file:
                    content.append(line.rstrip())

#Connecting with mysql
db = mariadb.connect(
          host=content[0],
          user=content[1],
          passwd=content[2],
          database=content[3],
          port=int(content[4])
)

#Adding a mysql cursor
cursor = db.cursor()

#Importing data from mysql into lists
pytanie = []
media = []
odpowiedz_a, odpowiedz_b, odpowiedz_c = [],[],[]
poprawna_odpowiedz = []
wylosowano, wylosowano_przed = [],[]
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

cursor.execute("SELECT Wylosowano FROM pytania_egzminacyjne WHERE Kategorie LIKE '%B%' ")
for los_p in cursor:
          wylosowano_przed.append(los_p)

#Selecting 32 random questions
print(str(media[0]).strip("(),"))
is_changed = False
nr_pytan = []
for _ in range(20):
          i = random.randint(0,2017)
          is_changed = False
          while(not is_changed):
                    if(i not in nr_pytan):
                              if(str(poprawna_odpowiedz[i]).strip("(),'") == "Tak" or str(poprawna_odpowiedz[i]).strip("(),'") == "Nie"):
                                        for o in range(0,2017):
                                                  if (int(str(wylosowano_przed[o]).strip("(),'")) < int(str(wylosowano_przed[i]).strip("(),'")) and (str(poprawna_odpowiedz[o]).strip("(),'") == "Tak" or str(poprawna_odpowiedz[o]).strip("(),'") == "Nie") and o not in nr_pytan):
                                                            i = o
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
                                        for o in range(0,2017):
                                                  if (int(str(wylosowano_przed[o]).strip("(),'")) < int(str(wylosowano_przed[i]).strip("(),'")) and (str(poprawna_odpowiedz[o]).strip("(),'") == "A" or str(poprawna_odpowiedz[o]).strip("(),'") == "B" or str(poprawna_odpowiedz[o]).strip("(),'") == "C") and o not in nr_pytan):
                                                            i = o
                                        is_changed = True
                              else:
                                        i = random.randint(0,2017)
                    else:
                              i = random.randint(0,2017)
          nr_pytan.append(i)

for j in range(len(nr_pytan)):
          sting = f"UPDATE pytania_egzminacyjne SET Wylosowano = Wylosowano + 1 WHERE Pytanie = {str(pytanie[nr_pytan[j]]).strip("(),")} AND `Odpowiedź A` = {str(odpowiedz_a[nr_pytan[j]]).strip("(),")} AND `Odpowiedź B` = {str(odpowiedz_b[nr_pytan[j]]).strip("(),")} AND `Odpowiedź C` = {str(odpowiedz_c[nr_pytan[j]]).strip("(),")} AND `Poprawna odp` = {str(poprawna_odpowiedz[nr_pytan[j]]).strip("(),")} AND Media = {str(media[nr_pytan[j]]).strip("(),")}"
          cursor.execute(sting)
          db.commit()

cursor.execute("SELECT Wylosowano FROM pytania_egzminacyjne WHERE Kategorie LIKE '%B%' ")
for los in cursor:
          wylosowano.append(los)
# db.close()
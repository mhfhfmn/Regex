from pprint import pprint
import re
import csv

## модуль проверки данных в новом файле

with open("phonebook.csv") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)



pprint(contacts_list)


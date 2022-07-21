from pprint import pprint
import re
import csv

phone_pattern = re.compile(r'(\+7|8)\s*\(?(\d{3})\)?(\s*|-)(\d{3})(\s*|-*)(\d{2})-?(\d{2})(\s*(\(?(\доб.)?)\s*(\d{4}))?(\))*')


## читаем адресную книгу в формате CSV в список contacts_list

with open("phonebook_raw.csv") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)


## TODO 1: выполните пункты 1-3 ДЗ
## ваш код

contact_data = contacts_list[1::]
contact_headers = contacts_list[0]


## Усложним задачу, пусть один контакт повторяется несколько раз;
## Во всех примерах решения этой задачи, которые мне попадались
## логика опиралась на то, что запись будет повторяться 2 раза, а при добавлении
## еще одного повторения код переставал правильно работать.

contact_data.append(['Мартиняхин', 'Виталий', 'Геннадьевич', '', '', '+74959130000', 'mail_1@mail.com'])
contact_data.append(['Мартиняхин', 'Виталий', 'Геннадьевич', 'ФНС', '', '', 'mail@mail.com'])
contact_data.append(['Ярин Виталий', '', '', 'ФНС', '', '', 'mail@mail.com'])
contact_data.append(['Ярин Виталий', 'Валентинович', '', 'ФСС', '', '89265437698 доб. 2044', ''])


## Функция возвращает список Фамилия-Имя-Отчество

def get_correct_name():
    correct_name = []
    for contacts in contact_data:
        full_name = str(contacts[0:3])
        full_name = full_name.replace("'", "")
        full_name = full_name.replace(",", "")
        full_name = full_name.strip('[] ')
        full_name = full_name.split(' ')
        correct_name.append(full_name)
    return correct_name


## Функция возвращает список данных с расставлеными значениями в соответствующиее позиции

def fix_data():
    fixed_data = []
    list_correct_name = get_correct_name()
    index = 0
    for contact in contact_data:
        for record in range(len(list_correct_name[index])):
            contact[record] = list_correct_name[index][record]
        index += 1
        fixed_data.append(contact)
    fixed_data.sort()
    return fixed_data


## Служебная функия для обработки повторяющихся записей
## На вход принимает 2 списка и объединяет их в один

def _twice_record(list1, list2):
    new_list = []
    for index in range(7):
        if list1[index] == '':
            new_list.append(list2[index])
        elif list2[index] == '':
            new_list.append(list1[index])
        else:
            new_list.append(list1[index])
    return new_list


"""
Функция с логикой обработки повторяющихся данных, при определенных условиях мы передаем
повторяющиеся списки в служебную функцию _twice_record()
На выходе имеем список без повторяющихся записей с сохранением данных из каждой
дублирующийся записи
Минус в том, что при разных значениях в столбцах с данными(тел., email и т.д.)
данные берутся из первой записи по порядку после сортировки списка
"""

def double_name_fix():
    data = fix_data()
    fixed_data = []
    fixed_data.append(data[0])
    try:
        for index in range(len(data)):
            if fixed_data[-1][0] == data[index][0] and fixed_data[-1][1] == data[index][1]:
                fixed_data[-1] = _twice_record(fixed_data[-1], data[index + 1])

            elif data[index][0] == data[index + 1][0] and data[index][1] == data[index + 1][1]:
                fixed_data.append(_twice_record(data[index], data[index + 1]))
            else:
                fixed_data.append(data[index])
    except IndexError:
        if fixed_data[-1][0] == data[index][0] and fixed_data[-1][1] == data[index][1]:
            fixed_data[-1] = _twice_record(fixed_data[-1], data[index])
        else:
            fixed_data.append(data[index])
    return fixed_data


## Применяем регулярку

def regular_use():
    contacts_list = double_name_fix()
    for record in contacts_list:
        if record[5] != None:
                record[5] = phone_pattern.sub(r'+7(\2)\4-\6-\7 \10\11', record[5]).strip()
    return contacts_list


## Добавляем header с заголовками

def update_header():
    contact_data = regular_use()
    contact_data.insert(0, contact_headers)
    return contact_data


out_data = update_header()

## TODO 2: сохраните получившиеся данные в другой файл
## код для записи файла в формате CSV
## следует добавить параметр newline='', что бы запись в файл была без пустых строк

with open("phonebook.csv", "w", newline='') as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(out_data)



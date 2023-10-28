from pprint import pprint
## Читаем адресную книгу в формате CSV в список contacts_list:
import csv
import re


def get_data():
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    contacts_list.pop(0)
    return contacts_list


def change_name_phone(contacts_list):
    pattern_fio = r'\s'
    pattern_phone = r'\d+'
    pattern_number = r'(\d{1})(\d{3})(\d{3})(\d{2})(\d{2})(\d{4}|)'
    i = 0
    for el in contacts_list:
        result = re.split(pattern_fio, el[0])
        if len(result) == 3:
            contacts_list[i][0] = result[0]
            contacts_list[i][1] = result[1]
            contacts_list[i][2] = result[2]
        elif len(result) == 2:
            contacts_list[i][0] = result[0]
            contacts_list[i][1] = result[1]
        second_res = re.split(pattern_fio, el[1])
        if len(second_res) == 2:
            contacts_list[i][1] = second_res[0]
            contacts_list[i][2] = second_res[1]
        number = ''.join(re.findall(pattern_phone, el[5]))
        if len(number) <= 11:
            subst = r'+7(\2)\3-\4-\5'
            result_ = re.sub(pattern_number, subst, str(number))
        else:
            subst = r'+7(\2)\3-\4-\5 доб.\6'
            result_ = re.sub(pattern_number, subst, str(number))
        contacts_list[i][5] = result_
        i += 1
    return contacts_list


def delete_dublicate(contacts_list):
    new_dict = {}
    j = 0
    for el in contacts_list:
        fi = el[0] + ' ' + el[1]
        if fi in new_dict:
            i = 0
            for item in contacts_list[j]:
                if item == '':
                    contacts_list[j][i] = contacts_list[new_dict[fi]][i]
                i += 1
            contacts_list.pop(new_dict[fi])
        else:
            new_dict[fi] = j
        j += 1
    return contacts_list


def whrite_change(contacts_list):
    with open("phonebook.csv", "w", encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)


get_data()
change_name_phone(contacts_list=get_data())
delete_dublicate(contacts_list=change_name_phone(contacts_list=get_data()))
whrite_change(contacts_list=delete_dublicate(change_name_phone(contacts_list=get_data())))



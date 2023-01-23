import re
reference_book_structure = [['Second_name'], [
    'First_name'], ['Last_name'], ['Number']]


def Export_data(data):
    data_file = open('reference_book.txt', 'w')
    for i in data:
        for i2 in i:
            data_file.write(str(i2)+'   ')
        data_file.write('\n')


def Import_data():
    data_file = open('reference_book.txt', 'r')
    data = [(line.strip().split()) for line in data_file]
    return data


def print_menu():
    print("Введите номер действия:"+'\n'+"1-Показать все записи"+'\n'+"2-Найти запись по вхождению частей имени"+'\n'+"3-Найти запись по телефону" +
          '\n'+"4-добавить новый контакт"+'\n'+"5-удалить контакт"+'\n'+"6-изменить номер телефона у контакта"+'\n'+"7-Выход")


def Search_by_name(data):
    Display_array = []
    select_contact = input("введите часть имени поиска " +
                           str(data[0][1])+" ")
    for i in data:
        a = re.search(select_contact, i[1])
        if (re.search(select_contact, i[1]) != None):
            Display_array.append(i)
    for i in Display_array:
        for i2 in i:
            print(i2, end=' ')
        print()
    retention_text("для продолжния нажмите ввод")


def retention_text(String_warning):
    while (True):
        print(String_warning)
        answer = input()
        if answer == '':
            answer = "Empty"            # заглушка, чтобы сохранить структуру, если поля не введены
        return answer


def find_from_numder(data):
    flag_no_coincidence = False
    search_number = input("введите номер телефона ")
    for i in data:
        # задание найти запись по телефону рассмотрено как найти по строгому совпадению номера
        if (i.count(search_number) != 0):
            print(i)
            flag_no_coincidence = True
    if not (flag_no_coincidence):
        print("Совпадений не найдено")
    retention_text("для продолжния нажмите ввод")


def New_contact(data):
    New_contact_data = ["" for i in range(len(reference_book_structure))]
    for i in range(len(reference_book_structure)):
        New_contact_data[i] = retention_text(
            " введите поле " + str(reference_book_structure[i]))
    data.append(New_contact_data)
    # print(data)


# функция почти полная копия изменить контакт, однако оригинал решил не усложнять еще больше
def delete_contact(data):
    tmp_arr = []
    select_contact = input("введите поле для поиска " +
                           str(reference_book_structure[0][0])+" ")
    for i in data:
        if (i.count(select_contact) != 0):
            tmp_arr.append(i)
    for i in tmp_arr:
        for i2 in i:
            print(i2, end=' ')
        print()
    while True:
        try:
            ON_delete = int(input(
                "Выберите контакт, который хотите удалить (по порядковому номеру с 0) :"))
            if (0 <= ON_delete < len(tmp_arr)):
                break
            else:
                raise
        except:
            print("Неверный ввод порядкового номера")
    i = 0
    while True:
        if (tmp_arr.index(tmp_arr[i]) == ON_delete):
            del data[data.index(tmp_arr[i])]
            return data


# я явно перемудрил с этой фунцией в попытках обработки однофамильцев
def change_contact_number(data, Flag_no_rec, tmp_arr, Save_array):

    if (Flag_no_rec):
        Save_array = []
        tmp_arr = []
        select_contact = input("введите поле для поиска " +
                               str(reference_book_structure[0][0])+" ")
        for i in data:
            if (i.count(select_contact) != 0):
                tmp_arr.append(i)

    if (len(tmp_arr) == 0):
        print("Нет такого контакта")
        return
    elif len(tmp_arr) == 1 or Flag_no_rec == False:
        New_contact_number = input("Введите новый номер: ")
        for i in data:
            for element in i:
                if element == tmp_arr[0][0]:
                    data[data.index(i)][3] = New_contact_number
        for j in Save_array:
            data.append(j)
        return data
    else:
        for i in tmp_arr:
            for i2 in i:
                print(i2, end=' ')
            print()
        while True:
            try:
                ON_delete = int(input(
                    "Выберите контакт, у которого хотите заменить номер (по порядковому номеру с 0) :"))
                if (0 <= ON_delete < len(tmp_arr)):
                    break
                else:
                    raise
            except:
                print("Неверный ввод порядкового номера")
        i = 0
        while len(tmp_arr) != 1:
            if (tmp_arr.index(tmp_arr[i]) != ON_delete):
                if (data.count(tmp_arr[i]) != 0):
                    del data[data.index(tmp_arr[i])]
                    Save_array.append(tmp_arr[i])
                    del tmp_arr[i]
            else:
                i += 1
    return change_contact_number(data, False, tmp_arr, Save_array)


print("Импорт данных из файла")
data = Import_data()
while (True):
    print_menu()
    command = ""
    try:
        command = int(input("Введите команду:"))
        if (not (1 <= command <= 7)):
            raise
    except:
        print("Неккорекный ввод числа")
    match command:
        case 7:
            # экспорт конечно... Варварский. однако условиям задачи выполняет. для боле коректной записи было бы
            print("Экспорт в файл")
            # неплохо определить что за новые данные появились или удалились и исправлять именно это. однако это порядком усложнило бы код(лишние проходы в поисках пустой строки при удалении)
            Export_data(data)
            break
        case 1:
            for i in data:
                for i2 in i:
                    print(i2, end=' ')
                print()
            retention_text("для продолжния нажмите ввод")
        case 2:
            print("2-Найти запись по вхождению частей имени")
            Search_by_name(data)
        case 3:
            find_from_numder(data)
        case 4:
            New_contact(data)
        case 5:
            delete_contact(data)
        case 6:
            change_contact_number(data, True, None, None)

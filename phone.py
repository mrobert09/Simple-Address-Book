def update_number(cur, name_id):
    print('\nChoose an number to edit:')
    print('1. Mobile number')
    print('2. Home number')
    print('3. Work number')
    selection = input('>>> ')
    match selection:
        case '1':
            next_selection = update_number_prompt(cur, name_id, selection)
            print(next_selection)
        case '2':
            next_selection = update_number_prompt(cur, name_id, selection)
            print(next_selection)
        case '3':
            next_selection = update_number_prompt(cur, name_id, selection)
            print(next_selection)
        case _:
            print('Invalid selection')


def update_number_prompt(cur, name_id, selection):
    print('\nWhat would you like to do?')
    if has_number(cur, name_id, selection):
        print('1. Update number')
        print('2. Delete number')
        choice = input('>>>> ')
        if choice == '1':
            update_specific_number(cur, name_id, selection)
        elif choice == '2':
            delete_number(cur, name_id, selection)
    else:
        print('1. Add number')
        choice = input('>>>> ')
        if choice == '1':
            add_number(cur, name_id, selection)


def delete_number(cur, name_id, selection):
    cur.execute("DELETE FROM Phone WHERE personID = ? AND phoneType = ?", (name_id, selection))


def add_number(cur, name_id, selection):
    new_number = input('>>>>> ')
    cur.execute("INSERT INTO Phone (personID, phoneType, phoneNumber) VALUES (?, ?, ?)",
                (name_id, selection, new_number))


def update_specific_number(cur, name_id, selection):
    new_number = input('>>>>> ')
    cur.execute("UPDATE Phone SET phoneNumber = ? WHERE personID = ? AND phoneType = ?",
                (new_number, name_id, selection))


def has_number(cur, name_id, type_id):
    cur.execute("SELECT * FROM Phone WHERE personID = ? and phoneType = ?", (str(name_id), str(type_id)))
    return cur.fetchone()


def fetch_numbers(cur, name_id):
    phone_info = []
    cur.execute(
        'SELECT ph.phoneType, ph.phoneNumber '
        'FROM Person p '
        'JOIN Phone ph ON p.personID = ph.personID '
        'WHERE p.personID = ?',
        (str(name_id))
    )
    rows = cur.fetchall()
    for row in rows:
        phone_info.append((get_phone_type(row[0]), row[1]))

    return phone_info


def get_phone_type(type):
    match type:
        case 1:
            return 'Mobile'
        case 2:
            return 'Home'
        case 3:
            return 'Work'
        case _:
            return


def print_phone_numbers(phone_info):
    print('Phone Number(s):')
    for element in phone_info:
        print('    {}: {}'.format((element[0]), element[1]))


def main():
    pass


if __name__ == '__main__':
    main()

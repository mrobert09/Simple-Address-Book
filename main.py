import sqlite3
from person import *
from address import *
from phone import *


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)

    return conn


def view_all(cur):
    cur.execute('SELECT firstname, lastname FROM Person')
    rows = cur.fetchall()

    print('All names in address book.')
    print('--------------------')
    for row in rows:
        print(row[0] + ' ' + row[1])


def add_entry(cur):
    first_name, last_name = name_entry(cur)
    if first_name and last_name:
        person_id = add_person(cur, first_name, last_name)
        cur.execute("INSERT INTO PersonAddress (personID, addressID) VALUES (?, ?)", (person_id, 1))
        edit_entry(cur, first_name, last_name)


def view_entry(cur, *names):
    name = return_name(*names)
    if not name:
        return

    name_id = return_name_id(cur, name[0], name[1])

    if name_id:
        address_info = fetch_address(cur, name_id)
        phone_info = fetch_numbers(cur, name_id)

        # User didn't exist in system
        if address_info is None:
            print('No entry by that name found.')
            return

        print(full_name_convert(*names))
        print('--------------------')
        print_address(address_info)
        print_phone_numbers(phone_info)
        print()

    else:
        print('No entry by that name found.')


def edit_entry(cur, *names):
    name = return_name(*names)
    if not name:
        return

    first_name, last_name = name
    name_id = return_name_id(cur, first_name, last_name)

    if name_id:
        address_info = fetch_address(cur, name_id)
        phone_info = fetch_numbers(cur, name_id)

        print(full_name_convert(*names))
        print('--------------------')
        print_address(address_info)
        print_phone_numbers(phone_info)
        print('--------------------')
        print('\nChoose an option:')
        print('1. Edit name')
        print('2. Add/edit address')
        print('3. Add/edit phone number(s)')
        print('4. Delete entry')
        selection = input('>> ')
        match selection:
            case '1':
                update_name(cur, name_id)
            case '2':
                update_address(cur, name_id)
            case '3':
                update_number(cur, name_id)
            case '4':
                delete_name(cur, name_id)
            case _:
                print('Invalid selection')

    else:
        print('No entry by that name found.')


def view_table(cur, table):
    # Mostly used for debugging
    table_list = ['Person', 'PersonAddress', 'Address']
    if table in table_list:
        search = "SELECT * FROM " + table
        cur.execute(search)
        rows = cur.fetchall()
        for row in rows:
            print(row)
    else:
        print('No such table found.')


def main():
    conn = create_connection('addressBook.db')
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON")

    print("Simple Address Book. For commands type 'help'.")
    quit_flag = False
    while not quit_flag:
        user_input = input('> ')
        match user_input.split():
            case ['exit' | 'quit']:
                quit_flag = True
            case ['help']:
                print("'exit' --  Exits the program.")
                print("'viewall' --  Views all names in address book.")
                print("'view <name>' --  Views address book entry for <name>")
                print("'edit <name>' --  Edits address book entry for <name>")
                print("'add' --  Adds a new entry to the address book.")
            case ['viewall']:
                view_all(cur)
            case ['view', *names]:
                view_entry(cur, *names)
            case ['edit', *names]:
                edit_entry(cur, *names)
            case ['add']:
                add_entry(cur)
            case ['viewtable', table]:
                view_table(cur, table)
            case _:
                print('Unknown command: ' + user_input)
        # conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    main()

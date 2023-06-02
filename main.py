import sqlite3


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)

    return conn


def view_all(conn):
    cur = conn.cursor()
    cur.execute('SELECT firstname, lastname FROM Person')
    rows = cur.fetchall()

    print('All names in address book.')
    print('--------------------')
    for row in rows:
        print(row[0] + ' ' + row[1])

    cur.close()


def view_entry(conn, *names):
    cur = conn.cursor()
    cur.execute(
        'SELECT a.street, a.city, a.state, a.zip '
        'FROM Person p '
        'JOIN PersonAddress pa ON p.personID = pa.personID '
        'JOIN Address a ON pa.addressID = a.addressID '
        'WHERE p.firstname = ? '
        'AND p.lastname = ?',
        (names[0], names[1])
    )
    entry = cur.fetchone()

    if entry is None:
        print('No entry by that name found.')
        return

    print(return_name(*names))
    print('--------------------')
    print('Address: ' + entry[0] + ', ' + entry[1]+ ', ' + entry[2] + ' ' + entry[3])

    cur.close()


def edit_entry(conn, *names):
    print('Editing entry: ' + return_name(*names))


def add_entry(conn):
    cur = conn.cursor()
    firstname = input('First name: ')
    lastname = input('Last name: ')

    if name_exists_in_book(cur, firstname, lastname):
        print("Can't add duplicate names in address book.")
        return

    print('Adding: ' + firstname + ' ' + lastname)


def return_name(*names):
    """
    Simple helper function for returning full name in string format.
    :param names:
    :return: string
    """
    full_name = ''
    for name in names:
        full_name = full_name + name + ' '
    return full_name.rstrip()


def name_exists_in_book(cur, firstname, lastname):
    cur.execute('SELECT 1 FROM Person WHERE firstname = ? AND lastname = ?', (firstname, lastname))
    if cur.fetchone():
        return True
    return False


def main():
    conn = create_connection('addressBook.db')

    print("Simple Address Book. For commands type 'help'.")
    quit_flag = False
    while not quit_flag:
        user_input = input()
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
                view_all(conn)
            case ['view', *names]:
                view_entry(conn, *names)
            case ['edit', *names]:
                edit_entry(conn, *names)
            case ['add']:
                add_entry(conn)
            case _:
                print('Unknown command: ' + user_input)


if __name__ == '__main__':
    main()

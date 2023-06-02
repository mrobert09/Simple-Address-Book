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

    for row in rows:
        print(row)


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
        print('No entry by the name found.')

    else:
        print(return_name(*names))
        print('--------------------')
        print('Address: ' + entry[0] + ', ' + entry[1]+ ', ' + entry[2] + ' ' + entry[3])


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
                print("'exit'  --  Exits the program.")
                print("'viewall' --  Views all names in address book.")
            case ['viewall']:
                view_all(conn)
            case ['view', *names]:
                view_entry(conn, *names)
            case _:
                print('Unknown command: ' + user_input)


if __name__ == '__main__':
    main()

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
    print('Address: {}, {}, {} {}'.format(entry[0], entry[1], entry[2], entry[3]))

    cur.close()


def edit_entry(conn, *names):
    cur = conn.cursor()
    cur.execute(
        'SELECT a.street, a.city, a.state, a.zip, p.personID, a.addressID '
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

    personID = entry[4]
    addressID = entry[5]

    print(return_name(*names))
    print('--------------------')
    print('Address: {}, {}, {} {}'.format(entry[0], entry[1], entry[2], entry[3]))
    print('--------------------')
    print('Choose an option:')
    print('1. Edit name')
    print('2. Edit addresses')
    print('3. Delete entry')
    selection = input('>> ')
    match selection:
        case '1':
            update_name(cur, personID)
        case '2':
            print('Address chosen')
        case '3':
            delete_name(cur, personID)
        case _:
            print('Invalid selection')

    cur.close()


def update_name(cur, personID):
    # Catches invalid names
    name_returned = name_entry(cur)
    if name_returned:
        firstname, lastname = name_returned
    else:
        return

    # Update entry in Table
    cur.execute("UPDATE Person SET firstname = ?, lastname = ? WHERE personID = ?", (firstname, lastname, personID))


def delete_name(cur, personID):
    cur.execute("DELETE FROM Person WHERE personID = ?", (personID,))


def add_entry(conn):
    cur = conn.cursor()

    # Catches invalid names
    name_returned = name_entry(cur)
    if name_returned:
        firstname, lastname = name_returned
    else:
        return

    # Accept input for address
    street = input('Street address: ')
    city = input('City: ')
    state = input('State: ')
    zip = input('Zip: ')

    # Switch any blank entries to None / NULL values for database
    street, city, state, zip = convert_null([street, city, state, zip])

    # Add Person row, return ID
    personID = add_person(cur, firstname, lastname)

    # Add Address row, return ID
    addressID = add_address(cur, street, city, state, zip)

    # Link Person and Address in PersonAddress
    cur.execute("INSERT INTO PersonAddress (personID, addressID) VALUES (?, ?)", (personID, addressID))
    cur.close()


def name_entry(cur):
    # Accept input for name
    firstname = input('First name: ')
    lastname = input('Last name: ')

    # Constraints
    if name_exists_in_book(cur, firstname, lastname):
        print("Can't add duplicate names in address book.")
        return

    if len(firstname) == 0 or len(lastname) == 0:
        print("First name and last name required.")
        return

    return firstname, lastname


def add_person(cur, firstname, lastname):
    cur.execute("INSERT INTO Person (firstname, lastname) VALUES (?, ?)", (firstname, lastname))
    cur.execute("SELECT personID FROM Person WHERE firstname = ? AND lastname = ?", (firstname, lastname))
    return cur.fetchone()[0]


def add_address(cur, street, city, state, zip):
    # Check if address already exists. If it does, return ID of address.
    query_address(cur, street, city, state, zip)
    addressID = cur.fetchone()
    if addressID:
        return addressID[0]

    # Insert address
    cur.execute("INSERT INTO Address (street, city, state, zip) VALUES (?, ?, ?, ?)", (street, city, state, zip))
    return cur.lastrowid


def query_address(cur, street, city, state, zip):
    query = "SELECT * FROM Address WHERE "
    params = []
    if street is None:
        query += "street IS NULL AND "
    else:
        query += "street = ? AND "
        params.append(street)
    if city is None:
        query += "city IS NULL AND "
    else:
        query += "city = ? AND "
        params.append(city)
    if state is None:
        query += "state IS NULL AND "
    else:
        query += "state = ? AND "
        params.append(state)
    if zip is None:
        query += "zip IS NULL"
    else:
        query += "zip = ?"
        params.append(zip)

    if params:
        cur.execute(query, params)
    else:
        cur.execute(query)


def convert_null(values):
    for i in range(len(values)):
        if len(values[i]) == 0:
            values[i] = None

    return values


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


def view_table(cur):
    # Mostly used for debugging
    rows = cur.fetchall()
    for row in rows:
        print(row)


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
                view_all(conn)
            case ['view', *names]:
                view_entry(conn, *names)
            case ['edit', *names]:
                edit_entry(conn, *names)
            case ['add']:
                add_entry(conn)
            case ['viewtable', 'Person']:
                cur.execute("SELECT * FROM Person")
                view_table(cur)
            case ['viewtable', 'PersonAddress']:
                cur.execute("SELECT * FROM PersonAddress")
                view_table(cur)
            case ['viewtable', 'Address']:
                cur.execute("SELECT * FROM Address")
                view_table(cur)
            case _:
                print('Unknown command: ' + user_input)
        conn.commit()
    conn.close()


if __name__ == '__main__':
    main()

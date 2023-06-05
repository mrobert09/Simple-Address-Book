def update_name(cur, person_id):
    # Catches invalid names
    name_returned = name_entry(cur)
    if name_returned:
        firstname, lastname = name_returned
    else:
        return

    # Update entry in Table
    cur.execute("UPDATE Person SET firstname = ?, lastname = ? WHERE personID = ?", (firstname, lastname, person_id))


def name_entry(cur):
    # Accept input for name
    firstname = input('First name: ')
    lastname = input('Last name: ')

    # Constraints
    if return_name_id(cur, firstname, lastname):
        print("Can't add duplicate names in address book.")
        return

    if len(firstname) == 0 or len(lastname) == 0:
        print("First name and last name required.")
        return

    return firstname, lastname


def return_name_id(cur, firstname, lastname):
    cur.execute('SELECT personID FROM Person WHERE firstname = ? AND lastname = ?', (firstname, lastname))
    return cur.fetchone()


def delete_name(cur, person_id):
    print('Delete entry? (Y/N)')
    selection = input('>> ')
    if selection.lower() == 'y':
        cur.execute("DELETE FROM Person WHERE personID = ?", (person_id,))


def add_person(cur, firstname, lastname):
    cur.execute("INSERT INTO Person (firstname, lastname) VALUES (?, ?)", (firstname, lastname))
    cur.execute("SELECT personID FROM Person WHERE firstname = ? AND lastname = ?", (firstname, lastname))
    return cur.fetchone()[0]


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
    pass


if __name__ == '__main__':
    main()

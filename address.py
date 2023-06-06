def update_address(cur, person_id):
    # Accept input for address
    street = input('Street address: ')
    city = input('City: ')
    state = input('State: ')
    zipcode = input('Zip: ')

    # Switch any blank entries to None / NULL values for database
    street, city, state, zipcode = convert_null([street, city, state, zipcode])

    # Check if address already exists. If it does, return ID of address.
    query_address(cur, street, city, state, zipcode)
    other_address_id = cur.fetchone()
    if other_address_id:
        cur.execute("UPDATE PersonAddress SET addressID = ? WHERE personID = ?", (other_address_id[0], person_id))
    else:
        new_address_id = add_address(cur, street, city, state, zipcode)
        cur.execute("UPDATE PersonAddress SET addressID = ? WHERE personID = ?", (new_address_id, person_id))


def add_address(cur, street, city, state, zipcode):
    # Check if address already exists. If it does, return ID of address.
    query_address(cur, street, city, state, zipcode)
    address_id = cur.fetchone()
    if address_id:
        return address_id[0]

    # Insert address
    cur.execute("INSERT INTO Address (street, city, state, zip) VALUES (?, ?, ?, ?)", (street, city, state, zipcode))
    return cur.lastrowid


def query_address(cur, street, city, state, zipcode):
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
    if zipcode is None:
        query += "zip IS NULL"
    else:
        query += "zip = ?"
        params.append(zipcode)

    if params:
        cur.execute(query, params)
    else:
        cur.execute(query)


def fetch_address(cur, name_id):
    cur.execute(
        'SELECT a.street, a.city, a.state, a.zip '
        'FROM Person p '
        'JOIN PersonAddress pa ON p.personID = pa.personID '
        'JOIN Address a ON pa.addressID = a.addressID '
        'WHERE p.personID = ?',
        (str(name_id))
    )

    return cur.fetchone()


def print_address(info):
    print('Address:')
    if info[0]:
        print('    Street: {}'.format(info[0]))
    if info[1]:
        print('    City: {}'.format(info[1]))
    if info[2]:
        print('    State: {}'.format(info[2]))
    if info[3]:
        print('    Zip: {}'.format(info[3]))


def convert_null(values):
    for i in range(len(values)):
        if len(values[i]) == 0:
            values[i] = None

    return values


def main():
    pass


if __name__ == '__main__':
    main()

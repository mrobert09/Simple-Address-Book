def fetch_numbers(cur, name_id):
    phone_info = []
    cur.execute(
        'SELECT ph.phoneType, ph.phoneNumber '
        'FROM Person p '
        'JOIN Phone ph ON p.personID = ph.personID '
        'WHERE p.personID = ?',
        (name_id)
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

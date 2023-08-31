import json


class AddressEntry:
    def __init__(self, name, street=None, city=None, state=None, zip=None, home=None, mobile=None, work=None):
        self.name = name
        self.address = {
            'Street' : street,
            'City' : city,
            'State' : state,
            'Zip' : zip
        }
        self.phone = {
            'Home' : home,
            'Mobile' : mobile,
            'Work' : work
        }


    def __repr__(self):
        address = ''
        address_flag = 0
        if self.address['Street']:
            address += '\n    Street: ' + self.address['Street']
            address_flag = 1
        if self.address['City']:
            address += '\n    City: ' + self.address['City']
            address_flag = 1
        if self.address['State']:
            address += '\n    State: ' + self.address['State']
            address_flag = 1
        if self.address['Zip']:
            address += '\n    Zip: ' + self.address['Zip']
            address_flag = 1
        if address_flag:
            address = '\nAddress: ' + address

        phone = ''
        phone_flag = 0
        if self.phone['Home']:
            phone += '\n    Home: ' + self.phone['Home']
            phone_flag = 1
        if self.phone['Mobile']:
            phone += '\n    Mobile: ' + self.phone['Mobile']
            phone_flag = 1
        if self.phone['Work']:
            phone += '\n    Work: ' + self.phone['Work']
            phone_flag = 1
        if phone_flag:
            phone = '\nPhone Number(s):' + phone

        return self.name + '\n--------------------' + address + phone


def main():
    a1 = AddressEntry('Joe Smith', street='12345 SE Nowhere Ln', mobile='(987) 654-3210')
    with open('AddressBook.json', 'w') as out:
        json.dump(a1.__dict__, out, indent=2)


if __name__ == '__main__':
    main()

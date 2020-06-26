class User():
    """ RESUMATE USER """

    def __init__(self, firstname, lastname, title, gender, address='', email='', telnum=''):
        self.firstname = firstname
        self.lastname = lastname
        self.fullname = firstname + ' ' + lastname
        self.title = title
        self.gender = gender
        self.address = address
        self.email = email
        self.telnum = telnum

    def exists(self):
        if self.firstname == '' and self.lastname == '':
            return False
        return True

    def __repr__(self):
        out = f'<User firstname={self.firstname}, lastname={self.lastname}>'
        return out

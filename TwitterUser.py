class User:
    username = ""
    password = ""
    email = ""
    token = ""
    two_fa_url = ""

    def __init__(self, username, password, email, token, two_fa_url):
        self.username = username
        self.password = password
        self.email = email
        self.token = token
        self.two_fa_url = two_fa_url

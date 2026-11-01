# Director/Admin login er jonno. Dictionary 

ADMINS = {
    "director": "flood123",
    "admin": "admin123",
}


def check_login(username, password):
    username = username.strip()
    if username == "" or password == "":
        raise ValueError("Username and password both needed.")
    if username in ADMINS and ADMINS[username] == password:
        return True
    return False

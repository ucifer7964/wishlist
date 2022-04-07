import re
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


class Validation:

    def name(self, name):
        if len(name) < 3:
            return True
        return False

    def phone_validation(self, number):
        if len(number) == 10:
            if "." not in number:
                return False
        return True

    def password_check(self, pswd1, pswd2):
        if pswd1 != pswd2:
            return True
        if len(pswd1) < 6:
            return True
        return False

    def email_validation(self, email):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        process = re.compile(regex)
        flag = re.match(process,email)
        if flag:
            return False
        return True

    def postal_code(self, code:str):
        regex = "^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$"
        process = re.compile(regex)
        flag = re.match(process, code)
        if flag:
            return False
        return True

        
validation = Validation()

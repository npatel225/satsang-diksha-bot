from os import getenv

from cryptography.fernet import Fernet


class Security:

    @staticmethod
    def encrypt_cred():
        key = getenv('CREDENTIALS_KEY')
        key = key.encode('utf-8')

        input_file = 'credentials.json'
        output_file = 'credentials.encrypted'

        with open(input_file, 'rb') as f:
            data = f.read()

            fernet = Fernet(key)
            encrypted = fernet.encrypt(data)

        with open(output_file, 'wb') as f:
            f.write(encrypted)

    @staticmethod
    def decrypt_cred():
        key = getenv('CREDENTIALS_KEY')
        key = key.encode('utf-8')

        output_file = 'credentials.json'
        input_file = 'credentials.encrypted'

        with open(input_file, 'rb') as f:
            data = f.read()

        fernet = Fernet(key)
        encrypted = fernet.decrypt(data)

        with open(output_file, 'wb') as f:
            f.write(encrypted)


if __name__ == '__main__':
    s = Security()
    s.decrypt_cred()

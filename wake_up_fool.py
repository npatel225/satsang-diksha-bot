from os import getenv

import requests


def wake_up():
    requests.get(getenv('APP_NAME'))


if __name__ == '__main__':
    wake_up()

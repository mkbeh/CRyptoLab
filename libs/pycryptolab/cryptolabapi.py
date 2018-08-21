# -*- coding: utf-8 -*-
import requests

from string import Template


class CryptolabApi(object):
    """Class for interaction with CRyptoLab REST API."""

    def __init__(self):
        self.content_type = 'application/json'
        self.url = 'https://127.0.0.1:4443/'

    def user_login(self, email, password, id_):
        """Method for login user in app."""
        headers = {
            'Content-Type': self.content_type,
        }

        template = Template('{"email": "$email", "password": "$password", "id": "$id_"}')
        data = template.substitute(email=email, password=password, id_=id_)

        url = self.url + 'user/login'

        try:
            response = requests.post(url=url, headers=headers, data=data, timeout=(3.05, 60), stream=True, verify=False)
            return response.json()
        except Exception as e:
            print(e)

    def user_registration(self, email, password, confirm_password, username):
        """Method for registration new user in app."""

        headers = {
            'Content-Type': self.content_type,
        }

        template = Template('{"email": "$email", "password": "$password", "confirm_password": "$confirm_password", \
                            "username": "$username"}')
        data = template.substitute(email=email, password=password, confirm_password=confirm_password, username=username)

        print(template)
        print(data)

        url = self.url + 'user/registration'

        try:
            response = requests.post(url=url, headers=headers, data=data, timeout=(3.05, 60), stream=True, verify=False)
            print(response.json())
            return response.json()
        except Exception as e:
            print(e)

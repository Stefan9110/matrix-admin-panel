#!/bin/python3
# matrix-admin-panel
# Copyright (C) 2022 Stefan9110
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import color
import menu
import getpass
import argparse
import requests
import json
import re
from clioptions import arg_define


def prefix():
    return color.YELLOW + "[MATRIX ADMIN] " + color.RESET


LOGO = " __  __    _  _____ ____  _____  __     _    ____  __  __ ___ _   _ \n\
|  \/  |  / \|_   _|  _ \|_ _\ \/ /    / \  |  _ \|  \/  |_ _| \ | |\n\
| |\/| | / _ \ | | | |_) || | \  /    / _ \ | | | | |\/| || ||  \| |\n\
| |  | |/ ___ \| | |  _ < | | /  \   / ___ \| |_| | |  | || || |\  |\n\
|_|  |_/_/   \_\_| |_| \_\___/_/\_\ /_/   \_\____/|_|  |_|___|_| \_|\n\
"


def check_auth(homeserver, auth_token):
    acc_request = requests.get((homeserver + "/_matrix/client/r0/account/whoami"),
                               headers={"Authorization": "Bearer " + auth_token})
    if acc_request.status_code != 200:
        print(prefix() + "Invalid auth token!" + color.RED + " ಠ-ಠ" + color.RESET)
        exit(2)

    user = json.loads(acc_request.content.decode())["user_id"]
    print(prefix() + "Logged in as " + color.GREEN + user)

    # Check if user is admin
    if requests.get((homeserver + "/_synapse/admin/v1/users/" + user + "/admin"),
                    headers={"Authorization": "Bearer " + auth_token}).status_code != 200:
        print(prefix() + color.RED + "You are not a server admin!" + color.RESET)
        exit(3)


# Format url by prefixing https:// if not present
def format_url(url):
    if not re.match('(?:http|https)://', url):
        return 'https://{}'.format(url)
    return url


def main():
    # Define options
    parser = argparse.ArgumentParser(description="A powerful CLI for managing your Matrix homeserver!")
    arg_define(parser)
    global options
    options = parser.parse_args()

    print(color.RED + LOGO + color.YELLOW + "\n               Welcome to Matrix Admin Control Panel!\n" + color.RESET)
    auth_token = getpass.getpass(prefix() + "Enter your matrix admin account authentication token: ")

    # Obtain homeserver from options or from stdin
    if options.url is not None:
        homeserver = options.url[0]
    else:
        homeserver = input(prefix() + "Enter homeserver URL: ")

    if str(homeserver) == "":
        print(prefix() + "Homeserver cannot be null " + color.RED + "(╯°□°）╯︵ ┻━┻" + color.RESET)
        exit(-1)

    # Format homeserver
    homeserver = format_url(homeserver)

    try:
        check_auth(homeserver, auth_token)
    except requests.exceptions.ConnectionError:
        print(prefix() + "Homeserver URL is not valid")
        exit(1)

    menu.main_menu(homeserver, auth_token)


if __name__ == '__main__':
    main()

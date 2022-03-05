#!/bin/python3
import color
import menu
import getpass
import argparse
import requests
import json
import re

prefix = color.YELLOW + "[MATRIX ADMIN] " + color.RESET
logo = " __  __    _  _____ ____  _____  __     _    ____  __  __ ___ _   _ \n\
|  \/  |  / \|_   _|  _ \|_ _\ \/ /    / \  |  _ \|  \/  |_ _| \ | |\n\
| |\/| | / _ \ | | | |_) || | \  /    / _ \ | | | | |\/| || ||  \| |\n\
| |  | |/ ___ \| | |  _ < | | /  \   / ___ \| |_| | |  | || || |\  |\n\
|_|  |_/_/   \_\_| |_| \_\___/_/\_\ /_/   \_\____/|_|  |_|___|_| \_|\n\
"


# Define cli options
def arg_define(arg_parser):
    arg_parser.add_argument("-u", "--url",
                            type=str, nargs=1, metavar="URL", default=None,
                            help="Your matrix homeserver URL")


def check_auth(homeserver, auth_token):
    acc_request = requests.get((homeserver + "/_matrix/client/r0/account/whoami"),
                               headers={"Authorization": "Bearer " + auth_token})
    if acc_request.status_code != 200:
        print(prefix + color.RED + "Invalid auth token!" + color.RESET)
        exit(0)

    user = json.loads(acc_request.content.decode())["user_id"]
    print(prefix + "Logged in as " + color.GREEN + user)

    # Check if user is admin
    if requests.get((homeserver + "/_synapse/admin/v1/users/" + user + "/admin"),
                    headers={"Authorization": "Bearer " + auth_token}).status_code != 200:
        print(prefix + color.RED + "You are not a server admin!" + color.RESET)
        exit(0)


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

    print(color.RED + logo + color.YELLOW + "\n               Welcome to Matrix Admin Control Panel!\n" + color.RESET)
    auth_token = getpass.getpass(prefix + "Enter your matrix admin account authentication token: ")

    # Obtain homeserver from options or from stdin
    if options.url is not None:
        homeserver = options.url[0]
    else:
        print(prefix + "Enter homeserver URL:")
        homeserver = input()

    # Format homeserver
    homeserver = format_url(homeserver)

    check_auth(homeserver, auth_token)
    menu.main_menu()


if __name__ == '__main__':
    main()

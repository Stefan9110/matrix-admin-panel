import color
from datetime import datetime


def parse_boolean(b):
    if b:
        return "yes"
    return "no"


def format_time(unix_time):
    if unix_time is None:
        return "no"
    return datetime.utcfromtimestamp(int(unix_time) / 1000).strftime('%d %b %Y %H:%M:%S')


def print_room(room):
    if room["name"] is not None:
        print(color.GREEN + "NAME: " + color.RESET + room["name"])

    print(
        color.GREEN + "ID: " + color.RESET + room["room_id"] + "\n" +
        color.GREEN + "CREATOR: " + color.RESET + room["creator"]
    )


def print_registration_token(reg_token):
    print(
        color.GREEN + "TOKEN: " + color.RESET + reg_token["token"] + "\n" +
        color.GREEN + "USES ALLOWED: " + color.RESET + str(reg_token["uses_allowed"]) + "\n" +
        color.GREEN + "TOTAL USES: " + color.RESET + str(reg_token["completed"]) + "\n" +
        color.GREEN + "EXPIRES: " + color.RESET + format_time(reg_token["expiry_time"]) + "\n"
    )

def print_user(user):
    print(
        color.GREEN + "ID: " + color.RESET + user["name"] + "\n" +
        color.GREEN + "NAME: " + color.RESET + user["displayname"] + "\n" +
        color.GREEN + "IS ADMIN: " + color.RESET + parse_boolean(user["admin"]) + "\n" +
        color.GREEN + "DEACTIVATED: " + color.RESET + parse_boolean(user["deactivated"])
    )
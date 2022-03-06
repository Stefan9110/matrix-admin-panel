import requests
import json
import color
from main import prefix
import re
from datetime import datetime
from time import time


def get_request(homeserver, token, path):
    return requests.get((homeserver + path),
                        headers={"Authorization": "Bearer " + token})


def post_request(homeserver, token, path, data):
    return requests.post((homeserver + path), headers={"Authorization": "Bearer " + token}, data=data)


def delete_request(homeserver, token, path):
    return requests.delete((homeserver + path), headers={"Authorization": "Bearer " + token})


def parse_boolean(b):
    if b:
        return "yes"
    return "no"


def format_time(unix_time):
    if unix_time is None:
        return "no"
    return datetime.utcfromtimestamp(int(unix_time) / 1000).strftime('%d %b %Y %H:%M:%S')


def list_users(homeserver, token):
    limit = input(color.YELLOW + "Enter user limit: " + color.RESET)
    request = get_request(homeserver, token, "/_synapse/admin/v2/users?from=0&limit=" + str(limit) + "&guests=false")
    if request.status_code != 200:
        return

    print(prefix() + "Fetching user accounts...")

    for user in json.loads(request.content.decode())["users"]:
        print(
            color.YELLOW + "──────────────────────────────────────────────────────\n" +
            color.GREEN + "ID: " + color.RESET + user["name"] + "\n" +
            color.GREEN + "NAME: " + color.RESET + user["displayname"] + "\n" +
            color.GREEN + "IS ADMIN: " + color.RESET + parse_boolean(user["admin"]) + "\n" +
            color.GREEN + "DEACTIVATED: " + color.RESET + parse_boolean(user["deactivated"]) + "\n"
        )
    print(color.YELLOW + "──────────────────────────────────────────────────────")


def search_user(homeserver, token):
    query = input(color.YELLOW + "Enter user search query: " + color.RESET)
    request = get_request(homeserver, token, "/_synapse/admin/v2/users?from=0&guests=false")
    if request.status_code != 200:
        return

    found = False

    for user in json.loads(request.content.decode())["users"]:
        if not re.search(query.lower(), str(user["name"]).lower()) \
                and not re.search(query.lower(), str(user["displayname"]).lower()):
            continue

        found = True
        print(
            color.YELLOW + "──────────────────────────────────────────────────────\n" +
            color.GREEN + "ID: " + color.RESET + user["name"] + "\n" +
            color.GREEN + "NAME: " + color.RESET + user["displayname"] + "\n" +
            color.GREEN + "IS ADMIN: " + color.RESET + parse_boolean(user["admin"]) + "\n" +
            color.GREEN + "DEACTIVATED: " + color.RESET + parse_boolean(user["deactivated"]) + "\n" +
            color.YELLOW + "──────────────────────────────────────────────────────\n"
        )

    if not found:
        print(prefix() + "User not found...")


def list_registration_tokens(homeserver, token):
    request = get_request(homeserver, token, "/_synapse/admin/v1/registration_tokens")
    if request.status_code != 200:
        return

    found = False

    print(prefix() + "Listing available registration tokens...")

    for reg_token in json.loads(request.content.decode())["registration_tokens"]:
        found = True
        print(
            color.YELLOW + "──────────────────────────────────────────────────────\n" +
            color.GREEN + "TOKEN: " + color.RESET + reg_token["token"] + "\n" +
            color.GREEN + "USES ALLOWED: " + color.RESET + str(reg_token["uses_allowed"]) + "\n" +
            color.GREEN + "TOTAL USES: " + color.RESET + str(reg_token["completed"]) + "\n" +
            color.GREEN + "EXPIRES: " + color.RESET + format_time(reg_token["expiry_time"]) + "\n"
        )

    if not found:
        print(prefix() + "No registration tokens were found.")
    else:
        print(color.YELLOW + "──────────────────────────────────────────────────────")


def create_registration_token(homeserver, token):
    print("\n" + prefix() + "Creating a registration token... Enter the details below:")
    uses_allowed = input(color.YELLOW + "Uses allowed (default 1): " + color.RESET)
    expire = input(color.YELLOW + "How many seconds should the token be available "
                                  "(default " + color.RED + "permanent" + color.YELLOW + "): " + color.RESET)
    length = input(color.YELLOW + "Token length (default 48): " + color.RESET)

    data = {
        "length": 48,
        "expiry_time": None,
        "uses_allowed": 1
    }

    if str(expire) != "" and str(expire).lower() != "no":
        data["expiry_time"] = (int(time()) + int(expire)) * 1000

    if str(length) != "":
        _len = int(length)
        # Cap length at 64 as synapse requires
        if _len > 64:
            _len = 64
        data["length"] = _len

    if str(uses_allowed) != "":
        data["uses_allowed"] = int(uses_allowed)

    request = post_request(homeserver, token, "/_synapse/admin/v1/registration_tokens/new", json.dumps(data))
    if request.status_code != 200:
        print("ERR " + str(request.status_code) + "\n" + request.content.decode())
        return

    print(prefix() + "A registration token was created: " +
          color.GREEN + json.loads(request.content.decode())["token"] + color.RESET)


def delete_registration_token(homeserver, token):
    print(prefix() + color.RED + "WARNING!" + color.RESET + " Deleting a registration token is a permanent action!")
    to_delete = input(color.YELLOW + "Input registration token to delete: " + color.RESET)
    if str(to_delete) == "":
        return

    request = delete_request(homeserver, token, "/_synapse/admin/v1/registration_tokens/" + to_delete)
    if request.status_code == 200:
        print(prefix() + "Successfully deleted token " + color.GREEN + to_delete + color.RESET)
    else:
        print(prefix() + "The token you were trying to delete does not exist")


# List all rooms that are created on the homeserver
def list_rooms(homeserver, token):
    request = get_request(homeserver, token, path="/_synapse/admin/v1/rooms")
    if request.status_code != 200:
        return

    print("\n" + prefix() + "Fetching rooms created on the " + color.GREEN + homeserver + color.RESET + " homeserver")

    for room in json.loads(request.content.decode())["rooms"]:
        # Check whether the room id contains the homeserver link
        if re.sub(r"http(s)?://", "", homeserver) not in room["room_id"]:
            continue

        # Print room data
        print(color.YELLOW + "──────────────────────────────────────────────────────")
        if room["name"] is not None:
            print(color.GREEN + "NAME: " + color.RESET + room["name"])

        print(
            color.GREEN + "ID: " + color.RESET + room["room_id"] + "\n" +
            color.GREEN + "CREATOR: " + color.RESET + room["creator"]
        )
    print(color.YELLOW + "──────────────────────────────────────────────────────")

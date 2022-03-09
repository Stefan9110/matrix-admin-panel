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

import requests
import json
import color
from main import prefix
import re
from time import time
import tui


def get_request(homeserver, token, path):
    return requests.get((homeserver + path), headers={"Authorization": "Bearer " + token})


def post_request(homeserver, token, path, data):
    return requests.post((homeserver + path), headers={"Authorization": "Bearer " + token}, data=data)


def delete_request(homeserver, token, path):
    return requests.delete((homeserver + path), headers={"Authorization": "Bearer " + token})


def list_users(homeserver, token):
    limit = input(color.YELLOW + "Enter user limit (default none): " + color.RESET)
    req_path = "/_synapse/admin/v2/users?from=0&limit=" + str(limit) + "&guests=false"
    if str(limit) == "":
        req_path = "/_synapse/admin/v2/users?from=0&guests=false"

    request = get_request(homeserver, token, req_path)
    if request.status_code != 200:
        print(prefix() + "An error as occurred (" + str(request.status_code) + ")")
        return

    print("\n" + prefix() + "Fetching user accounts...")

    for user in json.loads(request.content.decode())["users"]:
        print(color.YELLOW + "──────────────────────────────────────────────────────")
        tui.print_user(user)
    print(color.YELLOW + "──────────────────────────────────────────────────────")


def search_user(homeserver, token):
    query = input(color.YELLOW + "Enter user search query: " + color.RESET)
    request = get_request(homeserver, token, "/_synapse/admin/v2/users?from=0&guests=false")
    if request.status_code != 200:
        print(prefix() + "An error as occurred (" + str(request.status_code) + ")")
        return

    found = False

    for user in json.loads(request.content.decode())["users"]:
        if not re.search(query.lower(), str(user["name"]).lower()) \
                and not re.search(query.lower(), str(user["displayname"]).lower()):
            continue

        found = True
        print(color.YELLOW + "──────────────────────────────────────────────────────")
        tui.print_user(user)
        print(color.YELLOW + "──────────────────────────────────────────────────────")

    if not found:
        print(prefix() + "User not found...")


def list_registration_tokens(homeserver, token):
    request = get_request(homeserver, token, "/_synapse/admin/v1/registration_tokens")
    if request.status_code != 200:
        print(prefix() + "An error as occurred (" + str(request.status_code) + ")")
        return

    found = False

    print(prefix() + "Listing available registration tokens...")

    for reg_token in json.loads(request.content.decode())["registration_tokens"]:
        found = True
        print(color.YELLOW + "──────────────────────────────────────────────────────")
        tui.print_registration_token(reg_token)

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
        print(prefix() + "An error as occurred (" + str(request.status_code) + ")")
        return

    created_token = json.loads(request.content.decode())
    print(prefix() + "A registration token was created: " +
          color.GREEN + created_token["token"] + color.RESET)

    print(color.YELLOW + "──────────────────────────────────────────────────────")
    tui.print_registration_token(created_token)
    print(color.YELLOW + "──────────────────────────────────────────────────────")


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
    limit = input(color.YELLOW + "Enter room limit (default none): " + color.RESET)
    if str(limit) == "" or not str(limit).isnumeric():
        limit = 0

    request = get_request(homeserver, token, path="/_synapse/admin/v1/rooms")
    if request.status_code != 200:
        print(prefix() + "An error as occurred (" + str(request.status_code) + ")")
        return

    print("\n" + prefix() + "Fetching rooms created on the " + color.GREEN + homeserver + color.RESET + " homeserver")

    count = 0
    for room in json.loads(request.content.decode())["rooms"]:
        # Check whether the room id contains the homeserver link
        if re.sub(r"http(s)?://", "", homeserver) not in room["room_id"]:
            continue

        # Print room data
        print(color.YELLOW + "──────────────────────────────────────────────────────")
        tui.print_room(room)

        count += 1
        if count >= int(limit) != 0:
            break
    print(color.YELLOW + "──────────────────────────────────────────────────────")


def search_room(homeserver, token):
    to_search = input(color.YELLOW + "Enter room query: " + color.RESET)

    request = get_request(homeserver, token, path="/_synapse/admin/v1/rooms")
    if request.status_code != 200:
        print(prefix() + "An error as occurred (" + str(request.status_code) + ")")
        return

    found = False
    for room in json.loads(request.content.decode())["rooms"]:
        # Check whether room is valid
        if re.sub(r"http(s)?://", "", homeserver) not in room["room_id"] \
                or room["name"] is None \
                or to_search.lower() not in str(room["name"]).lower():
            continue

        found = True
        # Print room data
        print(color.YELLOW + "──────────────────────────────────────────────────────")
        tui.print_room(room)

    if not found:
        print(prefix() + "No room was found...")
    else:
        print(color.YELLOW + "──────────────────────────────────────────────────────")

import requests
import json
import color
from main import prefix
import re
import menu


def get_request(homeserver, token, path):
    return requests.get((homeserver + path),
                        headers={"Authorization": "Bearer " + token})


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

    # Call main menu
    menu.main_menu(homeserver, token)

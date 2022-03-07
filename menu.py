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

from commands import *
import getch


def main_menu(homeserver, token):
    print(
        color.YELLOW + "\n       Choose what you want to do\n" +
        color.YELLOW + "──────────────────────────────────────────\n" +
        color.GREEN + "1. " + color.RESET + "👦 List all registered users\n" +
        color.GREEN + "2. " + color.RESET + "👦 Search user account\n" +
        color.RED + "3. " + color.RESET + "👦 Deactivate user account\n" +
        color.GREEN + "4. " + color.RESET + "🔑 Create registration token\n" +
        color.GREEN + "5. " + color.RESET + "🔑 List registration tokens\n" +
        color.GREEN + "6. " + color.RESET + "🔑 Delete registration token\n" +
        color.GREEN + "7. " + color.RESET + "💬 List all registered rooms\n" +
        color.RED + "8. " + color.RESET + "💬 Search for a room\n" +
        color.RED + "9. " + color.RESET + "💬 Delete a room\n" +
        color.YELLOW + "──────────────────────────────────────────\n"
    )
    print("Choice [1-9]: " + color.RESET)
    choice = getch.getche()
    print("\n")
    match choice:
        case '1':
            list_users(homeserver, token)
        case '2':
            search_user(homeserver, token)
        case '4':
            create_registration_token(homeserver, token)
        case '5':
            list_registration_tokens(homeserver, token)
        case '6':
            delete_registration_token(homeserver, token)
        case '7':
            list_rooms(homeserver, token)
        case '10':
            exit(0)
        case _:
            exit(0)

    main_menu(homeserver, token)

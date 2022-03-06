from commands import *
import getch


def main_menu(homeserver, token):
    print(
        color.YELLOW + "\n       Choose what you want to do\n" +
        color.YELLOW + "──────────────────────────────────────────\n" +
        color.GREEN + "1. " + color.RESET + "👦 List all registered users\n" +
        color.GREEN + "2. " + color.RESET + "👦 Search user account\n" +
        color.GREEN + "3. " + color.RESET + "👦 Deactivate user account\n" +
        color.GREEN + "4. " + color.RESET + "🔑 Create registration token\n" +
        color.GREEN + "5. " + color.RESET + "🔑 List registration tokens\n" +
        color.GREEN + "6. " + color.RESET + "🔑 Delete registration token\n" +
        color.GREEN + "7. " + color.RESET + "💬 List all registered rooms\n" +
        color.GREEN + "8. " + color.RESET + "💬 Delete a room\n" +
        color.GREEN + "9. " + color.RESET + "❌ Exit\n" +
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
        case '9':
            exit(0)
        case _:
            exit(0)

    main_menu(homeserver, token)

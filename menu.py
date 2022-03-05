import color


def main_menu():
    print(
        color.YELLOW + "\n       Choose what you want to do\n" +
        color.YELLOW + "──────────────────────────────────────────\n" +
        color.GREEN + "1. " + color.RESET + "👦 List all registered users\n" +
        color.GREEN + "2. " + color.RESET + "👦 Deactivate user account\n" +
        color.GREEN + "3. " + color.RESET + "🔑 Create registration token\n" +
        color.GREEN + "4. " + color.RESET + "🔑 List registration tokens\n" +
        color.GREEN + "5. " + color.RESET + "🔑 Delete registration token\n" +
        color.GREEN + "6. " + color.RESET + "💬 List all registered rooms\n" +
        color.GREEN + "7. " + color.RESET + "💬 Delete a room\n" +
        color.GREEN + "8. " + color.RESET + "❌ Exit\n" +
        color.YELLOW + "──────────────────────────────────────────\n"
    )

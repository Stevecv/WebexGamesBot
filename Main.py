import Utils
from AccessToken import ACCESS_TOKEN
from commands import CommandsMain

# Everything to do on bot loading
if __name__ == "__main__":
    print("Starting GamesBot...")

    # Register all the commands
    print("Registering commands...")
    CommandsMain.registerCommands()

    # Log into the bot itself
    print("Logging in...")
    Utils.login(ACCESS_TOKEN)


from Utils import *
from commands import Hangman


@app.route('/messages_webhook', methods=['POST'])
def messages_webhook():
    if request.method == 'POST':
        webhook_obj = Webhook(request.json)
        return process_message(webhook_obj.data)


def help_card():
    return {
        "contentType": "application/vnd.microsoft.card.adaptive",
        "content": {
            "type": "AdaptiveCard",
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.3",
            "body": [
                {
                    "type": "TextBlock",
                    "text": "",
                    "wrap": True,
                    "fontType": "Monospace"
                }
            ]
        }
    }


"""
Takes a message, checks if its sent by the bot or not and processes it
"""


def process_message(data):
    if data.personId == get_teams_api().people.me().id:
        # Message sent by bot, do not respond
        return '200'
    else:
        message = get_teams_api().messages.get(data.id).text
        commands_split = (message.split())[1:]
        command = ' '.join(commands_split)
        if len(command) == 0:
            Utils.send_message_in_room(data.roomId, "@Hangman hangman - Starts a new hangman game\n"
                                                    "@Hangman hangman-custom - Starts a game with a custom word"
                                                    "@Hangman leaderboard-time - Opens the leaderboard for quickest time\n"
                                                    "@Hangman leaderboard-tries - Opens the leaderboard for the least amount of tries")

        parse_message(command, data.personEmail, data.roomId, data.personId)
        return '200'


"""
Registers all commands
"""


def registerCommands():
    print("Register commands")
    registerCommand("hangman", Hangman.HangmanGame.run_game, "Opens the hangman game")
    #registerCommand("leaderboard-time", Leaderboard.show_leaderboard, "Opens the time leaderboard")
    #registerCommand("leaderboard-tries", Leaderboard.show_leaderboard, "Opens the tries leaderboard")
    registerCommand("hangman-custom", Hangman.HangmanGame.run_game, "Creates a game with a custom word")


"""
Registers a singular command
"""


def registerCommand(commandName, commandFunc, desc):
    global commandsDescription

    commands[commandName] = commandFunc
    commandsDescription[commandName] = desc

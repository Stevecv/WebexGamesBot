from commands import Hangman, Leaderboard
from Utils import *


@app.route('/messages_webhook', methods=['POST'])
def messages_webhook():
    if request.method == 'POST':
        webhook_obj = Webhook(request.json)
        return process_message(webhook_obj.data)


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
        parse_message(command, data.personEmail, data.roomId, data.personId)
        return '200'


"""
Registers all commands
"""
def registerCommands():
    print("Register commands")
    registerCommand("hangman", Hangman.HangmanGame.run_game, "Opens the hangman game")
    registerCommand("leaderboard-time", Leaderboard.show_leaderboard, "Opens the leaderboard")


"""
Registers a singular command
"""
def registerCommand(commandName, commandFunc, desc):
    global commandsDescription

    commands[commandName] = commandFunc
    commandsDescription[commandName] = desc

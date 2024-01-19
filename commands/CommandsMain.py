from commands import Test
from Utils import *


@app.route('/messages_webhook', methods=['POST'])
def messages_webhook():
    if request.method == 'POST':
        webhook_obj = Webhook(request.json)
        return process_message(webhook_obj.data)


def process_message(data):
    if data.personId == get_teams_api().people.me().id:
        # Message sent by bot, do not respond
        return '200'
    else:
        message = get_teams_api().messages.get(data.id).text
        commands_split = (message.split())[1:]
        command = ' '.join(commands_split)
        parse_message(command, data.personEmail, data.roomId)
        return '200'


def registerCommands():
    print("Register commands")
    registerCommand("test", Test.test, "Simple test command")


def registerCommand(commandName, commandFunc, commandDescription):
    commands[commandName] = commandFunc
    commandDescription[commandName] = commandFunc

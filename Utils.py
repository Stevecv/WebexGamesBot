import requests

import json
from Utils import *
from flask import Flask, request
from webexteamssdk import WebexTeamsAPI, Webhook

from commands.Hangman import HangmanGame
from commands.Leaderboard import Leaderboard

teams_api = None
commands = {}
commandsDescription = {}


def get_teams_api():
    return teams_api


app = Flask(__name__)

hangmanGame = {}
runningGame = {}


@app.route('/attachmentActions_webhook', methods=['POST'])
def attachmentActions_webhook():
    if request.method == 'POST':
        webhook_obj = Webhook(request.json)
        return process_card_response(webhook_obj.data)


def process_card_response(data):
    global runningGame
    global hangmanGame

    attachment = (teams_api.attachment_actions.get(data.id)).json_data
    inputs = attachment['inputs']

    personId = attachment['personId']
    sender = teams_api.people.get(personId).userName
    room_id = attachment['roomId']

    if len(inputs.keys()) == 0:
        # If the person does not already have a game instance set up, create a new one
        if room_id not in hangmanGame.keys():
            runningGame[room_id] = True
            hangmanGame[room_id] = HangmanGame(sender, room_id, personId, None)
            hangmanGame[room_id].run_game()
            return '200'

        # If the player doesn't have a game running, create one
        if hangmanGame[room_id] is None:
            hangmanGame[room_id] = HangmanGame(sender, room_id, personId, None)
            hangmanGame[room_id].run_game()
            runningGame[room_id] = True
            return '200'
        else:
            # Otherwise, presume they've given up at their current game
            teams_api.messages.create(roomId=room_id, text="Cards Unsupported", attachments=[
                hangmanGame[room_id].generate_given_up_card()])
            hangmanGame[room_id].end_game(False)
            return '200'

    if 'guess' in list(inputs.keys()):
        if runningGame[room_id]:
            hangmanGame[room_id].guess(inputs['guess'])
            return '200'

    if 'submitcustomword' in list(inputs.keys()):
        hangmanGame[room_id] = HangmanGame(sender, room_id, personId, inputs['submitcustomword'])
        hangmanGame[room_id].run_game()
        runningGame[room_id] = True
        return '200'

    return '200'


def send_direct_message(person_email, message):
    teams_api.messages.create(toPersonEmail=person_email, text=message)


def send_message_in_room(room_id, message):
    teams_api.messages.create(roomId=room_id, text=message)


def create_webhook(teams_api, name, webhook, resource):
    delete_webhook(teams_api, name)
    teams_api.webhooks.create(
        name=name, targetUrl=get_ngrok_url() + webhook,
        resource=resource, event='created', filter=None)


def delete_webhook(teams_api, name):
    for hook in teams_api.webhooks.list():
        if hook.name == name:
            teams_api.webhooks.delete(hook.id)


def get_ngrok_url(addr='127.0.0.1', port=4040):
    try:
        ngrokpage = requests.get("http://{}:{}/api/tunnels".format(addr, port), headers="").text
    except:
        raise RuntimeError('Not able to connect to ngrok API')
    ngrok_info = json.loads(ngrokpage)
    return ngrok_info['tunnels'][0]['public_url']


# Logs into the bot with the access token on port 12000
def login(ACCESS_TOKEN):
    global teams_api

    print("Logging in...")
    teams_api = WebexTeamsAPI(access_token=ACCESS_TOKEN)
    print("Connecting webhooks...")
    create_webhook(teams_api, 'messages_webhook', '/messages_webhook', 'messages')
    create_webhook(teams_api, 'attachmentActions_webhook', '/attachmentActions_webhook', 'attachmentActions')
    print("Running app...")
    app.run(host='0.0.0.0', port=12000)


def generate_custom_game():
    return {
        "contentType": "application/vnd.microsoft.card.adaptive",
        "content": {
            "type": "AdaptiveCard",
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.3",
            "body": [
                {
                    "type": "TextBlock",
                    "text": "Enter a word to create a game with a specific word",
                    "wrap": True
                },
                {
                    "type": "Input.Text",
                    "placeholder": "Word",
                    "inlineAction": {
                        "type": "Action.Submit",
                        "id": "submit_custom_word",
                        "title": "Submit",
                        "associatedInputs": "auto"
                    },
                    "id": "submitcustomword"
                }
            ]
        }
    }


def parse_message(command, sender, room_id, personId):
    global commands
    global hangmanGame
    global runningGame

    if command == "hangman-custom":
        teams_api.messages.create(roomId=room_id, text="Cards Unsupported", attachments=[
            generate_custom_game()])
        return

    if command == "hangman":
        runningGame[room_id] = True
        hangmanGame[room_id] = HangmanGame(sender, room_id, personId, None)
        hangmanGame[room_id].run_game()
        return

    if command == "leaderboard-time":
        Leaderboard(room_id).show_leaderboard("quickestTime")
        return

    if command == "leaderboard-tries":
        Leaderboard(room_id).show_leaderboard("lessTries")
        return

    if commands.get(command) is not None:
        cmd = commands.get(command)
        cmd(sender, room_id)

    return

import requests

import json
from flask import Flask, request
from webexteamssdk import WebexTeamsAPI, Webhook

import Utils
from commands import Hangman
from commands.Hangman import HangmanGame

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
    room_id = attachment['roomId']

    if len(inputs.keys()) == 0:
        # If the person does not already have a game instance set up, create a new one
        #if room_id not in hangmanGame.keys():
        #    runningGame[room_id] = True
        #    hangmanGame[room_id] = HangmanGame(sender, room_id, personId)
        #    hangmanGame[room_id].run_game()
        #    return '200'

        # If the player doesn't have a game running, create one

        if hangmanGame[room_id] is None:
            hangmanGame[room_id] = HangmanGame(room_id)
            hangmanGame[room_id].run_game()
            runningGame[room_id] = True
            return '200'
        else:
            # Otherwise, presume they've given up at their current game
            Utils.teams_api.messages.create(roomId=room_id, text="Cards Unsupported", attachments=[
                hangmanGame[room_id].generate_given_up_card()])
            hangmanGame[room_id].end_game()
            return '200'

    if 'guess' in list(inputs.keys()):
        if runningGame[room_id]:
            hangmanGame[room_id].guess(inputs['guess'])
            return '200'

    return '200'


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


def parse_message(command, room_id):
    global commands
    global hangmanGame
    global runningGame

    if command == "hangman":
        print("new hangman game")
        runningGame[room_id] = True
        hangmanGame[room_id] = HangmanGame(room_id)
        hangmanGame[room_id].run_game()
        return

    if commands.get(command) is not None:
        cmd = commands.get(command)
        cmd(room_id)

    return

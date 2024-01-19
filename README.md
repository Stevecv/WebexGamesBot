# Getting Started

Bot with a couple of non-time dependant chat based games

## Set up for development
1. Run in IDE - Make sure to replace the auth token with the token from [here](https://dashboard.ngrok.com/get-started/your-authtoken)
```
.\ngrok.exe config add-authtoken <your access token>
```

2. Then open the port for development
```
.\ngrok.exe http 12000
```

3. Edit the access token in `AccessToken` and replace it with your own token.

4. Run the bot
```commandline
python Main.py
```


# Commands
Commands can be run through pinging the bot and entering a string.


## Creating a command
1. Create a new file in `commands`
2. Paste 
```python
import Utils


def test(sender, roomId):
    print("Send command")
    Utils.send_message_in_room(roomId, "Send message")
```
3. Change name & body of function
4. Navigate to `CommandsMain`, `registerCommands()` and add a line 
```python
registerCommand("test", Test.test, "Simple test command")
```

This will create a new command that can be run by messaging `@gamebot@webex.bot test`


# Sending

We will need to be able to send messages back to the users

## Simple messages

Simple messages can be sent by using a simple function

```Python
Utils.send_message_in_room(roomId, "message")
```
This will send `message` to our user

## Cards

Firstly we need to create a function to generate the card, this is done through json.
A generator can be found [here](https://developer.webex.com/buttons-and-cards-designer)

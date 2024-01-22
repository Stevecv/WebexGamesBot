import time

import Utils
import random
from wonderwords import RandomWord
import csv


class HangmanGame:
    hangmanArts = ["" +
                   "\n" +
                   "\n" +
                   "\n" +
                   "\n" +
                   "\n" +
                   "\n         ─────",

                   "\n           │" +
                   "\n           │" +
                   "\n           │" +
                   "\n           │" +
                   "\n           │" +
                   "\n           │ " +
                   "\n         ──┴──",

                   "            " +
                   "\n        \\  │" +
                   "\n         \\ │" +
                   "\n           │" +
                   "\n           │" +
                   "\n           │ " +
                   "\n         ──┴──",

                   "  ─────────┐" +
                   "\n        \\  │" +
                   "\n         \\ │" +
                   "\n           │" +
                   "\n           │" +
                   "\n           │ " +
                   "\n         ──┴──",

                   "  ┬────────┐" +
                   "\n  0     \\  │" +
                   "\n         \\ │" +
                   "\n           │" +
                   "\n           │" +
                   "\n           │ " +
                   "\n         ──┴──",

                   "  ┬────────┐" +
                   "\n  0     \\  │" +
                   "\n  │      \\ │" +
                   "\n  │        │" +
                   "\n  │        │" +
                   "\n           │ " +
                   "\n         ──┴──",

                   "  ┬────────┐" +
                   "\n  0     \\  │" +
                   "\n  │      \\ │" +
                   "\n ─┼─       │" +
                   "\n  │        │" +
                   "\n           │ " +
                   "\n         ──┴──",

                   "  ┬────────┐" +
                   "\n  0     \\  │" +
                   "\n  │      \\ │" +
                   "\n ─┼─       │" +
                   "\n  │        │" +
                   "\n   \       │ " +
                   "\n         ──┴──",

                   "  ┬────────┐" +
                   "\n  0     \\  │" +
                   "\n  │      \\ │" +
                   "\n ─┼─       │" +
                   "\n  │        │" +
                   "\n / \       │ " +
                   "\n         ──┴──"]

    def __init__(self, room_id):
        self.word = RandomWord().word()
        self.known_letters = []
        self.wrong_letters = []
        self.room_id = room_id
        self.games = 0
        self.won = 0

        self.guess_count = 0
        self.start_time = time.time()

    """
    Converts time from seconds into hours, minutes and seconds
    Only shows necessary values
    """
    def convert_time(self, seconds):
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60

        if hour != 0:
            return "%dh %02dm %02ds" % (hour, minutes, seconds)
        elif minutes != 0:
            return "%02dm %02ds" % (minutes, seconds)
        else:
            return "%02ds" % (seconds)

    """
    Generates a card for when the person has given up
    """
    def generate_given_up_card(self):
        return {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "type": "AdaptiveCard",
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "version": "1.3",
                "body": [
                    {
                        "type": "TextBlock",
                        "text": "The word was: " + self.word + "\n\n" +
                                self.hangmanArts[len(self.hangmanArts)-1].replace(" ", "&nbsp;"),
                        "wrap": True,
                        "fontType": "Monospace"
                    },
                    {
                        "type": "ActionSet",
                        "actions": [
                            {
                                "type": "Action.Submit",
                                "title": "Play again",
                                "style": "positive",
                                "id": "playagain"
                            }
                        ]
                    }
                ]
            }
        }


    """
    Returns a card that shows some basic data about the game
    Allows for correct/incorrect finishes
    """
    def generate_finished_card(self, correct):
        if correct:
            return {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.3",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": "Correct!\n\nThe word was: " + self.word
                                    + "\nYou got it in: "
                                    + str(self.guess_count) + " tries\nYou took: "
                                    + self.convert_time(time.time() - self.start_time),

                            "wrap": True
                        },
                        {
                            "type": "ActionSet",
                            "actions": [
                                {
                                    "type": "Action.Submit",
                                    "title": "Play again",
                                    "style": "positive",
                                    "id": "playagain"
                                }
                            ]
                        }
                    ]
                }
            }
        else:
            return {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.3",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": "Incorrect!\n\nThe word was: " + self.word + "\n\n" +
                                    self.hangmanArts[len(self.hangmanArts)-1].replace(" ", "&nbsp;"),
                            "wrap": True,
                            "fontType": "Monospace"
                        },
                        {
                            "type": "ActionSet",
                            "actions": [
                                {
                                    "type": "Action.Submit",
                                    "title": "Play again",
                                    "style": "positive",
                                    "id": "playagain"
                                }
                            ]
                        }
                    ]
                }
            }

    """
    Generates the card that shows the player the hangman art
    The amount of characters in the word
    Correctly chosen letters
    And incorrect letters
    """
    def generate_card(self):
        if len(self.wrong_letters) > 0:
            art = self.hangmanArts[len(self.wrong_letters) - 1]
        else:
            art = ""
        ans = ""
        for l in range(len(self.word)):
            if self.word[l] in self.known_letters:
                ans = ans + self.word[l] + " "
            else:
                ans = ans + "_ "

        finalArt = art + "\n\n" + ans + "\n\n" + ', '.join(self.wrong_letters)
        return {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "type": "AdaptiveCard",
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "version": "1.3",
                "body": [
                    {
                        "type": "TextBlock",
                        "text": finalArt.replace(" ", "&nbsp;"),
                        "wrap": True,
                        "fontType": "Monospace"
                    },
                    {
                        "type": "Input.Text",
                        "placeholder": "Guess",
                        "inlineAction": {
                            "type": "Action.Submit",
                            "id": "submitguess",
                            "title": "Submit",
                            "associatedInputs": "auto"
                        },
                        "id": "guess"
                    },
                    {
                        "type": "ActionSet",
                        "actions": [
                            {
                                "type": "Action.Submit",
                                "title": "Give up",
                                "id": "giveup",
                                "style": "destructive",
                                "associatedInputs": "none"
                            }
                        ]
                    }
                ]
            }
        }

    """
    Sends a card to the player containing all of the current game information
    Also prompts user for input
    """
    def run_game(self):
        if len(self.wrong_letters) < len(self.hangmanArts):
            Utils.teams_api.messages.create(roomId=self.room_id, text="Cards Unsupported", attachments=[
                self.generate_card()])

        else:
            Utils.teams_api.messages.create(roomId=self.room_id, text="Cards Unsupported", attachments=[
                self.generate_finished_card(False)])
            self.end_game()

    """
    Makes a guess at a character or word in the game
    """
    def guess(self, character_guess):
        self.guess_count += 1
        character_guess = character_guess.lower()

        if len(character_guess) > 1:
            # If the word is correct, exit the game
            if character_guess == self.word:
                Utils.teams_api.messages.create(roomId=self.room_id, text="Cards Unsupported", attachments=[
                    self.generate_finished_card(True)])

                self.end_game()
                return
            else:
                # Add the character to the list of wrong characters
                self.wrong_letters.append(character_guess)

        else:
            # If the character is correct
            if character_guess in self.word:
                # Characters
                self.known_letters.append(character_guess)

            else:
                # Words
                self.wrong_letters.append(character_guess)
                Utils.send_message_in_room(self.room_id, character_guess + " is not in the word")

        # If the game shouldn't be over, prompt for the next guess
        if self.isnt_ended():
            self.run_game()

    """
    Checks if a game can be ended
    And if it can, properly end and close it
    """

    def isnt_ended(self):
        # If the player has used up all their guesses
        if len(self.wrong_letters) > len(self.hangmanArts):
            Utils.teams_api.messages.create(roomId=self.room_id, text="Cards Unsupported", attachments=[
                self.generate_finished_card(False)])

            # Properly exit the game
            self.end_game()
            return False

        return True

    """
    Saves the game data to the database
    """
    def save_data(self):
        db = open('games.csv')
        type(db)

        csv_reader = csv.reader(db)



    """
    Properly exits a game and deletes existing data
    """
    def end_game(self):
        print(Utils.hangmanGame)
        print("end game - " + self.room_id)
        Utils.hangmanGame[self.room_id] = None
        Utils.runningGame[self.room_id] = False

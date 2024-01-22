import csv
import pandas as pd

import Utils


class Leaderboard:
    room_id = None

    def __init__(self, room_id):
        self.room_id = room_id

    def generate_leaderboard_card(self, leaderboard):
        return {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "type": "AdaptiveCard",
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "version": "1.3",
                "body": [
                    {
                        "type": "TextBlock",
                        "text": leaderboard.replace(" ", "&nbsp;"),
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


    def show_leaderboard(self, type):
        if type == "quickestTime":
            names = []
            words = []
            time = []
            tries = []

            lvl = 0
            with open('games.csv') as file_obj:
                reader_obj = csv.reader(file_obj)
                for row in reader_obj:
                    print(row)
                    if len(row) > 0 and lvl > 0:
                        names.append(row[0])
                        words.append(row[1])
                        time.append(row[2])
                        tries.append(row[3])

                    lvl += 1

            df = pd.DataFrame({'Name': names,
                               'Word':  words,
                               'Time' : time,
                               'Tries': tries})

            leaderboard = df.sort_values(by=['Time']).to_string(index=False)
            Utils.send_message_in_room(self.room_id, leaderboard.replace(" ", "&nbsp;"))

            Utils.teams_api.messages.create(roomId=self.room_id, text="Cards Unsupported", attachments=[
                self.generate_leaderboard_card(leaderboard)])

            print(df)
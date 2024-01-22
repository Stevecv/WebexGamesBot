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
                    }
                ]
            }
        }

    def show_leaderboard(self, type):
        names = []
        words = []
        time = []
        tries = []

        lvl = 0
        with open('games.csv') as file_obj:
            reader_obj = csv.reader(file_obj)
            for row in reader_obj:
                if len(row) > 0 and lvl > 0:
                    names.append(row[0])
                    words.append(row[1])
                    time.append(round(float(row[2]), 1))
                    tries.append(int(row[3]))

                lvl += 1

        if type == "quickestTime":
            df = pd.DataFrame({'Name': names,
                               'Word': words,
                               'Time': time})

            df.sort_values(by='Time', ascending=True, inplace=True)
            top_ten = df.head(10)
            Utils.teams_api.messages.create(roomId=self.room_id, text="Cards Unsupported", attachments=[
                self.generate_leaderboard_card(top_ten.to_string(index=False))])

        elif type == "lessTries":
            df = pd.DataFrame({'Name': names,
                               'Word': words,
                               'Tries': tries})

            df.sort_values(by='Tries', ascending=True, inplace=True)
            top_ten = df.head(10)
            Utils.teams_api.messages.create(roomId=self.room_id, text="Cards Unsupported", attachments=[
                self.generate_leaderboard_card(top_ten.to_string(index=False))])

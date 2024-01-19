import Utils


# Test command runner
def test(sender, roomId):
    print("Send command")
    Utils.send_message_in_room(roomId, "Send message")

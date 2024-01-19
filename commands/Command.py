from CommandsMain import commands


class Command:
    def __init__(self, name, method):
        command = self
        name = name.lower()

        commands.add(name, method)

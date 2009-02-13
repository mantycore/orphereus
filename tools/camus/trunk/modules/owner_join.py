# -*- coding: utf-8 -*-
def main(bot, args):
    """join <room> [password] (only for owner)\nJoin a room.\nSee also: leave, rooms"""

    password = ''
    if len(args) == 1 or len(args) == 2:
        if len(args) == 2: password = args[1]

        if bot.join((args[0], password)):
            return 'done'
        else:
            return 'I\'m already in this room'

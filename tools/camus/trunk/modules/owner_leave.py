# -*- coding: utf-8 -*-
def main(bot, args):
    "leave <room> [password] (only for owner)\nLeave a room.\nSee also: join, rooms"""

    password = ''
    if len(args) == 1 or len(args) == 2:
        if len(args) == 2: password = args[1]

        if bot.leave((args[0], password)):
            return 'done'
        else:
            return 'I\'m not in this room'

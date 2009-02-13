# -*- coding: utf-8 -*-
def main(bot, args):
    """rooms (only for owner)\nList rooms.\nSee also: join, leave"""

    if args: return

    if not bot.rooms:
        return 'None'
    else:
        rooms = ''
        for room in bot.rooms:
            rooms += room[0] + ', '
        return rooms[:-2]

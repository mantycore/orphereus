# -*- coding: utf-8 -*-
def main(bot, args):
    """exit (only for owner)\nExit."""

    if not args:
        bot.exit('EXIT: by request')

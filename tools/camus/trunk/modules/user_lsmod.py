def main(bot, args):
    '''lsmod\nShow loaded modules.\nSee also: load, modprobe, rmmod'''

    if not args:
        return 'avialable\nuser: ' + ' '.join(bot.userCommands) + '\nowner: ' + ' '.join(bot.ownerCommands)

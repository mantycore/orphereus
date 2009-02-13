def main(bot, args):
    """man [page]\nShow manual page.\nSee also: help"""

    if not args:
        return 'What manual page do you want?'
    elif len(args) == 1:
        man = ''
        if bot.userCommands.has_key(args[0]):
            man = bot.userCommands[args[0]].__doc__
        elif bot.ownerCommands.has_key(args[0]):
            man = bot.ownerCommands[args[0]].__doc__

        if man:
            return man
        else:
            return 'No manual entry for %s' %(args[0])

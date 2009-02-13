import os

def main(bot, args):
    if args: return

    str = 'Modules:\n'
    for file in os.listdir('modules'):
        if file.endswith('.py') and (file.startswith('user_') or file.startswith('owner_')):
            pos = file.index('_') + 1
            name = file[pos:-3]

            str += file[:-3]
            if bot.userCommands.has_key(name) or bot.ownerCommands.has_key(name):
                str += ': loaded'
            str += '\n'

    return str[:-1]

import datetime

def main(bot, args):
    '''date\nShow current date and time.'''

    if not args:
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

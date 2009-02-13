import re
import subprocess

def main(bot, args):
    """s\nShow radio state."""
    #p2 = Popen(["cowsay", ' '.join(args)], stdout=PIPE)
    output = Popen(["cowsay", 'wat'], stdout=PIPE).communicate()[0]
    return output
    #os.system("cowsay %s" %(args[0]))
#    txt = "
#    return txt

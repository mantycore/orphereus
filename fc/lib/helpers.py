"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
from webhelpers import *

def modLink(string, secid):
    p1 = string[0:4]
    p2 = string[4:8]
    p3 = string[8:len(string)]
    return p1 + str(secid) + p2 + p3


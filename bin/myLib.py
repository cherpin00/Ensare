# RED = "\033[1;31;200m"
# YELLOW = '\033[1;32;200m'

import os

def reverse(str):
    return str[::-1]


def endsWith(haystack, needle):
    if needle in haystack:
        return reverse(haystack).index(reverse(needle)) == 0
    else:
        return False


def setParams(filename):
    with open(filename) as file:
        for line in file:
            #print("line=", line)
            if line.lstrip().startswith('#'):
                continue
            if line.lstrip().startswith('//'):
                continue
            if line.lstrip().replace(chr(10), "") == "":
                continue
            try:
                key, value = line.strip().split('=', 1)
            except:
                raise Exception("An error occurred reading parameters from filename, " + filename + ".  Line the failed:" + line)
            os.environ[key] = value


def colorString(str, color):
    if color is None:
        return str
    else:
        return color+ str + '\033[1;37;200m'


def factorial(num):
    if num != 0:
        fact = factorial(num-1)
    else:
        fact = factorial(1)

print(factorial(5))

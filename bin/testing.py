import os
import myLib
#
# a = ['.exe', '.py', '.bat']
#
# file = 'getRun.exe'
#
# print(file.index('.'))
# print(file[file.index('.'):-1] + file[-1])
# if file[file.index('.'):-1] + file[-1] in a:
#     print("yes")
#
# if "." in file:
#     print("yes again")
#
# depth = 1
# structure = ['data', 'customer*', 'projects*', 'modules*']
# print(len(structure[depth][:-1])-1)
#
# x = "get.bat.bat"
#
# print(x[::-1].index(".bat"[::-1]))
#
#
# # if myLib.endsWith("jh", ".bat"):
# #     print("yes")
#
# if ".bat" in "hello.bat":
#     print("it is")
#
# # print(reversed(x).index(reversed(".bat")))


# print(os.chdir("../data"))
#
# print()
#
# for file in os.listdir("../data"):
#     print(file)
# # for file in os.walk(os.chdir("..\\data")):
# #     print(file)
#
# print()

import sys
import os

# if len(sys.argv) != 2:
#     print('Usage: %s input_file' % (sys.argv[0]))
#     sys.exit(1)  # 1 indicates error
#
# print('Opening file %s.' % sys.argv[1])
#
# if not os.path.exists(sys.argv[1]):  # Make sure file exists
#     print('File does not exist.')
#     sys.exit(1)  # 1 indicates error
#
# f = open(sys.argv[1], 'r')

# Input files should contain two integers on separate lines

# print('Reading two integers.')
# num1 = int(f.readline())
# num2 = int(f.readline())
#
# print('Closing file %s' % sys.argv[1])
# f.close()  # Done with the file, so close it
#
# print('\nnum1: %d' % num1)
# print('num2: %d' % num2)
# print('num1 + num2: %d' % (num1 + num2))

import myLib

RED = "\033[1;31;200m"
YELLOW = '\033[1;32;200m'

print(myLib.colorString("hello", RED))




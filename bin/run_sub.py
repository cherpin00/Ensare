import os
# from run_all import structure
# from run_all import counter


# structureValue = structure[counter]
# command = "cd" + " " + structure[counter] + " ", "&& python run_sub.py "
#
# if structureValue[len(structureValue)-1] == "*":
#     print(command)
#     os.system(command)
# else:
#     os.system("cd && python run_all.py")

import sys
import os


print(len(sys.argv))

if len(sys.argv) != 4:
    # sys.argv.pop(0)
    raise Exception(sys.argv[0] + " must be called with exactly 3 arguments.  Was called with " + str(sys.argv))

depth = int(sys.argv[1])
structure = sys.argv[2].split(',')
excc_extensions = sys.argv[3].split(',')

print('depth', depth)
print('structure', structure)
print("ext", excc_extensions)

if depth > len(structure) - 1:
    try:
        os.chdir('collectors')
    except:
        print("ERROR deepest folder must be collectors folder with get*.bat files")
        raise Exception('error was:' + sys.exc_infor()[0])
    for i in excc_extensions:
        for j in os.listdir():
            os.envion[""]


print(str(sys.argv))


import os
import myLib


ABORTONERROR = True

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

print("running run_sub ---------------------" + os.getcwd())

import sys
import os

def set_params(filename):

    with open(filename) as file:
        for line in file:
            #print("line=", line)
            if line.lstrip().startswith('#'):
                continue
            if line.lstrip().startswith('//'):
                continue
            if line.lstrip().replace(chr(10),"") == "":
                continue
            try:
                key, value = line.strip().split('=', 1)
            except:
                raise Exception("An error occurred reading parameters from filename, " + filename + ".  Line the failed:" + line)
            os.environ[key] = value


def getFolderList(parentFolderName, startsWith):
    retFolders=[]
    for folder in os.listdir(parentFolderName):
        # print("checking if", folder[:len(startsWith)], "matches with", startsWith)
        if folder[:len(startsWith)] == startsWith:
            retFolders.append(folder)
    print("the folders in", parentFolderName, 'that start with', startsWith, 'are', retFolders)
    return retFolders


def processFolder(element, folder):
    if folder == 'none':
        comand = 'python ' + str(bin_wd) + '/run_sub.py ' + str(element+1) + ' ' + strStructure + ' ' + strExtensions
        os.system(comand)
    else:
        comand = 'python ' + str(bin_wd) + '/run_sub.py ' + str(element+1) + ' ' + strStructure + ' ' + strExtensions
        os.system('cd ' + folder + "&&" + comand)

####################
# Beginning of run


param_filename = "params"

bin_wd = os.path.dirname(sys.argv[0])

RED = "\033[1;31;200m"
YELLOW = '\033[1;32;200m'

def colorString(str, color):
    if color is None:
        return str
    else:
        return color+ str + '\033[1;37;200m'


print(len(sys.argv))

if len(sys.argv) != 4:
    # sys.argv.pop(0)
    raise Exception(sys.argv[0] + " must be called with exactly 3 arguments.  Was called with " + str(sys.argv))

depth = int(sys.argv[1])
structure = sys.argv[2].split(',')
excc_extensions = sys.argv[3].split(',')

strStructure = ''
for i in structure:
    strStructure = strStructure + ',' + i
strStructure = strStructure.replace(',', "", 1)

strExtensions = ''
for i in excc_extensions:
    strExtensions = strExtensions + ',' + i
strExtensions = strExtensions.replace(',', "", 1)

if depth > len(structure) -1:
    msg="past end of structure"
else:
    msg= 'on ' + structure[depth]
print('PID:', os.getpid())
print('depth', depth)
print('structure', structure, msg)
print("ext", excc_extensions)

print("Params on entry to folder")
# os.system("set wd && pause")

if os.path.exists(param_filename):
    set_params(param_filename)
else:
    print("No", param_filename, "exists in", os.getcwd())

if depth > len(structure) - 1:
    try:
        print("changing to collectors")
        os.chdir('collectors')
        print("current folder is", os.getcwd())
    except:
        print(colorString(" ERROR deepest folder must be collectors folder with get*.bat files ", RED))
        exit() #  Note if the code coninues to run it will still check for get files and run those. This might not be bad if the user frogot to make a collocter folder
        # raise Exception('error was:' + sys.exc_infor()[0])
    for file in os.listdir(os.getcwd()):
        print("checking the file", file)
        isGood = False
        for x in excc_extensions:
            if myLib.endsWith(file, x) and file[:3] == "get":
                isGood = True
                break
        if not isGood:
            continue
        else:
            tempFolder = os.getcwd() + os.sep
            tempSting = "will run " + tempFolder + file
            print(colorString(tempSting, YELLOW)) #  TODO if the file with the right extension is found change to data and run the get file
            try:
                os.chdir("../data")
            except:
                print(colorString(os.getcwd() + "/../data does not exist. Not running collectors", RED))
            ret = os.system("echo off &&" + tempFolder + file + ">" + file + ".txt 2>&1")
            print("ret is", ret)
            os.system("pause")
            if ret != 0:
                # Checks only last returned value of collector.bat file
                # TODO: To properly determine if error exsists - rederect error to diffrent file and if error file is empty no error otherwise there is an error
                if ABORTONERROR:
                    raise Exception("get returned error aborting module...")
                else:
                    print(colorString("Warning get returned an error but abort on error = False", RED))
        print("params after get's run")
        # os.system("set wd && pause")
else:
    if structure[depth][-1] == "*":
        folders = getFolderList(os.getcwd(), structure[depth][:-1])
        for f in folders:
            print("trying to change to", f)
            processFolder(depth, f)
    else:
        processFolder(depth, structure[depth])

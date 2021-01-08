import os
from subprocess import Popen, PIPE
from time import sleep
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
import configparser


def run(cmd):
    print("cmd:",cmd)
    p = Popen(cmd.split(" "), stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    return out.decode()

def gitSaveDiff(filename):
    with open(filename, "w") as f:
        f.write(run("git diff head head~1 ."))

def gitCommit():
    reldir = os.path.join(os.getcwd(), "..")
    run(f"git add {reldir}")
    run(f'git commit ../. -m "Ensnare auto commit. {os.sep.join(reldir.split(os.sep)[:-2])}{os.sep}"')

def set_params(filename):
    config = configparser.ConfigParser()
    default = "DEFAULT"
    with open(filename, "r") as f:
        iniStr = f.read()
    iniStr = f"[{default}]\n" + iniStr
    config.read_string(iniStr)
    for param_key in config[default]:
        os.environ[param_key] = config[default][param_key]
    # with open(filename) as file:
    #     for line in file:
    #         #print("line=", line)
    #         if line.lstrip().startswith('#'):
    #             continue
    #         if line.lstrip().startswith('//'):
    #             continue
    #         if line.lstrip().replace(chr(10),"") == "":
    #             continue
    #         try:
    #             key, value = line.strip().split('=', 1)
    #         except:
    #             raise Exception("An error occurred reading parameters from filename, " + filename + ".  Line the failed:" + line)
    #         os.environ[key] = value


def getFolderList(parentFolderName, startsWith):
    retFolders=[]
    for folder in os.listdir(parentFolderName):
        if not os.path.isdir(folder):
            continue
        # print("checking if", folder[:len(startsWith)], "matches with", startsWith)
        if folder[:len(startsWith)] == startsWith:
            retFolders.append(folder)
        else:#TODO: need to use logging module
            print(colorString(f"WARNING: Folder ignored, does not start with {startsWith}", RED), os.path.join(parentFolderName, folder))
    print("the folders in", parentFolderName, 'that start with', startsWith, 'are', retFolders)
    return retFolders


def processFolder(element, folder):
    comand = 'python ' + str(bin_wd) + '/run_sub.py ' + str(element+1) + ' ' + strStructure + ' ' + strExtensions
    if folder == 'none':
        os.system(comand)
    else:
        os.system('cd ' + folder + "&&" + comand)
    
    #TODO: If ABORTONERROR then stop processing folder

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
        return color + str + '\033[1;37;200m'


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

# print("Params on entry to folder")
# os.system("set wd && pause")

if os.path.exists(param_filename):
    set_params(param_filename)
    # os.system(f"type {param_filename} && cmd")
    print(f"Processing params file, {param_filename}.")
else:
    print("No", param_filename, "exists in", os.getcwd())

if depth > len(structure) - 1:
    try:
        print("changing to collectors")
        os.chdir('collectors')
        print("current folder is", os.getcwd())
    except:
        print(colorString(f"ERROR: missing collectors with get* files. Deepest folder must be named collectors.", RED), os.getcwd())
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
            dataDir = str(os.path.join("..", "data"))
            try:
                os.chdir(dataDir)
            except:
                print(colorString(os.getcwd() + dataDir + " does not exist. Not running collectors", RED))
            ret = os.system("echo off &&" + tempFolder + file + ">" + file + ".txt 2>&1") #TODO: Call extension type with correct interpreter
            #TODO: Use popen to make this cross platform
            #TODO: Use env variable flag to ignore stderr or not
            #TODO: Add flag: redirectStderr for collectors
            print("ret is", ret)
            # os.system("pause")
            if ret != 0:
                # Checks only last returned value of collector.bat file
                # TODO: To properly determine if error exsists - rederect error to diffrent file and if error file is empty no error otherwise there is an error
                if ABORTONERROR:
                    raise Exception("get returned error, aborting module...")
                else:
                    print(colorString("Warning get returned an error but abort on error = False", RED))
        # print("params after get's run")
        # os.system("set wd && pause")
        gitCommit()
        sleep(1)
        filename = f"{os.sep.join(tempFolder.split(os.sep)[:-1])}"
        gitSaveDiff(filename.replace(os.sep, "__"))
else:
    for file in os.listdir(os.getcwd()):
        if os.path.isfile(file) and file != param_filename:
            print(colorString(f"WARNING: File ignored, it is not at the end of dir structure.", RED), os.path.join(os.getcwd(), file))
    folders = getFolderList(os.getcwd(), structure[depth][:-1])
    if structure[depth][-1] == "*":
        for f in folders:
            print("trying to change to", f)
            processFolder(depth, f)
    else:
        for f in folders:
            if structure[depth] != f and not os.path.isfile(f):
                print(colorString(f"WARNING: Folder ignored, not in defined dir structure.", RED), f)
        processFolder(depth, structure[depth])

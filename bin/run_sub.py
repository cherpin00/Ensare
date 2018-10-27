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
        print("\033[1;31;200m ERROR deepest folder must be collectors folder with get*.bat files \033[1;37;200m")
        exit() #  Note if the code coninues to run it will still check for get files and run those. This might not be bad if the user frogot to make a collocter folder
        # raise Exception('error was:' + sys.exc_infor()[0])
    for file in os.listdir(os.getcwd()):
        print("checking the file", file)
        if "." in file:
            index = file.index('.')
        else:
            continue
        if file[index:-1] + file[-1] in excc_extensions and file[:3] == "get":  #TODO add condition start with "get"
            print('\033[1;32;200m \twill run', file, '\033[1;37;200m') #  TODO if the file with the right extension is found change to data and run the get file
else:
    if structure[depth][-1] == "*":
        folders = getFolderList(os.getcwd(), structure[depth][:-1])
        for f in folders:
            print("trying to change to", f)
            processFolder(depth, f)
    else:
        processFolder(depth, structure[depth]) #  Not sure why this is none

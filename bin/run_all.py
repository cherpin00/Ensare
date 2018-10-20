import os

bin_wd = os.getcwd()
os.chdir('../data')

structure = ['data', 'customers*', 'projects*', 'modules*']
excc_extensions = ['.bat', '.exe', '.py']

strStructure = ''
for i in structure:
    strStructure = strStructure + ',' + i
strStructure = strStructure.replace(',', "", 1)

strExtensions = ''
for i in excc_extensions:
    strExtensions = strExtensions + ',' + i
strExtensions = strExtensions.replace(',', "", 1)


element = 10
command = 'python ' + str(bin_wd) + '/run_sub.py ' + str(element) + ' ' + strStructure + ' ' + strExtensions

print("x =", os.system(command))
# TODO: allow user to specify weather to quit on error
# TODO: implement a read only mode(what if mode), could be parameter to this file or in params file

if os.system(command) != 0:
    raise Exception("We decided to stop processing because an error was found")
# os.system("cd xxx && python run_all.py")
#
# os.system("dir")
# os.system("cd .. && dir")
# os.system("dir")

print("run all just ran")




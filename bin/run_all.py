import os
import myLib

# https://www.python-course.eu/forking.php

stop_on_error = False

top_wd = os.path.abspath("..")
bin_wd = os.path.join(top_wd, "bin")
data_wd = os.path.join(top_wd, "data")
reports_wd = os.path.join(top_wd, "reports")
os.chdir(data_wd)    #change to ../data
if not os.path.exists(reports_wd):
    raise RuntimeError(f"Reports folder, {reports_wd} does not exist.")
os.environ["reportsFolder"] = reports_wd



structure = ['customer*', 'projects*', 'modules*']
excc_extensions = ['.bat', '.exe']
# excc_extensions = ['.bat', '.exe', '.py']

strStructure = ''
for i in structure:
    strStructure = strStructure + ',' + i
strStructure = strStructure.replace(',', "", 1)

strExtensions = ''
for i in excc_extensions:
    strExtensions = strExtensions + ',' + i
strExtensions = strExtensions.replace(',', "", 1)


element = 0
command = 'python ' + str(bin_wd) + '/run_sub.py ' + str(element) + ' ' + strStructure + ' ' + strExtensions

x = os.system(command)
# TODO: allow user to specify weather to quit on error
# TODO: implement a read only mode(what if mode), could be parameter to this file or in params file

if x != 0 and stop_on_error:
    raise Exception("We decided to stop processing because an error was found")
# os.system("cd xxx && python run_all.py")
#
# os.system("dir")
# os.system("cd .. && dir")
# os.system("dir")

print("Finished collecting all.")





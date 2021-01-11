import os
from subprocess import Popen, PIPE
from time import sleep
import myLib
import sys
import configparser
import logging
import coloredlogs
import multiprocessing

from sql import getSession

ABORTONERROR = True
RED = "\033[1;31;200m"
YELLOW = '\033[1;32;200m'

logger = logging.getLogger(__name__)
coloredlogs.install(level=logging.DEBUG)

def run(cmdArr):
    print("cmd:",cmdArr)
    p = Popen(cmdArr, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    if len(err.decode()) > 0:
        print("cmd error:", err.decode())
    return out.decode()

def gitSaveDiff(filename):
    with open(filename, "w") as f:
        cmd = ["git", "diff", "head", "head~1", "."]
        f.write(run(cmd))

def gitCommit():
    reldir = os.path.join(os.getcwd(), "..")
    cmd = ["git", "add", reldir]
    run(cmd)
    cmd = ["git", "commit", "../.", "-m", f"Ensnare auto commit. {os.sep.join(reldir.split(os.sep)[:-2])}{os.sep}"]
    run(cmd)

def set_params(filename):
    config = configparser.ConfigParser()
    default = "DEFAULT"
    with open(filename, "r") as f:
        iniStr = f.read()
    iniStr = f"[{default}]\n" + iniStr
    config.read_string(iniStr)
    for param_key in config[default]:
        os.environ[param_key] = config[default][param_key]

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

def colorString(str, color):
        if color is None:
            return str
        else:
            return color + str + '\033[1;37;200m'

def startSubProcess(depth, structure, excc_extensions, f) -> int:
    """
    Starts runSub waits for it to finished and then returns the exit code.
    """
    p = multiprocessing.Process(target=runSub, args=(depth, structure, excc_extensions, f))
    p.start()
    p.join()
    return p.exitcode

####################
# Beginning of run

def runSub(depth:int, structure:list, excc_extensions:list, folder:str = None):
    """

    """
    programs = {
        ".py" : "python",
        ".bat" : "",
        ".exe" : ""
    }

    param_filename = "params"

    bin_wd = os.path.dirname(sys.argv[0])

    print("running run_sub ---------------------" + os.getcwd())

    if folder is not None:
        os.chdir(folder)

    if depth > len(structure)-1:
        msg="past end of structure"
    else:
        msg= 'on ' + structure[depth]
    print('PID:', os.getpid())
    print('depth', depth)
    print('structure', structure, msg)
    print("ext", excc_extensions)

    if os.path.exists(param_filename):
        set_params(param_filename)
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
            return #  Note if the code coninues to run it will still check for get files and run those. This might not be bad if the user frogot to make a collocter folder
            # raise Exception('error was:' + sys.exc_infor()[0])
        for file in os.listdir(os.getcwd()):
            print("checking the file", file)
            isGood = False
            ext = None
            for x in excc_extensions:
                if myLib.endsWith(file, x) and file[:3] == "get":
                    ext = x
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
                # ret = os.system("echo off &&" + tempFolder + file + ">" + file + ".txt 2>&1") #TODO: Call extension type with correct interpreter
                if ext in programs:
                    error_occurred = False
                    prog = programs[ext]
                    cmd = " ".join([prog, tempFolder + file, ">", file + ".txt"]).strip() #Strip out space at front if there is no prog to run the file with
                    try:
                        # p = Popen(cmd.split(" "), stderr=PIPE, stdout=PIPE)
                        p = Popen(cmd, stderr=PIPE, stdout=PIPE, shell=True) #TODO: Shell is insecure
                        out, err = p.communicate()
                        if p.returncode != 0:
                            # Checks only last returned value of collector.bat file
                            # TODO: To properly determine if error exsists - rederect error to diffrent file and if error file is empty no error otherwise there is an error
                            error_occurred = True
                    except Exception as e:
                        error_occurred = True
                        err = e
                        out = "Error occurred executing getter"
                    if error_occurred:
                        print(f"Command ran: {cmd}")
                        print(f"Stdout: {out}")
                        print(f"Stderr: {err}")
                        if ABORTONERROR:
                            raise Exception("get returned error, aborting module...")
                        else:
                            print(colorString("Warning get returned an error but abort on error = False", RED))
                else:
                    print("Do not know what program to use for extension", ext)
                    continue
                #TODO: Use env variable flag to ignore stderr or not
                #TODO: Add flag: redirectStderr for collectors
            # print("params after get's run")
            # os.system("set wd && pause")
            gitCommit()
            filename = f"{os.sep.join(tempFolder.split(os.sep)[:-1])}"
            gitSaveDiff(os.path.join(os.environ["reportsFolder"], filename.replace(os.sep, "__")))
    else:
        for file in os.listdir(os.getcwd()):
            if os.path.isfile(file) and file != param_filename:
                print(colorString(f"WARNING: File ignored, it is not at the end of dir structure.", RED), os.path.join(os.getcwd(), file))
        
        folders = getFolderList(os.getcwd(), structure[depth][:-1])
        newFolder = ""
        for f in folders:
            if structure[depth][-1] == "*":
                print("trying to change to", f)
                newFolder = f
            else:
                if structure[depth] != f and not os.path.isfile(f):
                    print(colorString(f"WARNING: Folder ignored, not in defined dir structure.", RED), f)
                    continue
                newFolder = structure[depth]
            errorCode = startSubProcess(depth+1, structure, excc_extensions, newFolder)
            if errorCode != 0:
                raise RuntimeError("Caught Error in subprocess")
            
            
        # if structure[depth][-1] == "*":
        #     for f in folders:
        #         print("trying to change to", f)
        #         # processFolder(depth, f)
        #         # runSub(depth+1, structure, excc_extensions, f)
        #         startSubProcess(depth+1, structure, excc_extensions, f)
        # else:
        #     for f in folders:
        #         if structure[depth] != f and not os.path.isfile(f):
        #             print(colorString(f"WARNING: Folder ignored, not in defined dir structure.", RED), f)
        #     startSubProcess(depth+1, structure, excc_extensions, structure[depth])



def send_emails():
    print("Sending emails.")
    path = os.environ["reportsFolder"]
    files = os.listdir(".")
    for f in files:
        if not os.path.isfile(f):
            logging.warning(f"{f} is not a file. Skipping.")
        print(f)



if __name__ == "__main__":

    top_wd = os.path.abspath("..")
    bin_wd = os.path.join(top_wd, "bin")
    data_wd = os.path.join(top_wd, "data")
    reports_wd = os.path.join(top_wd, "reports")
    os.chdir(data_wd)    #change to ../data
    if not os.path.exists(reports_wd):
        raise RuntimeError(f"Reports folder, {reports_wd} does not exist.")
    os.environ["reportsFolder"] = reports_wd

    sqlSession = getSession()
    exit()

    structure = ['customer*', 'projects*', 'modules*']
    excc_extensions = ['.bat', '.exe', '.py']
    element = 0
    runSub(element, structure, excc_extensions)

    print("Finished running collectors.")
    send_emails()
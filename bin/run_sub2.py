import sqlite3
import datetime
import os
from subprocess import Popen, PIPE
from time import sleep
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import session, sessionmaker
from sqlalchemy.pool.impl import NullPool, StaticPool
import myLib
import sys
import configparser
import logging
import coloredlogs
import multiprocessing
import sqlalchemy
from sqlalchemy.sql import select, text

from sql import Base, Notify

# engine = create_engine("sqlite:///:memory:", echo=True) #Echo is debug var
database = r"C:\Data\clients\Rudd\programming\Ensnare\bin\temp.db"
engine = create_engine(f"sqlite:///{database}", )
# import sqlite3
# import sqlalchemy.pool

# sqlite = sqlalchemy.pool.manage(sqlite3, poolclass=sqlalchemy.pool.SingletonThreadPool)
# engine = sqlite.connect(':memory:')


ABORTONERROR = True
RED = "\033[1;31;200m"
YELLOW = '\033[1;32;200m'

logger = logging.getLogger(__name__)
coloredlogs.install(level=logging.DEBUG)

def getSession():
	Base.metadata.create_all(engine)
	DBSession = sessionmaker(bind=engine)
	return DBSession()

def run(cmdArr):
	logger.debug("cmd:" + " ".join(cmdArr))
	p = Popen(cmdArr, stdout=PIPE, stderr=PIPE)
	out, err = p.communicate()
	if len(err.decode()) > 0:
		logger.debug("cmd error:" + err.decode())
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
		if folder[:len(startsWith)] == startsWith:
			retFolders.append(folder)
		else:#TODO: need to use logging module
			p = os.path.join(parentFolderName, folder)
			logger.warning(f"WARNING: Folder ignored, does not start with {startsWith} {p}")
	logger.info(f"the folders in {parentFolderName} that start with startsWith are {retFolders}")
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

def startSubProcess(depth, structure, excc_extensions, f, runCollectors) -> int:
	"""
	Starts runSub waits for it to finished and then returns the exit code.
	"""
	pass


####################
# Beginning of run

def runSub(depth:int, structure:list, excc_extensions:list, folder:str = None, runCollectors=True, startTime=None, baseDir=None):
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
	logger.debug(f'PID: {os.getpid()}')
	logger.debug(f'depth {depth}')
	logger.debug(f'structure {structure} {msg}')
	logger.debug(f"ext {excc_extensions}")

	if os.path.exists(param_filename):
		logger.info(f"Processing params file, {param_filename}.")
		set_params(param_filename)
	else:
		logger.warning("No " + param_filename + " exists in " + os.getcwd())

	currentFolder = os.getcwd() + os.sep
	collected_filename = f"{os.sep.join(currentFolder.split(os.sep)[1:])}".replace(baseDir, "")
	collected_filename = collected_filename.replace(os.sep, "__")+".txt" #-2 -> take off the collector from the path

	if depth > len(structure) - 1:
		try:
			os.chdir('collectors')
			logger.debug("current folder is" + os.getcwd())
		except:
			logger.error(f"ERROR: missing collectors with get* files. Deepest folder must be named collectors." + os.getcwd())
			return #  Note if the code coninues to run it will still check for get files and run those. This might not be bad if the user frogot to make a collocter folder
			# raise Exception('error was:' + sys.exc_infor()[0])
		number_of_collectors = 0
		if runCollectors:
			for file in os.listdir(os.getcwd()):
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
					tempSting = "will run " + currentFolder + file
					logger.debug(tempSting)
					dataDir = str(os.path.join("..", "data"))
					try:
						os.chdir(dataDir)
					except:
						logger.warning(str(os.getcwd() + dataDir + " does not exist. Not running collectors"))
					# ret = os.system("echo off &&" + tempFolder + file + ">" + file + ".txt 2>&1") #TODO: Call extension type with correct interpreter
					if ext in programs:
						error_occurred = False
						prog = programs[ext]
						cmd = " ".join([prog, os.path.join(currentFolder, "collectors", file), ">", file + ".txt"]).strip() #Strip out space at front if there is no prog to run the file with
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
							logger.error(f"Error on command: {cmd}")
							logger.error(f"Stdout: {out}")
							logger.error(f"Stderr: {err}")
							if ABORTONERROR:
								raise Exception("get returned error, aborting module...")
							else:
								logger.warning("Warning get returned an error but abort on error = False")
						else:
							number_of_collectors += 1
					else:
						logger.error(f"Cannot find program for extension {ext}")
						if ABORTONERROR:
							raise RuntimeError("See error message above")
						continue
					#TODO: Use env variable flag to ignore stderr or not
					#TODO: Add flag: redirectStderr for collectors
				gitCommit()
				gitSaveDiff(os.path.join(os.environ["reportsFolder"], collected_filename))
		else:
			logger.info("Skipping collectors because of flag.")
		if number_of_collectors > 0 or not runCollectors:
			session = getSession()
			start = "notify"
			for key in os.environ:
				if key[:len(start)] == start.upper(): #We expect all env variable to be upper case
					email = os.environ[key]
					logger.debug(f"Adding {key}'s email ({email}) to the email list.")
					n = Notify(
						name=key, 
						email=email, 
						file=collected_filename,
						batchTime=startTime
						)
					session.add(n)
			session.commit()
	else:
		for file in os.listdir(os.getcwd()):
			if os.path.isfile(file) and file != param_filename:
				p = os.path.join(os.getcwd(), file)
				logger.warning(f"WARNING: File ignored, it is not at the end of dir structure. {p}")
		
		folders = getFolderList(os.getcwd(), structure[depth][:-1])
		newFolder = ""
		for f in folders:
			if structure[depth][-1] == "*":
				logger.debug("trying to change to " + f)
				newFolder = f
			else:
				if structure[depth] != f and not os.path.isfile(f):
					logger.warning(f"WARNING: Folder ignored, not in defined dir structure." + f)
					continue
				newFolder = structure[depth]
			p = multiprocessing.Process(target=runSub, args=(depth+1, structure, excc_extensions, newFolder, runCollectors, startTime, baseDir))
			p.start()
			p.join()
			if p.exitcode != 0:
				raise RuntimeError("Caught Error in subprocess")
			
def sqlGetJsonFromQuery(sql, conn):
	cursor = conn.cursor()
	cursor.execute(sql)
	headers = [x[0] for x in cursor.description]
	rows = cursor.fetchall()

	my_json = []
	for row in rows:
		current_dict = {}
		for index, col in enumerate(headers):
			current_dict[col] = row[index]
		my_json.append(current_dict)
	return my_json

def send_emails(time):
	print("Sending emails.")
	session = getSession()
	conn = sqlite3.connect(database)
	sql = "select email, count(*) from tblNotify where batchTime in (select batchTime from tblNotify order by batchTime desc limit 1) group by email"
	toNotify = session.query(Notify).all()
	emailDict = sqlGetJsonFromQuery(sql, conn)
	for row in emailDict:
		logger.debug(f"row:{row}")
		to = row["email"]
		sql = f"select * from tblNotify where email = '{to}' and batchTime in (select batchTime from tblNotify order by batchTime desc limit 1)"
		toNotify = sqlGetJsonFromQuery(sql, conn)
		logger.debug(f"toNotify:{toNotify}")
		for x in toNotify:
			logger.debug(f"x:{x}")
			path = os.environ["reportsFolder"]
			path = os.path.join(path, x["file"])
			if not os.path.exists(path):
				logger.error(f"Cannot send {path}. Does not exist.")
				continue
			try:
				myLib.sendEmail([x["email"]], "Ensnare found change.", "", filename=path) #TODO: Move this to the first for loop so that we send one email to each recepient
			except Exception as e:
				logger.error(f"Error sending email. ({e})")
		



if __name__ == "__main__":
	# if os.path.exists(database):
		# os.remove(database)

	top_wd = os.path.abspath("..")
	bin_wd = os.path.join(top_wd, "bin")
	data_wd = os.path.join(top_wd, "data")
	reports_wd = os.path.join(top_wd, "reports")
	os.chdir(data_wd)    #change to ../data
	if not os.path.exists(reports_wd):
		raise RuntimeError(f"Reports folder, {reports_wd} does not exist.")
	os.environ["reportsFolder"] = reports_wd


	runCollectors = True
	structure = ['customer*', 'projects*', 'modules*']
	excc_extensions = ['.bat', '.exe', '.py']
	element = 0
	startTime = datetime.datetime.now()
	p = multiprocessing.Process(target=runSub, args=(element, structure, excc_extensions, data_wd, runCollectors, startTime, top_wd))
	p.start()
	p.join()

	print("Finished running collectors.")
	send_emails(startTime)
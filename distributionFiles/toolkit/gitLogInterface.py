import os
import subprocess
import pandas as pd
from StringIO import StringIO

def isGitRepo(path):
    return subprocess.call(['git', '-C', path, 'status'], stderr=subprocess.STDOUT, stdout = open(os.devnull, 'w')) == 0

def cloneGitRepo(baseDirectory,repositoryURL):
	os.system("cd %s; git clone %s" % (baseDirectory, repositoryURL))

def switchToRevision(baseDirectory,revisionHash):
	os.system("cd %s; git checkout %s" % (baseDirectory, revisionHash))

def makeGitLog(sourceDirectory,filesToInspect,lastTimestamp,previousTimestamp,storageConnection):
	import storage
	tableName = 'gitLog_'+lastTimestamp+'_'+previousTimestamp

	if storage.tableExists(tableName, storageConnection):
		return

	command = "cd %s; git log %s...%s --pretty=format:'[%%h] %%aN %%ad %%s' --date=short --date-order --numstat  -- %s" % (sourceDirectory, lastTimestamp, previousTimestamp, filesToInspect)
	gitlog = subprocess.check_output(command, shell=True)

	storage.writeFile(tableName, storageConnection, gitlog)

def makeCommitDateMapping(sourceDirectory,filesToInspect,storageConnection,branchname='master'):
	import storage

	tableName = branchname + '_commitDates'
	if storage.tableExists(tableName, storageConnection):
		return storage.readTable(tableName, storageConnection)

	switchToRevision(sourceDirectory,branchname)

	command = "cd %s; git log --pretty=format:'%%h,%%ad' --date=short -- %s" % (sourceDirectory, filesToInspect)
	try:
		dates = pd.read_csv(StringIO(subprocess.check_output(command, shell=True)), names=['sha','date'],dtype={'sha': str, 'date': str})
		storage.writeTable(tableName, storageConnection, dates)
	except subprocess.CalledProcessError:
	    dates = "no commit date mapping available"

	return dates
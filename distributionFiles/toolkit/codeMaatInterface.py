import os
import subprocess
import pandas as pd
from StringIO import StringIO
import pdb

def runAnalysis(logFile,logFileType,analysisType):
	codeMaatPath =  os.path.dirname(os.path.abspath(__file__)) + "/../code-maat"
	command = "cd " + codeMaatPath + "; lein run -l %s -c %s -a %s" % (logFile, logFileType, analysisType)
	return subprocess.check_output(command, shell=True)

def runAnalysisList(logFile,logFileType,analysisList):
	results = [] 
	for analysisType in analysisList:   
		mys = runAnalysis(logFile,logFileType,analysisType)
		results.append(StringIO(mys))
	return results

def changeMetricsTable(lastTime, previousTime, logFileType, storageConnection):
	import storage

	tableNameChange = lastTime + '_changeMetrics'
	if storage.tableExists(tableNameChange, storageConnection):
		return storage.readTable(tableNameChange, storageConnection)

	tableNameLog = 'gitLog_'+lastTime+'_'+previousTime
	scmLogPath = storage.readFile(tableNameLog, storageConnection, toTemporaryFile=True)

	results = runAnalysisList(scmLogPath,logFileType,entityAnalysisTypes)

	changeMetrics = pd.read_csv(results[0])
	for result in results[1:]:
		changeMetrics = changeMetrics.merge(pd.read_csv(result), on='entity')

	changeMetrics.drop('n-revs_y', axis=1, inplace=True)
	changeMetrics = changeMetrics.rename(columns = {'n-revs_x':'n-revs'})

	storage.writeTable(tableNameChange, storageConnection, changeMetrics)

	return changeMetrics

entityAnalysisTypes = [ 'age', 'authors', 'entity-churn', 'fragmentation', 'revisions', 'soc' ]

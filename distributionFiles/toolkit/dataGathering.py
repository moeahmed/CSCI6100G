import os
import scmData as scm
import storage
import pandas as pd
import pdb

def processTimeData(timeData, model, responseVariable, useScaler, categoryFunction):
	print "Response variable was %s" % (responseVariable)

	if hasattr(model, 'classes_') and categoryFunction is not None:
		response = categoryFunction(timeData[responseVariable]).astype(int)
	else:
		response = timeData[responseVariable]

	features = timeData.copy(deep=True)
	features.drop(responseVariable, axis=1, inplace=True)

	import dataUtilities as utilities
	features = utilities.replaceWithLabelEncoded(features, 'time')
	features = utilities.replaceWithOneHotEncoded(features, 'entity')

	if useScaler:
		features = utilities.scaleFeatures(features)

	return dict(features = features, response = response, names = features.columns)

def gatherTimeMetrics(studyDirectory, repositoryURL, sourceFilesDirectory, filesToInspect, language, branch='master', skipEvery=200, replaceMissing=True):
	import pandas as pd

	if not scm.gitlog.isGitRepo(sourceFilesDirectory):
		scm.gitlog.cloneGitRepo(studyDirectory,repositoryURL)

	databasePath = studyDirectory+'databases/'
	if not os.path.exists(databasePath):
	    os.makedirs(databasePath)
	storageConnection = storage.openDatabase(databasePath+'metrics.db')

	dates = scm.gitlog.makeCommitDateMapping(sourceFilesDirectory,filesToInspect,storageConnection,branch)

	timeDataSet = []
	previousTime = dates.iloc[0]
	for index, nextTime in dates[skipEvery::skipEvery].iterrows():
		nextTable = gatherData(studyDirectory,
								repositoryURL,
								sourceFilesDirectory,
								filesToInspect,
								nextTime['sha'],
								previousTime['sha'],
								language,
								storageConnection)
		previousTime = nextTime
		if not nextTable.empty:
			nextTable['time'] = nextTime['date']
			timeDataSet.append(nextTable)

	timeMetrics = pd.concat(timeDataSet)

	if not timeMetrics.empty and replaceMissing:
		for column in timeMetrics.columns:
			if 'entity' not in column and 'time' not in column:
				timeMetrics[column].fillna(timeMetrics[column].median(), inplace=True)

	timesSampled = len(timeDataSet)

	return dict(data = timeMetrics, times = timesSampled)

def gatherData(studyDirectory, repositoryURL, sourceFilesDirectory, filesToInspect, nextTime, previousTime, language=None, storageConnection=None):
	if storageConnection is not None:
		databasePath = studyDirectory+'databases/'
		if not os.path.exists(databasePath):
		    os.makedirs(databasePath)
		storageConnection = storage.openDatabase(databasePath+'metrics.db')

	scm.gitlog.makeGitLog(sourceFilesDirectory, filesToInspect, nextTime, previousTime, storageConnection)

	import changeMetrics as change
	changeMetrics = change.codemaat.changeMetricsTable(nextTime, previousTime, 'git', storageConnection)

	codeMetrics = None
	if language is not None:
		import staticMetrics as static
		codeMetrics = static.gatherStaticMetrics(language, nextTime, changeMetrics, sourceFilesDirectory, storageConnection)

	#changeMetrics['entity'] = changeMetrics['entity'].apply(lambda x: x.replace('/','_'))
	changeMetrics['netchurn'] = changeMetrics['added'] - changeMetrics['deleted']
	changeMetrics.drop('total-revs', axis=1, inplace=True)
	print("changeMetrics:",changeMetrics)
	print("codeMetrics:",codeMetrics)

	allData = pd.DataFrame()
    
	if language is not None and codeMetrics is not None:
        
		allData = changeMetrics.merge(codeMetrics, on='entity')
        
	#pdb.set_trace()        

	return allData

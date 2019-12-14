import subprocess
import pandas as pd
from StringIO import StringIO

def runAllAnalysisOnFile(fileToMeasure):
	results = []
	for analysisType in analysisTypes:
		results.append(pd.read_json(StringIO(runAnalysisOnFile(fileToMeasure,analysisType))))

	combined = pd.concat(results)
	combined = combined.transpose()

	combined = combined.reset_index()
	combined = combined.rename(columns = {'index':'entity'})

	return combined

def runAnalysisOnFile(fileToMeasure,analysisType):
	command = "radon %s %s -j" % (analysisType, fileToMeasure)
	return subprocess.check_output(command, shell=True)

def codeMetricsTable(nameLabel, dataFrame, sourceFilesDirectory, storageConnection):
    import scmData as scm
    import storage
    import dataUtilities

    scm.gitlog.switchToRevision(sourceFilesDirectory,nameLabel)

    metricsData = []
    for entityName in dataFrame['entity']:
        nextSample = runAllAnalysisOnFile(sourceFilesDirectory+entityName)
        if nextSample.shape[1] is 10:
            metricsData.append(nextSample)

    if metricsData:
        metricsData = pd.concat(metricsData)
        metricsData = dataUtilities.formatEntityNames(metricsData, sourceFilesDirectory)
        metricsData.drop('rank', axis=1, inplace=True)

    return metricsData

analysisTypes = ['mi', 'raw']
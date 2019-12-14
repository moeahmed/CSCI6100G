import os
import subprocess
import pandas as pd
import numpy as np
from StringIO import StringIO

pmdMetricsPath = os.path.dirname(os.path.abspath(__file__)) + "/../pmd-bin-6.20.0/bin/run.sh"
#pmdMetricsPath = os.getcwd() + "/../pmd-bin-6.20.0/bin/run.sh"


def runAnalysisOnFile(fileToMeasure):
    #command = pmdMetricsPath + 'qmcalc -a %s' % (fileToMeasure)
    # pmd -d src/main/java -f text -R rulesets/java/quickstart.xml -language java -version 8
    command = pmdMetricsPath + ' ' + 'pmd -d %s' % (fileToMeasure) + \
        ' -R rulesets/java/quickstart.xml -language java -version 8 -f csv > output.csv'
    try:
        output = pd.read_csv(StringIO(subprocess.check_output(
            command, shell=True)), delimiter='\t', names=featureHeader)
        return output
    except subprocess.CalledProcessError:
        output = pd.DataFrame(np.nan, index=[0], columns=featureHeader)
        output['entity'] = fileToMeasure
        return output


def dropUnusedMetrics(metricsTable):
    for name in metricsTable.columns:
        if name not in usedFeatureNames:
            metricsTable.drop(name, axis=1, inplace=True)

    return metricsTable


def codeMetricsTable(nameLabel, dataFrame, sourceFilesDirectory, storageConnection):
    import storage
    import scmData as scm
    import dataUtilities

    tableName = nameLabel + '_codeMetrics'
    if storage.tableExists(tableName, storageConnection):
        return storage.readTable(tableName, storageConnection)

    scm.gitlog.switchToRevision(sourceFilesDirectory, nameLabel)

    metricsData = []

    for entityName in dataFrame['entity']:
        analysis = runAnalysisOnFile(sourceFilesDirectory+entityName)
        print(analysis)
        metricsData.append(analysis)

    if not metricsData:
        return None

    metricsData = pd.concat(metricsData)

    metricsData = dropUnusedMetrics(metricsData)

    metricsData = dataUtilities.formatEntityNames(
        metricsData, sourceFilesDirectory)

    storage.writeTable(tableName, storageConnection, metricsData)

    return metricsData


usedFeatureNames = ['entity', 'priority', 'rule']

featureHeader = ['problem', 'package', 'entity', 'priority', 'line', 'desc', 'ruleSet', 'rule']

from __future__ import division # To make floating division work correctly
import pandas as pd
import os
import subprocess

isWhiteSpace = -1

def indentation(line, tabsize=4):
    line = line.expandtabs(tabsize)
    # Whitespace lines get -1, since lines of code may have identation 0
    return isWhiteSpace if line.isspace() else len(line) - len(line.lstrip())

def countLeadingSpaces(inputFile, tabsize=4):
	try:
	    with open(inputFile) as ifile:
	        indentLengths = [indentation(line, tabsize) for line in ifile]
	        return indentLengths
	except EnvironmentError:
	    return [0]

def spacesToTabs(indentCounts, tabsize=4):
    return [(entry / tabsize) for entry in indentCounts]

def indentCountStats(inputFile, tabsize=4):
	spaceCounts = countLeadingSpaces(inputFile, tabsize)
	df_spaces = pd.DataFrame(spaceCounts)

	indentCounts = spacesToTabs(spaceCounts, tabsize)
	df = pd.DataFrame(indentCounts)

	mean = df[0].mean()
	std = df[0].std()
	median = df[0].median()
	max = df[0].max()

	totalLines = len(df)
	indentLines = len(df_spaces[df_spaces[0] != isWhiteSpace])

	data = [indentLines, mean, std, median, max]

	frame = pd.DataFrame(data)
	frame = frame.transpose()
	frame.columns = ['indent_lines', 'indent_mean', 'indent_sd', 'indent_median', 'indent_max']

	return frame

def indentMetricsTable(nameLabel, dataFrame, sourceFilesDirectory, storageConnection, tabsize=4):
	import storage
	import scmData as scm
	import dataUtilities

	tableName = nameLabel + '_indentMetrics'
	if storage.tableExists(tableName, storageConnection):
		return storage.readTable(tableName, storageConnection)

	scm.gitlog.switchToRevision(sourceFilesDirectory,nameLabel)
	indentMetrics = pd.DataFrame()
	for entityName in dataFrame['entity']:
		nextFrame = indentCountStats(sourceFilesDirectory+entityName, tabsize)
		nextFrame['entity'] = sourceFilesDirectory+entityName
		indentMetrics = pd.concat([indentMetrics,nextFrame])

	if indentMetrics.empty:
		return None

	indentMetrics = dataUtilities.formatEntityNames(indentMetrics, sourceFilesDirectory)

	storage.writeTable(tableName, storageConnection, indentMetrics)
	return indentMetrics
import os
import subprocess
import pandas as pd
import numpy as np
from StringIO import StringIO

cqMetricsPath = os.path.dirname(os.path.abspath(__file__)) + "/../cqmetrics/"

def runAnalysisOnFile(fileToMeasure):
	command = cqMetricsPath + 'qmcalc -a %s' % (fileToMeasure)
	try:
	    output = pd.read_csv(StringIO(subprocess.check_output(command, shell=True)),delimiter = '\t', names=featureHeader)
	    return output
	except subprocess.CalledProcessError:
	    output = pd.DataFrame(np.nan, index=[0], columns=featureHeader)
	    output['entity'] = fileToMeasure
	    return output

def dropUnusedCMetrics(metricsTable):
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

	scm.gitlog.switchToRevision(sourceFilesDirectory,nameLabel)

	metricsData = []

	for entityName in dataFrame['entity']:
		analysis = runAnalysisOnFile(sourceFilesDirectory+entityName)
		metricsData.append(analysis)

	if not metricsData:
		return None

	metricsData = pd.concat(metricsData)

	metricsData = dropUnusedCMetrics(metricsData)

	metricsData = dataUtilities.formatEntityNames(metricsData, sourceFilesDirectory)

	storage.writeTable(tableName, storageConnection, metricsData)

	return metricsData

usedFeatureNames =  ['entity','nchar','nline','line_length_mean', 'line_length_median', 'line_length_max','line_length_sd', 'nfunction', 'nstatement','statement_nesting_min', 'statement_nesting_mean','statement_nesting_median', 'statement_nesting_max','statement_nesting_sd', 'ninternal', 'nconst', 'nenum', 'ngoto','ninline', 'nnoalias', 'nregister', 'nrestrict', 'nsigned','nstruct', 'nunion', 'nunsigned', 'nvoid', 'nvolatile','ntypedef', 'ncomment', 'ncomment_char', 'ncpp_directive','ncpp_include', 'ncpp_conditional', 'nfun_cpp_directive','nfun_cpp_conditional', 'nfunction2', 'halstead_min','halstead_mean', 'halstead_median', 'halstead_max', 'halstead_sd','nfunction3', 'cyclomatic_min', 'cyclomatic_mean','cyclomatic_median', 'cyclomatic_max', 'cyclomatic_sd','nidentifier', 'unique_nidentifier']

featureHeader = ['nchar','nline','line_length_min','line_length_mean','line_length_median','line_length_max','line_length_sd','nfunction','nstatement','statement_nesting_min','statement_nesting_mean','statement_nesting_median','statement_nesting_max','statement_nesting_sd','ninternal','nconst','nenum','ngoto','ninline','nnoalias','nregister','nrestrict','nsigned','nstruct','nunion','nunsigned','nvoid','nvolatile','ntypedef','ncomment','ncomment_char','nboilerplate_comment_char','ndox_comment','ndox_comment_char','nfun_comment','ncpp_directive','ncpp_include','ncpp_conditional','nfun_cpp_directive','nfun_cpp_conditional','style_inconsistency','nfunction2','halstead_min','halstead_mean','halstead_median','halstead_max','halstead_sd','nfunction3','cyclomatic_min','cyclomatic_mean','cyclomatic_median','cyclomatic_max','cyclomatic_sd','nidentifier','identifier_length_min','identifier_length_mean','identifier_length_median','identifier_length_max','identifier_length_sd','unique_nidentifier','unique_identifier_length_min','unique_identifier_length_mean','unique_identifier_length_median','unique_identifier_length_max','unique_identifier_length_sd','indentation_spacing_count','indentation_spacing_min','indentation_spacing_mean','indentation_spacing_median','indentation_spacing_max','indentation_spacing_sd','nno_space_after_binary_op','nno_space_after_closing_brace','nno_space_after_comma','nno_space_after_keyword','nno_space_after_opening_brace','nno_space_after_semicolon','nno_space_before_binary_op','nno_space_before_closing_brace','nno_space_before_keyword','nno_space_before_opening_brace','nspace_after_opening_square_bracket','nspace_after_struct_op','nspace_after_unary_op','nspace_at_end_of_line','nspace_before_closing_bracket','nspace_before_closing_square_bracket','nspace_before_comma','nspace_before_opening_square_bracket','nspace_before_semicolon','nspace_before_struct_op','nspace_after_binary_op','nspace_after_closing_brace','nspace_after_comma','nspace_after_keyword','nspace_after_opening_brace','nspace_after_semicolon','nno_space_after_struct_op','nspace_before_binary_op','nspace_before_closing_brace','nspace_before_keyword','nspace_before_opening_brace','nno_space_before_struct_op','nno_space_after_opening_square_bracket','nno_space_after_unary_op','nno_space_before_closing_bracket','nno_space_before_closing_square_bracket','nno_space_before_comma','nno_space_before_opening_square_bracket','nno_space_before_semicolon','entity']
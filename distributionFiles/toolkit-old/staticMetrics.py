import cqmetricsInterface as cqmetrics
import radonInterface as radon
import indentationInterface as indentation

def gatherStaticMetrics(language, time, changeMetrics, sourceFilesDirectory, storageConnection):
	languageSpecific = None
	languageAgnostic = None

	if 'c' in language:
		languageSpecific = cqmetrics.codeMetricsTable(time, changeMetrics, sourceFilesDirectory, storageConnection)
	elif 'python' in language:
		languageSpecific = radon.codeMetricsTable(time, changeMetrics, sourceFilesDirectory, storageConnection)

	if 'indent' in language:
		languageAgnostic = indentation.indentMetricsTable(time, changeMetrics, sourceFilesDirectory, storageConnection)

	if languageSpecific is not None and languageAgnostic is not None:
		staticMetrics = languageSpecific.merge(languageAgnostic, on='entity')
	elif languageSpecific is not None and languageAgnostic is None:
		staticMetrics = languageSpecific
	elif languageAgnostic is not None and languageSpecific is None:
		staticMetrics = languageAgnostic
	else:
		return None

	return staticMetrics
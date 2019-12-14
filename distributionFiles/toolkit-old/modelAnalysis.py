# Original idea from: http://francescopochetti.com/pythonic-cross-validation-time-series-pandas-scikit-learn/
def timeSeriesFolds(features, response, numberOfFolds, foldNumber):
	import numpy as np
	k = int(np.floor(float(features.shape[0]) / numberOfFolds))
	i = foldNumber
	split = float(i-1)/i

	X = features[:(k*i)]
	y = response[:(k*i)]
	index = int(np.floor(X.shape[0] * split))

	Xtr = X[:index]
	Ytr = y[:index]
	Xte = X[(index + 1):]
	Yte = y[(index + 1):]

	return dict(xtr = Xtr, ytr = Ytr, xte = Xte, yte = Yte)

def analyseModel(model, featureNames, featuresTest, responseTest, scoreOnly):
	import pandas as pd
	print "Model.score: %f" % model.score(featuresTest, responseTest)

	if scoreOnly:
		return

	if hasattr(model,'classes_') and model.classes_ is not None:
		from sklearn.metrics import accuracy_score
		print "accuracy_score: %f" % accuracy_score(responseTest, model.predict(featuresTest))

		from sklearn.metrics import classification_report
		print classification_report(responseTest, model.predict(featuresTest))

		try:
			from sklearn.metrics import roc_auc_score
			responsesScore = model.predict(featuresTest)
			print "roc_auc_score: %f" % roc_auc_score(responseTest,responsesScore)
		except ValueError:
		    print "roc_auc_score cannot be computed for this test set"

	if hasattr(model,'feature_importances_'):
		fi = pd.Series(model.feature_importances_)
		fn = pd.Series(featureNames)
		fin = pd.concat([fn, fi], axis=1)
		fin.columns=['name','importance']
		fin = fin[fin.importance != 0]
		print fin.sort_values(by='importance',ascending=False)

def timeSeriesCV(features, featureNames, response, numberOfFolds, model, scoreOnly):
	for foldNumber in range(2, numberOfFolds+1):
		cvSplitData = timeSeriesFolds(features, response, numberOfFolds, foldNumber)

		model.fit(cvSplitData['xtr'], cvSplitData['ytr'])
		analyseModel(model, featureNames, cvSplitData['xte'], cvSplitData['yte'], scoreOnly)

	return model

def timeSeriesModel(data, CVfolds, responseVariable, model, useScaler=False, scoreOnly=True, categoryFunction=lambda r: (r > r.mean())):
	if CVfolds < 2:
		return

	import dataGathering
	timeData = dataGathering.processTimeData(data, model, responseVariable, useScaler, categoryFunction)
	fittedModel = timeSeriesCV(timeData['features'], timeData['names'], timeData['response'], CVfolds, model, scoreOnly)
	return dict(fittedModel = fittedModel, data = timeData)
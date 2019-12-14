def formatEntityNames(dataframe, sourceFilesDirectory):
	nameTrimLength = len(sourceFilesDirectory)
	dataframe['entity'] = dataframe['entity'].apply(lambda x: str(x)[nameTrimLength:])
	dataframe['entity'] = dataframe['entity'].apply(lambda x: x.replace('/','_'))
	return dataframe

def scaleFeatures(features):
	from sklearn import preprocessing as pp
	scaler = pp.StandardScaler()
	scaler.fit(features)
	scaledFeatures = scaler.transform(features)
	return scaledFeatures

def replaceWithLabelEncoded(features, featureName):
	from sklearn import preprocessing as pp
	encoder = pp.LabelEncoder()
	encoder.fit(features[featureName])
	labelledTimes = encoder.transform(features[featureName])
	features.drop([featureName], axis=1, inplace=True)
	features[featureName] = labelledTimes
	return features

def replaceWithOneHotEncoded(features, featureName):
	import pandas as pd
	oneHotNames = pd.get_dummies(features[featureName], featureName)

	features = pd.concat([features, oneHotNames], axis=1)
	features.drop(featureName, axis=1, inplace=True)

	features.columns = [name.encode('utf-8') for name in features.columns]
	return features

def addBinnedResponseCategory(data, responseVariable, binLabels):
	import pandas as pd
	binnedData, bins = pd.cut(data[responseVariable], len(binLabels), labels=False, retbins=True)

	from sklearn import preprocessing as pp
	lb = pp.LabelBinarizer()
	lb.fit(binnedData)

	binnedCategories = pd.DataFrame(lb.transform(binnedData))
	binnedCategories.index = data.index
	binnedCategories.columns = binLabels
	binnedDataSet = pd.concat([data, binnedCategories], axis=1)
	binnedDataSet.drop(responseVariable, axis=1, inplace=True)

	return binnedDataSet
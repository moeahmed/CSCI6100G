def updateModel(studyDirectory, features, featureNames, responses, folds, fittedModel, modelInstance, scoreOnly=True, visualize=False):
    selectedFeatures = selectImportantFeatures(fittedModel, features, featureNames)

    import modelAnalysis as analysis
    updatedModel = analysis.timeSeriesCV(selectedFeatures['features'], selectedFeatures['names'], responses, folds, modelInstance, scoreOnly=scoreOnly)

    if visualize is True:
        import presentation
        presentation.visualizeModelRefinement(studyDirectory, fittedModel, updatedModel, featureNames, selectedFeatures)

    return dict(updated = updatedModel, selected = selectedFeatures)

def makeAndUpdateModel(studyDirectory, data, folds, responseVariable, model, modelRefined=None, categoryFunction=None, scoreOnly=True, visualize=False):
    import modelAnalysis as analysis
    timeModel = analysis.timeSeriesModel(data, folds, responseVariable, model, categoryFunction, scoreOnly)
    return updateModel(studyDirectory, timeModel['data']['features'], timeModel['data']['names'],
                        timeModel['data']['response'], folds, timeModel['fittedModel'],
                        modelRefined if modelRefined is not None else model, scoreOnly, visualize)

def selectImportantFeatures(fittedModel, features, featureNames):
    from sklearn.feature_selection import SelectFromModel
    reducedFeatures = SelectFromModel(fittedModel, prefit=True)
    featuresSelected = reducedFeatures.transform(features)

    featureNamesSelected = []
    for featureIndex in reducedFeatures.get_support(indices=True):
        featureNamesSelected.append(featureNames[featureIndex])

    return dict(features = featuresSelected, names = featureNamesSelected)

import matplotlib.pyplot as plt

def initializeFigurePlotting(width=4,height=3):
    plt.rcParams["figure.figsize"] = [width, height]

def visualizeModelRefinement(studyDirectory, fittedModel, updatedModel, featureNames, selectedFeatures):
    import os
    import presentation

    visualizationDirectory = studyDirectory + '/models/'
    if not os.path.exists(visualizationDirectory):
        os.makedirs(visualizationDirectory)

    if not hasattr(fittedModel, 'estimators_'):
        filename = visualizationDirectory + 'modelOld.svg'
        presentation.visualizeTree(fittedModel, featureNames, filename)
        presentation.show_svg(filename)
    elif hasattr(fittedModel, 'estimators_'):
        for estTree in updatedModel.estimators_:
            filename = visualizationDirectory + 'modelOld'+str(estTree.random_state)+'.svg'
            presentation.visualizeTree(estTree, featureNames, filename)
            presentation.show_svg(filename)
    if not hasattr(updatedModel, 'estimators_'):
        filename = visualizationDirectory + 'model.svg'
        presentation.visualizeTree(updatedModel, selectedFeatures['names'], filename)
        presentation.show_svg(filename)
    elif hasattr(updatedModel, 'estimators_'):
        for estTree in updatedModel.estimators_:
            filename = visualizationDirectory + 'model'+str(estTree.random_state)+'.svg'
            presentation.visualizeTree(estTree, selectedFeatures['names'], filename)
            presentation.show_svg(filename)

def visualizeTree(model, featureNames, fileName):
    from sklearn import tree
    from StringIO import StringIO

    dot_data = StringIO()
    tree.export_graphviz(decision_tree=model, out_file=dot_data,
                        feature_names=featureNames,
                        filled=True, rounded=True,
                        proportion=True)

    import pydot
    (graph,) = pydot.graph_from_dot_data(dot_data.getvalue())
    graph.write_svg(fileName)

def is_interactive():
    import __main__ as main
    return not hasattr(main, '__file__')

def show_svg(filename):
	if is_interactive():
	    from IPython.display import SVG, display
	    display(SVG(filename))

def seaBornTest(dataSet):
	import seaborn as sb
	sb.set_context("notebook", font_scale=2.0)
	g = sb.PairGrid(dataSet.ix[:,0:9], size=5)
	g.map_diag(plt.hist)
	g.map_offdiag(plt.scatter);
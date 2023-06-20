# -*- coding: utf-8 -*-

# 2022-2023 Programação 2 (LTI)
# Grupo 18
# 60289 Gonçalo Gouveia
# 60232 Duarte Correia

from example import Example

class Cluster(object):
    """
    Cluster of examples
    """

    def __init__(self, examples):

        self._examples = examples
        self._centroid = self.computeCentroid()
    
    def update(self, examples):
        """
        Update the cluster with a given collection of examples

        Requires:
        examples a list of objects of the type of members in self._examples
        Ensures:
        examples = getExamples();
        returns how much the centroid has changed
        """
        
        oldCentroid = self._centroid
        self._examples = examples
        if(len(examples) > 0):
            self._centroid = self.computeCentroid()
            return oldCentroid.distance(self._centroid)
        else:
            return 0.0

    def computeCentroid(self):

        dim = self._examples[0].dimensionality()
        totVals = [0]*dim
        for e in self._examples:
            for i in range(dim):
                totVals[i] = totVals[i] + e.getFeatures()[i]
        totValsAveraged = []
        for i in range(dim):
            totValsAveraged.append(totVals[i]/float(len(self._examples)))
        centroid = Example("centroid", totValsAveraged)
        return centroid
    
    def getExamples(self):

        return self._examples
    
    def setCentroid(self, centroid):

        self._centroid = centroid
    
    def getCentroid(self):

        return self._centroid
    
    def members(self):
        """
        Generator method
        """
        for e in self._examples:
            yield e

    def __str__(self):
        
        """
        Returns a string representation of the cluster

        Requires: The cluster has a valid centroid object with the getFeatures() method and the examples in the cluster have a valid getName() method.
        Ensures: The returned string includes the centroid features and the names of the examples contained in the cluster.
        """

        names = []
        for e in self._examples:
            names.append(e.getName())
        names.sort()
        result = "Cluster with centroid " + \
            str(self.getCentroid().getFeatures()) + " contains:\n"
        for e in names:
            result = result + e + ", "
        return result[:-2]
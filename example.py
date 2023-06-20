# -*- coding: utf-8 -*-

# 2022-2023 Programação 2 (LTI)
# Grupo 18
# 60289 Gonçalo Gouveia
# 60232 Duarte Correia

from constants import *

def minkowskiDistance(v1, v2, p):
    """
    Minkowski distance
    
    Requires: v1 and v2 are lists of numbers with the same lenght
    Ensures: Minkowski distance of order p between v1 and v2
    """
    dist = 0.0
    for i in range(len(v1)):
        dist += abs(v1[i] - v2[i])**p
    return dist**(1.0/p)

class Example():
    """
    Example for clustering
    """

    def __init__(self, name, features, label = None):
        """
        """

        self._name = name
        self._features = features
        self._label = label
    
    def dimensionality(self):

        return len(self._features)
    
    def setName(self, name):

        self._name = name
    
    def getName(self):

        return self._name

    def setFeatures(self, features):

        self._features = features

    def getFeatures(self):

        return self._features
    
    def distance(self, other):

        return minkowskiDistance(self._features, other.getFeatures(), 2)

    def __str__(self):
        """
        String representation

        Ensures:
        string representation in the form "name:features:label"
        """
        return self._name + ':' + str(self._features) + ':' + str(self._label)
    
    def __eq__(self, other):
        """
        Compares two candidates

        Requires: 
        other is a candidate to compare with the first one
        Ensures:
        If the features are the same or not
        """

        return self.getFeatures() == other.getFeatures()

    def __lt__(self):
        pass

def createExamples(candidates, features):
    """
    Function that creates a list of examples for the clustering

    Requires: candidates is a list of candidates, features is a 
    list of each candidate feature
    Ensures: A list containing a example from the class Example
    """
    examples = []
    if(len(features) ==0):
        return []
    for x in range(len(candidates)):
        #create variable candidate and assign the
        #name of a candidate each time that the for is
        #activated
        candidate = candidates[x][NUM_CANDIDATES_NAME]
        #create a new example with the candidate´s name
        #and his/ her feature
        candidate = Example(candidate, features[x])
        #append the candidate that is a new example to 
        #the list examples so it can be used in the kmeans
        #function in the main file, clusteringRealities.py
        examples.append(candidate)
    
    return examples
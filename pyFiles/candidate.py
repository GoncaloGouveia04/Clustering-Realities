# -*- coding: utf-8 -*-

# 2022-2023 Programação 2 (LTI)
# 60289 Gonçalo Gouveia

from constants import *


class Candidate:

    def __init__(self, name, features):
        """
        Initializes the class

        """
        self._candidatesName = name
        self._features = features

    def setCandidatesName(self, candidatesList):
        """
        Set the candidates name

        Requires: Recieve a candidates list
        Ensures: self._candidatesName = candidatesList
        """

        self._candidatesName = candidatesList

    def getCandidatesName(self):
        """
        Returns the name of a candidate at the specified index.

        Requires:
        Must be a valid index within the range of candidate names.

        Ensures:
        Returns the name of the candidate at the specified index.
        """
        return self._candidatesName[NUM_CANDIDATES_NAME]

    def setFeatures(self, features):
        """
        Saves a candidate feature with every title

        Requires: features a list of the candidate
        Requires: features a list of strings with 
                  the candidate´s title
        """
        self._features = features

    def getFeatures(self):
        """

        Ensures: returns a list of every title
        """

        return self._features[NUM_CANDIDATES_FATHERS_TITLE:]

    def __str__(self):
        """
        Ensures: returns the candidate´s name and feature´s
                 as a string
        """       
        return self.getCandidatesName()+ "; " + "; ".join(self.getFeatures()) 

    def __eq__(self):
        """


        """
        pass

    def __lt__(self):
        """


        """
        pass


def convertCandidatesList(titlesDic, candidatesList):
    """
    Function that matches a number in the titles dictionary to the
    candidates list.

    Requires: titlesDic is a dictionary of the tiles and 
              the names to each degree
              candidatesList is a list of the candidates
    Ensures: A features list where each number in the 
             list represents de titles. 
             This list contains each feature of each candidate.
    """

    features = []
    # run every candidate in the candidatesList
    for candidate in candidatesList:
        if len(candidate) > 7:
            raise ValueError("Error in candidate " + candidate[NUM_CANDIDATES_NAME] + \
                             "\nCandidate has a number of titles higher than 7")
        if candidate == ["void"]:
            return []
        # create a list with the features of each
        # candidate, where the list is numbers only
        newFeature = []
        # run 6 times beacuse the lenght of the features
        # of a candidate is only 6
        for i in range(6):
            # assign the title of each candidate to
            # a variable
            title = candidate[i+1]
            for key in titlesDic:
                # compare if the title of the candidates
                # is in the titles dictionary
                if title in titlesDic[key]:
                    # assign the title´s degree to
                    # the newFeature list
                    newFeature.append(int(key))
        # when the second 'for' ends assign the new
        # feature the the features list
        # representing each of the candidates features
        features.append(newFeature)

    return features


def getExemplarsIndex(candidatesList):
    """
    Function that takes the Exemplares into a list,
    the Exemplars

    Requires:

    Ensures: 
    """

    element = "#Exemplars:"
    for i, item in enumerate(candidatesList):
        if element in item:
            index = i

    return index
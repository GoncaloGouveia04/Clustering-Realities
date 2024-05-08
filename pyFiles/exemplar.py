# -*- coding: utf-8 -*-

# 2022-2023 Programação 2 (LTI)
# 60289 Gonçalo Gouveia

from constants import *

class Exemplar:

    def __init__(self, name, features):
        """
        Initializes the class

        """
        self._exemplarName = name
        self._features = features

    def getExemplarName(self):

        return self._exemplarName
    
    def setExemplarName(self, name):

        self._exemplarName = name
    
    def getExemplarFeatures(self):

        return self._features
    
    def setExemplarFeatures(self, features):

        self._features = features

    def __str__(self):
        """
        Ensures: returns the candidate´s name and feature´s
                    as a string
        """       
        return self.getExemplarName+ "; " + "; ".join(self.getExemplarFeatures())
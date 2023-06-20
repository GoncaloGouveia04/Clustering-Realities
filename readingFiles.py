# -*- coding: utf-8 -*-

# 2022-2023 Programação 2 (LTI)
# Grupo 18
# 60289 Gonçalo Gouveia
# 60232 Duarte Correia

import constants

class readingFiles:

    def __init__(self):
        self._candidatesFile = ""
        self._titlesFile = ""
        self._titlesDic = {}

    
    def setCandidatesFile(self, fileName):

        self._candidatesFile = fileName
    
    def setTitlesFile(self, fileName):

        self._titlesFile = fileName

    def getCandidatesFile(self):

        inFile = open(self._candidatesFile, "r")
        self._candidatesList = []

        for line in inFile:
            self._candidatesData = line.rstrip().split("; ")
            self._candidatesList.append(self._candidatesData)
        

        return self._candidatesList[constants.NUM_CANDIDATES_LINE:]
    
    def getTitlesFile(self):

        inFile = open(self._titlesFile, "r")
        self._titlesList = []

        for line in inFile:
            self._titlesData = line.rstrip().split("; ")
            self._titlesList.append(self._titlesData)
        
        return self._titlesList[constants.NUM_TITLES_LINE:]
    
    def turnTitlesListIntoDictionary(self, list):

        for line in list:
            self._titlesDic[line[constants.NUM_TITLES_DEGREE]] \
                = line[constants.NUM_TITLES_NAME_MASCULINE], \
                    line[constants.NUM_TITLES_NAME_FEMININE]
            
        return self._titlesDic 
    
    def __str__(self):

        return "Candidates File: "+ self._candidatesFile + \
            "\nTitles File: " + self._titlesFile
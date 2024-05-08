# -*- coding: utf-8 -*-

# 2022-2023 Programação 2 (LTI)
# Grupo 18
# 60289 Gonçalo Gouveia
# 60232 Duarte Correia

import random
import sys
from pyFiles.readingFiles import readingFiles
from pyFiles.constants import *
from pyFiles.cluster import Cluster
from pyFiles.example import *
from pyFiles.candidate import *
from pyFiles.exemplar import *

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


def kmeans(examples, k, exemplars, verbose):
    """
    K-means clustering

    Requires: examples is a list of candidates of a same type;
              k is a positive int, number of clusters;
              exemplars is a list of exemplars of a same type;
              verbose Boolean, printing details on/off
    Ensure: list containing k clusters if no exemplars;
            if the exemplars list is not empty, return the same number of clusters
            as the lenght of the exemplars list
            if verbose is True, result of each interation of k-means is printed
    """

    #check if the examplers list is empty
    #meaning that in the candidates text file
    #that was used as as input, below the
    #Exemplares: there is no inicial centroid
    #being introduced, meaning that the only
    #value in the there is 'void'
    if exemplars == []:
        # Get k randomly chosen initial centroids,
        # create cluster for each
        initialCentroids = random.sample(examples, k)

        clusters = []
        for e in initialCentroids:
            clusters.append(Cluster([e]))

        # Iterate until centroids do not change
        converged = False
        numInterations = 0
        while not converged:

            numInterations += 1
            # Create a list containing k distinct
            # empty lists
            newClusters = []
            for i in range(k):
                newClusters.append([])

            # Associate each example with closest centroid
            for e in examples:
                # Find the closes to e
                smallestDistance = e.distance(clusters[0].getCentroid())
                index = 0
                for i in range(1, k):
                    distance = e.distance(clusters[i].getCentroid())
                    if distance < smallestDistance:
                        smallestDistance = distance
                        index = i
                # Add e to the list of examples for the
                # appropriate custer
                newClusters[index].append(e)

            # Avoid having empty clusters
            for c in newClusters:
                if len(c) == 0:
                    raise ValueError("Empty Cluster")

            # Update each cluster
            # check if a centroid has changed
            converged = True
            for i in range(len(clusters)):
                if clusters[i].update(newClusters[i]) > 0.0:
                    converged = False

            # Trace intermediate levels of clustering
            # if verbose on
            if verbose:
                print("Interaction #" + str(numInterations))
                for c in clusters:
                    print(c)
                print("")  # add blank line

        # with this 'for' we replace the centroids that were assigned
        # before and update it with the nearest candidate that has
        # a feature that is as near as the centroid´s feature
        for c in clusters:
            currentCentroid = c.getExamples()[0]
            smallestDistance = c.getExamples()[0].distance(c.getCentroid())
            for example in c.getExamples():
                distance = example.distance(c.getCentroid())
                if distance <= smallestDistance:
                    smallestDistance = distance
                    currentCentroid = example

            c.getCentroid().setFeatures(currentCentroid.getFeatures())
            # updates the name of the current centroid beacause
            # it was automatically assigned 'centroid' and
            # we dont want that but instead the candidate´s name
            c.getCentroid().setName(currentCentroid.getName())
    else:
        clusters = []
        #go thro the exemplars list, assigning 
        #every exemplar as a centroid
        for e in exemplars:
            clusters.append(Cluster([e]))
        
        converged = False
        numInterations = 0
        while not converged:

            numInterations +=1
            newClusters = []
            k = len(clusters)
            for i in range(k):
                newClusters.append([])
            
            for e in examples:
                smallestDistance = e.distance(clusters[0].getCentroid())
                index = 0
                for i in range(1, k):
                    distance = e.distance(clusters[i].getCentroid())
                    if distance < smallestDistance:
                        smallestDistance = distance
                        index = i
                
                newClusters[index].append(e)
            
            for c in newClusters:
                if len(c) == 0:
                    raise ValueError("Empty Cluster")
            
            converged = True
            for i in range(len(clusters)):
                if clusters[i].update(newClusters[i]) > 0.0:
                    converged = False

            if verbose:
                print("Interaction #" + str(numInterations))
                for c in clusters:
                    print(c)
                print("")  # add blank line
            
        #since the centroids are already provided in the 
        #input file, tupdate the features and name
        #of the centroid according to the exemplare´s
        #name and features
        #the x variable is used to go thro the exemplars
        #list, to get every exemplar in the list
        x = 0
        for c in clusters:
            c.getCentroid().setFeatures(exemplars[x].getFeatures())
            c.getCentroid().setName(exemplars[x].getName())
            x +=1
        
    return clusters


def runProgram(k, titlesFileName, candidatesFileName):
    """
    Function that returns a txt file with a candidate that becomes
    the centroid of one or more candidates, where those candidates
    become the clusters of the candidate

    Requires: k int is the number of centroids that is going to be formed
              titlesFileName is a fixed text file with a maculine and
               feminine title that is associated to a degree
              candidatesFileName is a text file with the name of each 
               candidate and 6 titles, where each candidate contain the
               fathers title, mothers title, grandfathers and grandmothers
               title of the fathers side, and grandfathers and grandmothers
               title of the mothers side
    Ensures: A text file with the name candidates.txt where the exemplar
             is the centroid and the cluster is the group of each centroid
    """

    r = readingFiles()
    r.setCandidatesFile(candidatesFileName)
    r.setTitlesFile(titlesFileName)
    # create a list with the candidates from the text file candidatesFileName
    candidate = r.getCandidatesFile()
    #assign the index where the exemplars are
    index = getExemplarsIndex(candidate)
    #make an exemplars list containing the centroids
    exemplars = candidate[index+1:]
    #update the candidates list removing the exemplars part
    candidates = candidate[:index]
    #create a list of objects with the candidates
    candidatesObjects = []
    for candidate in candidates:
        candidatesObjects.append(Candidate(candidate, candidate))
    #create a list of objects with the candidates
    exemplaresObjects = []
    for exemplar in exemplars:
        exemplaresObjects.append(Exemplar(exemplar, exemplar))
    #check if k is higher than the candidates lenght
    #if is higher, raise an exception because
    #the number of clusters to be formed cannot be higher than
    #the number of candidates
    if k > len(candidates):
        raise ValueError("k has to be equal or less than the number of candidates")
    # create a dictionary with the degree of each masculine and feminine
    # title so it can be compared with the candidates list
    titlesDic = r.turnTitlesListIntoDictionary(r.getTitlesFile())
    # using the titles dictionary and the candidates list, create
    # a new list, features, where each of the candidates title
    # is replace by the degree from the titles dictionary
    features = convertCandidatesList(titlesDic, candidates)
    #make the exemplars feature, if the exemplars list has a ['void']
    #then the output is gonna be an empty list. If not empty, then
    #create the exemplar´s features like the candidate´s
    featuresExemplares = convertCandidatesList(titlesDic, exemplars)
    # convert each candidate and feature into a list with
    # examples from the class Example, to be used in the
    # kmeans function
    examples = createExamples(candidates, features)
    #if the exemplars list is empty, then return an empty examples list
    #if not, return a list of examples containing the exemplars
    examplesExemplars = createExamples(exemplars, featuresExemplares)
    # assign the kmeans result into the variable clusters
    clusters = kmeans(examples, k, examplesExemplars, False)
    # the clustersList variable is to save the clusters of
    # a specific centroid so we can write it into the candidates
    # text file.
    clustersList = []
    for c in clusters:
        # to do so we need to split the str result, of the
        # Cluster class, with a '\n' so the program knows
        # the clusters are separed from the rest with a '\n'
        c = c.__str__().split("\n")
        clustersList.append(c[1]) #append the clusters to the 
                                  #clusterList

    #split the clusters into a list of lists
    clustersList = [x.split(", ") for x in clustersList]
    #check if the centroid exists in the clustersList
    #if so delete the clust in the clustersList
    for centroid in clusters:
        for cluster in clustersList:
            if centroid.getCentroid().getName() in cluster:
                index = cluster.index(centroid.getCentroid().getName())
                cluster.pop(index)
    #dictionary used to assign every candidate to their feature
    #the feature is a list of strings
    clusterDic = {}
    for candidate in candidatesObjects:
        clusterDic[candidate.getCandidatesName()] = candidate.getFeatures()
    #dictionary used to assign every exemplar to their feature 
    #the feature is a list of strings
    exemplarDic = {}
    for exemplar in exemplaresObjects:
        exemplarDic[exemplar.getCandidatesName()] = exemplar.getFeatures()
    candidatesFile = open("candidates.txt", "w")
    interaction = 0
    for cluster, c1 in zip(clusters, clustersList):
        candidatesFile.write("#exemplar " + str(interaction+1) + ":\n")
        #if the exemplars name is 'void', dont write void but instead
        #the centroid´s name with his or hers features. Meaning that the
        #centroid is a random candidate
        if exemplaresObjects[0].getCandidatesName() == "void":
            candidatesFile.write(cluster.getCentroid().getName() + "; " \
                                     + "; ".join(clusterDic[cluster.getCentroid()
                                                            .getName()]) + "\n")
        #if the exemplar´s name is not void, write his or her name and
        #feature, since the centroid is a candidate that was already 
        #assigned in the text file
        else:
            candidatesFile.write(cluster.getCentroid().getName() + "; " \
                                 + "; ".join(exemplarDic[cluster.getCentroid()\
                                                         .getName()]) + "\n")
        candidatesFile.write("#cluster " + str(interaction+1) + ":\n")
        #write the clusters name and features
        #that belong to the specific centroid
        for clusterName in c1:
            candidatesFile.write(clusterName + "; " + "; ".join(clusterDic[clusterName]) + "\n")
        interaction += 1

k = int(sys.argv[1])
titlesFileName = str(sys.argv[2])
inFile = str(sys.argv[3])

# function that is used to make the whole program work
# uses arguments from the terminal, k as int,
# titlesFileName as a text file name with the titles
# being a fixed file and inFile that is a text file
# with candidates so it can generate a new text file
# in return with centroids and clusters assign to each one
runProgram(k, titlesFileName, inFile)
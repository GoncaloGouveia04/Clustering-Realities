# main.py
# 2022-2023 Programação 2 (LTI)
# Grupo 18
# 60289 Gonçalo Gouveia
# 60232 Duarte Correia

import sys
import random

from cluster_module.candidate import *
from cluster_module.cluster import *
from cluster_module.constants import *
from cluster_module.example import *
from cluster_module.exemplar import *
from cluster_module.reading_files import *


def kmeans(examples: list, k: int, exemplars: list, verbose: bool) -> list:
    """
    K-means clustering

    Args:
        examples: list of Example objects
        k: number of clusters
        exemplars: list of Example objects used as centroids (can be empty)
        verbose: if True, prints iteration details

    Returns:
        List of Cluster objects
    """

    if not exemplars:
        # Randomly select initial centroids
        initial_centroids = random.sample(examples, k)
        clusters = [Cluster([e]) for e in initial_centroids]
    else:
        clusters = [Cluster([e]) for e in exemplars]
        k = len(clusters)

    converged = False
    iteration = 0

    while not converged:
        iteration += 1
        # Create empty lists for new cluster members
        new_cluster_members = [[] for _ in range(k)]

        # Assign each example to closest centroid
        for e in examples:
            distances = [e.distance(c.get_centroid()) for c in clusters]
            min_index = distances.index(min(distances))
            new_cluster_members[min_index].append(e)

        # Avoid empty clusters
        for i, cluster_members in enumerate(new_cluster_members):
            if not cluster_members:
                raise ValueError(f"Empty cluster detected at index {i}")

        # Update clusters and check convergence
        converged = True
        for i, cluster in enumerate(clusters):
            if cluster.update(new_cluster_members[i]) > 0:
                converged = False

        if verbose:
            print(f"Iteration #{iteration}")
            for cluster in clusters:
                print(cluster)
            print()

    # Align centroids with nearest example
    for i, cluster in enumerate(clusters):
        centroid = cluster.get_centroid()
        if exemplars:
            centroid.set_features(exemplars[i].get_features())
            centroid.set_name(exemplars[i].get_name())
        else:
            closest_example = min(
                cluster.get_examples(),
                key=lambda e: e.distance(centroid)
            )
            centroid.set_features(closest_example.get_features())
            centroid.set_name(closest_example.get_name())

    return clusters


def run_program(k: int, titles_file: str, candidates_file: str):
    """
    Main program function that generates clusters and writes results.

    Args:
        k: number of clusters
        titles_file: path to titles file
        candidates_file: path to candidates file
    """

    reader = ReadingFiles()
    reader.set_candidates_file(candidates_file)
    reader.set_titles_file(titles_file)

    raw_candidates = reader.get_candidates_file()
    exemplars_index = get_exemplars_index(raw_candidates)

    raw_exemplars = raw_candidates[exemplars_index + 1:]
    raw_candidates = raw_candidates[:exemplars_index]

    # Create Candidate and Exemplar objects
    candidate_objs = [Candidate(c, c) for c in raw_candidates]
    exemplar_objs = [Exemplar(e[0], e[1:]) for e in raw_exemplars]

    # Check k validity
    if k > len(candidate_objs):
        raise ValueError("k cannot exceed the number of candidates")

    # Build titles dictionary
    titles_dict = reader.turn_titles_list_into_dict(reader.get_titles_file())

    # Convert candidates and exemplars to feature lists
    candidate_features = convert_candidates_list(titles_dict, raw_candidates)
    exemplar_features = convert_candidates_list(titles_dict, raw_exemplars)

    # Create Example objects
    examples = create_examples(raw_candidates, candidate_features)
    exemplar_examples = create_examples(raw_exemplars, exemplar_features)

    # Run k-means clustering
    clusters = kmeans(examples, k, exemplar_examples, verbose=False)

    # Prepare dictionaries for writing output
    candidate_dict = {c.get_name(): c.get_features()
                      for c in candidate_objs}

    exemplar_dict = {e.get_name(): e.get_features()
                     for e in exemplar_objs
                     if e.get_name() != ["void"]}

    # Write results to file
    with open("output/candidates.txt", "w", encoding="utf-8") as f:
        for i, cluster in enumerate(clusters):
            f.write(f"#exemplar {i + 1}:\n")
            centroid = cluster.get_centroid()
            centroid_name = centroid.get_name()
            if exemplar_objs and exemplar_objs[0].get_name() != "void":
                f.write(
                    f"{centroid_name}; {'; '.join(exemplar_dict[centroid_name])}\n")
            else:
                f.write(
                    f"{centroid_name}; {'; '.join(candidate_dict[centroid_name])}\n")

            f.write(f"#cluster {i + 1}:\n")
            cluster_members = [
                e.get_name() for e in cluster.get_examples() if e.get_name() != centroid_name]
            for member_name in cluster_members:
                f.write(
                    f"{member_name}; {'; '.join(candidate_dict[member_name])}\n")


if __name__ == "__main__":
    k = int(sys.argv[1])
    titles_file = sys.argv[2]
    candidates_file = sys.argv[3]

    run_program(k, titles_file, candidates_file)

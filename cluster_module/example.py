# example.py

from .constants import *

def minkowski_distance(v1: list, v2: list, p: int) -> float:
    return sum(abs(a - b) ** p for a, b in zip(v1, v2)) ** (1 / p)


class Example:
    """Example for clustering."""

    def __init__(self, name: str, features: list, label=None):
        self.name = name
        self.features = features
        self.label = label


    def dimensionality(self) -> int:
        return len(self.features)

    def distance(self, other) -> float:
        return minkowski_distance(self.features, other.features, 2)
    
    def set_features(self, features):
        self.features = features
        
    def get_features(self):
        return self.features
        
    def set_name(self, name):
        self.name = name
    
    def get_name(self):
        return self.name

    def __str__(self):
        return f"{self.name}:{self.features}:{self.label}"

    def __eq__(self, other):
        return self.features == other.features


def create_examples(candidates: list, features: list) -> list:
    if not features:
        print('No feature was passed')
        return []

    return [
        Example(c[NUM_CANDIDATES_NAME], feat)
        for c, feat in zip(candidates, features)
    ]

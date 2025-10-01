# cluster.py

from .example import *

class Cluster:
    """Cluster of examples."""

    def __init__(self, examples: list):
        self.examples = examples
        self.centroid = self.compute_centroid()

    def compute_centroid(self) -> Example:
        dim = self.examples[0].dimensionality()
        avg_features = [
            sum(e.features[i] for e in self.examples) / len(self.examples)
            for i in range(dim)
        ]
        return Example("centroid", avg_features)

    def update(self, examples: list) -> float:
        old_centroid = self.centroid
        self.examples = examples
        if examples:
            self.centroid = self.compute_centroid()
            return old_centroid.distance(self.centroid)
        return 0.0

    def get_examples(self) -> list:
        return self.examples

    def get_centroid(self) -> Example:
        return self.centroid

    def __repr__(self):
        names = sorted(e.name for e in self.examples)
        return f"Cluster with centroid {self.centroid.features} contains:\n" + ", ".join(names)

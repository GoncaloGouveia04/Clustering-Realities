# candidate.py

from .constants import *
from .example import Example

class Candidate:
    """Represents a candidate with a name and a list of features."""

    def __init__(self, name: list, features: list):
        self._name_list = name
        self._features = features

    def set_name(self, name_list: list):
        self._name_list = name_list

    def get_name(self) -> str:
        return self._name_list[NUM_CANDIDATES_NAME]

    def set_features(self, features: list):
        self._features = features

    def get_features(self) -> list:
        return self._features[NUM_CANDIDATES_FATHERS_TITLE:]

    def __str__(self):
        return f"{self.get_name()}; {'; '.join(self.get_features())}"


def convert_candidates_list(titles_dict: dict, candidates_list: list) -> list:
    """Convert candidate titles to feature numbers based on titles_dict."""

    features = []

    for candidate in candidates_list:
        if len(candidate) > 7:
            raise ValueError(f"Candidate {candidate[NUM_CANDIDATES_NAME]} has too many titles.")
        if candidate == ["void"]:
            return []

        candidate_features = [
            int(key)
            for i in range(6)
            for key, vals in titles_dict.items()
            if candidate[i + 1] in vals
        ]
        features.append(candidate_features)

    return features


def get_exemplars_index(candidates_list: list) -> int:
    """Return the index of '#Exemplars:' in candidates_list or raise ValueError if not found."""

    for i, item in enumerate(candidates_list):
        if "#Exemplars:" in item:
            return i

    raise ValueError("'#Exemplars:' not found in candidates list.")

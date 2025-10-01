# exemplar.py

class Exemplar:
    """Represents an exemplar (centroid) with a name and features."""

    def __init__(self, name: str, features: list):
        self.name = name
        self.features = features

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str):
        self.name = name

    def get_features(self) -> list:
        return self.features

    def set_features(self, features: list):
        self.features = features

    def __repr__(self) -> str:
        return f"{self.get_name()}; {'; '.join(self.get_features())}"

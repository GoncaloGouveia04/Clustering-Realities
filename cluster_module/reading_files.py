# reading_files.py

from .constants import *

class ReadingFiles:
    """Handles reading candidates and titles from files."""

    def __init__(self):
        self.candidates_file = ""
        self.titles_file = ""

    def set_candidates_file(self, file_name: str):
        self.candidates_file = file_name

    def set_titles_file(self, file_name: str):
        self.titles_file = file_name

    def get_candidates_file(self) -> list:
        with open(self.candidates_file, "r", encoding="utf-8") as f:
            lines = [line.strip().split("; ") for line in f]
        return lines[NUM_CANDIDATES_LINE:]

    def get_titles_file(self) -> list:
        with open(self.titles_file, "r", encoding="utf-8") as f:
            lines = [line.strip().split("; ") for line in f]
        return lines[NUM_TITLES_LINE:]

    def turn_titles_list_into_dict(self, title_list: list) -> dict:
        return {
            line[NUM_TITLES_DEGREE]: (
                line[NUM_TITLES_NAME_MASCULINE],
                line[NUM_TITLES_NAME_FEMININE]
            )
            for line in title_list
        }

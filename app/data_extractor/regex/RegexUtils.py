import re
from typing import List, Optional


class RegexUtils:
    @staticmethod
    def match_pattern(pattern: str, text: str, group: int = 0, flags: int = re.DOTALL) -> Optional[str]:
        """
        Matches a regex pattern in the given text and returns the specified group.

        Args:
            pattern (str): The regex pattern to match.
            text (str): The text to search within.
            group (int): The group number to return from the match. Defaults to 0.
            flags (int): Flags for regex compilation. Defaults to re.DOTALL.

        Returns:
            Optional[str]: The matched group text if found, otherwise None.
        """
        match = re.search(pattern, text, flags)
        return match.group(group).strip() if match else None

    @staticmethod
    def find_all(pattern: str, text: str, flags: int = re.DOTALL) -> List[str]:
        """
        Finds all matches for a regex pattern in the given text.

        Args:
            pattern (str): The regex pattern to match.
            text (str): The text to search within.
            flags (int): Flags for regex compilation. Defaults to re.DOTALL.

        Returns:
            List[str]: A list of matched strings.
        """
        return re.findall(pattern, text, flags)

    @staticmethod
    def find_all_named_groups(pattern: str, text: str, flags: int = re.DOTALL) -> List[dict]:
        """
        Finds all matches for a regex pattern and returns a list of named groups as dictionaries.

        Args:
            pattern (str): The regex pattern with named groups.
            text (str): The text to search within.
            flags (int): Flags for regex compilation. Defaults to re.DOTALL.

        Returns:
            List[dict]: A list of dictionaries with named groups and their values.
        """
        compiled_pattern = re.compile(pattern, flags)
        matches = compiled_pattern.finditer(text)
        return [match.groupdict() for match in matches]

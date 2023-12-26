from enum import Enum

class ProjectTypeEnum(Enum):
    """Enum for project types"""

    # Regex for a typical dissertation project (contains organ, group, and sample)
    DISSERTATION = {
        "Title": "Dissertation Project",
        "Description": "The track name contains the organ, group, and sample number",
        "Example": "Track 1, ID: Organ Group1",
        "Regex": r"Track \d+, ID: ([a-zA-Z ]*) ([a-zA-Z]+) *(\d+) \(.*"
    }

    # Regex for another type of project (contains only group and sample)
    OTHER = {
        "Title": "Other Project",
        "Description": "The track name contains the group and sample",
        "Example": "Track 1, ID: Group_Sample",
        "Regex": r"Track \d+, ID: (.+)_([^_]+) *\(.*"
    }

    # Functions
    @staticmethod
    def get_regex(project_type: str) -> str:
        """
        Gets the regex for a project type.

        :param project_type: The project type.
        :return: The regex for the project type.
        """
        return ProjectTypeEnum[project_type.upper()].value["Regex"]
    
    @staticmethod
    def get_dropdown_options() -> list:
        """
        Gets the dropdown options.

        :return: The dropdown options.
        """
        return [
            ProjectTypeEnum[name].value["Title"] + " - " + ProjectTypeEnum[name].value["Example"]
            for name in ProjectTypeEnum.__members__.keys()
        ]
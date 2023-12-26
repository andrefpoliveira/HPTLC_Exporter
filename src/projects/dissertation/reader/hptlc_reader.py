from __future__ import annotations

import re

from src.projects.dissertation.writer.excel_writer import DissertationExcelWriter
from src.general.reader.hptlc_reader import HptlcReader

class DissertationHptlcReader(HptlcReader):
    def __init__(self, filename: str, regex_expression: str, output: str = "Teste.xlsx") -> DissertationHptlcReader:
        super().__init__(filename, regex_expression, DissertationExcelWriter, output)


    def build_excel(self, tables, configuration):
        """
        Builds the excel file from the tables and the configuration.
    
        :param tables: The tables extracted from the PDF.
        :param configuration: The configuration extracted from the JSON.
        """
        groups = configuration["groups"]
        samples = configuration["samples"]
        
        keys = sorted(list(tables.keys()))
        for id, k in enumerate(keys):
            substances = [x[-1] for x in tables[k]]

            organ, group, number = re.findall(self.regex_expression, k)[0]

            project_config = {"groups": groups, "samples": samples, "substances": substances}
            
            self.excel_writer.build_sheet_structure(organ, project_config)
            self.excel_writer.fill_values(organ, {"samples": samples, "group_id": [x["acronym"] for x in groups].index(group), "number": int(number), "table": tables[k], "left_col": id % 2 == 0}, project_config)
    
        self.excel_writer.save()
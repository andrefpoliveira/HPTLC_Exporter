from __future__ import annotations

import re

from pypdf import PdfReader
from src.general.writer.excel_writer import ExcelWriter

from abc import ABC, abstractmethod

class HptlcReader(ABC):
    def __init__(self, filename: str, regex_expression: str, excel_writer: ExcelWriter, output: str = "Teste.xlsx") -> HptlcReader:
        self.filename = filename
        self.regex_expression = regex_expression
        self.output = output
        self.excel_writer = excel_writer(self.output)
        self.text = self.pdf_to_text()


    def pdf_to_text(self) -> str:
        """
        Extracts the text from the PDF file
        """

        reader = PdfReader(self.filename)
        text = ""
        for p in reader.pages:
            text += p.extract_text() + "\n"
        return text
    

    def extract_info(self) -> dict:
        """
        Get all the relevant information from the PDF's text (Tracks, IDS, and tables).

        :return: A dictionary where the keys are the tracks and the values are the tables.
        """

        tables = {}
        tracks = [x.strip() for x in re.findall(r"Track \d+, [^\n]+", self.text)]
        for id, track in enumerate(tracks):

            current_text = self.text[self.text.find(track):]
            current_text = current_text.split("Assigned substance")[1]

            if id < len(tracks) - 1:
                current_text = current_text.split(tracks[id + 1])[0]

            tables[track] = self.text_to_array(current_text.strip())

        return tables
    
    
    def text_to_array(self, text: str) -> list:
        """
        Converts the text representation of the table to a list of lists.

        :param text: The text representation of the table.
        :return: A list of lists with the table's content.
        """

        table = []
        lines = text.split("\n")

        for line in lines:
            if not line.split(): continue
            peak = line.split()[0]

            m = re.findall(r"^\d", peak)
            if len(m) == 0: continue

            if "Peak deleted" in line: continue
            if len(line.split()) <= 10: continue
            
            peak, start_rf, start_h, max_rf, max_h, max_perc, end_rf, end_h, area, area_perc, *substance = line.split()
            table.append([peak, start_rf, start_h, max_rf, max_h, max_perc, end_rf, end_h, area, area_perc, " ".join(substance)])

        return table


    @abstractmethod
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
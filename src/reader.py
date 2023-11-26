from abc import ABC, abstractmethod
from pypdf import PdfReader


class Reader(ABC):
    def __init__(self, filename):
        self.filename = filename
        self.text = self.extract_text()

    def extract_text(self):
        reader = PdfReader(self.filename)
        text = ""
        for p in reader.pages:
            text += p.extract_text() + "\n"

        with open("text2.txt", "w", encoding="utf8") as f:
            f.write(text)
        return text

    @abstractmethod
    def extract_info(self) -> dict:
        pass

    @abstractmethod
    def build_excel(self):
        pass
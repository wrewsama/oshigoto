import spacy

class WordProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def processPoint(self, text: str) -> list[str]:
        doc = self.nlp(text) 
        return [chunk.text for chunk in doc.noun_chunks]

    def processData(self, data: list[list[str]]):
        flattenedData = [point for lst in data for point in lst]
        return list(map(self.processPoint, flattenedData))



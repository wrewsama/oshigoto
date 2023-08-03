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
s = WordProcessor()
test = [['The for construct iterates over the items in iterable', "while expression(item) provides"],
        ['Note that comprehensions can also have nested for clauses and conditional statements']]
print(s.processData(test))



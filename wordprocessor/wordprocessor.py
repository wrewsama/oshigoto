import spacy

class WordProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def processPoint(self, text):
        doc = self.nlp(text) 
        return [chunk.text for chunk in doc.noun_chunks]

s = WordProcessor()



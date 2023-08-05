from collections import Counter
import spacy

class WordProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def processPoint(self, text: str) -> list[str]:
        doc = self.nlp(text) 
        return [chunk.text for chunk in doc.noun_chunks]

    def processData(self, data: list[list[str]], count: int):
        flattenedPoints = [point for lst in data for point in lst]
        processedPoints = []
        for pt in flattenedPoints:
            processedPoints.extend(self.processPoint(pt))
        
        phraseCount = Counter(processedPoints)
        return phraseCount.most_common(count)




